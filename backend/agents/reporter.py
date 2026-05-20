import os                     
from dotenv import load_dotenv 
from groq import Groq          


load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

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

    combined_summaries = ""

    for topic, summary in summaries.items():
        combined_summaries += f"\n### {topic}\n"
        combined_summaries += f"{summary}\n"

    # ----------------------------------------
    # Write the prompt for Groq
    # Tell it to write a proper research report
    # ----------------------------------------
    prompt = f"""
You are a professional research report writer.
Your job is to take research summaries and turn them into one clean report.

The user's original question was:
"{user_question}"

Here are the research summaries:
{combined_summaries}

Instructions:
- Write a complete research report
- Start with a short introduction (2-3 sentences)
- Then write one section for each topic with a clear heading
- End with a short conclusion (2-3 sentences)
- Use simple clear language
- Make it easy to read
- Do NOT add any extra commentary outside the report

Write a research report without any headings or sections.
Just write everything as plain flowing paragraphs one after another.
No Introduction heading, no Conclusion heading, no section titles.
Just plain paragraphs from start to finish.
"""

    # ----------------------------------------
    # Send to Groq and get the full report back
    # ----------------------------------------
    print("📤 Sending summaries to Groq AI...")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=2000   # allow longer response for full report
    )

    # Get the report text from the response
    report = response.choices[0].message.content.strip()

    print("📨 Groq responded!")
    print("✅ Reporter finished! Report is ready.\n")

    return report


# ============================================
# STEP 3 — Test this file directly
#
# Run in terminal:
#     python backend/agents/reporter.py
# ============================================

if __name__ == "__main__":

    print("=" * 50)
    print("  Testing the Reporter Agent")
    print("=" * 50)

    # Original question
    test_question = "What is artificial intelligence and how does it work?"

    # Fake summaries to test with
    # Normally Agent 3 provides these
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

    # Run the reporter
    report = run_reporter(test_question, test_summaries)

    # Print the full report
    print("=" * 50)
    print("📋 FINAL RESEARCH REPORT:")
    print("=" * 50)
    print(report)
    print("=" * 50)
    print("\n✅ Reporter Agent test complete!")