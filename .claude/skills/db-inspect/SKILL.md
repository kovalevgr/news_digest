---
name: db-inspect
description: Inspect pipeline state in Postgres — items/sightings flow, cluster ranking, triage status, article lifecycle, cursors. Use when debugging the researcher, checking what landed, or verifying behavior via the DB.
---

# DB inspection

Interactive: `docker compose exec db psql -U app -d content`
One-shot: `docker compose exec db psql -U app -d content -c "<query>"`
(Postgres is internal-only — never exposed outside the compose network; this is the only way in.)

## Ingest flow

Recent items with sighting counts:
```sql
SELECT i.id, left(i.title, 60) AS title, count(s.*) AS sightings, i.fetched_at
FROM items i LEFT JOIN sightings s ON s.item_id = i.id
GROUP BY i.id ORDER BY i.fetched_at DESC LIMIT 20;
```

Cross-source stories (the strongest ranking signal — must be > 1 for echoed stories):
```sql
SELECT item_id, array_agg(source_key) AS sources, count(*)
FROM sightings GROUP BY item_id HAVING count(*) > 1 ORDER BY count(*) DESC LIMIT 15;
```

Per-source activity (is every configured source alive?):
```sql
SELECT source_key, count(*) AS sightings, max(seen_at) AS last_seen
FROM sightings GROUP BY source_key ORDER BY last_seen DESC;
```

Cursors (poll state):
```sql
SELECT source_key, cursor, updated_at FROM cursors ORDER BY updated_at DESC;
```

## Clusters & triage

Top clusters / triage queue:
```sql
SELECT id, topic, round(score::numeric, 3) AS score, status, left(coalesce(triage_title,'-'), 50) AS title
FROM clusters ORDER BY score DESC LIMIT 15;
```

Gate-1 funnel:
```sql
SELECT status, count(*) FROM clusters GROUP BY status;
```

## Articles & knowledge base

Lifecycle / KB membership:
```sql
SELECT id, piece_type, status, embedding IS NOT NULL AS in_kb, updated_at
FROM articles ORDER BY updated_at DESC LIMIT 10;
```

Voice signal:
```sql
SELECT article_id, left(instruction, 70) AS instruction, created_at
FROM edit_log ORDER BY created_at DESC LIMIT 10;
```

Variants produced:
```sql
SELECT article_id, platform, created_at FROM variants ORDER BY created_at DESC LIMIT 10;
```

Digest coverage (what's excluded from the next digest run):
```sql
SELECT ac.cluster_id, a.piece_type, a.status
FROM article_clusters ac JOIN articles a ON a.id = ac.article_id
ORDER BY a.updated_at DESC LIMIT 20;
```
