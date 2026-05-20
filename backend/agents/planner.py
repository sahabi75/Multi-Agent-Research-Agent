import os                      
from dotenv import load_dotenv 
from groq import Groq          

# Load your API keys from .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)


# The Planner Function

def run_planner(user_question):
    """
    Takes the user's question.
    Returns a list of sub-topics to research.

    How to use it:
        topics = run_planner("What is climate change?")
        print(topics)
    """

    print(f"\n🧠 Planner Agent started...")
    print(f"📥 Question received: {user_question}")

    prompt = f"""
You are a research planner.
Your job is to break down a research question into exactly 3 to 4 sub-topics.

The user wants to research this topic:
"{user_question}"

Instructions:
- Give exactly 3 to 4 sub-topics
- Each sub-topic should be short (5-8 words max)
- Each sub-topic should be on its own line
- Do NOT number them
- Do NOT add extra explanation
- Just return the sub-topics, one per line

Example output format:
Causes of climate change
Effects on global weather patterns
Solutions and renewable energy
Current climate statistics and data
"""

    print("📤 Sending question to Groq AI...")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # free and very smart model
        messages=[
            {
                "role": "user",       # "user" means this is our message
                "content": prompt     # the actual instructions
            }
        ]
    )

    raw_text = response.choices[0].message.content

    print("📨 Groq responded!")


    lines = raw_text.strip().split("\n")

    sub_topics = []
    for line in lines:
        clean_line = line.strip()    
        if clean_line:               
            sub_topics.append(clean_line)

    sub_topics = sub_topics[:4]

    print(f"✅ Planner finished! Found {len(sub_topics)} sub-topics.\n")

    return sub_topics


#  Test this file directly


if __name__ == "__main__":

    print("=" * 50)
    print("  Testing the Planner Agent")
    print("=" * 50)

    # Test question
    test_question = "What is artificial intelligence and how does it work?"

    # Run the planner
    result = run_planner(test_question)

    # Show results
    print("📋 Sub-topics generated:")
    for i, topic in enumerate(result, start=1):
        print(f"   {i}. {topic}")

    print("\n✅ Planner Agent test complete!")