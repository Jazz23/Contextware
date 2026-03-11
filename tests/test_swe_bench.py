import os
import json
import subprocess
import tempfile
from datasets import load_dataset

def main():
    # 1. Load SWE-bench_Lite and select the first entry
    print("Loading SWE-bench_Lite dataset...")
    swebench_lite = load_dataset('princeton-nlp/SWE-bench_Lite', split='test')
    instance = swebench_lite[0]
    instance_id = instance['instance_id']
    repo = instance['repo'].split('/')[-1]
    base_commit = instance['base_commit']
    problem_statement = instance['problem_statement']
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as temp_file:
        temp_file.write(problem_statement)
        temp_prompt_path = temp_file.name

    
    docker_run_cmd = [
        "docker", "run", "--rm",
        "-v", "/home/vscode/.gemini:/root/.gemini",
        "-v", f"{temp_prompt_path}:/prompt.txt",
        "-w", f"/{repo}",
        "headless-gemini:latest",
        "bash", "-c", f"git reset --hard {base_commit} && cat ../prompt.txt | gemini -y && echo '---GIT_DIFF_START---' && git diff && echo '---GIT_DIFF_END---'"
    ]

    print(f"Running commands in container for instance {instance_id}...")
    
    process = subprocess.Popen(
        docker_run_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    patch_lines = []
    is_capturing_diff = False
    
    for line in process.stdout:
        print(line, end="")
        if "---GIT_DIFF_START---" in line:
            is_capturing_diff = True
            continue
        if "---GIT_DIFF_END---" in line:
            is_capturing_diff = False
            continue
        if is_capturing_diff:
            patch_lines.append(line)

    process.wait()
    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, docker_run_cmd)

    patch_content = "".join(patch_lines)

    # 4. Write output to file in 'output' folder next to the script
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f"{instance_id}.json")
    
    output_data = {
        "instance_id": instance_id,
        "model_name_or_path": "headless-gemini",
        "model_patch": patch_content
    }

    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=2)
        
    if os.path.exists(temp_prompt_path):
        os.remove(temp_prompt_path)
    
    print(f"Successfully wrote patch to {output_file}")

if __name__ == "__main__":
    main()
