import fire
import sys
import os
from fastembed import TextEmbedding
import db

# Initialize embedding model
embedding_model = TextEmbedding()

def search_facts(query: str, limit: int = 5):
    try:
        table = db.get_table("facts")
        embeddings = list(embedding_model.embed([query]))
        vector = embeddings[0].tolist()
        return table.search(vector).limit(limit).to_list()
    except Exception:
        return []

def search_episodes(query: str, limit: int = 5):
    try:
        table = db.get_table("episodes")
        embeddings = list(embedding_model.embed([query]))
        vector = embeddings[0].tolist()
        return table.search(vector).limit(limit).to_list()
    except Exception:
        return []

def search_code(query: str, limit: int = 5):
    try:
        table = db.get_table("code_index")
        embeddings = list(embedding_model.embed([query]))
        vector = embeddings[0].tolist()
        return table.search(vector).limit(limit).to_list()
    except Exception:
        return []

def main(query: str, scope: str = "all", limit: int = 5, mode: str = "summary"):
    try:
        if scope == "all":
            scopes = ["memory", "episodes", "code"]
        elif scope == "fact" or scope == "memory":
            scopes = ["memory"]
        else:
            scopes = [scope]
        
        for s in scopes:
            if s == "memory":
                results = search_facts(query, limit)
                if results:
                    print("\n--- Facts ---")
                    for r in results:
                        print(f"- {r['content']}")
            elif s == "episodes":
                results = search_episodes(query, limit)
                if results:
                    print("\n--- Episodes ---")
                    for r in results:
                        print(f"[{r['result'].upper()}] [{r['category'].upper()}] Goal: {r['goal']} | Summary: {r['summary']}")
            elif s == "code":
                results = search_code(query, limit)
                if results:
                    print("\n--- Codebase Index ---")
                    for r in results:
                        # Staleness check
                        try:
                            mtime = os.path.getmtime(r['file_path']) if os.path.exists(r['file_path']) else 0
                            is_stale = mtime > r['last_modified']
                        except Exception:
                            is_stale = False
                        
                        prefix = "[STALE] " if is_stale else ""
                        if mode == "exact":
                            print(f"\n--- {prefix}{r['file_path']} ---")
                            if os.path.exists(r['file_path']):
                                with open(r['file_path'], 'r') as f:
                                    print(f.read())
                            else:
                                print("File not found.")
                        else:
                            print(f"{prefix}{r['file_path']}: {r['summary']}")
                            if r['symbols']:
                                print(f"  Symbols: {', '.join(r['symbols'])}")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fire.Fire(main)
