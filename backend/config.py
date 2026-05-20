

import os                    # os = lets Python talk to your computer
from dotenv import load_dotenv  # load_dotenv = reads your .env file

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GROQ_API_KEY   = os.getenv("GROQ_API_KEY")


if __name__ == "__main__":

    print("Checking your API keys...\n")

    # Check Gemini key
    if GEMINI_API_KEY and GEMINI_API_KEY != "paste_your_gemini_key_here":
        print("✅ GEMINI_API_KEY   → Loaded successfully")
    else:
        print("❌ GEMINI_API_KEY   → NOT found. Please check your .env file")

    # Check Tavily key
    if TAVILY_API_KEY and TAVILY_API_KEY != "paste_your_tavily_key_here":
        print("✅ TAVILY_API_KEY   → Loaded successfully")
    else:
        print("❌ TAVILY_API_KEY   → NOT found. Please check your .env file")

    # Check Groq key
    if GROQ_API_KEY and GROQ_API_KEY != "paste_your_groq_key_here":
        print("✅ GROQ_API_KEY     → Loaded successfully")
    else:
        print("❌ GROQ_API_KEY     → NOT found. Please check your .env file")

    print("\nDone! Fix any ❌ items before moving to Phase 2.")