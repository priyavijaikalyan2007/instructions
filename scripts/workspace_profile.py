#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 615baad6-aa20-4077-bb5d-c9cb90b26abb
# Created: 2026

# COMPONENT: Google Workspace profile choices
# PURPOSE: Explain compatible hosts, runtimes, builds, and distribution before recording project scope.
# RELATES: profile_interview.py, configure_instructions.py, instructions/google-workspace/GOOGLE_WORKSPACE.md
# FLOW: Host -> model -> runtime -> account -> distribution -> source languages -> guidance summary.

from profile_choices import language_values, select_languages

from terminal_ui import input, print


WORKSPACE_FIELDS = {
    'workspace_model': 'Workspace model', 'workspace_runtime': 'Workspace runtime',
    'workspace_account': 'Workspace account', 'workspace_distribution': 'Workspace distribution',
}
HOSTS = ['Google Docs', 'Gmail', 'Google Sheets', 'Google Slides', 'Google Forms', 'Google Calendar', 'Google Drive']
EDITOR_HOSTS = {'Google Docs', 'Google Sheets', 'Google Slides', 'Google Forms'}
CHOICES = {
    'workspace_model': [('editor', 'Editor add-on: menus and custom HTML sidebars/dialogs in desktop editors.'),
                        ('workspace', 'Workspace add-on: host-rendered cards across hosts, including Gmail.')],
    'workspace_runtime': [('apps-script', 'Apps Script: JavaScript runs in Google-managed Apps Script.'),
                          ('http', 'HTTP: your HTTPS service handles add-on events and returns card responses.')],
    'workspace_account': [('personal', 'Personal Google account: developer testing or public distribution.'),
                          ('organization',
                           'Workspace organization account: also supports private domain distribution.')],
    'workspace_distribution': [('test', 'Test installation: developer/test accounts, no Marketplace listing yet.'),
                               ('private', 'Private Marketplace: users in your Workspace organization only.'),
                               ('public', 'Public Marketplace: external users, review, and OAuth checks.')],
}


def ask_choice(key: str, current: str = '') -> str:
    """Explain numbered choices and keep a valid recorded value on Enter."""
    current = current.strip('`')
    options = CHOICES[key]
    print('\n' + WORKSPACE_FIELDS[key] + ':')
    for index, (_, description) in enumerate(options, 1):
        print(f'  {index}. {description}')
    default = next((str(i) for i, (value, _) in enumerate(options, 1) if value == current), '')
    while True:
        answer = input(f'{WORKSPACE_FIELDS[key]} number [{default or "required"}]: ').strip() or default
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return options[int(answer) - 1][0]
        print('Choose one of the displayed numbers.')


def ask_hosts(current: str) -> list[str]:
    """Select current host support without enabling possible future products."""
    print('\nWhich Google applications will this component support now?')
    print('Keep possible future hosts out of this selection. Add them when you implement their integration.')
    for index, host in enumerate(HOSTS, 1):
        print(f'  {index}. {host}')
    existing = [part.strip().strip('`') for part in current.split(',')]
    default = ','.join(str(HOSTS.index(host) + 1) for host in existing if host in HOSTS)
    while True:
        answer = input(f'Host numbers, separated by commas [{default or "required"}]: ').strip() or default
        numbers = [part.strip() for part in answer.split(',')]
        if all(number.isdigit() and 1 <= int(number) <= len(HOSTS) for number in numbers):
            return list(dict.fromkeys(HOSTS[int(number) - 1] for number in numbers))
        print('Choose the displayed host numbers. A generic browser or operating system is not a Workspace host.')


def choose_model(hosts: list[str], current: str) -> str:
    """Reject Editor choices for hosts that require the Workspace model."""
    print('For a Docs writing tool with a custom sidebar, consider Editor add-ons.')
    print('For shared cards across hosts or Gmail, consider Workspace add-ons. Verify required document operations.')
    while True:
        model = ask_choice('workspace_model', current)
        error = model_error(model, hosts)
        if not error:
            return model
        print(error)


def model_error(model: str, hosts: list[str]) -> str:
    """Return the incompatible host explanation shared by the interview and JSON validator."""
    if model == 'editor' and not set(hosts) <= EDITOR_HOSTS:
        return 'Editor add-ons support Docs, Sheets, Slides, and Forms. Choose Workspace for the selected hosts.'
    if model == 'workspace' and 'Google Forms' in hosts:
        return 'Google Forms uses the Editor model. Separate Forms from Workspace hosts in another component.'
    return ''


def choose_distribution(account: str, current: str) -> str:
    """Keep private organization distribution distinct from personal testing."""
    while True:
        mode = ask_choice('workspace_distribution', current)
        if mode != 'private' or account == 'organization':
            return mode
        print('Private Marketplace distribution requires a Workspace organization account.')
        print('For a personal account, choose test installation or public Marketplace distribution.')


def ask_script_languages(current: str, label: str, html_ui: bool) -> list[str]:
    """Explain runtime choices and require selected script, markup, and stylesheet languages."""
    print('\n' + label + ' source choices:')
    print('JavaScript: runs in the extension or Apps Script runtime without a TypeScript compilation step.')
    print('TypeScript: compiles to JavaScript. Its type checks run during the build.')
    if html_ui:
        print('HTML defines custom UI. CSS supplies styles. SCSS is optional and compiles to CSS.')
        print('Choose script-only source when no custom HTML UI is used. Add markup or styles only when used.')
    role = 'browser-extensions' if label == 'Browser' else ('workspace-html' if html_ui else 'workspace-cards')
    return select_languages(role, [], current)


def ask_languages(values: dict) -> list[str]:
    """Select Apps Script source choices or the supported HTTPS service languages."""
    if values['workspace_runtime'] == 'apps-script':
        print('\nApps Script runs JavaScript. TypeScript is compiled before upload.')
        return ask_script_languages(values.get('languages', ''), 'Workspace', values['workspace_model'] == 'editor')
    print('\nChoose the HTTPS service source languages. Google renders the Workspace card UI.')
    return select_languages('backend', ['server'], values.get('languages', ''))


def has_script_language(languages: list[str]) -> bool:
    """Recognize languages that produce executable Apps Script code."""
    return bool({name.lower() for name in languages} &
                {'javascript', 'typescript', 'apps script', 'google apps script'})


def show_apps_script_build(values: dict) -> None:
    """Explain the artifact steps for the selected source languages and host UI."""
    languages = {name.lower() for name in language_values(values['languages'])}
    print('- Keep appsscript.json and source under version control. Pin clasp and the build tool versions.')
    if 'typescript' in languages:
        print('- Compile TypeScript to Apps Script-compatible JavaScript. Retain callable function names.')
    else:
        print('- Prepare Apps Script-compatible JavaScript and retain callable function names.')
    print('- Bundle supported dependencies and inspect the generated upload directory.')
    if values['workspace_model'] == 'editor':
        print('- Package HTML-service sidebars/dialogs and their scripts and styles as HTML files when used.')
        if 'scss' in languages:
            print('- SCSS compilation produces CSS embedded in the HTML-service files.')
        elif 'css' in languages:
            print('- Package CSS in HTML-service style elements.')
    else:
        print('- Build host-rendered cards. Cards do not require HTML sidebars, SCSS, or browser bundles.')
    print('- Upload only prepared output with clasp. Verify the destination script project first.')
    print('- Separate local build, clasp upload, test installation, version creation, and Marketplace publication.')


def show_build_guidance(values: dict) -> None:
    """Show the required artifact boundary without inventing repository commands."""
    print('\nBuild and packaging for these choices:')
    if values['workspace_runtime'] == 'apps-script':
        show_apps_script_build(values)
    else:
        print('- Build and host an authenticated HTTPS service. Return the Workspace card JSON contract.')
        print('- Keep HTTP deployment configuration and service artifacts separate from Marketplace assets.')
        print('- Configure the deployment endpoints and verify Google request authentication before host testing.')
    print('- Review OAuth scopes and test consent, denied access, host callbacks, and document changes in the host.')
    print('Required release guidance: instructions/google-workspace/GOOGLE_WORKSPACE.md#build-and-package')


def show_distribution_guidance(mode: str) -> None:
    """Explain assets and release work only for the selected audience."""
    if mode == 'test':
        print('Test installation: use the selected model\'s developer test flow and synthetic documents.')
        print('A Marketplace listing is not needed yet. This is not general distribution to external users.')
    else:
        print(f'{mode.capitalize()} Marketplace: prepare icons, a listing banner, and actual integration screenshots.')
        print('Prepare descriptions, support, privacy-policy, and terms-of-service URLs for the listing.')
        print('Configure a standard Cloud project, OAuth consent, scopes, and the Marketplace SDK.')
        print('Record an Editor version number or Workspace deployment ID, as appropriate.')
        if mode == 'public':
            print('Public distribution requires Marketplace review and applicable OAuth verification.')
        print('Confirm audience before saving Marketplace visibility. Google does not permit later visibility changes.')
    print('Keep runtime logo/image URLs separate from listing artwork. Check current Google asset requirements.')
    print('Full checklist: instructions/google-workspace/GOOGLE_WORKSPACE.md#distribution-and-release-assets')
    print('These choices select instructions. This setup does not build, upload, install, or publish an add-on.')


def interview_workspace(values: dict) -> dict:
    """Return structured component choices compatible with the existing profile editor."""
    result = dict(values)
    hosts = ask_hosts(values.get('platforms', ''))
    result['workspace_model'] = choose_model(hosts, values.get('workspace_model', ''))
    runtime = 'apps-script'
    if result['workspace_model'] == 'workspace':
        runtime = ask_choice('workspace_runtime', values.get('workspace_runtime', ''))
    else:
        print('Editor runtime: Apps Script. Each Editor host needs its own add-on project and test configuration.')
    result['workspace_runtime'] = runtime
    account = ask_choice('workspace_account', values.get('workspace_account', ''))
    result['workspace_account'] = account
    mode = choose_distribution(account, values.get('workspace_distribution', ''))
    result['workspace_distribution'] = mode
    languages = ask_languages(result)
    result['languages'] = ', '.join(languages)
    show_build_guidance(result)
    show_distribution_guidance(mode)
    return {**{key: result[key] for key in WORKSPACE_FIELDS}, 'platforms': hosts, 'languages': languages,
            'deployment': f'{runtime}; {mode} installation/distribution'}


def validate_workspace(values: dict) -> list[str]:
    """Validate structured choices while preserving legacy profiles with a visible setup gap."""
    present = [values.get(key, '').strip('`') for key in WORKSPACE_FIELDS]
    if not any(present):
        return ['Workspace setup is legacy: rerun the interview to select model, runtime, account, and distribution.']
    for key in WORKSPACE_FIELDS:
        if values.get(key, '').strip('`') not in {value for value, _ in CHOICES[key]}:
            raise ValueError(f'Choose a valid {WORKSPACE_FIELDS[key]} before enabling this component.')
    model, runtime, account, mode = present
    hosts = {part.strip().strip('`') for part in values['platforms'].split(',')}
    if not hosts <= set(HOSTS):
        raise ValueError('Workspace platforms must name supported Google hosts. Rerun the Workspace interview.')
    error = model_error(model, list(hosts))
    if error:
        raise ValueError(error)
    if model == 'editor' and runtime != 'apps-script':
        raise ValueError('Editor add-ons require Apps Script and Docs, Sheets, Slides, or Forms hosts.')
    if runtime == 'apps-script' and not has_script_language(language_values(values['languages'])):
        raise ValueError('Apps Script needs JavaScript, TypeScript, or Apps Script source.')
    if mode == 'private' and account != 'organization':
        raise ValueError('Private Marketplace distribution requires a Workspace organization account.')
    return []
