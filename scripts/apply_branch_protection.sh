#!/usr/bin/env bash
# Apply main-branch protection. Requires the repo to be public or on GitHub Pro/Team;
# on a private free-plan repo the API returns 403. Run once that condition is met.
set -euo pipefail

REPO="${1:-Moep90/agent-toolkit-for-kapitan}"

gh api -X PUT "repos/${REPO}/branches/main/protection" --input - <<'JSON'
{
  "required_status_checks": { "strict": true, "contexts": ["quality", "test", "integration"] },
  "enforce_admins": false,
  "required_pull_request_reviews": { "required_approving_review_count": 1, "dismiss_stale_reviews": true },
  "restrictions": null,
  "required_linear_history": true,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "required_conversation_resolution": true
}
JSON

echo "Branch protection applied to ${REPO}:main"
