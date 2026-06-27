### 🔬 PromptLens — LLM Prompt Strategy Benchmarker
PromptLens is a real-time benchmarking application designed to evaluate and compare the effectiveness of three core Large Language Model (LLM) prompting strategies: Zero-Shot, Few-Shot, and Chain-of-Thought (CoT).

By analyzing metrics like word count, execution time, and output consistency, PromptLens helps developers and prompt engineers choose the optimal strategy for their specific text-processing tasks.


🚀 How It Works
The application evaluates prompts across three distinct methodologies:

Zero-Shot: The model is given a direct instruction without any examples. (Fastest, but sometimes lower consistency).

Few-Shot: The model is provided with a few high-quality input-output examples to guide its style and structure. (Balanced performance).

Chain-of-Thought: The model is instructed to break down its reasoning step-by-step before producing the final output. (Highest accuracy and consistency for complex tasks).

🛠️ How to Use the Application
Define Your Task: In the Task / Instruction text field, enter what you want the AI to do (e.g., Extract data, analyze sentiment, or summarize text).

Provide Input Text: Paste the source text you want processed into the Input Text box.

Run the Benchmark: Click the ⚡ Run Benchmark button.

Analyze Results: Review the side-by-side comparison cards to see the breakdown of:

Generated Output: The exact response from each strategy.

Metrics: Real-time tracking of Words count, Execution Time (s), and Consistency (%).

Leaderboard: The app will automatically highlight the winning strategy based on the highest consistency score.

📝 Example Benchmarks to Try
1. Data Extraction (Default)
Task: Extract all names, job titles, and company names mentioned in the text and format them as a JSON list.

Input: Yesterday I grabbed coffee with Alex Rivera, a Senior Developer at TechCorp. She mentioned that their VP of Product, Marcus Vance, is looking to hire more remote engineers this quarter.

2. Sentiment Classification
Task: Classify the sentiment of this product review as Positive, Negative, or Neutral.

Input: I wanted to love this blender, but the motor started smelling like smoke on the third use. Returning it immediately.

3. Smart Summarization
Task: Summarize this email into 3 bullet points, focusing strictly on actionable next steps.

Input: Hi Team, following up on our meeting yesterday. We need to finalize the design mockups by Thursday so marketing can review them. Please upload your latest assets to the shared drive. Also, Sarah will be out on Friday, so get budget numbers to her by Wednesday.

📊 Key Performance Metrics Covered
⏱️ Latency (Time): Measures how fast the model responds under each strategy.

🎯 Consistency: Tracks how reliably the model adheres to formatting rules (like JSON syntax) and reasoning logic.

🔤 Token Efficiency (Words): Displays the length of the generated response to monitor token overhead costs.
