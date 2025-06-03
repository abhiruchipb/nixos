import os
import json
from groq import Groq
import subprocess

# Set your Groq API key here or ensure it's set in your environment
os.environ["GROQ_API_KEY"] = "yo api key"

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are an assistant that translates user requests for NixOS configuration changes into structured JSON commands.

Only use these actions:
- change_hostname (requires: hostname)
- add_user (requires: username, sudo [true/false])
- enable_ssh (no extra parameters)
- add_package (requires: package)
- change_timezone (requires: timezone)

For each request, output only a single JSON object with the action and required parameters.

If the user request is ambiguous, missing required information, or does not match any of the actions above, output only:
{"error": "invalid input"}

Never output anything except the JSON object.

Examples:
{"action": "add_user", "username": "bob", "sudo": false}
{"action": "change_hostname", "hostname": "workstation-01"}
{"error": "invalid input"}
"""

def get_structured_command(user_instruction):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_instruction}
        ],
        response_format={"type": "json_object"},  # Forces JSON output
        temperature=0
    )
    return json.loads(response.choices[0].message.content)

if __name__ == "__main__":
    print("Enter your configuration change request (natural language):")
    user_instruction = input("> ")
    command = get_structured_command(user_instruction)
    if "error" in command:
        print("invalid input.")
    else:
        print("Structured command for Rust tool:")
        print(json.dumps(command, indent=2))

        # Serialize the command as a compact JSON string
        json_command = json.dumps(command)

        # Path to your configuration.nix (edit if needed)
        config_path = r"D:\sem 6\project\ABHIRUCHI\configuration.nix"  # Or a full path if not in the same folder

        # Call the Rust CLI tool
        result = subprocess.run([
            "nix_config_editor/target/debug/nix_config_editor.exe",
            "--config", config_path,
            "--command", json_command
        ], capture_output=True, text=True)

        print("Rust tool output:")
        print(result.stdout)
        if result.stderr:
            print("Rust tool error output:")
            print(result.stderr)
