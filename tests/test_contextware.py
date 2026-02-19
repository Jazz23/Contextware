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
    if "  Classes: Greeter" not in output or "  Functions: greet, hello" not in output:
        raise Exception("Failed to display separated classes and functions in search results")

    # 7. Lookup by Path
    print("\n--- Test 7: Lookup Path ---")
    output = run_command(skill_dir, ["uv", "run", "scripts/recall.py", "--path", target_file])
    print("Output:", output)
    if "Main entry point" not in output:
        raise Exception("Failed to find summary for file path")
    if "Classes: Greeter" not in output or "Functions: greet, hello" not in output:
        raise Exception("Failed to display separated classes and functions in path lookup")

    # 8. Index with Manual Classes/Functions
    print("\n--- Test 8: Index with Manual Classes/Functions ---")
    manual_file = os.path.abspath(os.path.join(temp_dir, "manual.py"))
    with open(manual_file, "w") as f:
        f.write("# Dummy file")
    
    run_command(skill_dir, [
        "uv", "run", "scripts/store.py", 
        "--type", "index", 
        "--path", manual_file, 
        "--content", "Manual content",
        "--classes", "ManualClass",
        "--functions", "manual_func"
    ])
    
    output = run_command(skill_dir, ["uv", "run", "scripts/recall.py", "--path", manual_file])
    print("Output:", output)
    if "Classes: ManualClass" not in output or "Functions: manual_func" not in output:
        raise Exception("Failed to retrieve manual classes and functions")

    # 9. Automatic Symbol Extraction (Separated)
    print("\n--- Test 9: Automatic Symbol Extraction (Separated) ---")
    auto_symbol_file = os.path.abspath(os.path.join(temp_dir, "auto_symbols.py"))
    with open(auto_symbol_file, "w") as f:
        f.write("class MyClass:\n    def method_one(self): pass\n\ndef function_two(): pass")
    
    # Index without providing symbols manually
    run_command(skill_dir, ["uv", "run", "scripts/store.py", "--type", "index", "--path", auto_symbol_file])
    
    output = run_command(skill_dir, ["uv", "run", "scripts/recall.py", "--path", auto_symbol_file])
    print("Output:", output)
    if "Classes: MyClass" not in output or "Functions: function_two" not in output:
        raise Exception("Automatic separated symbol extraction failed")

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
    
    # Delete first match
    run_command(skill_dir, ["uv", "run", "scripts/store.py", "--type", "fact", "--content", "Selective Match", "--delete"])
    
    # Check that one still exists
    output = run_command(skill_dir, ["uv", "run", "scripts/recall.py", "--query", "Selective Match", "--scope", "memory"])
    if "Selective Match" not in output:
        raise Exception("Deleted all matches instead of just the first one")
    
    # Delete the second one
    run_command(skill_dir, ["uv", "run", "scripts/store.py", "--type", "fact", "--content", "Selective Match", "--delete"])
    output = run_command(skill_dir, ["uv", "run", "scripts/recall.py", "--query", "Selective Match", "--scope", "memory"])
    if "--- Facts ---" in output and "Selective Match" in output:
         raise Exception("Failed to delete the second match")

    # 12. Semantic Search of Symbols
    print("\n--- Test 12: Semantic Search of Symbols ---")
    # Re-index main.py to use new embedding strategy
    run_command(skill_dir, ["uv", "run", "scripts/store.py", "--type", "index", "--path", target_file, "--content", "Main entry point"])
    
    # Search for a class name
    output = run_command(skill_dir, ["uv", "run", "scripts/recall.py", "--query", "Greeter class", "--scope", "code"])
    print("Output (Class Search):", output)
    if "main.py" not in output or "Classes: Greeter" not in output:
        raise Exception("Failed to find file via class name semantic search")
        
    # Search for a function name
    output = run_command(skill_dir, ["uv", "run", "scripts/recall.py", "--query", "hello function", "--scope", "code"])
    print("Output (Function Search):", output)
    if "main.py" not in output or "Functions: greet, hello" not in output:
        raise Exception("Failed to find file via function name semantic search")

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