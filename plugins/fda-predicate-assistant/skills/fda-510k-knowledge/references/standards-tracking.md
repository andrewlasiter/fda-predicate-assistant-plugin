# Standards Tracking Reference

## FDA Recognized Consensus Standards

FDA maintains a database of recognized consensus standards at:
https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/search.cfm

Changes to recognized standards can affect:
- Testing requirements for your submission
- Predicate comparison validity (if predicate tested to older version)
- Guidance document applicability

## Key Standard Families for Medical Devices

### Biocompatibility (ISO 10993 series)
| Standard | Title | Key for |
|----------|-------|---------|
| ISO 10993-1 | Biological evaluation framework | All devices |
| ISO 10993-5 | Cytotoxicity | All patient-contact |
| ISO 10993-10 | Sensitization and irritation | All patient-contact |
| ISO 10993-11 | Systemic toxicity | Implants, prolonged contact |
| ISO 10993-12 | Sample preparation | Test methodology |

### Sterilization
| Standard | Title | Key for |
|----------|-------|---------|
| ISO 11135 | EO sterilization | Most sterile devices |
| ISO 11137 | Radiation sterilization | Alternative method |
| ISO 17665 | Moist heat sterilization | Reusable devices |

### Electrical Safety
| Standard | Title | Key for |
|----------|-------|---------|
| IEC 60601-1 | General safety | All powered devices |
| IEC 60601-1-2 | EMC | All powered devices |
| IEC 62304 | Software lifecycle | Software devices |
| IEC 62366 | Usability engineering | All devices |

### Risk Management
| Standard | Title | Key for |
|----------|-------|---------|
| ISO 14971 | Risk management | All devices |

### Packaging & Aging
| Standard | Title | Key for |
|----------|-------|---------|
| ASTM F1980 | Accelerated aging | Devices with shelf life |
| ISO 11607 | Packaging for sterile devices | Sterile devices |

### Cybersecurity
| Standard | Title | Key for |
|----------|-------|---------|
| AAMI TIR57 | Cybersecurity risk management | Connected devices |
| IEC 81001-5-1 | Health software security | Software devices |

## Monitor --watch-standards Usage

The `/fda:monitor --watch-standards` flag enables tracking of:

1. **FDA standard recognition updates**: New versions of recognized standards
2. **Standard withdrawals**: Standards no longer recognized by FDA
3. **Transition periods**: Time allowed to transition from old to new standard version
4. **Impact assessment**: Which project requirements are affected by standard changes

### Check Method

```
WebSearch: site:fda.gov "recognized consensus standards" update {YYYY}
```

Cross-reference found standards against project's guidance_cache/standards_list.json to identify impacts.

### Alert Format

```json
{
  "type": "standard_update",
  "standard": "ISO 10993-1",
  "old_version": "2018",
  "new_version": "2024",
  "recognition_date": "2025-06-15",
  "transition_deadline": "2026-06-15",
  "affected_requirements": ["REQ-BIOCOMPAT-001"],
  "severity": "warning",
  "action_required": "Update biocompatibility testing plan to reference ISO 10993-1:2024"
}
```
