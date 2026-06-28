# 🔬 PromptLens — LLM Prompt Strategy Benchmarker


Compare *Zero-Shot* vs *Few-Shot* vs *Chain-of-Thought* prompting strategies in real time. 

PromptLens is a lightweight **Streamlit** web application that automatically runs any given task against the **Groq API** (`llama3-8b-8192`) using Python `requests` to evaluate and compare three core prompting methodologies side by side.

---

## 🚀 How It Works

When you input a task, the application forks it into three distinct engineering strategies simultaneously:

*   **Zero-Shot:** Sends your task + input text directly without any guidance.
*   **Few-Shot:** Automatically injects **two hardcoded examples** before your input to steer the model's style and structure.
*   **Chain-of-Thought:** Injects the constraint *"Think step by step before answering"* to force explicit reasoning paths.

---

## 🛠️ How to Use the Application

1.  **Define Your Task:** In the **Task / Instruction** text field, enter what you want the AI to do (e.g., *Extract data, analyze sentiment, or summarize text*).
2.  **Provide Input Text:** Paste the source text you want processed into the **Input Text** box.
3.  **Run the Benchmark:** Click the **⚡ Run Benchmark** button to trigger all 3 API calls.
4.  **Analyze Results:** Review the clean, 3-column output layout (styled with grey, blue, and green headers) to see the responses side by side.

---

## 📊 Key Performance Metrics & Badges
Directly underneath each strategy's column output, the app displays real-time analytics badges calculated via custom Python heuristics:

*   ⏱️ **Execution Time:** Uses precise timer deltas (`time.perf_counter()`) to track raw network and model latency in seconds.
*   🔤 **Words:** Displays a split-string word count approximation to measure verbosity.
*   🎯 **Consistency:** A simple string-matching heuristic that checks if key terms from your task appear in the model's response, returning an accuracy percentage.

🏆 **Leaderboard Summary:** A summary bar at the base of the page automatically highlights and ranks the top-performing strategy based on the highest consistency score.

---
### 🔗 [⚡ Click Here for the Live Demo](https://prompt-strategy-benchmark.streamlit.app/)  

---
## 🚀 Quick Start Example (Try It in 30 Seconds)

To test the application instantly on the live deployment, 
Example Benchmarks to Try

### 1. Data Extraction
*   **Task:** `Extract all names, job titles, and company names mentioned in the text and format them as a JSON list.`
*   **Input:** `Yesterday I grabbed coffee with Alex Rivera, a Senior Developer at TechCorp. She mentioned that their VP of Product, Marcus Vance, is looking to hire more remote engineers this quarter.`

### 2. Sentiment Classification
*   **Task:** `Classify the sentiment of this product review as Positive, Negative, or Neutral.`
*   **Input:** `I wanted to love this blender, but the motor started smelling like smoke on the third use. Returning it immediately.`

---
