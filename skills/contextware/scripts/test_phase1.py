import subprocess
import os
import shutil

def run_command(cmd):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        print(f"Output: {result.stdout}")
    else:
        print(result.stdout)
    return result

def main():
    # Ensure we are in the skill directory
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(skill_dir)
    
    # Clean up old data for testing
    data_dir = os.path.join(skill_dir, "data")
    if os.path.exists(data_dir):
        print(f"Cleaning up {data_dir}")
        shutil.rmtree(data_dir)

    print("--- Testing Facts ---")
    run_command(["uv", "run", "scripts/store.py", "--type", "fact", "--content", "User prefers TypeScript over JavaScript"])
    run_command(["uv", "run", "scripts/recall.py", "--query", "language preference", "--scope", "memory"])

    print("\n--- Testing Episodes ---")
    run_command(["uv", "run", "scripts/store.py", "--type", "episode", "--goal", "Fix login bug", "--result", "success", "--category", "code", "--content", "Fixed the issue by adding null check in auth.ts"])
    run_command(["uv", "run", "scripts/recall.py", "--query", "login", "--scope", "episodes"])

    print("\n--- Testing Indexing ---")
    test_file = os.path.join(skill_dir, "README.md")
    run_command(["uv", "run", "scripts/store.py", "--type", "index", "--path", test_file])
    run_command(["uv", "run", "scripts/recall.py", "--query", "contextware documentation", "--scope", "code"])

    print("\n--- Testing Crawl ---")
    run_command(["uv", "run", "scripts/store.py", "--type", "crawl", "--path", "."])
    run_command(["uv", "run", "scripts/recall.py", "--query", "store script", "--scope", "code"])

    print("\n--- Testing Exact Mode ---")
    run_command(["uv", "run", "scripts/recall.py", "--query", "db connection", "--scope", "code", "--mode", "exact", "--limit", "1"])

if __name__ == "__main__":
    main()
