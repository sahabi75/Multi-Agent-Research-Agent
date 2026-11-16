import os
from datetime import date
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# Model name in one place, so it is easy to change next time
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


def run_reporter(user_question, summaries):
    """
    Takes the original question and all summaries.
    Returns one complete research report as a string.

    How to use it:
        report = run_reporter("What is AI?", summaries)
        print(report)
    """

    print("\n📄 Reporter Agent started...")
    print(f"📥 Received {len(summaries)} summaries to compile\n")

    today = date.today().strftime("%B %d, %Y")

    combined_summaries = ""

    for topic, summary in summaries.items():
        combined_summaries += f"\n### {topic}\n"
        combined_summaries += f"{summary}\n"

    # ----------------------------------------
    # Write the prompt for Groq
    # ----------------------------------------
    prompt = f"""
You are a professional research report writer.
Today's date is {today}.

Your job is to take research summaries and turn them into one clean report.

The user's original question was:
"{user_question}"

Here are the research summaries:
{combined_summaries}

Instructions:
- Write a complete research report in Markdown
- Start with a short introduction (2-3 sentences)
- Then write one section for each topic with a clear heading
- End with a short conclusion (2-3 sentences)
- Use ONLY the information in the summaries above
- Do NOT use your own background knowledge, especially for recent events
- If the summaries do not cover something, do not make it up
- Use simple clear language
- Make it easy to read
- Do NOT add any extra commentary outside the report
"""

    # ----------------------------------------
    # Send to Groq and get the full report back
    # ----------------------------------------
    print("📤 Sending summaries to Groq AI...")

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            reasoning_effort="low",
            max_completion_tokens=3000   
        )

        report = (response.choices[0].message.content or "").strip()

        if not report:
            report = "The report could not be generated. Please try again."

    except Exception as e:
        print(f"⚠️ Error while writing the report: {e}")
        report = "The report could not be generated. Please try again."

    print("📨 Groq responded!")
    print("✅ Reporter finished! Report is ready.\n")

    return report


# ============================================
# Test this file directly
#
# Run in terminal:
#     python backend/agents/reporter.py
# ============================================

if __name__ == "__main__":

    print("=" * 50)
    print("  Testing the Reporter Agent")
    print("=" * 50)

    test_question = "What is artificial intelligence and how does it work?"

    test_summaries = {
        "Definition of artificial intelligence": (
            "Artificial intelligence is the simulation of human intelligence by machines. "
            "It enables computers to learn from experience and perform tasks that normally "
            "require human thinking such as speech recognition, decision making, and visual "
            "perception. AI is a branch of computer science that has grown rapidly in recent years."
        ),
        "Types of AI systems": (
            "There are three main types of AI: narrow AI, general AI, and super AI. "
            "Narrow AI is designed for one specific task like playing chess or recognizing faces. "
            "General AI can perform any intellectual task a human can do. "
            "Super AI would surpass human intelligence but does not exist yet."
        ),
        "AI algorithms and models": (
            "AI algorithms are step by step instructions that tell a machine how to learn. "
            "Common algorithms include decision trees, neural networks, and support vector machines. "
            "These algorithms process large amounts of data to find patterns and make predictions. "
            "The choice of algorithm depends on the problem being solved."
        ),
        "Machine learning techniques": (
            "Machine learning is a subset of AI where machines learn from data without being "
            "explicitly programmed. The three main techniques are supervised learning, "
            "unsupervised learning, and reinforcement learning. Deep learning is an advanced "
            "technique that uses multi-layer neural networks to solve complex problems."
        )
    }

    report = run_reporter(test_question, test_summaries)

    print("=" * 50)
    print("📋 FINAL RESEARCH REPORT:")
    print("=" * 50)
    print(report)
    print("=" * 50)
    print("\n✅ Reporter Agent test complete!")
