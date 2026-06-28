import streamlit as st
import requests
import time
import os

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"

FEW_SHOT_EXAMPLES = [
    {
        "input": "The package arrived broken and customer service never responded.",
        "output": "Negative — product damage complaint with unresolved support issue.",
    },
    {
        "input": "Delivery was fast and the item was exactly as described. Very happy!",
        "output": "Positive — satisfied customer praising shipping speed and product accuracy.",
    },
]


def call_groq(prompt: str, api_key: str) -> tuple[str, float]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 512,
    }
    start = time.time()
    response = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=30)
    elapsed = time.time() - start
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"].strip()
    return content, round(elapsed, 2)


def build_zero_shot(task: str, text: str) -> str:
    return f"{task}\n\nInput:\n{text}"


def build_few_shot(task: str, text: str) -> str:
    examples = "\n\n".join(
        f"Example {i+1}:\nInput: {ex['input']}\nOutput: {ex['output']}"
        for i, ex in enumerate(FEW_SHOT_EXAMPLES)
    )
    return f"{task}\n\nHere are some examples:\n\n{examples}\n\nNow do the same for this input:\n{text}"


def build_cot(task: str, text: str) -> str:
    return f"{task}\n\nThink step by step before answering.\n\nInput:\n{text}"


def consistency_score(task: str, output: str) -> int:
    if not output:
        return 0
    task_terms = set(w.lower().strip(".,?!") for w in task.split() if len(w) > 3)
    output_lower = output.lower()
    if not task_terms:
        return 0
    hits = sum(1 for term in task_terms if term in output_lower)
    return round((hits / len(task_terms)) * 100)


def word_count(text: str) -> int:
    return len(text.split()) if text else 0


st.set_page_config(
    page_title="PromptLens",
    page_icon="🔬",
    layout="wide",
)

st.markdown(
    """
    <style>
        .strategy-header {
            font-size: 1.05rem;
            font-weight: 700;
            padding: 8px 14px;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        .output-box {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 14px 16px;
            min-height: 160px;
            font-size: 0.92rem;
            line-height: 1.6;
            color: #1a202c;
            white-space: pre-wrap;
        }
        .winner-banner {
            background: linear-gradient(90deg, #ebf8ff 0%, #e6fffa 100%);
            border: 1.5px solid #63b3ed;
            border-radius: 10px;
            padding: 14px 22px;
            font-size: 1.05rem;
            font-weight: 600;
            color: #2b6cb0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🔬 PromptLens — LLM Prompt Strategy Benchmarker")
st.markdown(
    "<p style='color:#4a5568;margin-top:-10px;font-size:1.02rem;'>"
    "Compare <b>Zero-Shot</b> vs <b>Few-Shot</b> vs <b>Chain-of-Thought</b> "
    "prompting strategies in real time."
    "</p>",
    unsafe_allow_html=True,
)
st.divider()

api_key = os.environ.get("GROQ_API_KEY", "")
if not api_key:
    st.error("⚠️ GROQ_API_KEY is not set. Please add it as a secret and restart the app.")
    st.stop()

col_left, col_right = st.columns([1, 1])
with col_left:
    task = st.text_input(
        "Task / Instruction",
        placeholder="e.g. Classify this customer complaint by sentiment",
        help="Describe what you want the model to do with the input text.",
    )
with col_right:
    input_text = st.text_area(
        "Input Text",
        placeholder="Paste the text you want to process here…",
        height=120,
        help="The raw content the model will work on.",
    )

run_btn = st.button("⚡ Run Benchmark", type="primary")

if run_btn:
    if not task.strip():
        st.warning("Please enter a task/instruction.")
        st.stop()
    if not input_text.strip():
        st.warning("Please paste some input text.")
        st.stop()

    strategies = [
        {
            "name": "Zero-Shot",
            "build": build_zero_shot,
            "header_color": "#4a5568",
            "bg": "#edf2f7",
        },
        {
            "name": "Few-Shot",
            "build": build_few_shot,
            "header_color": "#2b6cb0",
            "bg": "#ebf8ff",
        },
        {
            "name": "Chain-of-Thought",
            "build": build_cot,
            "header_color": "#276749",
            "bg": "#f0fff4",
        },
    ]

    results = []
    with st.spinner("Running all 3 strategies against Groq API…"):
        for s in strategies:
            prompt = s["build"](task.strip(), input_text.strip())
            try:
                output, elapsed = call_groq(prompt, api_key)
                error = None
            except Exception as e:
                output = ""
                elapsed = 0.0
                error = str(e)
            results.append(
                {
                    **s,
                    "output": output,
                    "elapsed": elapsed,
                    "error": error,
                    "words": word_count(output),
                    "score": consistency_score(task.strip(), output),
                }
            )

    st.subheader("Results")
    cols = st.columns(3)
    for col, r in zip(cols, results):
        with col:
            icon = {"Zero-Shot": "✦", "Few-Shot": "✧", "Chain-of-Thought": "◈"}[r["name"]]
            st.markdown(
                f"<div class='strategy-header' style='background:{r['bg']};color:{r['header_color']};'>"
                f"{icon} {r['name']}</div>",
                unsafe_allow_html=True,
            )
            if r["error"]:
                st.error(f"Error: {r['error']}")
            else:
                st.markdown(
                    f"<div class='output-box'>{r['output']}</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div style='margin-top:8px;display:flex;gap:6px;flex-wrap:wrap;'>"
                    f"<span style='background:{r['header_color']}18;border:1px solid {r['header_color']}40;"
                    f"color:{r['header_color']};border-radius:6px;padding:2px 10px;font-size:0.78rem;font-weight:600;'>"
                    f"Words: {r['words']}</span>"
                    f"<span style='background:{r['header_color']}18;border:1px solid {r['header_color']}40;"
                    f"color:{r['header_color']};border-radius:6px;padding:2px 10px;font-size:0.78rem;font-weight:600;'>"
                    f"Time: {r['elapsed']}s</span>"
                    f"<span style='background:{r['header_color']}18;border:1px solid {r['header_color']}40;"
                    f"color:{r['header_color']};border-radius:6px;padding:2px 10px;font-size:0.78rem;font-weight:600;'>"
                    f"Consistency: {r['score']}%</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

    st.divider()
    valid = [r for r in results if not r["error"]]
    if valid:
        best = max(valid, key=lambda r: r["score"])
        ranking = sorted(valid, key=lambda r: r["score"], reverse=True)
        score_display = " → ".join(f"{r['name']} ({r['score']}%)" for r in ranking)
        st.markdown(
            f"<div class='winner-banner'>"
            f"🏆 <b>{best['name']}</b> scored highest on consistency "
            f"({best['score']}%)&nbsp;&nbsp;|&nbsp;&nbsp;Ranking: {score_display}"
            f"</div>",
            unsafe_allow_html=True,
        )
    else:
        st.error("All strategies encountered errors. Check your API key and try again.")
