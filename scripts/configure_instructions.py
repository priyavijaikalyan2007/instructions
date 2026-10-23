#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: f60aaafe-dafe-43a5-82cf-e4a7b81d2cff
# Created: 2026

# COMPONENT: Instruction profile configurator
# PURPOSE: Initialize or modify Markdown selections without replacing project-owned content.
# RELATES: instructions/PROJECT_PROFILE_TEMPLATE.md, instructions/REPO.md
# FLOW: Read -> interview/JSON merge -> validate -> preview -> explicit apply.
# SECURITY: Confine paths to the target repository and reject symlink destinations before writes.

from __future__ import annotations

import argparse
import difflib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import uuid

from profile_interview import run_interview
from agent_roles import (agent_entry_changes, apply_agent_roles, interview_agent_roles, profile_agent_roles)
from project_layout import (LEGACY_PATHS, PROFILE_PATH, STATE_PATH, canonical_profile, existing_project_path,
                            layout_changes, read_project_bytes, PUBLIC_DOCUMENTS)
from project_scaffolding import print_readiness, scaffolding_changes
from browser_profile import BROWSER_FIELDS, validate_browser
from source_folders import plan_source_folders, source_scope_warnings
from terminal_ui import input, print, set_color_mode, interactive_requested, run_interview_ui
from terminal_ui import present_preview, lock_navigation
from setup_review import summary_lines, detail_lines
from interview_cancelled import InterviewCancelled
from workspace_profile import WORKSPACE_FIELDS, validate_workspace
from profile_choices import LANGUAGE_GUIDES, language_values
from project_initialization import (initialization_changes, is_inherited, is_source_repository,
                                    prepare_initialization, safe_path)


LIBRARY_ROOT = Path(__file__).resolve().parents[1]
START = "<!-- instructions:managed:start -->"
END = "<!-- instructions:managed:end -->"
COMMON_GUIDES = {
    "WORKFLOW.md", "REPO.md", "LANGUAGE.md", "SECURITY_GUIDELINES.md", "CODING_STYLE.md",
    "COMMENTING.md", "MARKERS.md", "TESTING.md", "LOGGING.md", "COPYRIGHT_HEADER.md",
    "CODE_COMPLETE.md", "CODE_COMPLETE.checklist.md", "PRAGMATIC_PROGRAMMER.md",
    "PRAGMATIC_PROGRAMMER.checklist.md", "LITERATE_ERRORS.md",
}
FIELDS = {
    "source_paths": "Source paths", "targets": "Targets", "languages": "Languages", "platforms": "Platforms",
    "saas_client": "SaaS client", "sdk_component": "SDK component", "deployment": "Deployment",
}
REQUIRED_FIELDS = tuple(FIELDS)
FIELDS.update({"source_state": "Source state", "source_folders": "Source folders",
               **WORKSPACE_FIELDS, **BROWSER_FIELDS})
LIST_FIELDS = {"source_paths", "source_folders", "targets", "languages", "platforms", "browser_targets"}
TARGET_GUIDES = {
    "backend": "backend/BACKEND.md", "frontend": "frontend/FRONTEND.md", "saas": "saas/SAAS.md",
    "tools": "tools/TOOLS.md",
    "apps": "apps/APPS.md", "websites": "website/WEBSITES.md", "static-assets": "static-assets/STATIC_ASSETS.md",
    "google-workspace": "google-workspace/GOOGLE_WORKSPACE.md",
    "browser-extensions": "browser-extensions/BROWSER_EXTENSIONS.md",
    "sdks": "sdk/SDKs.md", "documentation": "DOCUMENTATION.md",
}
IDENTIFIER = re.compile(r"[a-z][a-z0-9-]*\Z")


def read_optional(root: Path, relative: str) -> str | None:
    """Read UTF-8 project configuration, preserving its newline bytes."""
    data = read_project_bytes(root, relative)
    return data.decode("utf-8") if data is not None else None


def fresh_template(name: str) -> str:
    """Copy a template with a new file identity and neutral, explicit unknown facts."""
    text = (LIBRARY_ROOT / "instructions" / name).read_text()
    text = re.sub(r"File GUID: [\w-]+", f"File GUID: {uuid.uuid4()}", text, count=1)
    if name == "PROJECT_PROFILE_TEMPLATE.md":
        text = text.replace('](REPO.md', '](instructions/REPO.md')
    if name == "PROJECT_TEMPLATE.md":
        text = re.sub(r"`<[^>]+>`", "`unspecified`", text)
    return text


def component_region(text: str) -> tuple[int, int]:
    """Locate the single Components section without treating other headings as components."""
    headings = list(re.finditer(r"^## Components\s*$", text, re.M))
    if len(headings) != 1:
        raise ValueError("Profile needs exactly one '## Components' section.")
    start = headings[0].end()
    following = re.search(r"^## ", text[start:], re.M)
    return start, start + following.start() if following else len(text)


def component_blocks(text: str) -> dict[str, tuple[int, int]]:
    """Return component spans, rejecting duplicate or ambiguous identifiers."""
    start, end = component_region(text)
    headings = list(re.finditer(r"^### (.+?)\s*$", text[start:end], re.M))
    result = {}
    for index, heading in enumerate(headings):
        identifier = heading.group(1)
        if not IDENTIFIER.fullmatch(identifier):
            raise ValueError(f"Invalid component identifier: {identifier}")
        if identifier in result:
            raise ValueError(f"Duplicate component identifier: {identifier}")
        stop = start + headings[index + 1].start() if index + 1 < len(headings) else end
        result[identifier] = (start + heading.start(), stop)
    return result


def field_line(label: str) -> str:
    """Return the exact-line expression used for editable Markdown fields."""
    return rf"^- {re.escape(label)}: ([^\r\n]*)\r?$"


def component_values(block: str) -> dict:
    """Parse known fields while leaving unknown prose and custom fields untouched."""
    enabled = re.findall(r"^- \[([ xX])\] Enabled\s*$", block, re.M)
    if len(enabled) != 1:
        raise ValueError("Each component needs exactly one Enabled checkbox.")
    result = {"enabled": enabled[0].lower() == "x"}
    for key, label in FIELDS.items():
        matches = re.findall(field_line(label), block, re.M)
        if len(matches) > 1:
            raise ValueError(f"Duplicate component field: {label}")
        value = matches[0].strip() if matches else ""
        result[key] = value
    return result


def split_values(value: str) -> list[str]:
    """Read comma-separated Markdown values, allowing the optional inline-code style."""
    return [part.strip().strip("`").strip() for part in value.split(",") if part.strip()]


def checked_saas(text: str) -> bool:
    """Read the existing SaaS product choice without enabling its scoped examples."""
    matches = re.findall(r"^- \[([ xX])\] SaaS product\s*$", text, re.M)
    if len(matches) != 1:
        raise ValueError("Profile needs exactly one SaaS product checkbox.")
    return matches[0].lower() == "x"


def formatted_value(key: str, value) -> str:
    """Validate JSON field types and produce a single safe Markdown line."""
    if key in {"enabled", "saas_client"}:
        if not isinstance(value, bool):
            raise ValueError(f"{key} must be a boolean.")
        return "yes" if value else "no"
    if key == "source_folders" and value == []:
        return ""
    if key in LIST_FIELDS:
        if not isinstance(value, list) or not value or any(not isinstance(item, str) for item in value):
            raise ValueError(f"{key} must be a nonempty list of strings.")
        if any("," in item for item in value):
            raise ValueError(f"{key} items cannot contain commas.")
        value = ", ".join(value)
    if not isinstance(value, str) or not value.strip() or any(char in value for char in "\r\n`|"):
        raise ValueError(f"{key} must contain nonempty text without Markdown delimiters or newlines.")
    return value.strip()


def same_field_value(key: str, current: dict, value, rendered: str) -> bool:
    """Retain handwritten formatting when a JSON update or accepted default has the same meaning."""
    if key == "enabled":
        return current["enabled"] == value
    existing = current.get(key, "")
    if key in LIST_FIELDS:
        return split_values(existing) == split_values(rendered)
    if key == "saas_client":
        return existing.lower() == rendered
    return existing.strip("`") == rendered


def update_component(block: str, changes: dict) -> str:
    """Change only selected field lines, preserving all surrounding component notes."""
    unknown = set(changes) - set(FIELDS) - {"enabled"}
    if unknown:
        raise ValueError(f"Unknown component fields: {', '.join(sorted(unknown))}")
    newline = "\r\n" if "\r\n" in block else "\n"
    current = component_values(block)
    for key, value in changes.items():
        rendered = formatted_value(key, value)
        if same_field_value(key, current, value, rendered):
            continue
        if key == "enabled":
            pattern = r"^- \[[ xX]\] Enabled\r?$"
            replacement = f"- [{'x' if value else ' '}] Enabled"
        else:
            pattern = field_line(FIELDS[key])
            replacement = f"- {FIELDS[key]}: {rendered}"
        matches = list(re.finditer(pattern, block, re.M))
        if len(matches) > 1:
            raise ValueError(f"Duplicate component field: {key}")
        if matches:
            block = re.sub(pattern, lambda _: replacement + ("\r" if newline == "\r\n" else ""), block, flags=re.M)
        else:
            block = block.rstrip("\r\n") + newline + replacement + newline + newline
    return block


def apply_answers(text: str, answers: dict) -> str:
    """Merge an explicit answer document into the existing Markdown profile."""
    if not isinstance(answers, dict) or set(answers) - {"saas_product", "components", "agent_roles"}:
        raise ValueError("Unknown answer fields. Use saas_product, components, and agent_roles only.")
    if "saas_product" in answers:
        value = answers["saas_product"]
        formatted_value("enabled", value)
        checked_saas(text)
        text = re.sub(r"(?m)^- \[[ xX]\] SaaS product", f"- [{'x' if value else ' '}] SaaS product", text)
    if "agent_roles" in answers:
        text = apply_agent_roles(text, answers["agent_roles"])
    updates = answers.get("components", {})
    if not isinstance(updates, dict):
        raise ValueError("components must be an object keyed by component identifier.")
    for identifier, changes in updates.items():
        if not IDENTIFIER.fullmatch(identifier) or not isinstance(changes, dict):
            raise ValueError(f"Invalid component update: {identifier}")
        blocks = component_blocks(text)
        if identifier not in blocks:
            _, end = component_region(text)
            text = text[:end] + f"\n### {identifier}\n\n- [ ] Enabled\n\n" + text[end:]
            blocks = component_blocks(text)
        start, end = blocks[identifier]
        text = text[:start] + update_component(text[start:end], changes) + text[end:]
    return text


def ask(prompt: str, default: str) -> str:
    """Keep the current value when the interview receives an empty answer."""
    answer = input(f"{prompt} [{default}]: ").strip()
    return answer or default


def ask_boolean(prompt: str, default: bool) -> bool:
    """Accept unambiguous yes/no responses instead of treating a typo as approval."""
    while True:
        answer = ask(prompt, "yes" if default else "no").lower()
        if answer in {"yes", "y", "no", "n"}:
            return answer in {"yes", "y"}
        print("Enter yes or no.")


def project_paths(text: str) -> dict[str, str]:
    """Read the existing project-file references without changing custom locations."""
    result = {}
    templates = [("Project facts", "PROJECT_TEMPLATE.md"), ("Additional instructions", "ADDITIONAL_TEMPLATE.md")]
    for label, name in templates:
        matches = re.findall(rf"^\| {label} \| `([^`]+)` \|\s*$", text, re.M)
        if len(matches) != 1:
            raise ValueError(f"Profile needs one Project files row for {label}.")
        if matches[0] in result:
            raise ValueError("Project facts and additional instructions need separate files.")
        result[matches[0]] = name
    return result


def validate_project_paths(root: Path, text: str) -> None:
    """Keep project context separate from shared guides, scripts, and agent entry points."""
    reserved = {PROFILE_PATH, "AGENTS.md", "CLAUDE.md", "CODEX.md", "GEMINI.md", "SETUP.md", *PUBLIC_DOCUMENTS}
    reserved.update(str(path.relative_to(LIBRARY_ROOT))
                    for path in (LIBRARY_ROOT / "instructions").rglob("*")
                    if path.is_file() and path.relative_to(LIBRARY_ROOT / "instructions").parts[0]
                    not in {"project", "maintenance"})
    seen = set()
    for relative in project_paths(text):
        path = safe_path(root, relative)
        normalized = str(path.relative_to(root))
        if normalized in reserved or normalized in seen or path.suffix.lower() != ".md":
            raise ValueError(f"Project context needs a separate Markdown file: {relative}")
        if path.exists() and not path.is_file():
            raise ValueError(f"Project context must be a regular file: {relative}")
        seen.add(normalized)


def validate_source_paths(root: Path, identifier: str, paths: str, state: str = "existing") -> list[str]:
    """Check literal or glob source paths against the target repository."""
    if state not in {"existing", "planned"}:
        raise ValueError(f"{identifier}: Source state must be existing or planned.")
    warnings = []
    values = split_values(paths)
    if not values:
        raise ValueError(f"{identifier}: at least one source path is required.")
    for value in values:
        path = safe_path(root, value)
        if any(parent.exists() and not parent.is_dir() for parent in path.parents):
            raise ValueError(f"{identifier}: source path parent is not a directory: {value}")
        matches = list(root.glob(value))
        if not matches and value in LEGACY_PATHS:
            previous = existing_project_path(root, value)
            matches = [previous] if previous.is_file() else []
        if value == "none" or (not matches and (state != "planned" or any(c in value for c in "*?[]"))):
            raise ValueError(f"{identifier}: source path does not exist: {value}. "
                             "Correct it or explicitly mark a literal new path as planned.")
        if not matches:
            warnings.append(f"{identifier}: planned source path is not created yet: {value}")
        for match in matches:
            safe_path(root, str(match.relative_to(root)))
    return warnings


def workspace_runtime_guides(values: dict) -> set[str]:
    """Select runtime guidance from validated Workspace metadata, not language guesses."""
    runtime = values.get("workspace_runtime", "").strip("`")
    if runtime == "apps-script":
        return {"apps-script/APPS_SCRIPT.md", "javascript/JAVASCRIPT.md"}
    if runtime == "http":
        return {"backend/BACKEND.md"}
    return set()


def language_scope(identifier: str, languages: str) -> tuple[set[str], list[str]]:
    """Resolve only declared languages and report coverage gaps without substituting another language."""
    guides, warnings = set(), []
    for language in language_values(languages):
        if language.lower() == "none":
            continue
        known = LANGUAGE_GUIDES.get(language.lower())
        if known:
            guides.update(known)
        else:
            warnings.append(f"{identifier}: language coverage gap for {language}; retain the actual language.")
    return guides, warnings


def validate_component(root: Path, identifier: str, values: dict) -> tuple[set, list, list]:
    """Validate enabled metadata and report guide gaps without inventing coverage."""
    for key in REQUIRED_FIELDS:
        value = values[key]
        if not value or "<" in value or ">" in value:
            raise ValueError(f"{identifier}: resolve {FIELDS[key]} before enabling this component.")
    targets = split_values(values["targets"])
    if not targets or set(targets) - set(TARGET_GUIDES):
        raise ValueError(f"{identifier}: unknown target in {values['targets']}")
    if values["saas_client"].lower() not in {"yes", "no"}:
        raise ValueError(f"{identifier}: SaaS client must be yes or no.")
    warnings = validate_source_paths(root, identifier, values["source_paths"],
                                     values.get("source_state", "").strip("`") or "existing")
    guides = {TARGET_GUIDES[target] for target in targets}
    if "google-workspace" in targets:
        warnings.extend(validate_workspace(values))
        guides.update(workspace_runtime_guides(values))
    if "browser-extensions" in targets:
        warnings.extend(validate_browser(values))
    language_guides, language_warnings = language_scope(identifier, values["languages"])
    guides.update(language_guides)
    warnings.extend(language_warnings)
    platforms = {value.lower() for value in split_values(values["platforms"])}
    if "apps" in targets and platforms - {"ios", "ipados", "macos"}:
        warnings.append(f"{identifier}: native platform coverage gap. Detailed app guidance covers Apple platforms.")
    return guides, warnings, targets


def validate_profile(root: Path, text: str) -> tuple[set, list]:
    """Validate relationships after every update so referenced SDKs cannot silently disappear."""
    saas = checked_saas(text)
    components = {key: component_values(text[start:end]) for key, (start, end) in component_blocks(text).items()}
    guides, warnings = ({"saas/SAAS.md"} if saas else set()), []
    for identifier, values in components.items():
        if not values["enabled"]:
            continue
        selected, gaps, _ = validate_component(root, identifier, values)
        guides.update(selected)
        warnings.extend(gaps)
        client = values["saas_client"].lower() == "yes"
        if client and not saas:
            raise ValueError(f"{identifier}: a SaaS client requires the SaaS product choice.")
        if client:
            guides.update(["saas/SAAS.md", "sdk/SDKs.md"])
        sdk = values["sdk_component"].strip("`")
        if sdk != "none":
            other = components.get(sdk, {})
            if not other.get("enabled") or "sdks" not in split_values(other.get("targets", "")):
                raise ValueError(f"{identifier}: SDK component {sdk!r} must name an enabled sdks component.")
        elif client:
            warnings.append(f"{identifier}: SaaS client has no SDK component; verify the explicit integration choice.")
    profile_agent_roles(text)
    validate_project_paths(root, text)
    return guides, warnings


def routing_block(guides: set[str]) -> str:
    """Derive scope links from the profile while keeping common and conditional obligations explicit."""
    lines = [START,
             "Read [the shared workflow](instructions/WORKFLOW.md) before planning or editing.",
             "Read `PROJECT_PROFILE.md` and its configured facts and additional instructions.",
             "The profile is authoritative. Regenerate this block after changing its selections.",
             "Use its tool-role assignments with [shared role definitions](instructions/AGENT_ROLES.md).",
             "",
             "Common requirements apply in every profile. Read the relevant task sections:", ""]
    lines.extend(f"- [{name}](instructions/{name})" for name in sorted(COMMON_GUIDES - {"WORKFLOW.md"}))
    lines.extend(["", "Enabled target and language guides. Read only those affected by the task:", ""])
    lines.extend(f"- [{name}](instructions/{name})" for name in sorted(guides))
    if not guides:
        lines.append("- No target or language guides selected.")
    lines.extend(["", "For AI or ML work, also read [AIML_SECURITY.md](instructions/AIML_SECURITY.md).",
                  "For credentials or sensitive data, read [SECRET_HANDLING.md](instructions/SECRET_HANDLING.md).",
                  "Select other task concerns from [WORKFLOW.md](instructions/WORKFLOW.md#select-shared-concerns).",
                  "Unselected guides remain installed for future use.", END])
    return "\n".join(lines)


def missing_shared_guides(root: Path) -> dict[str, bytes]:
    """Install nested shared guides, excluding project records and maintenance fixtures."""
    changes = {}
    library = LIBRARY_ROOT / "instructions"
    for path in sorted(library.rglob("*")):
        local = path.relative_to(library)
        if local.parts[0] in {"project", "maintenance"} or path.is_dir():
            continue
        relative = "instructions/" + local.as_posix()
        source = safe_path(LIBRARY_ROOT, relative)
        if source.is_file() and not safe_path(root, relative).exists():
            changes[relative] = source.read_bytes()
    return changes


def missing_setup_tools(root: Path) -> dict[str, bytes]:
    """Make a local target self-contained without replacing its existing scripts."""
    names = ['configure-instructions.sh', 'configure_instructions.py', 'project_initialization.py',
             'project_layout.py', 'agent_roles.py', 'license_selection.py', 'profile_interview.py',
             'browser_profile.py', 'workspace_profile.py', 'source_folders.py', 'terminal_ui.py',
             'project_context.py', 'project_scaffolding.py', 'interview_widgets.py',
             'curses_interview.py', 'interview_cancelled.py', 'setup_review.py', 'interview_history.py',
             'interview_question.py', 'interview_revisit.py', 'profile_choices.py']
    paths = ['configure.sh', *['scripts/' + name for name in names]]
    return {path: (LIBRARY_ROOT / path).read_bytes() for path in paths
            if not safe_path(root, path).exists()}


def managed_agents(existing: str, guides: set[str]) -> str:
    """Replace only our complete managed block or append it to handwritten root instructions."""
    managed = routing_block(guides)
    if existing.count(START) != existing.count(END) or existing.count(START) > 1:
        raise ValueError("Malformed AGENTS.md managed block. Preserve and repair it manually before configuration.")
    if START not in existing:
        return existing + ("\n\n" if existing else "") + managed + "\n"
    start, end = existing.index(START), existing.index(END)
    if end < start:
        raise ValueError("Malformed AGENTS.md managed block order.")
    return existing[:start] + managed + existing[end + len(END):]


def plan_changes(root: Path, profile: str, check: bool, guides: set[str]) -> dict[str, bytes]:
    """Plan additions without replacing installed guides, project facts, or local refinements."""
    if check:
        for relative in project_paths(profile):
            if not safe_path(root, relative).is_file():
                raise ValueError(f"Missing configured project file: {relative}")
        return {}
    changes = {PROFILE_PATH: profile.encode("utf-8")}
    changes.update(missing_shared_guides(root))
    for relative, template in project_paths(profile).items():
        if relative in changes or relative in {PROFILE_PATH, "AGENTS.md", "CLAUDE.md", "CODEX.md", "GEMINI.md"}:
            raise ValueError(f"Project file conflicts with an instruction file: {relative}")
        if read_project_bytes(root, relative) is None:
            changes[relative] = fresh_template(template).encode("utf-8")
    agents = read_optional(root, "AGENTS.md")
    agents = (LIBRARY_ROOT / "AGENTS.md").read_text() if agents is None else agents
    agents = canonical_profile(agents)
    changes["AGENTS.md"] = managed_agents(agents, guides).encode("utf-8")
    changes.update(agent_entry_changes(root, profile, LIBRARY_ROOT))
    return {name: data for name, data in changes.items()
            if not safe_path(root, name).exists() or safe_path(root, name).read_bytes() != data}


def preview(root: Path, changes: dict[str, bytes | None], folders: list[str], profile: str = '') -> None:
    """Show configuration diffs and list missing guides without dumping every shared document."""
    if present_preview(summary_lines(root, changes, folders, profile), detail_lines(root, changes)):
        return
    for folder in folders:
        print(f"Create source folder {folder}")
    for name, data in sorted(changes.items()):
        path = safe_path(root, name)
        action = 'Remove inherited' if data is None else ('Update' if path.exists() else 'Create')
        print(f"{action} {name}")
        review_files = {PROFILE_PATH, "AGENTS.md", "PROJECT.md", "ADDITIONAL.md", "SETUP.md",
                        "LICENSE", "THIRD_PARTY_NOTICES.md", *PUBLIC_DOCUMENTS}
        if data is not None and (name in review_files or name.startswith('.github/')):
            before = path.read_text().splitlines(True) if path.exists() else []
            after = data.decode("utf-8").splitlines(True)
            print("".join(difflib.unified_diff(before, after, fromfile=name, tofile=name)), end="")
    if not changes and not folders:
        print("No changes.")


def preflight_file_changes(root: Path, changes: dict[str, bytes | None]) -> None:
    """Validate every file destination before source folders or instruction files are written."""
    for name in changes:
        path = safe_path(root, name)
        if path.exists() and not path.is_file():
            raise ValueError(f"Destination is not a regular file: {name}")
        for parent in path.parents:
            if parent.exists() and not parent.is_dir():
                raise ValueError(f"Destination parent is not a directory: {parent}")
            if parent == root:
                break


def atomic_write(path: Path, data: bytes, mode: int) -> None:
    """Replace one file within its parent directory while preserving its selected permissions."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".instructions-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def write_changes(root: Path, changes: dict[str, bytes | None], folders: list[str]) -> None:
    """Preflight the complete plan and retain legacy state until its canonical replacement is written."""
    preflight_file_changes(root, changes)
    for folder in folders:
        safe_path(root, folder).mkdir(parents=True, exist_ok=True)
    ordered = sorted(changes, key=lambda name: (not name.startswith('.instructions/template-backup/'),
                                                name == LEGACY_PATHS[STATE_PATH], name == STATE_PATH,
                                                changes[name] is None, name))
    for name in ordered:
        path, data = safe_path(root, name), changes[name]
        if data is None:
            path.unlink(missing_ok=True)
            continue
        previous = existing_project_path(root, name)
        default_mode = 0o755 if name.endswith('.sh') else 0o644
        mode = previous.stat().st_mode & 0o777 if previous.exists() else default_mode
        atomic_write(path, data, mode)


def arguments() -> argparse.Namespace:
    """Define the public CLI without network access or automatic Git operations."""
    parser = argparse.ArgumentParser(description="Interview, preview, check, or edit a Markdown instruction profile.")
    target = parser.add_mutually_exclusive_group()
    target.add_argument("--root", type=Path, help="existing target repository (default: cwd)")
    target.add_argument("--target-folder", type=Path, help="initialize or edit a local folder without Git or GitHub")
    parser.add_argument("--configure-agents", action="store_true", help="interview tool-role assignments")
    parser.add_argument("--answers", type=Path, help="JSON selections merged into the existing Markdown profile")
    parser.add_argument("--initialize-project", action="store_true",
                        help="initialize project documents from templates, preserving customized files")
    parser.add_argument("--project-answers", type=Path,
                        help="JSON project identity and license choices for --initialize-project")
    parser.add_argument("--ui", choices=["auto", "curses", "plain"], default="auto",
                        help="ncurses forms on interactive terminals, or plain stream output")
    parser.add_argument("--color", choices=["auto", "always", "never"], default="auto",
                        help="terminal styling (auto respects redirected output, NO_COLOR, and TERM=dumb)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="preview only; never write")
    mode.add_argument("--apply", action="store_true", help="apply validated changes without a confirmation prompt")
    mode.add_argument("--check", action="store_true", help="validate the installed profile and selected guides")
    args = parser.parse_args()
    if args.target_folder and args.project_answers:
        args.initialize_project = True
    if args.project_answers and not (args.initialize_project or args.target_folder):
        parser.error("--project-answers requires --initialize-project")
    if args.initialize_project and args.check:
        parser.error("--initialize-project cannot be combined with --check")
    if args.check and (args.answers or args.configure_agents):
        parser.error("--check reads the installed profile; do not combine it with --answers")
    return args


def interview_profile(root: Path, profile: str, is_new: bool, configure_agents: bool) -> str:
    """Collect project choices and optional roles through the existing answer contract."""
    assignments = interview_agent_roles(profile_agent_roles(profile)) if is_new or configure_agents else None
    components = {key: component_values(profile[start:end])
                  for key, (start, end) in component_blocks(profile).items()}
    answers = run_interview(root, LIBRARY_ROOT, components, checked_saas(profile), is_new)
    if assignments is not None:
        answers['agent_roles'] = assignments
    return apply_answers(profile, answers)


def load_profile(root: Path, args: argparse.Namespace, identity: dict | None = None) -> str:
    """Read or initialize the profile, then collect only the requested input mode."""
    profile = read_optional(root, PROFILE_PATH)
    if profile is not None:
        profile = canonical_profile(profile)
    if identity is not None and is_inherited(root, PROFILE_PATH):
        profile = None
    is_new = profile is None
    if profile is None:
        if args.check:
            raise ValueError(f"Missing profile: {PROFILE_PATH}")
        profile = fresh_template("PROJECT_PROFILE_TEMPLATE.md")
        if identity is not None:
            profile = profile.replace('Repository: instructions', 'Repository: ' + identity['name'])
    if args.answers:
        answers = json.loads(args.answers.read_text())
        profile = apply_answers(profile, answers)
    elif args.configure_agents and not is_new:
        return apply_agent_roles(profile, interview_agent_roles(profile_agent_roles(profile)))
    elif not args.check and (not args.dry_run or args.target_folder):
        profile = interview_profile(root, profile, is_new, args.configure_agents)
    if args.configure_agents and args.answers:
        profile = apply_agent_roles(profile, interview_agent_roles(profile_agent_roles(profile)))
    return profile


def check_root_routing(root: Path, guides: set[str]) -> None:
    """Require the current managed routing block when validating an installed setup."""
    agents = read_optional(root, "AGENTS.md")
    if agents is None or START not in agents or managed_agents(agents, guides) != agents:
        raise ValueError("AGENTS.md needs the current managed routing block. Run the configurator to preview repair.")


def validated_root(path: Path, allow_missing: bool = False) -> Path:
    """Resolve an existing directory or an explicitly allowed missing local target without creating it."""
    if path.is_symlink() or (path.exists() and not path.is_dir()) or (not allow_missing and not path.is_dir()):
        raise ValueError("Target must be a directory without a final symlink. "
                         "Only --target-folder permits missing paths.")
    return path.resolve()


def report_selection(guides: set[str], warnings: list[str]) -> None:
    """Keep coverage warnings and selected guidance visible before the write preview."""
    for warning in warnings:
        print(f"Note: {warning}", file=sys.stderr)
    print("Selected target/language guides (narrow further by the task): " + ", ".join(sorted(guides)))


def validate_selected_guides(root: Path, guides: set[str], changes: dict) -> None:
    """Require selected files either on disk or in the validated installation plan."""
    for guide in sorted(guides | COMMON_GUIDES | {"AIML_SECURITY.md", "SECRET_HANDLING.md", "AGENT_ROLES.md"}):
        relative = "instructions/" + guide
        if relative not in changes and not safe_path(root, relative).is_file():
            raise ValueError(f"Missing selected guide: {relative}")


def project_setup_changes(root: Path, args, profile: str, identity: dict | None) -> tuple[dict, bool]:
    """Keep project-owned scaffolding separate from generic profile selection and checking."""
    changes = missing_setup_tools(root) if args.target_folder and not args.check else {}
    changes.update(initialization_changes(root, identity, project_paths(profile)))
    scaffold = bool(identity is not None or args.target_folder or existing_project_path(root, STATE_PATH).exists())
    if scaffold and not args.check:
        changes.update(scaffolding_changes(root, profile, project_paths(profile)))
    return changes, scaffold


def apply_preview(root: Path, args, changes: dict, folders: list[str]) -> None:
    """Apply only after the full preview, or leave all files unchanged on dry run and cancellation."""
    if args.dry_run or not (changes or folders):
        return
    if args.apply or ask_boolean("Apply these changes?", False):
        lock_navigation()
        write_changes(root, changes, folders)
        print(f"Applied {len(changes)} file changes and created {len(folders)} source folders.")
    else:
        print("Cancelled. No files changed.")


def configure_project(args) -> int:
    """Orchestrate input, validation, preview, and optional application."""
    root = validated_root(args.target_folder or args.root or Path.cwd(), bool(args.target_folder))
    if args.target_folder and is_source_repository(root):
        raise ValueError("Use a different target folder. This is the source instruction repository.")
    if args.target_folder and not args.check and read_optional(root, PROFILE_PATH) is None:
        args.initialize_project = True
    changes = layout_changes(root, args.check)
    identity = prepare_initialization(root, args)
    profile = load_profile(root, args, identity)
    guides, warnings = validate_profile(root, profile)
    changes.update(plan_changes(root, profile, args.check, guides))
    project_changes, scaffold = project_setup_changes(root, args, profile, identity)
    changes.update(project_changes)
    components = [component_values(profile[start:end]) for start, end in component_blocks(profile).values()]
    folders = plan_source_folders(root, components, changes, args.check)
    validate_selected_guides(root, guides, changes)
    report_selection(guides, warnings + source_scope_warnings(components))
    if args.check:
        check_root_routing(root, guides)
        print("Profile check passed.")
        return 0
    preview(root, changes, folders, profile)
    apply_preview(root, args, changes, folders)
    if scaffold:
        print_readiness(profile, project_paths(profile))
    return 0


def main() -> int:
    """Select presentation separately from the project configuration workflow."""
    args = arguments()
    set_color_mode(args.color)
    return run_interview_ui(lambda: configure_project(argparse.Namespace(**vars(args))),
                            args.ui, interactive_requested(args))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except InterviewCancelled:
        print("Cancelled. No files changed.")
        sys.exit(0)
    except KeyboardInterrupt:
        print("Interrupted. Review any reported changes before retrying.", file=sys.stderr)
        sys.exit(130)
    except (ValueError, OSError, EOFError) as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        sys.exit(2)
