# Allowlist probe: lmsys.org + semianalysis.substack.com (2026-08-09)

Targeted probe of two stubborn domains from `news/config/sources.json`, run from the current
Claude Code cloud session, plus a control probe against a sibling Substack domain known to work.

## Method

For each target domain, three commands:

1. `curl -sS -m 15 -A "Mozilla/5.0" -o /dev/null -w "%{http_code}" <url>` — basic reachability + HTTP status.
2. `curl -sSv -m 15 https://<domain>/ 2>&1 | grep -iE "connect|proxy|403|established" | head -5` — verbatim CONNECT tunnel negotiation lines, to distinguish a proxy-side refusal from an origin-side response.
3. Control: same basic probe against `https://cameronrwolfe.substack.com/feed` (known-working sibling).

## Results

### lmsys.org

- `GET https://lmsys.org/blog/` → **HTTP 307** (exit code 0 — no curl/proxy error)
- CONNECT negotiation (verbatim):
  ```
  * Uses proxy env variable no_proxy == 'localhost,127.0.0.1,::1,127.0.0.0/8,0.0.0.0/8,::,169.254.0.0/16,anthropic.com,.anthropic.com,*.anthropic.com,registry.npmjs.org,jsr.io,npm.jsr.io,pypi.org,files.pythonhosted.org,index.crates.io,proxy.golang.org,host.docker.internal,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,100.64.0.0/10,.svc.cluster.local,*.svc.cluster.local'
  * Uses proxy env variable https_proxy == 'http://127.0.0.1:40935'
  * Connected to 127.0.0.1 (127.0.0.1) port 40935
  * CONNECT tunnel: HTTP/1.1 negotiated
  * allocate connect buffer
  ```
- **Verdict: proxy CONNECT tunnel succeeded** (negotiated cleanly, no 403/refusal). The 307 is an
  origin-side redirect response, not a proxy block.

### semianalysis.substack.com

- `GET https://semianalysis.substack.com/feed` → **HTTP 301** (exit code 0 — no curl/proxy error)
- CONNECT negotiation (verbatim):
  ```
  * Uses proxy env variable no_proxy == 'localhost,127.0.0.1,::1,127.0.0.0/8,0.0.0.0/8,::,169.254.0.0/16,anthropic.com,.anthropic.com,*.anthropic.com,registry.npmjs.org,jsr.io,npm.jsr.io,pypi.org,files.pythonhosted.org,index.crates.io,proxy.golang.org,host.docker.internal,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,100.64.0.0/10,.svc.cluster.local,*.svc.cluster.local'
  * Uses proxy env variable https_proxy == 'http://127.0.0.1:40935'
  * Connected to 127.0.0.1 (127.0.0.1) port 40935
  * CONNECT tunnel: HTTP/1.1 negotiated
  * allocate connect buffer
  ```
- **Verdict: proxy CONNECT tunnel succeeded** (negotiated cleanly, no 403/refusal). The 301 is an
  origin-side redirect response, not a proxy block.

### Control: cameronrwolfe.substack.com (known-working)

- `GET https://cameronrwolfe.substack.com/feed` → **HTTP 200** (exit code 0)

## Summary

In this session's environment, neither `lmsys.org` nor `semianalysis.substack.com` was refused
by the proxy — both CONNECT tunnels negotiated successfully, and both origins responded with
redirect status codes (307, 301) rather than a proxy-level 403. This contrasts with the "CONNECT
refused" failure mode described for these domains elsewhere; here the proxy let the traffic
through and the origin server issued a redirect instead of the expected content.

Caveat: this probe ran in the current interactive/scheduled-routine session, not necessarily
inside the daily routine's dedicated "Test" custom-network environment referenced in
`news/workflow.md`. If the daily routine's failure is proxy-side allowlisting specific to that
environment, this result does not rule that out — it only shows these two domains are not
blocked from *this* session's egress path. The 307/301 redirects themselves may still need
`-L` (follow redirects) in the fetch script, or indicate the feed URLs have moved.

## 2026-08-09 second probe: new hostnames

Quick allowlist probe for two newly added hostnames:

- `curl -sS -m 15 -A "Mozilla/5.0" -o /dev/null -w "%{http_code}" https://www.lmsys.org/blog/` → **www.lmsys.org: 200**
- `curl -sS -m 15 -A "Mozilla/5.0" -o /dev/null -w "%{http_code}" https://newsletter.semianalysis.com/feed` → **newsletter.semianalysis.com: 200**

Both green — no curl/proxy errors, no "Tunnel connection failed: 403". The allowlist has propagated for both hostnames in this session's environment.
