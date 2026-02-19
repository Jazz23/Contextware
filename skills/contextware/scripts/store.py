import fire
import sys
import os
import time
import ast
from fastembed import TextEmbedding
import db

# Initialize embedding model
embedding_model = TextEmbedding()

def extract_python_symbols(path: str):
    """Extracts function and class names from a Python file separately."""
    try:
        with open(path, "r") as f:
            tree = ast.parse(f.read())
        
        classes = []
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
        return sorted(list(set(classes))), sorted(list(set(functions)))
    except Exception as e:
        print(f"Warning: Could not extract symbols from {path}: {e}")
        return [], []

def store_fact(content: str):
    table = db.get_table("facts")
    # Migration check for timestamp
    if "timestamp" not in table.schema.names:
        print("Migrating facts table to new schema...")
        conn = db.get_db()
        conn.drop_table("facts")
        table = db.get_table("facts")

    embeddings = list(embedding_model.embed([content]))
    vector = embeddings[0].tolist()
    
    table.add([{
        "content": content, 
        "timestamp": time.time(),
        "vector": vector
    }])
    print(f"Stored fact: {content}")

def delete_fact(query: str):
    table = db.get_table("facts")
    escaped = query.replace("'", "''")
    try:
        # Find the first match specifically
        matches = table.search().where(f"content LIKE '%{escaped}%'").limit(1).to_list()
        if matches:
            target = matches[0]
            # Use exact content and timestamp for precision (to avoid deleting identical content)
            target_content = target['content'].replace("'", "''")
            target_ts = target['timestamp']
            table.delete(f"content = '{target_content}' AND timestamp = {target_ts}")
            print(f"Deleted first matching fact: {target['content']}")
        else:
            print(f"No facts found matching: {query}")
    except Exception as e:
        print(f"Error deleting fact: {e}")
        sys.exit(1)

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

def delete_episode(query: str):
    table = db.get_table("episodes")
    escaped = query.replace("'", "''")
    try:
        # Find the first match specifically
        matches = table.search().where(f"goal LIKE '%{escaped}%'").limit(1).to_list()
        if matches:
            target = matches[0]
            target_goal = target['goal'].replace("'", "''")
            target_ts = target['timestamp']
            table.delete(f"goal = '{target_goal}' AND timestamp = {target_ts}")
            print(f"Deleted first matching episode: {target['goal']}")
        else:
            print(f"No episodes found matching: {query}")
    except Exception as e:
        print(f"Error deleting episode: {e}")
        sys.exit(1)

def store_index(path: str, summary: str = None, classes: list = None, functions: list = None):
    table = db.get_table("code_index")
    
    # Check if we need to migrate the table (schema change)
    if "classes" not in table.schema.names:
        print("Migrating code_index table to new schema...")
        conn = db.get_db()
        conn.drop_table("code_index")
        table = db.get_table("code_index")
    
    if not os.path.exists(path):
        print(f"Error: Path {path} does not exist.")
        return

    # Auto-extract symbols for Python files if not provided manually
    if not classes and not functions and path.endswith(".py"):
        classes, functions = extract_python_symbols(path)

    if summary is None:
        # In a real scenario, this would trigger a headless Gemini call.
        # For now, we'll just use a placeholder.
        # Phase 2 will implement the actual headless Gemini summarization.
        summary = f"Summary for {path}"
    
    # Include symbols in the text to embed to enable semantic search of symbols
    text_to_embed = f"Summary: {summary}"
    if classes:
        text_to_embed += f" Classes: {', '.join(classes)}"
    if functions:
        text_to_embed += f" Functions: {', '.join(functions)}"

    embeddings = list(embedding_model.embed([text_to_embed]))
    vector = embeddings[0].tolist()
    
    mtime = os.path.getmtime(path)
    
    data = [{
        "file_path": os.path.abspath(path),
        "summary": summary,
        "classes": classes if classes is not None else [],
        "functions": functions if functions is not None else [],
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

def delete_index(path: str):
    table = db.get_table("code_index")
    abs_path = os.path.abspath(path)
    escaped = abs_path.replace("'", "''")
    try:
        table.delete(f"file_path = '{escaped}'")
        print(f"Deleted index entry for: {abs_path}")
    except Exception as e:
        print(f"Error deleting index: {e}")
        sys.exit(1)

def main(type: str, content: str = None, goal: str = None, result: str = None, category: str = None, path: str = None, symbols: str = None, classes: str = None, functions: str = None, delete: bool = False):
    try:
        if type == "fact":
            if not content:
                print("Error: content is required for type 'fact'")
                sys.exit(1)
            if delete:
                delete_fact(content)
            else:
                store_fact(content)
        elif type == "episode":
            # For episodes, if content is provided as positional, use it as summary
            summary = content
            if delete:
                if not goal:
                    # If only summary (content) is provided, use it as query
                    if summary:
                        delete_episode(summary)
                    else:
                        print("Error: goal or content (query) is required for type 'episode' deletion")
                        sys.exit(1)
                else:
                    delete_episode(goal)
            else:
                if not goal or not result or not category or not summary:
                    print("Error: goal, result, category, and summary (content) are required for type 'episode'")
                    sys.exit(1)
                store_episode(goal, result, category, summary)
        elif type == "index":
            if not path:
                # If path is not provided but content is, use content as path
                if content:
                    path = content
                else:
                    print("Error: path is required for type 'index'")
                    sys.exit(1)
            
            if delete:
                delete_index(path)
            else:
                summary_to_use = content if content != path else None
                # Parse classes/functions from comma-separated strings
                class_list = [c.strip() for c in classes.split(",")] if classes else None
                func_list = [f.strip() for f in functions.split(",")] if functions else None
                
                # Legacy support for --symbols flag (assigns to functions)
                if symbols and not func_list:
                    if isinstance(symbols, str):
                        func_list = [s.strip() for s in symbols.split(",")]
                    elif isinstance(symbols, (list, tuple)):
                        func_list = list(symbols)
                
                store_index(path, summary=summary_to_use, classes=class_list, functions=func_list)
        else:
            print(f"Unknown type: {type}")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fire.Fire(main)
