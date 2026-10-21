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
from workspace_profile import WORKSPACE_FIELDS, language_values, validate_workspace
from project_initialization import initialization_changes, is_inherited, prepare_initialization, safe_path


LIBRARY_ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = "instructions/project/PROJECT_PROFILE.md"
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
FIELDS.update({"source_state": "Source state", **WORKSPACE_FIELDS})
LIST_FIELDS = {"source_paths", "targets", "languages", "platforms"}
TARGET_GUIDES = {
    "backend": "backend/BACKEND.md", "frontend": "frontend/FRONTEND.md", "saas": "saas/SAAS.md",
    "tools": "tools/TOOLS.md",
    "apps": "apps/APPS.md", "websites": "website/WEBSITES.md", "static-assets": "static-assets/STATIC_ASSETS.md",
    "google-workspace": "google-workspace/GOOGLE_WORKSPACE.md",
    "browser-extensions": "browser-extensions/BROWSER_EXTENSIONS.md",
    "sdks": "sdk/SDKs.md", "documentation": "DOCUMENTATION.md",
}
LANGUAGE_GUIDES = {
    "c#": ["csharp/CSHARP.md"], "swift": ["swift/SWIFT.md"], "go": ["go/GO.md"], "rust": ["rust/RUST.md"],
    "java": ["java/JAVA.md"], "python": ["python/PYTHON.md"], "javascript": ["javascript/JAVASCRIPT.md"],
    "typescript": ["typescript/TYPESCRIPT.md", "javascript/JAVASCRIPT.md"], "html": ["html/HTML.md"],
    "css": ["css/CSS.md"],
    "scss": ["scss/SCSS.md", "css/CSS.md"], "sql": ["sql/SQL.md"], "shell": ["shell/SHELL.md"],
    "bash": ["shell/SHELL.md"],
    "apps script": ["javascript/JAVASCRIPT.md"], "google apps script": ["javascript/JAVASCRIPT.md"],
}
IDENTIFIER = re.compile(r"[a-z][a-z0-9-]*\Z")


def read_optional(root: Path, relative: str) -> str | None:
    """Read UTF-8 project configuration, preserving its newline bytes."""
    path = safe_path(root, relative)
    return path.read_bytes().decode("utf-8") if path.exists() else None


def fresh_template(name: str) -> str:
    """Copy a template with a new file identity and neutral, explicit unknown facts."""
    text = (LIBRARY_ROOT / "instructions" / name).read_text()
    text = re.sub(r"File GUID: [\w-]+", f"File GUID: {uuid.uuid4()}", text, count=1)
    if name == "PROJECT_PROFILE_TEMPLATE.md":
        text = text.replace('](REPO.md#', '](../REPO.md#')
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
    if not isinstance(answers, dict) or set(answers) - {"saas_product", "components"}:
        raise ValueError("Unknown answer fields. Use saas_product and components only.")
    if "saas_product" in answers:
        value = answers["saas_product"]
        formatted_value("enabled", value)
        checked_saas(text)
        text = re.sub(r"(?m)^- \[[ xX]\] SaaS product", f"- [{'x' if value else ' '}] SaaS product", text)
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
    reserved = {PROFILE_PATH, "AGENTS.md", "CLAUDE.md", "CODEX.md", "GEMINI.md"}
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
        if value == "none" or (not matches and (state != "planned" or any(c in value for c in "*?[]"))):
            raise ValueError(f"{identifier}: source path does not exist: {value}. "
                             "Correct it or explicitly mark a literal new path as planned.")
        if not matches:
            warnings.append(f"{identifier}: planned source path is not created yet: {value}")
        for match in matches:
            safe_path(root, str(match.relative_to(root)))
    return warnings


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
        if values.get("workspace_runtime", "").strip("`") == "http":
            guides.add("backend/BACKEND.md")
    for language in language_values(values["languages"]):
        if language.lower() == "none":
            continue
        known = LANGUAGE_GUIDES.get(language.lower())
        if known:
            guides.update(known)
        else:
            warnings.append(f"{identifier}: language coverage gap for {language}; retain the actual language.")
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
    validate_project_paths(root, text)
    return guides, warnings


def routing_block(guides: set[str]) -> str:
    """Derive scope links from the profile while keeping common and conditional obligations explicit."""
    lines = [START,
             "Read [the shared workflow](instructions/WORKFLOW.md) before planning or editing.",
             "Read `instructions/project/PROJECT_PROFILE.md` and its configured facts and additional instructions.",
             "The profile is authoritative. Regenerate this block after changing its selections.",
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
        if not safe_path(root, relative).exists():
            changes[relative] = fresh_template(template).encode("utf-8")
    agents = read_optional(root, "AGENTS.md")
    agents = (LIBRARY_ROOT / "AGENTS.md").read_text() if agents is None else agents
    changes["AGENTS.md"] = managed_agents(agents, guides).encode("utf-8")
    for name in ["CLAUDE.md", "CODEX.md", "GEMINI.md"]:
        if not safe_path(root, name).exists():
            changes[name] = (LIBRARY_ROOT / name).read_bytes()
    return {name: data for name, data in changes.items()
            if not safe_path(root, name).exists() or safe_path(root, name).read_bytes() != data}


def preview(root: Path, changes: dict[str, bytes | None]) -> None:
    """Show configuration diffs and list missing guides without dumping every shared document."""
    for name, data in sorted(changes.items()):
        path = safe_path(root, name)
        action = 'Remove inherited' if data is None else ('Update' if path.exists() else 'Create')
        print(f"{action} {name}")
        review_files = {PROFILE_PATH, "AGENTS.md", "LICENSE", "THIRD_PARTY_NOTICES.md"}
        if data is not None and (name in review_files or name.startswith('.github/')):
            before = path.read_text().splitlines(True) if path.exists() else []
            after = data.decode("utf-8").splitlines(True)
            print("".join(difflib.unified_diff(before, after, fromfile=name, tofile=name)), end="")
    if not changes:
        print("No changes.")


def write_changes(root: Path, changes: dict[str, bytes | None]) -> None:
    """Preflight every destination, then replace each file atomically within its parent directory."""
    for name in changes:
        path = safe_path(root, name)
        if path.exists() and not path.is_file():
            raise ValueError(f"Destination is not a regular file: {name}")
        for parent in path.parents:
            if parent.exists() and not parent.is_dir():
                raise ValueError(f"Destination parent is not a directory: {parent}")
            if parent == root:
                break
    ordered = sorted(changes, key=lambda name: (not name.startswith('instructions/project/template-backup/'),
                                                name == 'instructions/project/INITIALIZATION.json', name))
    for name in ordered:
        data = changes[name]
        path = safe_path(root, name)
        if data is None:
            path.unlink()
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary = tempfile.mkstemp(prefix=".instructions-", dir=path.parent)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(data)
            os.chmod(temporary, path.stat().st_mode & 0o777 if path.exists() else 0o644)
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)


def arguments() -> argparse.Namespace:
    """Define the public CLI without network access or automatic Git operations."""
    parser = argparse.ArgumentParser(description="Interview, preview, check, or edit a Markdown instruction profile.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="existing target repository (default: cwd)")
    parser.add_argument("--answers", type=Path, help="JSON selections merged into the existing Markdown profile")
    parser.add_argument("--initialize-project", action="store_true",
                        help="initialize project documents from templates, preserving customized files")
    parser.add_argument("--project-answers", type=Path,
                        help="JSON project identity and license choices for --initialize-project")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="preview only; never write")
    mode.add_argument("--apply", action="store_true", help="apply validated changes without a confirmation prompt")
    mode.add_argument("--check", action="store_true", help="validate the installed profile and selected guides")
    args = parser.parse_args()
    if args.project_answers and not args.initialize_project:
        parser.error("--project-answers requires --initialize-project")
    if args.initialize_project and args.check:
        parser.error("--initialize-project cannot be combined with --check")
    if args.check and args.answers:
        parser.error("--check reads the installed profile; do not combine it with --answers")
    return args


def load_profile(root: Path, args: argparse.Namespace, identity: dict | None = None) -> str:
    """Read or initialize the profile, then collect only the requested input mode."""
    profile = read_optional(root, PROFILE_PATH)
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
    elif not args.check and not args.dry_run:
        components = {key: component_values(profile[start:end])
                      for key, (start, end) in component_blocks(profile).items()}
        answers = run_interview(root, LIBRARY_ROOT, components, checked_saas(profile), is_new)
        profile = apply_answers(profile, answers)
    return profile


def check_root_routing(root: Path, guides: set[str]) -> None:
    """Require the current managed routing block when validating an installed setup."""
    agents = read_optional(root, "AGENTS.md")
    if agents is None or START not in agents or managed_agents(agents, guides) != agents:
        raise ValueError("AGENTS.md needs the current managed routing block. Run the configurator to preview repair.")


def validated_root(path: Path) -> Path:
    """Require a real existing target directory before any profile or project operation."""
    if path.is_symlink() or not path.is_dir():
        raise ValueError("--root must name an existing directory without a final symlink.")
    return path.resolve()


def main() -> int:
    """Orchestrate input, validation, preview, and optional application."""
    args = arguments()
    root = validated_root(args.root)
    identity = prepare_initialization(root, args)
    profile = load_profile(root, args, identity)
    guides, warnings = validate_profile(root, profile)
    changes = plan_changes(root, profile, args.check, guides)
    changes.update(initialization_changes(root, identity, project_paths(profile)))
    for guide in sorted(guides | COMMON_GUIDES | {"AIML_SECURITY.md", "SECRET_HANDLING.md"}):
        relative = "instructions/" + guide
        if relative not in changes and not safe_path(root, relative).is_file():
            raise ValueError(f"Missing selected guide: {relative}")
    for warning in warnings:
        print(f"Note: {warning}", file=sys.stderr)
    print("Selected target/language guides (narrow further by the task): " + ", ".join(sorted(guides)))
    if args.check:
        check_root_routing(root, guides)
        print("Profile check passed.")
        return 0
    preview(root, changes)
    if not args.dry_run and changes:
        if args.apply or ask_boolean("Apply these changes?", False):
            write_changes(root, changes)
            print(f"Applied {len(changes)} file changes.")
        else:
            print("Cancelled. No files changed.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, EOFError) as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        sys.exit(2)
