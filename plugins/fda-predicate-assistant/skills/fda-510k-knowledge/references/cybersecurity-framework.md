# Cybersecurity Documentation Framework

## When Cybersecurity Documentation is Required

Per FDA guidance "Cybersecurity in Medical Devices" (2023, updated for eSTAR 5.6+):

### Trigger Conditions
A cybersecurity section is required if the device:
- Contains software or firmware
- Has wireless connectivity (Bluetooth, WiFi, cellular, RF)
- Connects to a network (hospital, cloud, internet)
- Exchanges data with other devices or systems
- Has USB or other data ports
- Is a Software as a Medical Device (SaMD)

### Auto-Detection from Product Code
Product code families likely requiring cybersecurity:
- Software/SaMD codes: QAS, QBJ, QDK, QEH, QFP, QMT, QPC, QPZ
- Connected/wireless device codes: Any with "wireless", "connected", "software" in classification
- Implantable with telemetry: Pacemakers, neurostimulators, pumps

## eSTAR Cybersecurity Section Content

### Required Elements

1. **Threat Model**
   - System architecture diagram
   - Data flow diagram (DFD)
   - Attack surface analysis
   - Threat identification (STRIDE or equivalent)
   - Risk scoring (CVSS or equivalent)

2. **Software Bill of Materials (SBOM)**
   - Format: SPDX or CycloneDX
   - All third-party components listed
   - Version numbers for each component
   - Known vulnerability status (CVE check)

3. **Security Controls**
   - Authentication and authorization
   - Encryption (data at rest and in transit)
   - Software integrity verification
   - Audit logging
   - Secure update mechanism

4. **Vulnerability Management**
   - Coordinated vulnerability disclosure policy
   - Patch/update plan and timeline
   - End-of-support / end-of-life plan
   - Customer notification procedures

5. **Security Testing**
   - Penetration testing scope and results
   - Fuzz testing results
   - Static and dynamic code analysis
   - Third-party component vulnerability scan

## Template Structure

### Threat Model Template
```markdown
## Threat Model

### System Architecture
[TODO: Company-specific — insert system architecture diagram]

### Data Flow
| Data | Source | Destination | Transport | Encryption | Sensitivity |
|------|--------|------------|-----------|-----------|-------------|
| Patient data | Sensor | Mobile app | BLE | AES-128 | PHI |
| Device config | Cloud | Device | HTTPS/TLS 1.3 | Yes | Moderate |

### Attack Surfaces
| Surface | Description | Mitigations |
|---------|-----------|-------------|
| Wireless (BLE) | Bluetooth Low Energy data channel | Pairing, encryption |
| Cloud API | REST API for data sync | OAuth 2.0, TLS, rate limiting |
| USB | Configuration port | Physical access control |

### Threats (STRIDE Analysis)
| Threat | Category | Risk | Mitigation | Residual Risk |
|--------|----------|------|-----------|---------------|
| Data interception | Information Disclosure | High | BLE encryption | Low |
| Firmware tampering | Tampering | High | Code signing | Low |
| DoS via BLE | Denial of Service | Medium | Connection throttling | Low |
```

### SBOM Template
```markdown
## Software Bill of Materials

**Format:** CycloneDX 1.5
**Generated:** {date}
**Tool:** [TODO: Company-specific — SBOM generation tool]

### Components
| Component | Version | License | Supplier | CVE Status |
|-----------|---------|---------|----------|-----------|
| [TODO: List all third-party components] | | | | |

### Known Vulnerabilities
| CVE | Component | Severity | Status | Mitigation |
|-----|-----------|---------|--------|-----------|
| [TODO: Run vulnerability scan] | | | | |
```

### Patch Plan Template
```markdown
## Vulnerability Management Plan

### Coordinated Disclosure
- Contact: [TODO: Company-specific — security contact email]
- Response timeline: Acknowledge within 48 hours
- Fix timeline: Critical within 30 days, High within 90 days

### Update Mechanism
- Method: [TODO: OTA / manual / service visit]
- Validation: [TODO: Code signing, integrity check]
- Rollback: [TODO: Ability to revert to previous version]

### End of Support
- Planned support duration: [TODO: years]
- End-of-life notification: [TODO: advance notice period]
- Post-EOL risk mitigation: [TODO: plan]
```

## Applicable Standards

| Standard | Title | When Required |
|----------|-------|--------------|
| AAMI TIR57 | Cybersecurity risk management | All software devices |
| IEC 81001-5-1 | Health software security | All health software |
| IEC 62443 | Industrial cybersecurity | Network-connected devices |
| NIST SP 800-171 | Protecting CUI | Government use devices |
| UL 2900 | Software cybersecurity | Voluntary, recognized by FDA |
