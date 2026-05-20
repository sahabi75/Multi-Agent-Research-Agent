from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict

from backend.agents.planner       import run_planner
from backend.agents.searcher      import run_searcher
from backend.agents.summarizer    import run_summarizer
from backend.agents.reporter      import run_reporter
from backend.memory.memory_manager import save_session   # ← new import


# State (same as before)


class ResearchState(TypedDict):
    question      : str
    sub_topics    : List[str]
    search_results: Dict
    summaries     : Dict
    final_report  : str


# Nodes (same as before)


def planner_node(state: ResearchState):
    print("\n--- Running Agent 1: Planner ---")
    question   = state["question"]
    sub_topics = run_planner(question)
    return {"sub_topics": sub_topics}


def searcher_node(state: ResearchState):
    print("\n--- Running Agent 2: Searcher ---")
    sub_topics     = state["sub_topics"]
    search_results = run_searcher(sub_topics)
    return {"search_results": search_results}


def summarizer_node(state: ResearchState):
    print("\n--- Running Agent 3: Summarizer ---")
    search_results = state["search_results"]
    summaries      = run_summarizer(search_results)
    return {"summaries": summaries}


def reporter_node(state: ResearchState):
    print("\n--- Running Agent 4: Reporter ---")
    question     = state["question"]
    summaries    = state["summaries"]
    final_report = run_reporter(question, summaries)
    return {"final_report": final_report}


#  Memory Node


def memory_node(state: ResearchState):
    print("\n--- Saving to Memory ---")

    # Read everything from state
    question     = state["question"]
    sub_topics   = state["sub_topics"]
    final_report = state["final_report"]

    # Save to memory file
    save_session(
        question     = question,
        sub_topics   = sub_topics,
        final_report = final_report
    )

    
    return {}


# Build the Graph (updated with memory)


def build_graph():

    graph = StateGraph(ResearchState)

    # Add all nodes including memory
    graph.add_node("planner",    planner_node)
    graph.add_node("searcher",   searcher_node)
    graph.add_node("summarizer", summarizer_node)
    graph.add_node("reporter",   reporter_node)
    graph.add_node("memory",     memory_node)     # ← new node

    # Connect in order — memory runs last
    graph.set_entry_point("planner")
    graph.add_edge("planner",    "searcher")
    graph.add_edge("searcher",   "summarizer")
    graph.add_edge("summarizer", "reporter")
    graph.add_edge("reporter",   "memory")        # ← reporter → memory
    graph.add_edge("memory",     END)             # ← memory → END

    app = graph.compile()
    return app


#  Main Run Function 


def run_research(question: str):
    """
    Runs the full research pipeline for a question.
    Automatically saves to memory when done.

    How to use it:
        report = run_research("What is climate change?")
        print(report)
    """

    print("\n" + "=" * 50)
    print("  Starting Research Pipeline")
    print("=" * 50)
    print(f"Question: {question}")

    app = build_graph()

    final_state = app.invoke({
        "question"      : question,
        "sub_topics"    : [],
        "search_results": {},
        "summaries"     : {},
        "final_report"  : ""
    })

    return final_state["final_report"]


#  Test



if __name__ == "__main__":

    print("=" * 50)
    print("  Testing Full Pipeline with Memory")
    print("=" * 50)

    test_question = "What is climate change and why does it matter?"

    report = run_research(test_question)

    print("\n" + "=" * 50)
    print("FINAL REPORT:")
    print("=" * 50)
    print(report)
    print("=" * 50)
    print("\n✅ Full pipeline with memory test complete!")