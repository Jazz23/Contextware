import os
import shutil
import subprocess
import sys
import argparse
import time

def setup_test_env(project_root, temp_dir):
    print(f"Setting up test environment in {temp_dir}...")
    
    # Clean up existing temp dir
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    # Copy test codebase
    test_codebase_src = os.path.join(project_root, "codebases", "test_codebase")
    for item in os.listdir(test_codebase_src):
        s = os.path.join(test_codebase_src, item)
        d = os.path.join(temp_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)
            
    # Copy skills/contextware to .temp/.gemini/skills/contextware
    skill_src = os.path.join(project_root, "skills", "contextware")
    skill_dest = os.path.join(temp_dir, ".gemini", "skills", "contextware")
    os.makedirs(os.path.dirname(skill_dest), exist_ok=True)
    shutil.copytree(skill_src, skill_dest)
    
    print("Setup complete.")
    return skill_dest

def run_command(cwd, command):
    print(f"Running: {' '.join(command)} in {cwd}")
    result = subprocess.run(
        command, 
        cwd=cwd, 
        capture_output=True, 
        text=True
    )
    if result.returncode != 0:
        print(f"Command failed with return code {result.returncode}")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        raise Exception("Command failed")
    return result.stdout

def test_integration(skill_dir, temp_dir):
    print("Running integration tests...")
    
    # Use uv run from the skill directory
    # Note: we need to handle relative paths carefully.
    
    # 1. Store a Fact
    print("\n--- Test 1: Store Fact ---")
    run_command(skill_dir, ["uv", "run", "scripts/store.py", "--type", "fact", "--content", "Integration Test Fact"])
    
    # 2. Recall Fact
    print("\n--- Test 2: Recall Fact ---")
    output = run_command(skill_dir, ["uv", "run", "scripts/recall.py", "--query", "Integration Test", "--scope", "memory"])
    print("Output:", output)
    if "Integration Test Fact" not in output:
        raise Exception("Failed to recall fact")
        
    # 3. Store Episode
    print("\n--- Test 3: Store Episode ---")
    run_command(skill_dir, [
        "uv", "run", "scripts/store.py", 
        "--type", "episode", 
        "--goal", "Test Goal",
        "--result", "success",
        "--category", "test",
        "--content", "We ran a test and it worked"
    ])
    
    # 4. Recall Episode
    print("\n--- Test 4: Recall Episode ---")
    output = run_command(skill_dir, ["uv", "run", "scripts/recall.py", "--query", "Test Goal", "--scope", "episodes"])
    print("Output:", output)
    if "Test Goal" not in output or "SUCCESS" not in output:
        raise Exception("Failed to recall episode")

    # 5. Index File
    print("\n--- Test 5: Index File manually ---")
    # Path is relative to where we run or absolute. 
    # Let's use absolute path to be safe, pointing to the main.py in .temp root
    target_file = os.path.abspath(os.path.join(temp_dir, "main.py"))
    run_command(skill_dir, ["uv", "run", "scripts/store.py", "--type", "index", "--path", target_file, "--content", "Main entry point"])
    
    # 6. Search Code
    print("\n--- Test 6: Search Code ---")
    output = run_command(skill_dir, ["uv", "run", "scripts/recall.py", "--query", "entry point", "--scope", "code"])
    print("Output:", output)
    if target_file not in output:
        raise Exception(f"Failed to find indexed file: {target_file}")
        
    # 7. Crawl
    print("\n--- Test 7: Crawl ---")
    # Crawl the temp_dir.
    run_command(skill_dir, ["uv", "run", "scripts/store.py", "--type", "crawl", "--path", os.path.abspath(temp_dir)])
    
    # 8. Search Content from Crawl
    print("\n--- Test 8: Search Crawled Content ---")
    # In store.py, if summary is None (which it is for crawl), it uses a placeholder "Summary for {path}".
    # Let's search for "Summary for" and the filename
    target_readme = os.path.abspath(os.path.join(temp_dir, "README.md"))
    output = run_command(skill_dir, ["uv", "run", "scripts/recall.py", "--query", "README", "--scope", "code"])
    print("Output:", output)
    if target_readme not in output:
        raise Exception("Failed to find crawled README")

    print("\nAll integration tests passed!")

def main():
    parser = argparse.ArgumentParser(description="Test Contextware Skill")
    parser.add_argument("--setup-only", action="store_true", help="Only set up the test environment, do not run tests")
    args = parser.parse_args()
    
    project_root = os.getcwd()
    temp_dir = os.path.join(project_root, ".temp")
    
    try:
        skill_dir = setup_test_env(project_root, temp_dir)
        
        if not args.setup_only:
            test_integration(skill_dir, temp_dir)
            
    except Exception as e:
        print(f"\nTest failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()