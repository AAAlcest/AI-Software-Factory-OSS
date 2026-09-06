# Security and disclosure boundaries

The helpers are offline declaration/fixture tools, not authorization services,
transport security or sandboxes against concurrent filesystem mutation. Never
run an unknown repository script against production or confidential material
merely because it is named a validator. Use disposable synthetic inputs first.

## Report a vulnerability privately

The Human-approved reporting channel is **GitHub Private Vulnerability Reporting**.
No private or personal email address is published as a reporting contact.

After the owner-authorized Public rollout and channel enablement, open this
repository's **Security -> Advisories -> Report a vulnerability** and use the
[private report form](https://github.com/AAAlcest/AI-Software-Factory-OSS/security/advisories/new).
The form requires GitHub sign-in. A link in this file is not proof the feature
has been enabled or that a report has been received.

**Preparation checkpoint:** enablement and entry-point verification are deferred
to the explicitly authorized Public rollout. Their actual results must be
recorded in Issue #1 before publishing the Release. No live reporting-channel
test or test advisory is claimed by this document.

Do not put vulnerability details, credentials, private hostnames, customer facts
or sensitive exploit evidence in public Issues, PRs or Discussions. Provide a
minimal synthetic reproduction, affected version/commit and observed impact in
the private report; omit secrets and unrelated personal or operational data.
If the private form is unavailable, retain the sensitive details. A public issue
may report only that the reporting channel is unavailable, without the
vulnerability or exploit details. Do not substitute a private email address.

## Maintainer activation and verification

Only after explicit Human authorization to make this repository Public, enable
Private vulnerability reporting in **Settings -> Advanced Security**. Verify the
setting is enabled and that **Report a vulnerability** leads to the private form
for this exact repository using an authorized signed-in reporter view where
available. Do not submit a fake vulnerability to test it. Record what was actually
verified; an unavailable reporter view remains a limitation, not a successful test.
An owner/administrator should ensure GitHub security-report notifications are
received; this does not require publishing their account email.

Follow the [publication checklist](docs/PUBLICATION_CHECKLIST.md). Failure to enable
or verify the reporting entry blocks Release publication; report the exception
rather than changing permissions or using public disclosure as a workaround.

Reference: [GitHub's private-reporting configuration guide](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository).

A clean keyword scan is not semantic privacy clearance. Final independent
privacy/public-safety review and explicit Human publication approval remain
required; this document grants neither. No response-time or bounty commitment
is made by this policy.
