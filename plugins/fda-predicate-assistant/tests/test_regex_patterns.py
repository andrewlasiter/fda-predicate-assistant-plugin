"""Tests for section detection regex patterns from section-patterns.md.

Validates all section heading patterns against known 510(k) text samples.
"""

import re
import pytest


# Section heading patterns from section-patterns.md
SECTION_PATTERNS = {
    "predicate_se": re.compile(
        r"(?i)(?:substantial\s+equivalen|predicate\s+device|comparison\s+(?:of|to|with)\s+predicate|SE\s+(?:comparison|discussion|summary))"
    ),
    "indications": re.compile(
        r"(?i)(?:indications?\s+for\s+use|intended\s+use|IFU\b)"
    ),
    "device_description": re.compile(
        r"(?i)(?:device\s+description|description\s+of\s+(?:the\s+)?device|principle\s+of\s+operation)"
    ),
    "performance": re.compile(
        r"(?i)(?:performance\s+(?:testing|data|characteristics)|test(?:ing)?\s+(?:summary|results|data))"
    ),
    "biocompatibility": re.compile(
        r"(?i)(?:biocompatib|biological?\s+(?:evaluation|testing|safety))"
    ),
    "sterilization": re.compile(
        r"(?i)(?:sterilizat|sterility\s+(?:assurance|testing|validation))"
    ),
    "software": re.compile(
        r"(?i)(?:software\s+(?:description|documentation|level|validation)|cybersecurity|SBOM|threat\s+model)"
    ),
    "labeling": re.compile(
        r"(?i)(?:label(?:ing)?\s+(?:requirements?|review)|instructions?\s+for\s+use|package\s+(?:insert|label))"
    ),
    "clinical": re.compile(
        r"(?i)(?:clinical\s+(?:data|evidence|stud(?:y|ies)|information)|literature\s+review)"
    ),
    "shelf_life": re.compile(
        r"(?i)(?:shelf\s+life|accelerated\s+aging|real[\-\s]time\s+aging|package\s+(?:integrity|validation))"
    ),
    "emc_electrical": re.compile(
        r"(?i)(?:electromagnetic\s+compatib|EMC\b|electrical\s+safety|IEC\s+60601)"
    ),
}


class TestPredicateSEPattern:
    """Test Substantial Equivalence section detection."""

    @pytest.mark.parametrize("text", [
        "SUBSTANTIAL EQUIVALENCE COMPARISON",
        "Substantial Equivalence Discussion",
        "substantial equivalence",
        "Predicate Device Selection",
        "Comparison of Predicate Devices",
        "Comparison to Predicate",
        "Comparison with Predicate Device",
        "SE Comparison Table",
        "SE Discussion",
        "SE Summary",
    ])
    def test_matches(self, text):
        assert SECTION_PATTERNS["predicate_se"].search(text)

    @pytest.mark.parametrize("text", [
        "Device Description",
        "Performance Testing",
        "The device is equivalent in size",
    ])
    def test_no_match(self, text):
        assert not SECTION_PATTERNS["predicate_se"].search(text)


class TestIndicationsPattern:
    """Test Indications for Use section detection."""

    @pytest.mark.parametrize("text", [
        "INDICATIONS FOR USE",
        "Indications for Use",
        "Indication for Use",
        "Intended Use",
        "intended use of the device",
        "IFU Statement",
    ])
    def test_matches(self, text):
        assert SECTION_PATTERNS["indications"].search(text)

    @pytest.mark.parametrize("text", [
        "Device Description",
        "For use with the applicator",
    ])
    def test_no_match(self, text):
        assert not SECTION_PATTERNS["indications"].search(text)


class TestDeviceDescriptionPattern:
    """Test Device Description section detection."""

    @pytest.mark.parametrize("text", [
        "DEVICE DESCRIPTION",
        "Device Description",
        "Description of the Device",
        "Description of Device",
        "Principle of Operation",
    ])
    def test_matches(self, text):
        assert SECTION_PATTERNS["device_description"].search(text)


class TestPerformancePattern:
    """Test Performance Testing section detection."""

    @pytest.mark.parametrize("text", [
        "PERFORMANCE TESTING",
        "Performance Data",
        "Performance Characteristics",
        "Testing Summary",
        "Testing Results",
        "Test Summary",
        "Test Data",
        "test results for the device",
    ])
    def test_matches(self, text):
        assert SECTION_PATTERNS["performance"].search(text)


class TestBiocompatibilityPattern:
    """Test Biocompatibility section detection."""

    @pytest.mark.parametrize("text", [
        "BIOCOMPATIBILITY",
        "Biocompatibility Testing",
        "Biological Evaluation",
        "Biological Testing",
        "Biological Safety",
        "biological evaluation of medical devices",
    ])
    def test_matches(self, text):
        assert SECTION_PATTERNS["biocompatibility"].search(text)


class TestSterilizationPattern:
    """Test Sterilization section detection."""

    @pytest.mark.parametrize("text", [
        "STERILIZATION",
        "Sterilization Validation",
        "Sterility Assurance Level",
        "Sterility Testing",
        "Sterility Validation",
    ])
    def test_matches(self, text):
        assert SECTION_PATTERNS["sterilization"].search(text)


class TestSoftwarePattern:
    """Test Software/Cybersecurity section detection."""

    @pytest.mark.parametrize("text", [
        "SOFTWARE DESCRIPTION",
        "Software Documentation",
        "Software Level of Concern",
        "Software Validation",
        "Cybersecurity Documentation",
        "SBOM",
        "Threat Model",
    ])
    def test_matches(self, text):
        assert SECTION_PATTERNS["software"].search(text)


class TestLabelingPattern:
    """Test Labeling section detection."""

    @pytest.mark.parametrize("text", [
        "Labeling Review",
        "Labeling Requirements",
        "Labeling Requirement",
        "Instructions for Use",
        "Instruction for Use",
        "Package Insert",
        "Package Label",
    ])
    def test_matches(self, text):
        assert SECTION_PATTERNS["labeling"].search(text)

    def test_standalone_labeling_no_match(self):
        """'LABELING' alone doesn't match — pattern requires labeling + qualifier."""
        assert not SECTION_PATTERNS["labeling"].search("LABELING")


class TestClinicalPattern:
    """Test Clinical section detection."""

    @pytest.mark.parametrize("text", [
        "CLINICAL DATA",
        "Clinical Evidence",
        "Clinical Studies",
        "Clinical Study",
        "Clinical Information",
        "Literature Review",
    ])
    def test_matches(self, text):
        assert SECTION_PATTERNS["clinical"].search(text)


class TestShelfLifePattern:
    """Test Shelf Life section detection."""

    @pytest.mark.parametrize("text", [
        "SHELF LIFE",
        "Shelf Life Testing",
        "Accelerated Aging",
        "Real-Time Aging",
        "Real Time Aging",
        "Package Integrity",
        "Package Validation",
    ])
    def test_matches(self, text):
        assert SECTION_PATTERNS["shelf_life"].search(text)


class TestEMCElectricalPattern:
    """Test EMC/Electrical Safety section detection."""

    @pytest.mark.parametrize("text", [
        "ELECTROMAGNETIC COMPATIBILITY",
        "Electromagnetic Compatibility Testing",
        "EMC Testing",
        "Electrical Safety Testing",
        "IEC 60601 Compliance",
    ])
    def test_matches(self, text):
        assert SECTION_PATTERNS["emc_electrical"].search(text)


class TestPatternIndependence:
    """Verify patterns don't cross-match inappropriately."""

    def test_device_description_not_performance(self):
        assert not SECTION_PATTERNS["performance"].search("Device Description")

    def test_se_not_clinical(self):
        assert not SECTION_PATTERNS["clinical"].search("Substantial Equivalence")

    def test_sterilization_not_shelf_life(self):
        assert not SECTION_PATTERNS["shelf_life"].search("Sterilization Validation")

    def test_labeling_not_software(self):
        assert not SECTION_PATTERNS["software"].search("Labeling Requirements")
