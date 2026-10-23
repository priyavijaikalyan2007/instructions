#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 8c7ff787-7793-4959-8d6e-e606e47bfa66
# Created: 2026

# COMPONENT: Browser extension profile choices
# PURPOSE: Collect supported browser/OS pairs, source languages, and installation channels.
# RELATES: profile_interview.py, configure_instructions.py, instructions/browser-extensions/BROWSER_EXTENSIONS.md
# FLOW: Browsers -> operating systems for each browser -> distribution -> source -> required artifact guidance.

from terminal_ui import print
from workspace_profile import ask_script_languages
from profile_choices import choose_many, language_values


BROWSER_FIELDS = {'browser_targets': 'Browser targets', 'browser_distribution': 'Browser distribution'}
BROWSERS = {
    'chrome': ('Chrome', ['Windows', 'macOS', 'Linux', 'ChromeOS']),
    'edge': ('Edge', ['Windows', 'macOS', 'Linux']),
    'firefox': ('Firefox', ['Windows', 'macOS', 'Linux', 'Android']),
    'safari': ('Safari', ['macOS', 'iOS', 'iPadOS']),
}
TARGETS = {f'{browser}-{system.lower()}': f'{label} on {system}'
           for browser, (label, systems) in BROWSERS.items() for system in systems}
DISTRIBUTIONS = {
    'test': 'Developer testing: unpacked/temporary installs. Safari device tests can require app packaging.',
    'store': 'Browser stores: prepare packages, listing assets, privacy disclosures, and store review.',
    'self-hosted': 'Firefox self-distribution: distribute a Mozilla-signed XPI outside the public listing.',
}
STORES = {'chrome': 'Chrome Web Store', 'edge': 'Microsoft Edge Add-ons',
          'firefox': 'Mozilla Add-ons', 'safari': 'Apple App Store'}


def choose_targets(values: dict) -> list[str]:
    """Collect browser-specific OS support without implying mobile Chrome extension support."""
    previous = [value.strip() for value in values.get('browser_targets', '').split(',')]
    labels = [label for label, _ in BROWSERS.values()]
    platforms = values.get('platforms', '')
    platforms = '' if '<' in platforms else platforms
    defaults = [label for browser, (label, _) in BROWSERS.items()
                if any(value.startswith(browser + '-') for value in previous)
                or label in platforms]
    print('\nChoose installed extension targets, not the browser used to view your website.')
    print('This preset covers Chrome/Edge desktop, Firefox desktop/Android, and Safari Apple platforms.')
    selected = choose_many('Browsers', labels, defaults)
    targets = []
    for browser, (label, systems) in BROWSERS.items():
        if label not in selected:
            continue
        current = [system for system in systems if f'{browser}-{system.lower()}' in previous]
        for system in choose_many(label + ' operating systems', systems, current):
            targets.append(f'{browser}-{system.lower()}')
    return targets


def choose_distribution(values: dict, targets: list[str]) -> str:
    """Explain installation channels and prevent Firefox-only signing choices for other browsers."""
    keys = list(DISTRIBUTIONS)
    current = values.get('browser_distribution', '')
    while True:
        selected = choose_many('Browser distribution', list(DISTRIBUTIONS.values()),
                               [DISTRIBUTIONS[current]] if current in DISTRIBUTIONS else [], False)
        if len(selected) != 1:
            print('Choose one distribution mode for this component. Use separate components for different modes.')
            continue
        mode = keys[list(DISTRIBUTIONS.values()).index(selected[0])]
        if mode != 'self-hosted' or all(target.startswith('firefox-') for target in targets):
            return mode
        print('Self-distributed signed XPI packages are a Firefox choice. Use stores for general Chrome/Safari users.')
        print('Managed enterprise delivery needs a separately recorded browser policy and release procedure.')


def deployment_summary(targets: list[str], mode: str) -> str:
    """Describe extension delivery separately from any API hosting arrangement."""
    if mode == 'test':
        return 'Local developer extension installation'
    if mode == 'self-hosted':
        return 'Mozilla-signed XPI self-distribution'
    return ', '.join(STORES[browser] for browser in BROWSERS
                     if any(target.startswith(browser + '-') for target in targets))


def show_browser_guidance(values: dict) -> None:
    """Show the selected build and publication boundaries without deploying anything."""
    targets = values['browser_targets']
    languages = {value.lower() for value in values['languages']}
    print('\nBrowser build, assets, testing, and distribution:')
    print('- Keep manifest.json inputs, icons, source, lockfiles, and build configuration under version control.')
    if 'typescript' in languages:
        print('- Compile TypeScript to JavaScript. Bundle executable code into the extension package.')
    if 'scss' in languages:
        print('- Compile SCSS to CSS and include the resulting styles in the package.')
    print('- Include referenced HTML, CSS, scripts, icons, and locale files. Inspect each browser-specific manifest.')
    print('- Test popup/content/background boundaries, permissions, worker restart, navigation, and upgrades.')
    if any(target.startswith(('chrome-', 'edge-')) for target in targets):
        print('- Test unpacked builds in each selected Chromium browser. Store uploads use a ZIP package.')
    if any(target.startswith('firefox-') for target in targets):
        print('- Use temporary Firefox installs and web-ext lint/run. Distribution uses a Mozilla-signed XPI.')
    if any(target.startswith('safari-') for target in targets):
        show_safari_guidance(targets, values['browser_distribution'])
    show_browser_release(values)
    print('A backend may serve an API. It does not replace the installed extension package.')
    print('Required guide: instructions/browser-extensions/BROWSER_EXTENSIONS.md#build-assets-and-distribution')
    print('These choices do not build, install, sign, upload, or publish an extension.')


def show_safari_guidance(targets: list[str], mode: str) -> None:
    """Distinguish current Safari folder tests from app-based device testing and distribution."""
    if mode == 'test' and 'safari-macos' in targets:
        print('- Current macOS Safari supports temporary extension-folder testing. Verify the target Safari version.')
    print('- For app packaging, use Xcode or the Safari Web Extension Packager in App Store Connect.')
    print('- Test selected macOS/iOS/iPadOS targets. App Store Connect packaging can feed TestFlight device tests.')
    print('- Apple distribution requires the relevant developer account, signing, app records, and App Store review.')
    print('- Select Swift or Objective-C only for native wrapper edits. Web source stays JavaScript/TypeScript.')


def show_browser_release(values: dict) -> None:
    """Separate local tests, signed self-distribution, and store assets."""
    mode = values['browser_distribution']
    if mode == 'test':
        print('- Developer testing does not require a public store listing. Test actual browser installation.')
        return
    if mode == 'self-hosted':
        print('- Obtain a signed XPI from Mozilla. Record installation and updates for desktop/Android targets.')
        return
    print('- Prepare store icons, actual screenshots, descriptions, support details, and a privacy-policy URL.')
    print('- Declare data use and permissions, prepare review access, and verify current store artwork requirements.')
    print('- Keep signing, store submission, review, publication, and rollout separate from the local build.')
    print('Selected destinations: ' + values['deployment'])


def interview_browser(values: dict) -> dict:
    """Return typed browser facts through the existing component-answer contract."""
    targets = choose_targets(values)
    mode = choose_distribution(values, targets)
    languages = ask_script_languages(values.get('languages', ''), 'Browser', True)
    result = dict(browser_targets=targets, browser_distribution=mode, languages=languages,
                  platforms=[TARGETS[target] for target in targets], deployment=deployment_summary(targets, mode))
    show_browser_guidance(result)
    return result


def validate_browser(values: dict) -> list[str]:
    """Validate new metadata while retaining older free-text profiles with an actionable warning."""
    raw_targets = values.get('browser_targets', '').strip('`')
    mode = values.get('browser_distribution', '').strip('`')
    if not raw_targets and not mode:
        return ['Browser profile lacks structured targets/distribution. Rerun the browser interview. '
                'a backend delivery description does not define extension installation.']
    targets = [value.strip().strip('`') for value in raw_targets.split(',') if value.strip()]
    if not targets or not set(targets) <= TARGETS.keys() or mode not in DISTRIBUTIONS:
        raise ValueError('Choose valid browser targets and distribution through the browser interview.')
    if mode == 'self-hosted' and any(not target.startswith('firefox-') for target in targets):
        raise ValueError('Self-distributed signed XPI packages require Firefox targets only.')
    platforms = {value.strip().strip('`') for value in values['platforms'].split(',')}
    if platforms != {TARGETS[target] for target in targets}:
        raise ValueError('Browser platforms must match the selected browser and operating-system pairs.')
    if not {'javascript', 'typescript'} & {name.lower() for name in language_values(values['languages'])}:
        raise ValueError('Browser extensions need JavaScript or TypeScript source for this preset.')
    return []
