---
description: Look up UDI/GUDID records from openFDA — search by device identifier, product code, company, or brand name
allowed-tools: Bash, Read, Glob, Grep, Write
argument-hint: "--product-code CODE | --di NUMBER | --company NAME | --brand NAME [--project NAME] [--save]"
---

# FDA UDI/GUDID Database Lookup

## Resolve Plugin Root

**Before running any bash commands that reference `$FDA_PLUGIN_ROOT`**, resolve the plugin install path:

```bash
FDA_PLUGIN_ROOT=$(python3 -c "
import json, os
f = os.path.expanduser('~/.claude/plugins/installed_plugins.json')
if os.path.exists(f):
    d = json.load(open(f))
    for k, v in d.get('plugins', {}).items():
        if k.startswith('fda-predicate-assistant@'):
            for e in v:
                p = e.get('installPath', '')
                if os.path.isdir(p):
                    print(p); exit()
print('')
")
echo "FDA_PLUGIN_ROOT=$FDA_PLUGIN_ROOT"
```

---

You are querying the openFDA UDI (Unique Device Identification) endpoint to look up GUDID (Global Unique Device Identification Database) records.

## Parse Arguments

From `$ARGUMENTS`, extract:

- `--product-code CODE` — Search by FDA product code
- `--di NUMBER` — Search by primary device identifier (DI)
- `--company NAME` — Search by company name
- `--brand NAME` — Search by brand name
- `--project NAME` — Associate results with a project
- `--save` — Save results to project folder
- `--limit N` — Max results (default 10)

At least one of `--product-code`, `--di`, `--company`, or `--brand` is required.

## Step 1: Query openFDA UDI Endpoint

```bash
python3 << 'PYEOF'
import urllib.request, urllib.parse, json, os, re, time

settings_path = os.path.expanduser('~/.claude/fda-predicate-assistant.local.md')
api_key = os.environ.get('OPENFDA_API_KEY')
api_enabled = True
if os.path.exists(settings_path):
    with open(settings_path) as f:
        content = f.read()
    if not api_key:
        m = re.search(r'openfda_api_key:\s*(\S+)', content)
        if m and m.group(1) != 'null':
            api_key = m.group(1)
    m = re.search(r'openfda_enabled:\s*(\S+)', content)
    if m and m.group(1).lower() == 'false':
        api_enabled = False

if not api_enabled:
    print("UDI_SKIP:api_disabled")
    exit(0)

# Build search query from arguments (replace placeholders)
search_parts = []
product_code = "PRODUCT_CODE"  # Replace or None
di = "DI_NUMBER"               # Replace or None
company = "COMPANY_NAME"       # Replace or None
brand = "BRAND_NAME"           # Replace or None
limit = 10                     # Replace with actual

if product_code and product_code != "None":
    search_parts.append(f'product_codes.code:"{product_code}"')
if di and di != "None":
    search_parts.append(f'identifiers.id:"{di}"')
if company and company != "None":
    search_parts.append(f'company_name:"{company}"')
if brand and brand != "None":
    search_parts.append(f'brand_name:"{brand}"')

if not search_parts:
    print("ERROR:No search criteria provided")
    exit(1)

search = "+AND+".join(search_parts)
params = {"search": search, "limit": str(limit)}
if api_key:
    params["api_key"] = api_key

url = f"https://api.fda.gov/device/udi.json?{urllib.parse.urlencode(params)}"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (FDA-Plugin/4.9.0)"})

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
        total = data.get("meta", {}).get("results", {}).get("total", 0)
        print(f"TOTAL:{total}")
        for r in data.get("results", []):
            print(f"=== UDI RECORD ===")
            print(f"COMPANY:{r.get('company_name', 'N/A')}")
            print(f"BRAND:{r.get('brand_name', 'N/A')}")
            print(f"VERSION:{r.get('version_or_model_number', 'N/A')}")
            print(f"CATALOG:{r.get('catalog_number', 'N/A')}")
            print(f"DESCRIPTION:{r.get('device_description', 'N/A')}")

            # Device identifiers
            for ident in r.get("identifiers", []):
                dtype = ident.get("type", "")
                did = ident.get("id", "")
                issuing = ident.get("issuing_agency", "")
                print(f"IDENTIFIER:{dtype}|{did}|{issuing}")

            # Product codes
            for pc in r.get("product_codes", []):
                print(f"PRODUCT_CODE:{pc.get('code', '')}|{pc.get('name', '')}")

            # GMDN terms
            for gmdn in r.get("gmdn_terms", []):
                print(f"GMDN:{gmdn.get('name', '')}|{gmdn.get('definition', '')[:100]}")

            # Safety/compatibility info
            print(f"MRI_SAFETY:{r.get('mri_safety', 'N/A')}")
            print(f"LATEX:{r.get('is_natural_rubber_latex', 'N/A')}")
            print(f"SINGLE_USE:{r.get('is_single_use', 'N/A')}")
            print(f"STERILE:{r.get('is_sterile', 'N/A')}")
            print(f"STERILIZATION_PRIOR:{r.get('sterilization_prior_to_use', 'N/A')}")
            print(f"IMPLANT:{r.get('is_kit', 'N/A')}")
            print(f"RX:{r.get('is_rx', 'N/A')}")
            print(f"OTC:{r.get('is_otc', 'N/A')}")

            # Device sizes
            for size in r.get("device_sizes", []):
                print(f"SIZE:{size.get('type', '')}|{size.get('value', '')}|{size.get('unit', '')}")

            print()
except urllib.error.HTTPError as e:
    if e.code == 404:
        print("TOTAL:0")
    else:
        print(f"ERROR:HTTP {e.code}: {e.reason}")
except Exception as e:
    print(f"ERROR:{e}")
PYEOF
```

## Step 2: Present Results

```
  FDA UDI/GUDID Database Lookup
  {search context}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Generated: {date} | Source: openFDA UDI | v4.9.0

SEARCH RESULTS ({total} records found)
────────────────────────────────────────

  Record 1:
  Company:     {company_name}
  Brand:       {brand_name}
  Model:       {version_or_model_number}
  Catalog:     {catalog_number}
  Description: {device_description}

  Identifiers:
    Primary DI: {identifier}  (Issuing Agency: {GS1/HIBCC/ICCBBA})

  Product Codes: {code} — {name}
  GMDN Terms:   {gmdn_name}

  Device Properties:
  | Property          | Value |
  |-------------------|-------|
  | MRI Safety        | {mri_safety} |
  | Latex             | {Y/N} |
  | Single Use        | {Y/N} |
  | Sterile           | {Y/N} |
  | Requires Sterilization | {Y/N} |
  | Rx/OTC            | {Rx/OTC} |

  Sizes:
    {type}: {value} {unit}

  ---

  Record 2: ...

RECOMMENDATIONS
────────────────────────────────────────

  1. UDI data helps populate eSTAR labeling section
  2. For labeling compliance: /fda:draft labeling --project NAME
  3. For full device profile: /fda:validate {K-number}

────────────────────────────────────────
  This report is AI-generated from public FDA data.
  Verify independently. Not regulatory advice.
────────────────────────────────────────
```

## Save Results (--save)

If `--save` is specified, write results to `$PROJECTS_DIR/$PROJECT_NAME/udi_lookup.json`:

```json
{
  "query": {"product_code": "OVE", "company": null, "di": null},
  "total_results": 25,
  "records": [
    {
      "company_name": "...",
      "brand_name": "...",
      "primary_di": "...",
      "product_codes": ["OVE"],
      "sterile": true,
      "mri_safety": "MR Conditional"
    }
  ],
  "queried_at": "2026-02-07T12:00:00Z"
}
```

## UDI System Reference

See `references/udi-requirements.md` for:
- UDI system overview (21 CFR 801.20)
- GUDID database structure
- DI vs PI (Device Identifier vs Production Identifier)
- Compliance dates by device class
- Issuing agencies (GS1, HIBCC, ICCBBA)

## Error Handling

- **No arguments**: Show usage with examples
- **API unavailable**: "UDI lookup requires openFDA API access. Enable with `/fda:configure --set openfda_enabled true`"
- **No results**: "No UDI records found. Try broadening your search or check that the device is registered in GUDID."
