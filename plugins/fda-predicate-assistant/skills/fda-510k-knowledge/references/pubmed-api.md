# PubMed E-utilities API Reference

## Overview

NCBI E-utilities provide programmatic access to PubMed for structured, reproducible literature searches. Unlike web search, E-utilities return structured data with PMIDs, MeSH terms, and citation counts.

**Base URL:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`

## Endpoints

| Endpoint | Purpose | Used By |
|----------|---------|---------|
| `esearch.fcgi` | Search PubMed, return PMIDs | `/fda:literature` — primary search |
| `efetch.fcgi` | Retrieve article details (title, abstract, authors) | `/fda:literature` — article details |
| `elink.fcgi` | Find related articles, citation counts | `/fda:literature --depth deep` |
| `einfo.fcgi` | Database metadata | Diagnostic only |

## Rate Limiting

| Condition | Rate Limit |
|-----------|-----------|
| Without API key | 3 requests/second |
| With API key | 10 requests/second |
| Tool/email identification | Required for all requests |

**API key configuration:**
- **Priority 1:** Environment variable `NCBI_API_KEY`
- **Priority 2:** Settings file `~/.claude/fda-predicate-assistant.local.md` field `ncbi_api_key`
- **Obtain key:** Register at [NCBI](https://www.ncbi.nlm.nih.gov/account/) — free

Configure via: `/fda:configure --set ncbi_api_key YOUR_KEY`

## esearch — PubMed Search

```
GET esearch.fcgi?db=pubmed&term={query}&retmax=20&retmode=json&sort=relevance&tool=fda-predicate-assistant&email=plugin@example.com
```

**Parameters:**
- `db=pubmed` — Database
- `term` — Search query (supports PubMed query syntax)
- `retmax` — Maximum results (default 20, max 10000)
- `retmode=json` — Return format
- `sort=relevance` — Sort order (relevance, pub_date)
- `api_key` — Optional NCBI API key

**Response:**
```json
{
  "esearchresult": {
    "count": "142",
    "retmax": "20",
    "idlist": ["38123456", "37654321", ...]
  }
}
```

## efetch — Retrieve Article Details

```
GET efetch.fcgi?db=pubmed&id={pmid1,pmid2,...}&rettype=abstract&retmode=xml
```

Returns XML with article title, authors, journal, year, abstract, publication type, and MeSH terms.

## MeSH Term Mapping for Medical Devices

Use MeSH terms to improve search precision. Common mappings for device categories:

| Device Category | MeSH Terms |
|----------------|------------|
| Orthopedic implants | "Bone Screws"[MeSH], "Spinal Fusion"[MeSH], "Internal Fixators"[MeSH] |
| Cardiovascular | "Stents"[MeSH], "Heart Valve Prosthesis"[MeSH], "Balloon Dilatation"[MeSH] |
| Software/SaMD | "Software"[MeSH], "Artificial Intelligence"[MeSH], "Image Processing, Computer-Assisted"[MeSH] |
| Wound care | "Bandages"[MeSH], "Wound Healing"[MeSH], "Occlusive Dressings"[MeSH] |
| Dental | "Dental Implants"[MeSH], "Orthodontic Brackets"[MeSH], "Dental Prosthesis"[MeSH] |
| IVD/diagnostics | "Clinical Laboratory Techniques"[MeSH], "Biosensing Techniques"[MeSH] |
| Ophthalmic | "Lenses, Intraocular"[MeSH], "Contact Lenses"[MeSH], "Ophthalmoscopes"[MeSH] |
| Respiratory | "Ventilators, Mechanical"[MeSH], "Respiratory Protective Devices"[MeSH] |
| Infusion | "Infusion Pumps"[MeSH], "Drug Delivery Systems"[MeSH] |

## PubMed Query Syntax

### Field Tags
- `[Title/Abstract]` — Search title and abstract
- `[MeSH Terms]` — Search MeSH index
- `[Publication Type]` — Filter by type (e.g., "Clinical Trial", "Review", "Meta-Analysis")
- `[Title]` — Title only

### Boolean Operators
- `AND`, `OR`, `NOT` — Standard boolean
- Parentheses for grouping

### Filters
- `"clinical trial"[Publication Type]` — Clinical trials only
- `"review"[Publication Type]` — Reviews only
- `"last 5 years"[PDat]` — Date filter

### Example Queries for FDA Literature Review

**Clinical evidence for a specific device:**
```
("{device_name}"[Title/Abstract]) AND (clinical trial[Publication Type] OR clinical study[Title/Abstract])
```

**Safety/adverse events:**
```
("{device_name}"[Title/Abstract]) AND (adverse event[Title/Abstract] OR complication[Title/Abstract] OR safety[Title/Abstract])
```

**Biocompatibility:**
```
("{device_name}"[Title/Abstract]) AND (biocompatibility[Title/Abstract] OR cytotoxicity[Title/Abstract] OR "ISO 10993"[Title/Abstract])
```

**Systematic reviews (highest evidence):**
```
("{device_name}"[Title/Abstract]) AND (systematic review[Publication Type] OR meta-analysis[Publication Type])
```

## Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| HTTP 429 | Rate limit exceeded | Wait 1 second, retry; add API key for higher limits |
| HTTP 502/503 | NCBI server issue | Retry after 5 seconds; fall back to WebSearch |
| Empty result | No matching articles | Broaden search terms; try MeSH terms; fall back to WebSearch |
| Timeout | Slow response | Retry with smaller retmax; check network |
