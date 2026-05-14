"""Agent command helpers for skill-creator scripts."""

from __future__ import annotations

import os
import shlex
import subprocess
import tempfile
from pathlib import Path


AGENT_COMMAND_PRESETS = {
    # These are convenience presets, not a closed list of supported agents.
    "claude-code": "claude -p --output-format text",
    "claude": "claude -p --output-format text",
    "codex-cli": "codex exec",
    "codex": "codex exec",
    "gemini-cli": "gemini --prompt {prompt}",
    "gemini": "gemini --prompt {prompt}",
    "opencode": "opencode run {prompt}",
    "qwen-code": "qwen -p {prompt}",
    "qwen": "qwen -p {prompt}",
    "continue": "cn -p {prompt}",
    "cn": "cn -p {prompt}",
    "crush": "crush run {prompt}",
    "cursor": "cursor-agent -p {prompt} --output-format text",
    "cursor-agent": "cursor-agent -p {prompt} --output-format text",
    "copilot": "copilot -p {prompt}",
    "github-copilot": "copilot -p {prompt}",
    "goose": "goose run --no-session -t {prompt}",
    "aider": "aider --message {prompt}",
}


def resolve_agent_command(agent: str, command_template: str | None) -> str:
    """Return the command template for an agent.

    Unknown agent labels are treated as executable names that accept prompt
    text on stdin. This keeps the adapter open-ended as new agents appear.
    """
    if command_template:
        return command_template

    return AGENT_COMMAND_PRESETS.get(agent, agent)


def build_command(
    command_template: str,
    prompt: str,
    prompt_file: Path,
) -> tuple[list[str], bool]:
    """Build argv and report whether the prompt should also be sent on stdin."""
    argv: list[str] = []
    uses_prompt_placeholder = False

    for token in shlex.split(command_template):
        if token == "{prompt}":
            argv.append(prompt)
            uses_prompt_placeholder = True
            continue

        if "{prompt}" in token:
            argv.append(token.replace("{prompt}", prompt))
            uses_prompt_placeholder = True
            continue

        argv.append(
            token
            .replace("{prompt_file}", str(prompt_file))
        )
        if "{prompt_file}" in token:
            uses_prompt_placeholder = True

    return argv, not uses_prompt_placeholder


def run_agent_command(
    prompt: str,
    agent: str,
    command_template: str | None,
    timeout: int = 300,
    cwd: str | Path | None = None,
) -> str:
    """Run a configured agent CLI and return stdout."""
    resolved_template = resolve_agent_command(agent, command_template)

    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as handle:
        handle.write(prompt)
        prompt_file = Path(handle.name)

    try:
        cmd, send_stdin = build_command(resolved_template, prompt, prompt_file)
        env = os.environ.copy()
        if cmd and Path(cmd[0]).name == "claude":
            # Claude Code blocks nested interactive sessions via CLAUDECODE,
            # but one-shot subprocess calls are safe.
            env.pop("CLAUDECODE", None)

        result = subprocess.run(
            cmd,
            input=prompt if send_stdin else None,
            capture_output=True,
            text=True,
            env=env,
            timeout=timeout,
            cwd=cwd,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"{agent} command exited {result.returncode}\n"
                f"command: {' '.join(cmd)}\n"
                f"stderr: {result.stderr}"
            )
        return result.stdout
    finally:
        try:
            prompt_file.unlink()
        except FileNotFoundError:
            pass
