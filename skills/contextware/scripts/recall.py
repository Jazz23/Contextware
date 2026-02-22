import fire
import sys
import os
import json
from fastembed import TextEmbedding
import db
import atexit
import gc

def _cleanup():
    db.close_db()
    gc.collect()

atexit.register(_cleanup)

# Initialize embedding model
_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = TextEmbedding()
    return _embedding_model

def search_facts(query: str, limit: int = 5):
    try:
        table = db.get_table("facts")
        embeddings = list(get_embedding_model().embed([query]))
        vector = embeddings[0].tolist()
        return table.search(vector).limit(limit).to_list()
    except Exception:
        return []

def search_episodes(query: str, limit: int = 5):
    try:
        table = db.get_table("episodes")
        embeddings = list(get_embedding_model().embed([query]))
        vector = embeddings[0].tolist()
        return table.search(vector).limit(limit).to_list()
    except Exception:
        return []

def search_code(query: str, limit: int = 5):
    try:
        table = db.get_table("code_index")
        embeddings = list(get_embedding_model().embed([query]))
        vector = embeddings[0].tolist()
        return table.search(vector).limit(limit).to_list()
    except Exception:
        return []

def lookup_path(path: str):
    try:
        table = db.get_table("code_index")
        abs_path = os.path.abspath(path)
        escaped_path = abs_path.replace("'", "''")
        results = table.search().where(f"file_path = '{escaped_path}'").to_list()
        return results
    except Exception as e:
        print(f"Error during path lookup: {e}")
        return []

def print_hierarchical_symbols(data, indent="  "):
    if data.get('top_level_functions'):
        print(f"{indent}Functions: {', '.join(data['top_level_functions'])}")
    
    classes_raw = data.get('classes')
    if classes_raw:
        try:
            classes = json.loads(classes_raw) if isinstance(classes_raw, str) else classes_raw
            for class_name, methods in classes.items():
                print(f"{indent}Class {class_name}:")
                if methods:
                    print(f"{indent}  Methods: {', '.join(methods)}")
                else:
                    print(f"{indent}  (No methods)")
        except Exception as e:
            print(f"{indent}Error parsing classes metadata: {e}")

def main(query: str = None, scope: str = "all", limit: int = 5, path: str = None):
    try:
        # If path is provided, we ignore other filters and just do a direct lookup
        if path:
            results = lookup_path(path)
            if results:
                print(f"\n--- Metadata for {path} ---")
                for r in results:
                    mtime = os.path.getmtime(r['file_path']) if os.path.exists(r['file_path']) else 0
                    is_stale = mtime > r['last_modified']
                    prefix = "[STALE] " if is_stale else ""
                    print(f"{prefix}Summary: {r['summary']}")
                    print_hierarchical_symbols(r, indent="")
            else:
                print(f"No index entry found for path: {path}")
            return

        if not query:
            print("Error: query is required unless --path is provided")
            sys.exit(1)

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
                        print(f"{prefix}{r['file_path']}: {r['summary']}")
                        print_hierarchical_symbols(r, indent="  ")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fire.Fire(main)
