# Section Detection Patterns

Regex patterns for detecting and extracting sections from 510(k) PDF documents.

## K-Number Patterns

```regex
# Standard K-number (6 digits after K)
K\d{6}

# K-number with supplement suffix
K\d{6}/S\d{3}

# K-number with OCR errors (O→0, I→1, S→5)
[Kkℜ][O0I1]\d{5}
```

## P-Number Patterns

```regex
# Standard PMA number
P\d{6}

# PMA supplement
P\d{6}/S\d{3}
```

## DEN Number Patterns

```regex
# De Novo number
DEN\d{6,7}
```

## N-Number Patterns

```regex
# Pre-amendments device
N\d{4,5}
```

## Combined Device Number Pattern

```regex
(?:K\d{6}(?:/S\d{3})?|P\d{6}(?:/S\d{3})?|DEN\d{6,7}|N\d{4,5})
```

## Section Heading Patterns

These patterns detect 510(k) document sections for text extraction:

### Predicate/SE Sections (high value — weight 3x)

```regex
(?i)(?:substantial\s+equivalen|predicate\s+device|comparison\s+(?:of|to|with)\s+predicate|SE\s+(?:comparison|discussion|summary))
```

### Indications for Use

```regex
(?i)(?:indications?\s+for\s+use|intended\s+use|IFU\b)
```

### Device Description

```regex
(?i)(?:device\s+description|description\s+of\s+(?:the\s+)?device|principle\s+of\s+operation)
```

### Performance Testing

```regex
(?i)(?:performance\s+(?:testing|data|characteristics)|test(?:ing)?\s+(?:summary|results|data))
```

### Biocompatibility

```regex
(?i)(?:biocompatib|biological?\s+(?:evaluation|testing|safety))
```

### Sterilization

```regex
(?i)(?:sterilizat|sterility\s+(?:assurance|testing|validation))
```

### Software/Cybersecurity

```regex
(?i)(?:software\s+(?:description|documentation|level|validation)|cybersecurity|SBOM|threat\s+model)
```

### Labeling

```regex
(?i)(?:label(?:ing)?\s+(?:requirements?|review)|instructions?\s+for\s+use|package\s+(?:insert|label))
```

### Clinical

```regex
(?i)(?:clinical\s+(?:data|evidence|stud(?:y|ies)|information)|literature\s+review)
```

### Shelf Life

```regex
(?i)(?:shelf\s+life|accelerated\s+aging|real[\-\s]time\s+aging|package\s+(?:integrity|validation))
```

### EMC/Electrical Safety

```regex
(?i)(?:electromagnetic\s+compatib|EMC\b|electrical\s+safety|IEC\s+60601)
```

## eSTAR Section Number to XML Element Mapping

Used for routing imported eSTAR XML data to the correct parser:

| Section Regex | eSTAR Section | XML Root |
|---------------|---------------|----------|
| `section\s*0?1\b\|cover\s*letter` | 01 Cover Letter | `form1.CoverLetter` |
| `section\s*0?2\b\|cover\s*sheet\|3514` | 02 Cover Sheet | `form1.FDA3514` |
| `section\s*0?3\b\|510.*summary` | 03 510(k) Summary | `form1.Summary` |
| `section\s*0?4\b\|truthful` | 04 Truthful & Accuracy | `form1.TruthfulAccuracy` |
| `section\s*0?6\b\|device\s*desc` | 06 Device Description | `form1.DeviceDescription` |
| `section\s*0?7\b\|substantial\|SE\s` | 07 SE Comparison | `form1.SE` |
| `section\s*0?8\b\|standard` | 08 Standards | `form1.Standards` |
| `section\s*0?9\b\|label` | 09 Labeling | `form1.Labeling` |
| `section\s*10\b\|steriliz` | 10 Sterilization | `form1.Sterilization` |
| `section\s*11\b\|shelf` | 11 Shelf Life | `form1.ShelfLife` |
| `section\s*12\b\|biocompat` | 12 Biocompatibility | `form1.Biocompat` |
| `section\s*13\b\|software\|cyber` | 13 Software | `form1.Software` |
| `section\s*14\b\|EMC\|electric` | 14 EMC/Electrical | `form1.EMC` |
| `section\s*15\b\|performance` | 15 Performance Testing | `form1.Performance` |
| `section\s*16\b\|clinical` | 16 Clinical | `form1.Clinical` |

## Product Code Device Type Patterns

Product codes grouped by device category for test plan generation:

### Continuous Glucose Monitors
`MDS`, `QKQ`

### Wound Dressings
`FRO`, `KGN`, `KGO`, `MGP`, `NAO`

### Orthopedic Implants
`OVE`, `MAX`, `NKB`, `MQP`, `MQV`

### Cardiovascular
`DQY`, `DTB`, `DXY`, `MGB`, `NIQ`

### Software / SaMD
`QAS`, `QMT`, `QDQ`, `QPG`

### IVD / Diagnostics
`JJX`, `QKQ`, `MQB`, `OEW`

### Dental
`HQF`, `EHJ`, `EIG`

### Ophthalmic
`HQF`, `MRC`, `NQB`

### Respiratory
`BTK`, `BYF`, `CAK`

### General Surgery
`GEI`, `LYA`, `GAX`
