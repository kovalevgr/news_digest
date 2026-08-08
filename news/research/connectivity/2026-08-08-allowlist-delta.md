# Cloud connectivity: findings + allowlist delta — 2026-08-08

Cloud run (env "Test"): **5/52 OK** vs local 52/52. Failure taxonomy:

1. **`Tunnel connection failed: 403`** = the env's egress proxy refused CONNECT →
   **domain missing from the "Test" environment allowlist**. Not a site-side block.
2. **`HTTP 403 Forbidden`** (github.com + api.github.com only) = tunnel OK
   (domains already allowlisted for git ops), but **GitHub blocks anonymous
   requests from datacenter IPs**. Fix: a `GITHUB_TOKEN` env secret
   (fine-grained PAT, public-repo read-only) + `Authorization: Bearer` header in
   the fetch scripts. With a token: api.github.com = 5,000 req/hr, and releases
   can go through `/repos/<o>/<r>/releases` instead of the atom feed.
3. **Already working** (domains pre-allowlisted): anthropic.com (engineering page),
   huggingface.co (daily papers, trending models/spaces, mistral org API).

## Domains to add to the "Test" environment allowlist

Copy-paste list (36):

```
developer.nvidia.com
www.microsoft.com
machinelearning.apple.com
modal.com
www.together.ai
www.baseten.co
vllm.ai
lmsys.org
pytorch.org
blog.eleuther.ai
github.blog
netflixtechblog.com
blog.cloudflare.com
bair.berkeley.edu
allenai.org
www.answer.ai
cameronrwolfe.substack.com
semianalysis.substack.com
simonwillison.net
www.latent.space
www.interconnects.ai
magazine.sebastianraschka.com
eugeneyan.com
huyenchip.com
lilianweng.github.io
hamel.dev
karpathy.bearblog.dev
jxnl.co
vickiboykis.com
www.youtube.com
hn.algolia.com
www.reddit.com
lobste.rs
news.smol.ai
mshibanami.github.io
docs.mistral.ai
```

Notes:
- If the allowlist supports wildcards, `*.substack.com` covers cameronrwolfe +
  semianalysis (latent.space / interconnects.ai / magazine.sebastianraschka.com are
  Substack on custom domains — still individual entries).
- YouTube: only `www.youtube.com` is needed — the `/feeds/videos.xml` endpoint is
  not behind the consent wall (verified earlier); do NOT rely on channel `@handle`
  pages at runtime.
- After GITHUB_TOKEN is added, no new domains are needed for GitHub sources.

## Re-test procedure

1. Owner adds the domains above to env "Test" (claude.ai → Code → environments)
   and (optionally, for GitHub sources) a `GITHUB_TOKEN` secret.
2. Re-arm the one-time routine `test-radar-sources-cloud`
   (`trig_01UiZN4XVFPRGmDaiQZtcz7r`) with a fresh `run_once_at`, or just run it.
3. Expect: everything green except possibly Reddit / Medium (netflixtechblog) /
   Substack datacenter-IP blocks — those are the genuine site-side risks this
   test exists to separate from allowlist noise. Sources that still fail with the
   domain allowlisted get a fallback ladder (Jina / WebSearch) or are dropped.
