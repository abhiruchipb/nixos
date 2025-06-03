# Call the Rust CLI tool
result = subprocess.run([
    "nix_config_editor/target/debug/nix_config_editor.exe",
    "--config", config_path,
    "--command", json_command
], capture_output=True, text=True)