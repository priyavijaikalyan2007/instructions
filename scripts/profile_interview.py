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


PRODUCTS = {
    "1": ("SaaS", "Webapp with backend, browser frontend, and static assets.", {"backend", "frontend"}),
    "2": ("SaaS with Native Clients", "The webapp plus native apps and generated SDKs.",
          {"backend", "frontend", "sdks", "apps"}),
    "3": ("Microservice", "Backend only: APIs, data access, and an OpenAPI/Swagger endpoint.", {"backend"}),
    "4": ("Native App", "Standalone application for selected operating systems.", {"apps"}),
    "5": ("Static Website", "Website and static assets without an application backend.", {"websites"}),
    "6": ("CLI tools", "Command-line tools or plugins for selected operating systems.", {"tools"}),
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
    "documentation": ("Documentation", "Product or developer documentation and instruction files.",
                      "documentation", ["documentation"]),
    "static-assets": ("Static assets", "Shared bundles, styles, fonts, icons, and other browser assets.",
                      "assets", ["static-assets"]),
}
FIELD_HELP = {
    "source_paths": (
        "Which existing files or folders belong to this part? Paths are relative to the selected repository.",
        "Examples: src/server, apps/apple, web, scripts. A pattern such as *.md matches root Markdown files.",
        "Use commas for several paths. These paths limit where the selected guidance applies.",
    ),
    "languages": (
        "Enter the actual source languages used in this part, separated by commas.",
        "Examples: Java, C#, Swift, Go, Rust, or Python. Browser code may use TypeScript, HTML, and SCSS.",
    ),
    "platforms": (
        "Enter the operating systems or consumer platforms, separated by commas.",
        "Examples: iOS, iPadOS, macOS, Android, ChromeOS, Linux, or Windows. Use browser for a generated browser SDK.",
    ),
    "deployment": (
        "Describe how this part is packaged or delivered. This records a fact and does not deploy anything.",
        "Examples: container, served by the backend, CDN, native application, CLI binary, generated library, or none.",
    ),
}
FIELD_LABELS = {
    "source_paths": "Files or folders", "languages": "Source languages",
    "platforms": "Operating systems or platforms", "deployment": "Packaging or delivery",
}


def values_list(value: str) -> list[str]:
    """Read the profile's comma-separated strings for display and category selection."""
    return [item.strip().strip("`").strip() for item in value.split(",") if item.strip()]


def part_role(values: dict) -> str:
    """Use the existing component's scope rather than assuming its local identifier is a standard name."""
    targets = values_list(values.get("targets", ""))
    return next((role for role in PARTS if role in targets), "custom")


def show_intro(root: Path, library_root: Path, is_new: bool) -> None:
    """Identify the repository being edited before presenting any project choices."""
    print(f"Configuring repository: {root}")
    print("Profile: instructions/project/PROJECT_PROFILE.md")
    print("Creating a new profile." if is_new else "Editing an existing profile.")
    print("Component identifiers are local names in this profile, not product types.")
    print("Guidance is selected automatically from your product choices and actual source languages.")
    print("Press Enter to keep a displayed current value. No files change until you approve the final preview.")
    if root == library_root:
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


def connect_sdks(components: dict) -> None:
    """Connect selected clients to the single generated SDK scope when the relationship is unambiguous."""
    sdk_ids = [identifier for identifier, values in components.items()
               if values["enabled"] and part_role(values) == "sdks"]
    for values in components.values():
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
    return role


def ask_field(key: str, current: str) -> str:
    """Explain each requested fact and distinguish a required answer from an existing default."""
    print()
    for line in FIELD_HELP[key]:
        print(line)
    default = ", ".join(values_list(current)) if key != "deployment" else current.strip("`")
    if "<" in default:
        default = ""
    while True:
        answer = input(f"{FIELD_LABELS[key]} [{default or 'required'}]: ").strip()
        if answer or default:
            return answer or default
        print("Enter an actual value for this selected part.")


def configure_component(identifier: str, values: dict) -> dict:
    """Ask only for facts relevant to the selected part. Target codes remain an implementation detail."""
    role = show_component(identifier, values)
    changes = {"enabled": True, "targets": values_list(values["targets"])}
    changes["source_paths"] = values_list(ask_field("source_paths", values.get("source_paths", "")))
    if role != "documentation":
        changes["languages"] = values_list(ask_field("languages", values.get("languages", "")))
    else:
        changes["languages"] = values_list(values.get("languages", "none")) or ["none"]
    if role in {"apps", "sdks", "tools", "custom", "static-assets"}:
        changes["platforms"] = values_list(ask_field("platforms", values.get("platforms", "")))
    else:
        changes["platforms"] = values_list(values["platforms"])
        print("Platform retained: " + values["platforms"])
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
        connect_sdks(working)
    labels = [f"{PARTS.get(part_role(value), ('Project-specific part',))[0]} ({identifier})"
              for identifier, value in working.items() if value["enabled"]]
    print("\nIncluded parts: " + ", ".join(labels))
    print("Product selection changes instruction scope, not application source, folder structure, or deployments.")
    answers = {"saas_product": is_saas, "components": {}}
    for identifier, values in working.items():
        if values["enabled"]:
            answers["components"][identifier] = configure_component(identifier, values)
        else:
            answers["components"][identifier] = {"enabled": False}
    return answers
