---
name: skillsmp-api-client
description: "Use when: making HTTP requests to the SkillsMP API (skillsmp.com) to search for AI agent skills, query the skill marketplace, or retrieve skill metadata. Triggers: 'skillsmp', 'search skills', 'find skill', 'skill marketplace', 'AI skills', 'agent skills'. Requires API key from skillsmp.com. NOT for: skills that are already installed locally."
---

# SkillsMP API Client

Client library for the SkillsMP REST API (https://skillsmp.com/api/v1). Provides keyword and AI semantic search for AI skills built by the community.

## Base URL

```
https://skillsmp.com/api/v1
```

## Authentication

All requests require a Bearer token in the Authorization header:

```bash
-H "Authorization: Bearer sk_live_your_api_key"
```

Get your API key from https://skillsmp.com

## Rate Limits

- 500 requests per day per API key (resets at midnight UTC)
- Wildcard searches (`*`) are not supported

Check remaining quota via response headers:
- `X-RateLimit-Daily-Limit`: Daily request limit (500)
- `X-RateLimit-Daily-Remaining`: Remaining requests for today

## Endpoints

### GET /api/v1/skills/search

Keyword search for skills.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| q | string | Yes | Search query |
| page | number | No | Page number (default: 1) |
| limit | number | No | Items per page (default: 20, max: 100) |
| sortBy | string | No | Sort order: `stars` or `recent` (default: `recent`) |
| category | string | No | Filter by category slug (e.g. `data-ai`, `devops`) |
| occupation | string | No | Filter by SOC occupation slug (e.g. `software-developers-151252`) |

**Example:**

```bash
curl -X GET "https://skillsmp.com/api/v1/skills/search?q=SEO" \
  -H "Authorization: Bearer sk_live_your_api_key"
```

**Search with filters:**

```bash
curl -X GET "https://skillsmp.com/api/v1/skills/search?q=automation&occupation=software-developers-151252&sortBy=stars" \
  -H "Authorization: Bearer sk_live_your_api_key"
```

### GET /api/v1/skills/ai-search

AI semantic search powered by Cloudflare AI.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| q | string | Yes | AI search query (natural language) |

**Example:**

```bash
curl -X GET "https://skillsmp.com/api/v1/skills/ai-search?q=How+to+create+a+web+scraper" \
  -H "Authorization: Bearer sk_live_your_api_key"
```

## Response Format

Success response:

```json
{
  "success": true,
  "data": {
    "skills": [...],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100
    }
  }
}
```

Error response:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_API_KEY",
    "message": "The provided API key is invalid"
  }
}
```

## Error Codes

| Code | HTTP | Description |
|------|------|-------------|
| MISSING_API_KEY | 401 | API key not provided |
| INVALID_API_KEY | 401 | Invalid API key |
| MISSING_QUERY | 400 | Missing required query parameter |
| DAILY_QUOTA_EXCEEDED | 429 | Daily API quota exceeded |
| INTERNAL_ERROR | 500 | Internal server error |

## Python Client Example

```python
import requests
from typing import Optional, List, Dict, Any

class SkillsMPClient:
    BASE_URL = "https://skillsmp.com/api/v1"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})
    
    def search(
        self,
        q: str,
        page: int = 1,
        limit: int = 20,
        sortBy: str = "recent",
        category: Optional[str] = None,
        occupation: Optional[str] = None
    ) -> Dict[str, Any]:
        params = {
            "q": q,
            "page": page,
            "limit": min(limit, 100),
            "sortBy": sortBy
        }
        if category:
            params["category"] = category
        if occupation:
            params["occupation"] = occupation
        
        response = self.session.get(f"{self.BASE_URL}/skills/search", params=params)
        response.raise_for_status()
        return response.json()
    
    def ai_search(self, q: str) -> Dict[str, Any]:
        response = self.session.get(
            f"{self.BASE_URL}/skills/ai-search",
            params={"q": q}
        )
        response.raise_for_status()
        return response.json()
    
    def get_rate_limit_info(self, response: requests.Response) -> Dict[str, int]:
        return {
            "limit": int(response.headers.get("X-RateLimit-Daily-Limit", 500)),
            "remaining": int(response.headers.get("X-RateLimit-Daily-Remaining", 500))
        }

# Usage
client = SkillsMPClient("sk_live_your_api_key")

# Keyword search
results = client.search(q="SEO", sortBy="stars")
print(results)

# AI semantic search
ai_results = client.ai_search(q="How to create a web scraper")
print(ai_results)
```

## JavaScript/Node.js Example

```javascript
const axios = require('axios');

class SkillsMPClient {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.client = axios.create({
      baseURL: 'https://skillsmp.com/api/v1',
      headers: { Authorization: `Bearer ${apiKey}` }
    });
  }

  async search({ q, page = 1, limit = 20, sortBy = 'recent', category, occupation }) {
    const params = { q, page, limit: Math.min(limit, 100), sortBy };
    if (category) params.category = category;
    if (occupation) params.occupation = occupation;
    
    const response = await this.client.get('/skills/search', { params });
    return response.data;
  }

  async aiSearch(q) {
    const response = await this.client.get('/skills/ai-search', { params: { q } });
    return response.data;
  }
}
```

## Constraints

- MUST include `Authorization` header with Bearer token on all requests
- MUST URL-encode query parameters (spaces as `+` or `%20`)
- MUST handle 429 errors gracefully (quota exceeded)
- SHOULD check `X-RateLimit-Daily-Remaining` header to avoid hitting limits
- SHOULD limit `page` size to max 100
- SHOULD NOT use wildcard `*` in queries (not supported)
- SHOULD use keyword search for exact matches, AI search for semantic queries
- MAY combine `category` and `occupation` filters with `q` parameter
