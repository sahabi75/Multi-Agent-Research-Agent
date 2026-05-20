# ============================================
# backend/memory/memory_manager.py
#
# WHAT THIS FILE DOES:
# Saves and loads past research sessions.
#
# Think of it like a research diary:
# - Every time you research something → save it
# - Next time you ask → load past sessions
#
# We store everything in a simple JSON file.
# JSON = a text file that stores data neatly.
#
# The file looks like this:
# [
#   {
#     "id": 1,
#     "question": "What is AI?",
#     "sub_topics": [...],
#     "final_report": "...",
#     "date": "2024-01-15 10:30:00"
#   },
#   ...
# ]
# ============================================


import json                    # reads and writes JSON files
import os                      # works with files and folders
from datetime import datetime  # gets the current date and time


# ============================================
# STEP 1 — Set the memory file path
#
# All past sessions will be saved in this file.
# It will be created automatically if it doesn't exist.
# ============================================

# Get the folder where this file lives
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

# Memory file will be saved in the same folder
MEMORY_FILE = os.path.join(THIS_FOLDER, "research_history.json")


# ============================================
# STEP 2 — Helper: Load all sessions from file
# ============================================

def load_all_sessions():
    """
    Reads the JSON file and returns all past sessions as a list.
    If the file doesn't exist yet, returns an empty list.
    """

    # Check if the file exists
    if not os.path.exists(MEMORY_FILE):
        return []   # no history yet, return empty list

    # Open and read the file
    with open(MEMORY_FILE, "r") as f:
        sessions = json.load(f)

    return sessions


# ============================================
# STEP 3 — Helper: Save all sessions to file
# ============================================

def save_all_sessions(sessions):
    """
    Writes all sessions back to the JSON file.
    indent=2 makes the file human readable.
    """

    with open(MEMORY_FILE, "w") as f:
        json.dump(sessions, f, indent=2)


# ============================================
# STEP 4 — Save a new research session
# ============================================

def save_session(question, sub_topics, final_report):
    """
    Saves one research session to memory.

    How to use it:
        save_session(
            question     = "What is AI?",
            sub_topics   = ["Definition of AI", ...],
            final_report = "# Research Report..."
        )
    """

    # Load existing sessions first
    sessions = load_all_sessions()

    # Create a new session object
    new_session = {
        "id"          : len(sessions) + 1,           # auto increment ID
        "question"    : question,                     # the user's question
        "sub_topics"  : sub_topics,                   # topics researched
        "final_report": final_report,                 # the full report
        "date"        : datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # timestamp
    }

    # Add new session to the list
    sessions.append(new_session)

    # Save back to file
    save_all_sessions(sessions)

    print(f"💾 Session saved! Total sessions in memory: {len(sessions)}")

    return new_session


# ============================================
# STEP 5 — Get all past sessions
# ============================================

def get_all_sessions():
    """
    Returns all past research sessions.

    How to use it:
        sessions = get_all_sessions()
        for s in sessions:
            print(s["question"])
    """

    sessions = load_all_sessions()
    return sessions


# ============================================
# STEP 6 — Get one session by ID
# ============================================

def get_session_by_id(session_id):
    """
    Returns one specific session by its ID number.

    How to use it:
        session = get_session_by_id(1)
        print(session["final_report"])
    """

    sessions = load_all_sessions()

    # Loop through all sessions and find the one with matching ID
    for session in sessions:
        if session["id"] == session_id:
            return session

    # If not found, return None
    return None


# ============================================
# STEP 7 — Search past sessions by keyword
# ============================================

def search_sessions(keyword):
    """
    Searches past sessions for a keyword in the question.
    Returns a list of matching sessions.

    How to use it:
        results = search_sessions("climate")
        for r in results:
            print(r["question"])
    """

    sessions = load_all_sessions()
    keyword  = keyword.lower()   # make lowercase for easy matching

    # Find sessions where the question contains the keyword
    matches = []
    for session in sessions:
        if keyword in session["question"].lower():
            matches.append(session)

    return matches


# ============================================
# STEP 8 — Delete all sessions (clear memory)
# ============================================

def clear_all_sessions():
    """
    Deletes all saved sessions from memory.
    Use carefully — this cannot be undone!
    """

    save_all_sessions([])   # save an empty list
    print("🗑️  Memory cleared! All sessions deleted.")


# ============================================
# STEP 9 — Test this file directly
#
# Run in terminal:
#     python -m backend.memory.memory_manager
# ============================================

if __name__ == "__main__":

    print("=" * 50)
    print("  Testing Memory Manager")
    print("=" * 50)

    # --- Test 1: Save a session ---
    print("\n📝 Test 1: Saving a session...")
    save_session(
        question     = "What is artificial intelligence?",
        sub_topics   = ["Definition of AI", "Types of AI", "AI algorithms", "Machine learning"],
        final_report = "# Research Report: AI\n\nAI is the simulation of human intelligence..."
    )

    # --- Test 2: Save another session ---
    print("\n📝 Test 2: Saving another session...")
    save_session(
        question     = "What is climate change?",
        sub_topics   = ["Causes", "Effects", "Solutions", "Current trends"],
        final_report = "# Research Report: Climate Change\n\nClimate change is caused by..."
    )

    # --- Test 3: Load all sessions ---
    print("\n📋 Test 3: Loading all sessions...")
    all_sessions = get_all_sessions()
    print(f"   Total sessions found: {len(all_sessions)}")
    for s in all_sessions:
        print(f"   [{s['id']}] {s['question']} — saved on {s['date']}")

    # --- Test 4: Get session by ID ---
    print("\n🔎 Test 4: Getting session by ID 1...")
    session = get_session_by_id(1)
    if session:
        print(f"   Found: {session['question']}")
        print(f"   Topics: {session['sub_topics']}")

    # --- Test 5: Search sessions ---
    print("\n🔍 Test 5: Searching for 'climate'...")
    results = search_sessions("climate")
    print(f"   Found {len(results)} matching session(s)")
    for r in results:
        print(f"   → {r['question']}")

    # --- Test 6: Clear memory ---
    print("\n🗑️  Test 6: Clearing all sessions...")
    clear_all_sessions()
    print(f"   Sessions after clear: {len(get_all_sessions())}")

    print("\n✅ Memory Manager test complete!")