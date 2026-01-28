- If you are required to read/write files and or folders relating to a "skill", read this documentation before doing so: https://geminicli.com/docs/cli/skills/ and https://agentskills.io/specification.
- If you are instructed to write code regarding "headless mode", read this documentation first: https://geminicli.com/docs/cli/headless/.
- **Implementation Plans:** Always place and read implementation plans in the `docs/` directory (e.g., `docs/stage1.md`). Check this directory first when starting a new stage of work.
- Whenever you need to write a python script that "invokes gemini" or executes another gemini agent (say, to e2e test a skill), use this command:

```python
    gemini_path = shutil.which("gemini")
    if not gemini_path:
        print("Error: 'gemini' executable not found in PATH.")
        sys.exit(1)

    prompt = "YOUR PROMPT HERE"
    command = [
        gemini_path,
        "-p", prompt,
        "--model", "gemini-3-flash-preview",
        "--output-format", "stream-json",
        "--yolo"
    ]
```