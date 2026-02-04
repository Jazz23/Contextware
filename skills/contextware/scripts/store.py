import fire
import sys
import os
import time
from fastembed import TextEmbedding
import db

# Initialize embedding model
embedding_model = TextEmbedding()

def store_fact(content: str):
    table = db.get_table("facts")
    embeddings = list(embedding_model.embed([content]))
    vector = embeddings[0].tolist()
    
    table.add([{"content": content, "vector": vector}])
    print(f"Stored fact: {content}")

def store_episode(goal: str, result: str, category: str, summary: str):
    table = db.get_table("episodes")
    # For episodes, embed goal + summary
    text_to_embed = f"Goal: {goal}\nSummary: {summary}"
    embeddings = list(embedding_model.embed([text_to_embed]))
    vector = embeddings[0].tolist()
    
    table.add([{
        "goal": goal,
        "result": result,
        "category": category,
        "summary": summary,
        "timestamp": time.time(),
        "vector": vector
    }])
    print(f"Stored episode: {goal} -> {result}")

def store_index(path: str, summary: str = None, symbols: list = None):
    table = db.get_table("code_index")
    
    if not os.path.exists(path):
        print(f"Error: Path {path} does not exist.")
        return

    if summary is None:
        # In a real scenario, this would trigger a headless Gemini call.
        # For now, we'll just use a placeholder.
        # Phase 2 will implement the actual headless Gemini summarization.
        summary = f"Summary for {path}"
        symbols = []
    
    embeddings = list(embedding_model.embed([summary]))
    vector = embeddings[0].tolist()
    
    mtime = os.path.getmtime(path)
    
    data = [{
        "file_path": os.path.abspath(path),
        "summary": summary,
        "symbols": symbols if symbols is not None else [],
        "last_modified": mtime,
        "vector": vector
    }]
    
    # Simple check-and-delete for "upsert" behavior
    escaped_path = os.path.abspath(path).replace("'", "''")
    try:
        table.delete(f"file_path = '{escaped_path}'")
    except Exception:
        pass
    
    table.add(data)
    print(f"Indexed: {path}")

def crawl(dir_path: str = "."):
    # Placeholder for full crawl
    # In Phase 2, this will spawn a headless agent.
    print(f"Crawling {dir_path}...")
    for root, dirs, files in os.walk(dir_path):
        if ".git" in dirs:
            dirs.remove(".git")
        if ".venv" in dirs:
            dirs.remove(".venv")
        if "data" in dirs: # Skip our own data
            dirs.remove("data")
            
        for file in files:
            if file.endswith((".py", ".md", ".ts", ".js", ".json")):
                path = os.path.join(root, file)
                store_index(path)

def main(type: str, content: str = None, goal: str = None, result: str = None, category: str = None, path: str = None):
    try:
        if type == "fact":
            if not content:
                print("Error: content is required for type 'fact'")
                sys.exit(1)
            store_fact(content)
        elif type == "episode":
            # For episodes, if content is provided as positional, use it as summary
            summary = content
            if not goal or not result or not category or not summary:
                print("Error: goal, result, category, and summary (content) are required for type 'episode'")
                sys.exit(1)
            store_episode(goal, result, category, summary)
        elif type == "index":
            summary_to_use = content
            if not path:
                # If path is not provided but content is, use content as path
                if content:
                    path = content
                    summary_to_use = None
                else:
                    print("Error: path is required for type 'index'")
                    sys.exit(1)
            store_index(path, summary=summary_to_use)
        elif type == "crawl":
            crawl(path or content or ".")
        else:
            print(f"Unknown type: {type}")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fire.Fire(main)