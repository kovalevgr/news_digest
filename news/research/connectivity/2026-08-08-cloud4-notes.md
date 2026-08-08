# add_repo + Jina fallback test — 2026-08-08 (cloud4)

## add_repo outcomes

Both calls returned `status: "read_available"` — neither a clean success (attached with
credentials) nor a hard failure. The tool's own message: the repo is public and this
session's git proxy already serves anonymous `git clone`/`fetch` reads of public GitHub
repos directly, so **nothing was attached to the session**. Attaching (which the
GitHub-API-backed source fetchers in `test_sources.py` need) requires `access: "push"`,
which runs the full repository-access authorization checks — not requested here since
the task only asked to request read access.

- **vllm-project/vllm** — `add_repo(owner="vllm-project", repo="vllm", access="read")`
  → `status: "read_available"`, `workspace: "/workspace/vllm-project/vllm"`. No
  credentials attached; anonymous git-proxy read only. GitHub API access (used by the
  `github-releases-vllm-api` source, which calls `api.github.com`) is **not** covered by
  this.
- **mistralai/mistral-inference** — `add_repo(owner="mistralai", repo="mistral-inference", access="read")`
  → `status: "read_available"`, `workspace: "/workspace/mistralai/mistral-inference"`.
  Same result: anonymous git-proxy read only, no GitHub API access.

## test_sources.py results (`--label cloud4`)

0/3 OK. Full report: `2026-08-08-cloud4.md` / `2026-08-08-cloud4.json`.

| id | ok | status | error |
| --- | --- | --- | --- |
| karpathy-blog-jina | ❌ | 403 | Cloudflare "Just a moment..." challenge page via `r.jina.ai` (anonymous Jina still blocked — matches CLAUDE.md note: needs `JINA_API_KEY`) |
| github-releases-vllm-api | ❌ | 403 | `api.github.com` — "GitHub access to this repository is not enabled for this session. Use add_repo to request access." |
| mistral-releases-api | ❌ | 403 | same as above, for mistralai/mistral-inference |

**Conclusion:** the `add_repo` read-access path does not unblock the GitHub-API-based
source fetchers — `github-releases-vllm-api` and `mistral-releases-api` still 403 through
`api.github.com` after both `add_repo` calls returned `read_available`, because that
status only opens anonymous `git` clone/fetch, not the GitHub REST API. The
`karpathy-blog-jina` source remains blocked by an unauthenticated Jina request hitting a
Cloudflare challenge, consistent with the outstanding `JINA_API_KEY` requirement noted in
CLAUDE.md.
