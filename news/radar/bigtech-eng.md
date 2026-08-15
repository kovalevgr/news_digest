---
category: bigtech-eng
updated: 2026-08-15
---

# Radar: bigtech-eng

Technical-radar items for this category (sources in [`config/radar.json`](../config/radar.json)).
Appended by the daily routine under weekly headings; format matches topics files.

## 2026-W33

- **2026-08-14** — [How Cloudflare detects MCP traffic and helps secure it](https://blog.cloudflare.com/mcp-security-updates) — Verified via WebFetch: Gateway classifies MCP traffic via protocol-level heuristics (`MCP-Protocol-Version`, `Mcp-Method`/`Mcp-Name` headers, no body parsing), ships a new `experimental.is_mcp` policy selector, an MCP detection dashboard (shadow-MCP visibility, Portal vs. direct split), and Agents SDK v0.20.0 for the MCP 2026-07-28 stateless protocol; explicitly can't see local `stdio` or off-network traffic.
