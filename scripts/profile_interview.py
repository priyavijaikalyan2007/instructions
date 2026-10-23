#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 99f78177-2d0e-4d79-8834-06373323f751
# Created: 2026

# COMPONENT: Product profile interview
# PURPOSE: Explain product choices and collect facts without exposing internal target codes.
# RELATES: configure_instructions.py, instructions/REPO.md
# FLOW: Parsed profile -> product categories -> selected part details -> existing answer-document contract.

from copy import deepcopy
from pathlib import Path

from project_initialization import is_source_repository, safe_path
from workspace_profile import interview_workspace
from profile_choices import select_languages, select_platforms
from browser_profile import interview_browser
from terminal_ui import input, print


PRODUCTS = {
    "1": ("SaaS", "Webapp with backend, browser frontend, and static assets.", {"backend", "frontend"}),
    "2": ("SaaS with Native Clients", "The webapp plus native apps and generated SDKs.",
          {"backend", "frontend", "sdks", "apps"}),
    "3": ("Microservice", "Backend only: APIs, data access, and an OpenAPI/Swagger endpoint.", {"backend"}),
    "4": ("Native App", "Standalone application for selected operating systems.", {"apps"}),
    "5": ("Static Website", "Website and static assets without an application backend.", {"websites"}),
    "6": ("CLI tools", "Command-line tools or plugins for selected operating systems.", {"tools"}),
    "7": ("Google Workspace Extensions", "Workspace or Editor add-ons, such as a Google Docs writing assistant.",
          {"google-workspace"}),
    "8": ("Browser Extensions", "Extensions for Chrome, Safari, Firefox, or selected compatible browsers.",
          {"browser-extensions"}),
}
PARTS = {
    "backend": ("Server backend", "APIs, data models, persistence, and service runtime.", "backend", ["backend"]),
    "frontend": ("Browser frontend", "Webapp pages, login, browser UI, and compiled static assets.",
                 "frontend", ["frontend", "static-assets"]),
    "sdks": ("Generated SDKs", "Clients generated from an OpenAPI/Swagger contract.", "sdk", ["sdks"]),
    "apps": ("Native applications", "Native app targets and shared application logic.", "native-client", ["apps"]),
    "websites": ("Static website", "Public pages, navigation, styles, and static assets.",
                 "website", ["websites", "static-assets"]),
    "tools": ("CLI tools", "Command-line programs and plugins.", "tool", ["tools"]),
    "google-workspace": ("Google Workspace extension", "Host-integrated Workspace or Editor add-on behavior.",
                         "workspace-extension", ["google-workspace"]),
    "browser-extensions": ("Browser extension", "Packaged browser UI, content scripts, and background events.",
                           "browser-extension", ["browser-extensions"]),
    "documentation": ("Documentation", "Product or developer documentation and instruction files.",
                      "documentation", ["documentation"]),
    "static-assets": ("Static assets", "Shared bundles, styles, fonts, icons, and other browser assets.",
                      "assets", ["static-assets"]),
}
SOURCE_PATH_DEFAULTS = {
    "backend": "src/service/core/backend",
    "frontend": "src/service/core/frontend, src/service/core/static",
    "sdks": "src/sdk/core-api",
    "apps": "src/app/companion",
    "websites": "src/website/public",
    "tools": "src/tool/administration",
    "google-workspace": "src/extensions/googleworkspace/markdown",
    "browser-extensions": "src/extensions/browser/markdown",
    "documentation": "docs",
    "static-assets": "src/library/ui-components",
}
FIELD_HELP = {
    "source_paths": (
        "Which existing or planned files or folders belong to this part?",
        "Paths are relative to the selected repository.",
        "Examples: src/service/core/backend, src/app/companion, docs. Patterns can match existing files.",
        "Use commas for several paths. These paths limit where the selected guidance applies.",
    ),
    "deployment": (
        "Describe how this part is packaged or delivered. This records a fact and does not deploy anything.",
        "Examples: container, served by the backend, CDN, native application, CLI binary, generated library, or none.",
    ),
}
FIELD_LABELS = {
    "source_paths": "Files or folders", "deployment": "Packaging or delivery",
}


def values_list(value: str) -> list[str]:
    """Read the profile's comma-separated strings for display and category selection."""
    return [item.strip().strip("`").strip() for item in value.split(",") if item.strip()]


def part_role(values: dict) -> str:
    """Use the existing component's scope rather than assuming its local identifier is a standard name."""
    targets = values_list(values.get("targets", ""))
    if "google-workspace" in targets:
        return "google-workspace"
    return next((role for role in PARTS if role in targets), "custom")


def show_intro(root: Path, library_root: Path, is_new: bool) -> None:
    """Identify the repository being edited before presenting any project choices."""
    print(f"Configuring repository: {root}")
    print("Profile: PROJECT_PROFILE.md")
    print("Creating a new profile." if is_new else "Editing an existing profile.")
    print("Component identifiers are local names in this profile, not product types.")
    print("Guidance is selected automatically from your product choices and actual source languages.")
    print("Press Enter to keep a displayed current value. No files change until you approve the final preview.")
    if root == library_root and is_source_repository(root):
        print("This is the instruction library's own repository.")
        print("Its components cover instruction documents and CLI tools.")
        print("To configure another project, cancel and restart with --root /path/to/that/project.")


def choose_products(is_new: bool) -> set[str] | None:
    """Select compatible product categories or retain the existing component configuration."""
    print("\nChoose the product types that this repository contains:")
    for number, (label, description, _) in PRODUCTS.items():
        print(f"  {number}. {label}: {description}")
    print("SaaS describes the product. Backend means server-side work. Frontend means the browser UI.")
    print("The microservice choice includes no browser frontend or static assets.")
    print("Extensions can stand alone or combine with SaaS. Microsoft Office extensions are not included yet.")
    print("Combine compatible categories, such as 1, 5, 6 for a SaaS, public website, and CLI tools.")
    if not is_new:
        print("Press Enter to keep the existing profile's enabled parts and SaaS relationships.")
    while True:
        prompt = "Product numbers, separated by commas" + (": " if is_new else " [keep existing]: ")
        answer = input(prompt).strip()
        if not answer and not is_new:
            return None
        choices = set(values_list(answer))
        if choices and choices <= PRODUCTS.keys() and len(choices & {"1", "2", "3"}) <= 1:
            return choices
        print("Choose listed numbers. Select only one of 1, 2, and 3 because those categories overlap.")


def new_part(role: str) -> dict:
    """Supply scope defaults only. Leave unknown project facts for the interview."""
    return {
        "enabled": False, "source_paths": "", "targets": ", ".join(PARTS[role][3]), "languages": "",
        "platforms": "", "saas_client": "no", "sdk_component": "none", "deployment": "",
    }


def fill_scope_defaults(values: dict, role: str) -> None:
    """Fill fixed platform roles without assuming source languages, paths, or delivery facts."""
    fixed_platform = {"backend": "server", "frontend": "browser", "websites": "browser", "documentation": "none"}
    for key in ["platforms", "saas_client", "sdk_component"]:
        value = values.get(key, "")
        if not value or "<" in value:
            defaults = {"platforms": fixed_platform.get(role, ""), "saas_client": "no", "sdk_component": "none"}
            values[key] = defaults[key]


def select_parts(components: dict, choices: set[str]) -> tuple[dict, bool]:
    """Translate product choices into existing component roles while retaining identifiers and notes."""
    working = deepcopy(components)
    roles = set().union(*(PRODUCTS[choice][2] for choice in choices))
    if "frontend" in roles or "websites" in roles:
        roles.add("static-assets")
    for values in working.values():
        role = part_role(values)
        if role in PARTS and role != "documentation":
            values["enabled"] = role in roles
    for role in [role for role in PARTS if role in roles and role != "static-assets"]:
        if not any(part_role(values) == role for values in working.values()):
            identifier = PARTS[role][2]
            while identifier in working:
                identifier += "-new"
            working[identifier] = new_part(role)
            working[identifier]["enabled"] = True
    is_saas = bool(choices & {"1", "2", "3"})
    for values in working.values():
        role = part_role(values)
        fill_scope_defaults(values, role)
        if role == "apps":
            values["saas_client"] = "yes" if "2" in choices else "no"
            if "2" not in choices:
                values["sdk_component"] = "none"
        elif role == "frontend":
            values["saas_client"] = "yes" if is_saas else "no"
    return working, is_saas


def connect_sdks(components: dict, selected: set[str] | None = None) -> None:
    """Connect selected clients to the single generated SDK scope when the relationship is unambiguous."""
    sdk_ids = [identifier for identifier, values in components.items()
               if values["enabled"] and part_role(values) == "sdks"]
    for identifier, values in components.items():
        if selected is not None and identifier not in selected:
            continue
        if not values["enabled"] or values.get("saas_client") != "yes":
            continue
        current = values.get("sdk_component", "none")
        if current not in sdk_ids and len(sdk_ids) == 1:
            values["sdk_component"] = sdk_ids[0]
        elif current not in sdk_ids:
            values["sdk_component"] = "none"


def show_component(identifier: str, values: dict) -> str:
    """Explain an existing or selected component through its purpose and actual covered paths."""
    role = part_role(values)
    label, description = PARTS[role][:2] if role in PARTS else ("Project-specific part", "Retain its configured scope.")
    print(f"\nComponent: {identifier} ({label})")
    print(description)
    paths = values.get("source_paths", "")
    print("Covers: " + (", ".join(values_list(paths)) if paths and "<" not in paths else "not configured yet"))
    if values.get("saas_client") == "yes":
        print("This part consumes a hosted SaaS API.")
        sdk = values.get("sdk_component", "none")
        print(f"Uses generated SDK: {sdk}" if sdk != "none" else "No generated SDK component is linked.")
    elif role == "apps":
        print("This is a standalone native app. It does not select SaaS authentication or a generated SDK by default.")
    if role in {"google-workspace", "browser-extensions"}:
        show_extension_help(role)
    return role


def ask_field(key: str, current: str, role: str = "") -> str:
    """Explain each requested fact and distinguish a required answer from an existing default."""
    print()
    help_lines = FIELD_HELP[key]
    if key == "source_paths" and role == "google-workspace":
        help_lines = ("Enter repository-relative paths separated by commas. Missing literal paths can be planned.",)
    for line in help_lines:
        print(line)
    default = ", ".join(values_list(current)) if key != "deployment" else current.strip("`")
    if "<" in default:
        default = ""
    while True:
        answer = input(f"{FIELD_LABELS[key]} [{default or 'required'}]: ").strip()
        if answer or default:
            return answer or default
        print("Enter an actual value for this selected part.")


def show_extension_help(role: str) -> None:
    """Describe host and runtime facts without imposing a single extension architecture."""
    if role == "google-workspace":
        print("Choose current Google hosts, add-on UI, runtime, and audience in the following steps.")
        print("The choices include build, asset, host-testing, and release guidance.")
    else:
        print("Choose browsers, their operating systems, source languages, and installation channels.")
        print("Build output, packaged assets, local tests, and store requirements follow those choices.")


def configure_extension_clients(components: dict, is_saas: bool) -> set[str]:
    """Ask about SaaS use explicitly and clear obsolete links when selecting standalone extensions."""
    newly_connected = set()
    for identifier, values in components.items():
        if not values["enabled"] or part_role(values) not in {"google-workspace", "browser-extensions"}:
            continue
        default = values.get("saas_client", "no")
        if default not in {"yes", "no"}:
            default = "no"
        answer = "no"
        if is_saas:
            print(f"\n{identifier}: a SaaS API connection selects SaaS and SDK contract guidance.")
            while True:
                answer = input(f"Does this extension use this repository's SaaS API? [{default}]: ").strip().lower()
                answer = answer or default
                if answer in {"yes", "no"}:
                    break
                print("Enter yes or no. A Google or browser account alone does not make this a SaaS client.")
        if answer == "yes" and default != "yes":
            newly_connected.add(identifier)
        values["saas_client"] = answer
        if answer == "no":
            values["sdk_component"] = "none"
    return newly_connected


def source_path_default(values: dict, role: str) -> str:
    """Suggest a named component path only when no concrete project-owned path is configured."""
    current = values.get("source_paths", "")
    if current.strip() and "<" not in current:
        return current
    proposed = SOURCE_PATH_DEFAULTS.get(role, "")
    if proposed:
        print("\nSuggested source scope for a new component: " + proposed)
        print("Replace example component names if needed. Existing layouts can keep their configured paths.")
    if role == "backend":
        print("If this service owns database scripts, also include src/service/core/database in its source scope.")
    return proposed


def approve_missing_paths(missing: list[str], values: dict, bootstrap: bool) -> bool:
    """Explain the planned-path and first-setup directory semantics before collecting consent."""
    print("These source paths do not exist yet: " + ", ".join(missing))
    if bootstrap:
        print("First setup will create these paths as source folders after final approval.")
        print("For a future file, select its parent folder instead. No application files will be generated.")
    else:
        print("Planned scope selects future work. Existing profiles do not create new folders automatically.")
    default = "yes" if bootstrap or values.get("source_state", "").strip("`") == "planned" else "no"
    question = "Create these source folders after final approval?" if bootstrap else "Record these as planned paths?"
    answer = input(f"{question} [{default}]: ").strip().lower() or default
    if answer in {"yes", "y"}:
        return True
    print("Re-enter existing paths or choose planned paths explicitly.")
    return False


def ask_source_paths(root: Path, values: dict, role: str, bootstrap: bool = False) -> dict:
    """Collect safe source scope and explicit first-setup folder creation before the final preview."""
    current = source_path_default(values, role)
    if role == "google-workspace":
        print("\nInclude add-on source, manifest, build configuration, and release-asset paths in this scope.")
        print("Keep them inside the named extension. Add future host paths only when they enter scope.")
    while True:
        paths = values_list(ask_field("source_paths", current, role))
        try:
            missing = missing_source_paths(root, paths)
        except ValueError as error:
            print(str(error))
            continue
        result = {"source_paths": paths}
        if missing:
            if not approve_missing_paths(missing, values, bootstrap):
                continue
            result["source_state"] = "planned"
            if bootstrap:
                result["source_folders"] = missing
        elif values.get("source_state") and not values.get("source_folders"):
            result["source_state"] = "existing"
        if values.get("source_folders") and "source_folders" not in result:
            result["source_folders"] = [path for path in values_list(values["source_folders"]) if path in paths]
        return result


def missing_source_paths(root: Path, paths: list[str]) -> list[str]:
    """Reject unsafe paths and unmatched patterns before asking whether missing literal paths are planned."""
    missing = []
    for value in paths:
        path = safe_path(root, value)
        if any(parent.exists() and not parent.is_dir() for parent in path.parents):
            raise ValueError("A source path parent is a file. Enter a path beneath a directory.")
        matches = list(root.glob(value))
        if value == "none" or (not matches and any(char in value for char in "*?[]")):
            raise ValueError("Enter a literal planned path or a pattern that matches existing source files.")
        for match in matches:
            safe_path(root, str(match.relative_to(root)))
        if not matches:
            missing.append(value)
    if not paths:
        raise ValueError("Enter at least one source path.")
    return missing


def configure_component(identifier: str, values: dict, root: Path, bootstrap: bool = False) -> dict:
    """Ask only for facts relevant to the selected part. Target codes remain an implementation detail."""
    role = show_component(identifier, values)
    changes = {"enabled": True, "targets": values_list(values["targets"])}
    if role in {"google-workspace", "browser-extensions"}:
        interview = interview_workspace if role == "google-workspace" else interview_browser
        changes.update(interview(values))
        changes.update(ask_source_paths(root, values, role, bootstrap))
        changes.update(saas_client=values["saas_client"].lower() == "yes", sdk_component=values["sdk_component"])
        return changes
    changes.update(ask_source_paths(root, values, role, bootstrap))
    changes["platforms"] = select_platforms(role, values.get("platforms", ""))
    if role != "documentation":
        changes["languages"] = select_languages(role, changes["platforms"], values.get("languages", ""))
    else:
        changes["languages"] = values_list(values.get("languages", "none")) or ["none"]
    changes["saas_client"] = values["saas_client"].lower() == "yes"
    changes["sdk_component"] = values["sdk_component"]
    changes["deployment"] = ask_field("deployment", values.get("deployment", ""))
    return changes


def run_interview(root: Path, library_root: Path, components: dict, is_saas: bool, is_new: bool) -> dict:
    """Return the existing answer-document shape for the core editor to validate and preview."""
    show_intro(root, library_root, is_new)
    choices = choose_products(is_new)
    working = deepcopy(components)
    if choices is not None:
        working, is_saas = select_parts(components, choices)
    newly_connected = configure_extension_clients(working, is_saas)
    connect_sdks(working, None if choices is not None else newly_connected)
    labels = [f"{PARTS.get(part_role(value), ('Project-specific part',))[0]} ({identifier})"
              for identifier, value in working.items() if value["enabled"]]
    print("\nIncluded parts: " + ", ".join(labels))
    print("Product choices select instructions. First setup can also create approved source folders after the preview.")
    answers = {"saas_product": is_saas, "components": {}}
    for identifier, values in working.items():
        if values["enabled"]:
            answers["components"][identifier] = configure_component(identifier, values, root, is_new)
        else:
            answers["components"][identifier] = {"enabled": False}
    return answers
