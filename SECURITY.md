# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | Yes       |
| < 1.0   | No        |

## Reporting a Vulnerability

**Do NOT open a public GitHub issue for security vulnerabilities.**

Please report security concerns through [GitHub Security Advisories](../../security/advisories/new). This ensures the report remains private while we investigate and address the issue.

### What to Include

- **Description** — A clear, concise description of the vulnerability.
- **Steps to Reproduce** — Detailed steps to trigger the issue, including any sample HTML or JavaScript.
- **Impact Assessment** — What an attacker could achieve by exploiting this vulnerability.
- **Affected Component** — Which component(s) are affected (e.g., HelpDrawer, CommentOverlay).
- **Browser/Environment** — Browser name, version, and OS where the issue was observed.
- **Suggested Fix** — If you have one, a proposed remediation approach.

### Response Timeline

- **Acknowledgment** — We will acknowledge receipt of your report within 48-72 hours.
- **Initial Assessment** — We will provide an initial severity assessment within one week.
- **Resolution** — Critical vulnerabilities will be prioritized for the next patch release. We will coordinate with you on disclosure timing.

## Scope

This project is a **client-side UI theme and component library**. There is no server-side code, backend API, authentication system, or database. All components run entirely in the browser.

Because of this architecture, the typical web security attack surface is limited. The primary security concern is:

### Cross-Site Scripting (XSS)

The main attack vector is XSS through improper use of `innerHTML`. This project mitigates that risk by:

- Using `textContent` instead of `innerHTML` for all user-supplied content.
- Using `createElement` and `setAttr` DOM helpers for building component markup programmatically.
- Avoiding inline event handlers in generated HTML.

If you find a component that uses `innerHTML` with unsanitized user input, that is a valid security report.

### Out of Scope

The following are generally **not** security vulnerabilities in the context of this project:

- CSS-only styling issues (visual glitches, layout problems).
- Behavior that requires the consuming application to pass attacker-controlled HTML to a component's API, unless the component's documentation indicates that input will be sanitized.
- Vulnerabilities in third-party dependencies (report those to the upstream project directly, but do let us know so we can update).
- Issues that require physical access to the user's machine.

## Acknowledgments

We appreciate the security research community's efforts in responsibly disclosing vulnerabilities. Contributors who report valid security issues will be credited in the release notes (unless they prefer to remain anonymous).
