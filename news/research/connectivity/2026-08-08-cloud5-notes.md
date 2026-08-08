# Final full connectivity validation — 2026-08-08 (cloud5)

## test_sources.py (`--label cloud5`, full run, no `--only`)

45/55 OK. Full report: `2026-08-08-cloud5.md` / `2026-08-08-cloud5.json`.

10 failures, unchanged in kind from prior cloud runs:

- `lmsys-sglang`, `semianalysis` — Tunnel connection failed: 403 Forbidden (not on the
  domain allowlist)
- `karpathy-blog`, `karpathy-blog-jina` — Cloudflare "Just a moment..." challenge (direct
  fetch and anonymous `r.jina.ai` both blocked; matches CLAUDE.md note that Jina needs
  `JINA_API_KEY`)
- `github-search`, `github-releases-vllm`, `github-releases-vllm-api`,
  `mistral-gh-org`, `mistral-releases`, `mistral-releases-api` — all 403 via
  `api.github.com` / `github.com/.../releases.atom`. The GitHub MCP/API path in this
  session is repository-scoped to `kovalevgr/news_digest` only; `vllm-project/vllm` and
  `mistralai/mistral-inference` are not in scope for the REST API, and `add_repo`'s
  `read_available` status (established in cloud4) doesn't open the REST API either.

## Mechanism test A — git-proxy tags (release detection without the REST API)

Both succeeded — the git proxy serves anonymous `git ls-remote --tags` for these public
repos even though `api.github.com` 403s them for this session.

- **vllm-project/vllm**: success. Last 3 tags:
  - `v0.9.2`
  - `v0.9.2rc1`
  - `v0.9.2rc2`
- **mistralai/mistral-inference**: success. Last 3 tags:
  - `v1.5.0`
  - `v1.5.0^{}`
  - `v1.6.0`

**Conclusion:** `git ls-remote --tags <repo-url>` is a viable release-detection fallback
for GitHub-hosted sources blocked at the REST-API layer — it doesn't need `add_repo`,
a token, or repo-scope, just the plain git-proxy read path already open for public repos.

## Mechanism test B — WebFetch fallback

`https://karpathy.bearblog.dev/feed/` via WebFetch: **no**, real feed content did not
come back. WebFetch returned `HTTP 403 Forbidden` with no body — the same Cloudflare
block `test_sources.py` hits directly and via anonymous Jina. No newest-entry title to
report.

**Conclusion:** WebFetch is not a working fallback for `karpathy-blog` under the current
Cloudflare challenge; the source stays blocked pending `JINA_API_KEY` (authenticated
Jina), as already noted in CLAUDE.md and prior cloud-run notes.
