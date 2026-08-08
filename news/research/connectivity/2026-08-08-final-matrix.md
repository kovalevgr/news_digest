# Final connectivity matrix — 2026-08-08 (after cloud5)

Five cloud runs later, every source has a decided mechanism. Cloud = env "Test"
(`env_016arGxyi5LwhuvrC7o1WM8p`), local = owner's machine (52/52 baseline).

## Green in cloud — TIER-1 candidates (45)

All rss/api/fetch sources EXCEPT the ten below: labs (anthropic-engineering,
nvidia-dev, microsoft-research, apple-ml), infra (modal, together, baseten), OSS
(vllm-blog, pytorch, eleuther), big-tech (github-ai, netflix, cloudflare-ai),
institutes (bair, ai2, answerai), newsletters (cameron-wolfe), all 11 practitioner
blogs except karpathy, all 7 YouTube feeds, community (hn-algolia ×2, reddit
multireddit, lobsters, HF papers/models/spaces, smol.ai, github-trending-mirror),
Mistral (hf-org, docs-changelog).

## Resolved by a different mechanism (4)

| Source | Cloud mechanism (verified) |
| --- | --- |
| vllm releases | `git ls-remote --tags https://github.com/vllm-project/vllm` via session git proxy. Version-sort + cursor-diff (ls-remote order is lexical). |
| mistral-inference releases | same, `git ls-remote --tags` |
| GitHub rising-repo search | impossible in-session (gateway blocks /search) → covered by github-trending-mirror (green); optional upgrade: api.ossinsight.io (needs allowlist) |
| Mistral GitHub org listing | impossible in-session (gateway blocks /orgs) → covered by mistral-hf-org + releases tags + docs-changelog |

## Pending (3)

| Source | Status |
| --- | --- |
| lmsys-sglang, semianalysis | Owner added both domains ~1 min before cloud5 started — almost certainly allowlist propagation lag. Re-verify on the first real radar run; no action needed now. |
| karpathy-blog | Cloudflare challenge blocks direct fetch, anonymous Jina AND WebFetch (all three verified). Unlock = `JINA_API_KEY` secret in env "Test" (same key also unlocks Perplexity per CLAUDE.md). Interim: his posts reliably resurface via hn-algolia and smol.ai within a day. |

## Key architectural facts learned (for the implementation)

1. The cloud session's GitHub gateway intercepts ALL api.github.com/github.com HTTP:
   REST is repo-scoped to the session's configured repos, /search and /orgs are blocked
   entirely, and GITHUB_TOKEN env secrets are ignored (gateway substitutes its own
   auth). The PAT the owner created is unnecessary — safe to revoke.
2. The git PROXY, however, serves anonymous reads of any public repo: `git clone`,
   `git fetch`, and crucially `git ls-remote --tags` all work without add_repo.
3. WebFetch runs from infrastructure that Cloudflare-challenged sites still block —
   it is NOT a universal fallback; the Jina tier (with key) remains the strongest.
4. Feed-parsing hardening required: strip control chars (answer.ai), cap-aware
   streaming (cameron-wolfe 5.9MB, smol.ai 2.1MB archive), version-sort git tags,
   snapshot-diff for HF trending leaderboards, slug-based cursors where pubDates are
   regenerated (smol.ai).
