import os                      # lets Python read your .env keys
from dotenv import load_dotenv # reads the .env file
from groq import Groq          # Groq AI — free and fast

# Load your API keys from .env file
load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)




def run_summarizer(search_results):
    """
    Takes the search results dictionary from Agent 2.
    Returns a clean summary for each topic.

    How to use it:
        summaries = run_summarizer(search_results)
    """

    print("\n📝 Summarizer Agent started...")
    print(f"📥 Received {len(search_results)} topics to summarize\n")


    all_summaries = {}

    
    for i, (topic, articles) in enumerate(search_results.items(), start=1):

        print(f"✍️  Summarizing topic {i}/{len(search_results)}: '{topic}'")

        
        combined_text = ""

        for j, article in enumerate(articles, start=1):
            combined_text += f"\nArticle {j}: {article['title']}\n"
            combined_text += f"{article['content']}\n"

        
        prompt = f"""
You are a research summarizer.
Your job is to read the articles below and write a clear summary.

Topic: "{topic}"

Articles:
{combined_text}

Instructions:
- Write a summary of 4 to 6 sentences
- Use simple easy to understand language
- Only include the most important information
- Do NOT copy paste from the articles
- Write in your own words
- Do NOT add any intro like "Here is a summary" — just start writing
"""

        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Get the summary text from the response
        summary = response.choices[0].message.content.strip()

        # Save this topic's summary
        all_summaries[topic] = summary

        print(f"   ✅ Done!")

    print(f"\n✅ Summarizer finished! Summarized {len(all_summaries)} topics.\n")

    return all_summaries




if __name__ == "__main__":

    print("=" * 50)
    print("  Testing the Summarizer Agent")
    print("=" * 50)

    # Fake search results to test with
    # Normally Agent 2 provides this
    test_search_results = {
        "Definition of artificial intelligence": [
            {
                "title": "What is AI? - ISO",
                "url": "https://www.iso.org/artificial-intelligence/what-is-ai",
                "content": "Artificial intelligence is the simulation of human intelligence by machines. It involves learning, reasoning, and self-correction. AI systems are designed to perform tasks that normally require human intelligence such as visual perception, speech recognition, and decision-making."
            },
            {
                "title": "What is AI? - Michigan Tech",
                "url": "https://www.mtu.edu/computing/ai/",
                "content": "AI is a branch of computer science that aims to create intelligent machines. It has become an essential part of the technology industry. AI research is highly technical and specialized."
            },
            {
                "title": "Artificial Intelligence - NIBIB",
                "url": "https://www.nibib.nih.gov/science-education/science-topics/artificial-intelligence-ai",
                "content": "Artificial intelligence enables computers to learn from experience, adjust to new inputs and perform human-like tasks. Most AI examples that you hear about today rely heavily on deep learning and natural language processing."
            }
        ],
        "Machine learning techniques": [
            {
                "title": "Machine Learning Techniques Overview",
                "url": "https://www.leewayhertz.com/machine-learning-techniques/",
                "content": "Machine learning techniques include supervised learning, unsupervised learning, and reinforcement learning. Supervised learning uses labeled data to train models. Unsupervised learning finds hidden patterns in unlabeled data."
            },
            {
                "title": "Types of Machine Learning - Enlitia",
                "url": "https://www.enlitia.com/resources-blog-post/types-of-machine-learning-techniques",
                "content": "The main machine learning methods are classification, regression, clustering, and dimensionality reduction. Neural networks and deep learning are advanced techniques that mimic the human brain."
            },
            {
                "title": "Top Machine Learning Methods - Tableau",
                "url": "https://www.tableau.com/learn/articles/top-machine-learning-methods",
                "content": "Popular machine learning algorithms include linear regression, decision trees, random forests, and support vector machines. These algorithms are used across industries for predictions and automation."
            }
        ]
    }

    # Run the summarizer
    summaries = run_summarizer(test_search_results)

    # Show the results
    print("📋 Summaries Generated:")
    print("-" * 50)

    for topic, summary in summaries.items():
        print(f"\n📌 Topic: {topic}")
        print(f"   {summary}")

    print("\n✅ Summarizer Agent test complete!")