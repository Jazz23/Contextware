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
    target_file = os.path.abspath(os.path.join(temp_dir, "main.py"))
    run_command(skill_dir, ["uv", "run", "scripts/store.py", "--type", "index", "--path", target_file, "--content", "Main entry point"])
    
    # 6. Search Code (Hierarchical)
    print("\n--- Test 6: Search Code (Hierarchical) ---")
    output = run_command(skill_dir, ["uv", "run", "scripts/recall.py", "--query", "entry point", "--scope", "code"])
    print("Output:", output)
    if target_file not in output:
        raise Exception(f"Failed to find indexed file: {target_file}")
    if "  Functions: main, top_level_func" not in output:
        raise Exception("Failed to display top-level functions")
    if "  Class Processor:" not in output or "    Methods: __init__, log, process_all, process_item" not in output:
        raise Exception("Failed to display class methods hierarchical")

    # 7. Lookup by Path
    print("\n--- Test 7: Lookup Path ---")
    output = run_command(skill_dir, ["uv", "run", "scripts/recall.py", "--path", target_file])
    print("Output:", output)
    if "Main entry point" not in output:
        raise Exception("Failed to find summary for file path")
    if "Class Processor:" not in output or "  Methods: __init__, log, process_all, process_item" not in output:
        raise Exception("Failed to display hierarchical symbols in path lookup")

    # 10. Deletion
    print("\n--- Test 10: Deletion ---")
    
    # 10.1 Delete Fact
    run_command(skill_dir, ["uv", "run", "scripts/store.py", "--type", "fact", "--content", "Integration Test Fact", "--delete"])
    output = run_command(skill_dir, ["uv", "run", "scripts/recall.py", "--query", "Integration Test", "--scope", "memory"])
    if "Integration Test Fact" in output:
        raise Exception("Failed to delete fact")
        
    # 10.2 Delete Episode
    run_command(skill_dir, ["uv", "run", "scripts/store.py", "--type", "episode", "--content", "Test Goal", "--delete"])
    output = run_command(skill_dir, ["uv", "run", "scripts/recall.py", "--query", "Test Goal", "--scope", "episodes"])
    if "Test Goal" in output:
        raise Exception("Failed to delete episode")
        
    # 10.3 Delete Index
    run_command(skill_dir, ["uv", "run", "scripts/store.py", "--type", "index", "--path", target_file, "--delete"])
    output = run_command(skill_dir, ["uv", "run", "scripts/recall.py", "--path", target_file])
    if "No index entry found" not in output:
        raise Exception("Failed to delete index entry")

    # 11. Selective Deletion (Delete just the first match)
    print("\n--- Test 11: Selective Deletion ---")
    run_command(skill_dir, ["uv", "run", "scripts/store.py", "--type", "fact", "--content", "Selective Match 1"])
    run_command(skill_dir, ["uv", "run", "scripts/store.py", "--type", "fact", "--content", "Selective Match 2"])
    
    run_command(skill_dir, ["uv", "run", "scripts/store.py", "--type", "fact", "--content", "Selective Match", "--delete"])
    
    output = run_command(skill_dir, ["uv", "run", "scripts/recall.py", "--query", "Selective Match", "--scope", "memory"])
    if "Selective Match" not in output:
        raise Exception("Deleted all matches instead of just the first one")
    
    run_command(skill_dir, ["uv", "run", "scripts/store.py", "--type", "fact", "--content", "Selective Match", "--delete"])
    output = run_command(skill_dir, ["uv", "run", "scripts/recall.py", "--query", "Selective Match", "--scope", "memory"])
    if "--- Facts ---" in output and "Selective Match" in output:
         raise Exception("Failed to delete the second match")

    # 12. Semantic Search of Symbols
    print("\n--- Test 12: Semantic Search of Symbols ---")
    run_command(skill_dir, ["uv", "run", "scripts/store.py", "--type", "index", "--path", target_file, "--content", "Main entry point"])
    
    output = run_command(skill_dir, ["uv", "run", "scripts/recall.py", "--query", "Processor class", "--scope", "code"])
    if "main.py" not in output or "Class Processor" not in output:
        raise Exception("Failed to find file via class name semantic search")
        
    output = run_command(skill_dir, ["uv", "run", "scripts/recall.py", "--query", "log function", "--scope", "code"])
    if "main.py" not in output or "log, process_all" not in output:
        raise Exception("Failed to find file via function name semantic search")

    print("\nAll integration tests passed!")

def main():
    parser = argparse.ArgumentParser(description="E2E Test Environment for Contextware Skill")
    parser.add_argument("--test", action="store_true", help="Run integration tests after setup")
    args = parser.parse_args()
    
    project_root = os.getcwd()
    temp_dir = os.path.join(project_root, ".temp")
    
    try:
        skill_dir = setup_test_env(project_root, temp_dir)
        
        if args.test:
            test_integration(skill_dir, temp_dir)
        else:
            print("\nSetup complete. Skill directory is:", skill_dir)
            print("Run with --test to execute integration tests.")
            
    except Exception as e:
        print(f"\nFailed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
