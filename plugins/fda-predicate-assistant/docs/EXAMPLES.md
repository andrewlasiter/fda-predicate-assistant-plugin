# Device-Type Command Examples

Per-device-type examples showing common command usage patterns.

## Continuous Glucose Monitor (CGM) — Product Code MDS

```bash
# Research the landscape
/fda:research MDS --competitor-deep

# Extract predicates from recent clearances
/fda:extract both --product-code MDS --years 2022-2025 --project cgm-device

# Review predicates
/fda:review --project cgm-device

# Guidance analysis (expect software + biocompatibility + clinical)
/fda:guidance MDS --save --project cgm-device

# Safety analysis (CGMs have significant MAUDE data)
/fda:safety --product-code MDS

# Generate testing plan (expect: sensor accuracy, biocompatibility, software, cybersecurity)
/fda:test-plan MDS --project cgm-device

# Draft software section (CGM is SaMD — cybersecurity required)
/fda:draft software --project cgm-device --device-description "Continuous glucose monitoring sensor with wireless Bluetooth connectivity and mobile app"

# Draft clinical section (CGMs typically need clinical data)
/fda:draft clinical --project cgm-device
```

**Key considerations for CGMs:**
- Software Level of Documentation likely Class C (IEC 62304)
- Cybersecurity required (Section 524B — wireless connectivity)
- Clinical data almost always required
- Special controls per 21 CFR 862.1355

---

## Wound Dressing — Product Code KGN

```bash
# Research (lower complexity device)
/fda:research KGN

# Extract predicates
/fda:extract both --product-code KGN --years 2020-2025 --project wound-dressing

# Review
/fda:review --project wound-dressing

# Guidance
/fda:guidance KGN --save --project wound-dressing

# SE comparison
/fda:compare-se --predicates K221234,K201567 --project wound-dressing --device-description "Antimicrobial wound dressing with silver ions" --intended-use "Management of partial and full thickness wounds"

# Draft sections (wound dressing typically needs: biocompatibility, sterilization, shelf life)
/fda:draft biocompatibility --project wound-dressing
/fda:draft sterilization --project wound-dressing
/fda:draft shelf-life --project wound-dressing
```

**Key considerations for wound dressings:**
- Biocompatibility per ISO 10993-1 (surface device, prolonged contact)
- Sterilization validation required (typically gamma or EO)
- Shelf life testing (accelerated + real-time aging)
- Usually no software or cybersecurity section needed

---

## Orthopedic Implant — Product Code OVE

```bash
# Full pipeline (spinal fusion devices are well-documented)
/fda:pipeline OVE --project spine-fusion --device-description "PEEK interbody fusion device with titanium endplates" --intended-use "Intervertebral body fusion of the lumbar spine L2-S1"

# Or step by step:
/fda:research OVE --competitor-deep
/fda:extract both --product-code OVE --years 2020-2025 --project spine-fusion
/fda:review --project spine-fusion
/fda:guidance OVE --save --project spine-fusion

# Traceability matrix (orthopedic devices have many requirements)
/fda:traceability --project spine-fusion

# Test plan (expect: mechanical testing, biocompat, sterilization, fatigue)
/fda:test-plan OVE --project spine-fusion
```

**Key considerations for orthopedic implants:**
- Extensive mechanical testing (ASTM F2077, F2267, etc.)
- Biocompatibility for implant (permanent contact, Class C)
- Fatigue testing critical
- Usually no software section

---

## Cardiovascular Device — Product Code DQY

```bash
# Research (complex regulatory landscape)
/fda:research DQY --competitor-deep

# Predicate lineage (important for cardiovascular — check for recalls)
/fda:lineage K201234 --depth 5

# Safety analysis (cardiovascular devices have high MAUDE event rates)
/fda:safety --product-code DQY

# PCCP if AI/ML involved
/fda:pccp --project cardio-device --device-description "AI-enhanced coronary catheter with real-time imaging"

# Pre-Sub recommended for cardiovascular
/fda:presub DQY --project cardio-device --device-description "Percutaneous transluminal coronary catheter" --intended-use "Dilation of coronary arteries"
```

**Key considerations for cardiovascular:**
- Pre-Sub meeting strongly recommended
- Clinical data often required
- Biocompatibility for external communicating (blood contact)
- Sterilization + pyrogen testing
- EMC/electrical safety if powered

---

## Software as Medical Device (SaMD) — Product Code QAS

```bash
# Research (rapidly evolving space)
/fda:research QAS --competitor-deep

# Pathway determination (De Novo may apply for novel SaMD)
/fda:pathway QAS --device-description "AI-powered medical image analysis software for detecting lung nodules" --intended-use "Computer-aided detection of pulmonary nodules on CT scans"

# Guidance (expect: software guidance, cybersecurity, clinical)
/fda:guidance QAS --save --project samd-device

# Software-specific draft
/fda:draft software --project samd-device --device-description "Cloud-hosted AI/ML algorithm for radiological image analysis"

# PCCP (if algorithm will be updated post-clearance)
/fda:pccp --project samd-device --device-description "AI/ML algorithm with planned iterative improvements"

# Literature review (clinical evidence for AI/ML claims)
/fda:literature QAS --project samd-device
```

**Key considerations for SaMD:**
- IEC 62304 software lifecycle
- Cybersecurity mandatory (Section 524B — cloud, network)
- PCCP for AI/ML with predetermined change plan
- Clinical data typically required for diagnostic claims
- De Novo may apply if no predicate exists
- Predetermined Change Control Plan for AI/ML

---

## Tips by Device Complexity

### Simple devices (wound dressings, bandages, tongue depressors)
- `/fda:research` → `/fda:extract` → `/fda:review` → `/fda:compare-se` → `/fda:draft` → `/fda:assemble`
- Pre-Sub usually not needed
- Focus on biocompatibility, sterilization, shelf life

### Moderate complexity (orthopedic, dental, ophthalmic)
- Add `/fda:guidance` and `/fda:test-plan` to the pipeline
- Pre-Sub recommended if novel technology
- Full mechanical/performance testing section

### High complexity (cardiovascular, neurological, AI/ML)
- Start with `/fda:presub` to get FDA feedback first
- Add `/fda:safety`, `/fda:literature`, `/fda:lineage`
- Clinical data section critical
- PCCP if AI/ML components
- Consider using autonomous agents for comprehensive preparation
