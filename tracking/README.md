# Tracking & CRM

## Launch Tracking (`launches/`)

One JSON file per project. Each file has a list of **launch events** (a campaign/announcement moment).
Each launch event can have multiple **posts** across channels.

**Schema:**
```json
{
  "project": "string",
  "events": [
    {
      "id": "slug",
      "date": "YYYY-MM-DD",
      "title": "what you launched / announced",
      "posts": [
        {
          "channel": "twitter | linkedin | hn | reddit | email | ...",
          "url": "link to post",
          "content_summary": "one-liner",
          "metrics_1d": { ... channel-specific ... },
          "metrics_1w": { ... channel-specific ... }
        }
      ],
      "notes": "free-form learnings"
    }
  ]
}
```

**Add metrics when you have them** — paste 1d snapshot ~24h after posting, 1w snapshot ~7d after.

---

## CRM (`contacts/`)

### `known.json` — people you already know in the space

```json
[
  {
    "name": "...",
    "handle": "@twitter or linkedin url",
    "context": "how you know them",
    "what_they_do": "...",
    "notes": "last talked about X, connected via Y",
    "public_info": { ... anything worth noting from their public profile ... }
  }
]
```

### `prospects.json` — people in the space, not yet contacted

```json
[
  {
    "name": "...",
    "handle": "...",
    "why_relevant": "...",
    "public_info": { "role": "...", "org": "...", "notable": "..." },
    "status": "not_contacted | in_progress | done"
  }
]
```
