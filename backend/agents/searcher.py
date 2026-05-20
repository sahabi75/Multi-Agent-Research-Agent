# ============================================
# backend/agents/searcher.py
#
# WHAT THIS FILE DOES:
# This is Agent 2 - The Searcher.
#
# Job: Take the list of sub-topics from Agent 1
#      and search the web for each one using Tavily.
#
# Example:
#   Input  → ["Definition of AI",
#              "Types of AI systems",
#              "AI algorithms and models",
#              "Machine learning techniques"]
#
#   Output → A dictionary with search results for each topic
#             {
#               "Definition of AI": [ {title, url, content}, ... ],
#               "Types of AI systems": [ {title, url, content}, ... ],
#               ...
#             }
# ============================================


import os                      # lets Python read your .env keys
from dotenv import load_dotenv # reads the .env file
from tavily import TavilyClient  # Tavily — free web search API

# Load your API keys from .env file
load_dotenv()


# ============================================
# STEP 1 — Connect to Tavily Search
# ============================================

# Get the Tavily API key from .env
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Connect to Tavily using your key
client = TavilyClient(api_key=TAVILY_API_KEY)


# ============================================
# STEP 2 — The Searcher Function
# ============================================

def run_searcher(sub_topics):
    """
    Takes a list of sub-topics from the Planner.
    Searches the web for each one.
    Returns a dictionary of search results.

    How to use it:
        topics = ["Definition of AI", "Types of AI"]
        results = run_searcher(topics)
    """

    print("\n🔍 Searcher Agent started...")
    print(f"📥 Received {len(sub_topics)} sub-topics to search\n")

    # This dictionary will store all results
    # Key   = the sub-topic
    # Value = list of search results for that topic
    all_results = {}

    # ----------------------------------------
    # Loop through each sub-topic and search
    # ----------------------------------------
    for i, topic in enumerate(sub_topics, start=1):

        print(f"🌐 Searching topic {i}/{len(sub_topics)}: '{topic}'")

        # Search the web using Tavily
        # max_results=3 means get top 3 results per topic
        response = client.search(
            query=topic,
            max_results=3
        )

        # Tavily returns results inside response["results"]
        # Each result has: title, url, content
        raw_results = response["results"]

        # Store clean results for this topic
        topic_results = []

        for result in raw_results:
            
            clean_result = {
                "title"  : result["title"],    
                "url"    : result["url"],       
                "content": result["content"]    
            }
            topic_results.append(clean_result)

        # Save this topic's results in our big dictionary
        all_results[topic] = topic_results

        print(f"   ✅ Found {len(topic_results)} results")

    print(f"\n✅ Searcher finished! Searched {len(sub_topics)} topics.\n")

    return all_results



if __name__ == "__main__":

    print("=" * 50)
    print("  Testing the Searcher Agent")
    print("=" * 50)

    test_topics = [
        "Definition of artificial intelligence",
        "Types of AI systems",
        "AI algorithms and models",
        "Machine learning techniques"
    ]

    # Run the searcher
    results = run_searcher(test_topics)

    # Show the results
    print("📋 Search Results Summary:")
    print("-" * 50)

    for topic, articles in results.items():
        print(f"\n📌 Topic: {topic}")
        for j, article in enumerate(articles, start=1):
            print(f"   {j}. {article['title']}")
            print(f"      🔗 {article['url']}")

    print("\n✅ Searcher Agent test complete!")