# Security and disclosure boundaries

The helpers are offline declaration/fixture tools, not authorization services,
transport security or sandboxes against concurrent filesystem mutation. Never
run an unknown repository script against production or confidential material
merely because it is named a validator. Use disposable synthetic inputs first.

## Report a vulnerability privately

This repository uses **GitHub Private Vulnerability Reporting**, which is enabled.
No private or personal email address is published as a reporting contact.

Open this repository's **Security -> Advisories -> Report a vulnerability** or use
the [private report form](https://github.com/AAAlcest/AI-Software-Factory-OSS/security/advisories/new).
The form requires GitHub sign-in.

Do not put vulnerability details, credentials, private hostnames, customer facts
or sensitive exploit evidence in public Issues, PRs or Discussions. Provide a
minimal synthetic reproduction, affected version/commit and observed impact in
the private report; omit secrets and unrelated personal or operational data.
If the private form is unavailable, retain the sensitive details. A public issue
may report only that the reporting channel is unavailable, without the
vulnerability or exploit details. Do not substitute a private email address.

## Maintainer verification

Keep Private Vulnerability Reporting enabled and periodically verify that
**Report a vulnerability** opens the private reporting flow for this repository.
Do not submit a fake vulnerability merely to test the route. If the entry point is
unavailable, treat that as a reporting-channel issue and fix or document it before
publishing a Release that claims the channel is available.

An owner/administrator should ensure GitHub security-report notifications are
received; this does not require publishing their account email.

Follow the [publication checklist](docs/PUBLICATION_CHECKLIST.md).

Reference: [GitHub's private-reporting configuration guide](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository).

A clean keyword scan is not semantic privacy clearance. Final independent
privacy/public-safety review and explicit Human publication approval remain
separate from this reporting mechanism. No response-time or bounty commitment
is made by this policy.
