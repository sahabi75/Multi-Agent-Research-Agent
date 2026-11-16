import os
import re
from datetime import date
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# Small task, so the smaller model is enough. It also has its own
# free-tier quota, which keeps the other agents from hitting the limit.
MODEL = os.getenv("GROQ_PLANNER_MODEL", "openai/gpt-oss-20b")


# The Planner Function

def run_planner(user_question):
    """
    Takes the user's question.
    Returns a list of sub-topics to research.

    How to use it:
        topics = run_planner("What is climate change?")
        print(topics)
    """

    print("\n🧠 Planner Agent started...")
    print(f"📥 Question received: {user_question}")

    today = date.today().strftime("%B %d, %Y")

    prompt = f"""
You are a research planner.
Today's date is {today}.

Your job is to break down a research question into exactly 3 to 4 sub-topics.

The user wants to research this topic:
"{user_question}"

Instructions:
- Give exactly 3 to 4 sub-topics
- Each sub-topic should be short (5-8 words max)
- Each sub-topic should be on its own line
- If the question is about recent events or the latest news, include one sub-topic about the latest developments
- Do NOT number them
- Do NOT use bullet points or dashes
- Do NOT add extra explanation
- Just return the sub-topics, one per line

Example output format:
Causes of climate change
Effects on global weather patterns
Solutions and renewable energy
Current climate statistics and data
"""

    print("📤 Sending question to Groq AI...")

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
            max_completion_tokens=1000   # reasoning tokens count here too
        )

        raw_text = response.choices[0].message.content or ""

    except Exception as e:
        print(f"⚠️ Planner error: {e}")
        raw_text = ""

    print("📨 Groq responded!")

    sub_topics = []
    for line in raw_text.strip().split("\n"):
        # Remove bullets, dashes or numbers if the model adds them anyway
        clean_line = re.sub(r"^[\s\-\*\•\d\.\)]+", "", line).strip()
        if clean_line:
            sub_topics.append(clean_line)

    sub_topics = sub_topics[:4]

   
    if not sub_topics:
        sub_topics = [user_question]

    print(f"✅ Planner finished! Found {len(sub_topics)} sub-topics.\n")

    return sub_topics


# Test this file directly

if __name__ == "__main__":

    print("=" * 50)
    print("  Testing the Planner Agent")
    print("=" * 50)

    test_question = "What is artificial intelligence and how does it work?"

    result = run_planner(test_question)

    print("📋 Sub-topics generated:")
    for i, topic in enumerate(result, start=1):
        print(f"   {i}. {topic}")

    print("\n✅ Planner Agent test complete!")
