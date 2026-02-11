"""Tests for eSTAR XML parser (estar_xml.py).

Validates import parsing: section detection, product code extraction, predicate finding.
"""

import os
import sys
import pytest

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from estar_xml import (
    _xml_escape,
    _route_field,
    parse_xml_data,
    FIELD_MAP,
    KNUMBER_PATTERN,
    SECTION_PATTERNS,
)

# Check if XML parsing deps are available (parse_xml_data calls check_dependencies at runtime)
try:
    import pikepdf  # noqa: F401
    from bs4 import BeautifulSoup  # noqa: F401
    from lxml import etree  # noqa: F401
    HAS_XML_DEPS = True
except ImportError:
    HAS_XML_DEPS = False


class TestXMLEscape:
    """Test XML special character escaping."""

    def test_ampersand(self):
        assert _xml_escape("A & B") == "A &amp; B"

    def test_less_than(self):
        assert _xml_escape("A < B") == "A &lt; B"

    def test_greater_than(self):
        assert _xml_escape("A > B") == "A &gt; B"

    def test_double_quote(self):
        assert _xml_escape('A "B"') == "A &quot;B&quot;"

    def test_single_quote(self):
        assert _xml_escape("A 'B'") == "A &apos;B&apos;"

    def test_empty_string(self):
        assert _xml_escape("") == ""

    def test_none(self):
        assert _xml_escape(None) == ""

    def test_multiple_specials(self):
        assert _xml_escape("<a & b>") == "&lt;a &amp; b&gt;"


class TestFieldMapping:
    """Test XFA field name to structured key mapping."""

    def test_all_mapped_fields_have_targets(self):
        for field, target in FIELD_MAP.items():
            assert target, f"Field {field} maps to empty target"

    def test_route_applicant_fields(self):
        result = {
            "applicant": {},
            "classification": {},
            "indications_for_use": {},
            "sections": {},
        }
        _route_field(result, "applicant_name", "ACME Corp")
        assert result["applicant"]["applicant_name"] == "ACME Corp"

    def test_route_classification_fields(self):
        result = {
            "applicant": {},
            "classification": {},
            "indications_for_use": {},
            "sections": {},
        }
        _route_field(result, "product_code", "OVE")
        assert result["classification"]["product_code"] == "OVE"

    def test_route_ifu_fields(self):
        result = {
            "applicant": {},
            "classification": {},
            "indications_for_use": {},
            "sections": {},
        }
        _route_field(result, "indications_for_use", "For spinal fusion")
        assert result["indications_for_use"]["indications_for_use"] == "For spinal fusion"

    def test_route_section_fields(self):
        result = {
            "applicant": {},
            "classification": {},
            "indications_for_use": {},
            "sections": {},
        }
        _route_field(result, "device_description_text", "A fusion device...")
        assert result["sections"]["device_description_text"] == "A fusion device..."


class TestKNumberPatternInParser:
    """Test the K-number pattern used by the parser."""

    def test_finds_knumber(self):
        assert KNUMBER_PATTERN.findall("K192345") == ["K192345"]

    def test_finds_supplement(self):
        assert KNUMBER_PATTERN.findall("K192345/S001") == ["K192345/S001"]

    def test_finds_pnumber(self):
        assert KNUMBER_PATTERN.findall("P190001") == ["P190001"]

    def test_finds_den(self):
        assert KNUMBER_PATTERN.findall("DEN200045") == ["DEN200045"]

    def test_finds_nnumber(self):
        assert KNUMBER_PATTERN.findall("N0012") == ["N0012"]

    def test_multiple_in_text(self):
        text = "Predicates: K192345, K181234, and P190001"
        matches = KNUMBER_PATTERN.findall(text)
        assert len(matches) == 3


class TestSectionDetection:
    """Test section detection patterns used during import."""

    def test_device_description_detected(self):
        assert SECTION_PATTERNS["device_description"].search("Device Description")

    def test_se_discussion_detected(self):
        assert SECTION_PATTERNS["se_discussion"].search("Substantial Equivalence Comparison")

    def test_performance_detected(self):
        assert SECTION_PATTERNS["performance"].search("Performance Testing Summary")

    def test_indications_detected(self):
        assert SECTION_PATTERNS["indications"].search("Indications for Use")

    def test_biocompatibility_detected(self):
        assert SECTION_PATTERNS["biocompatibility"].search("Biocompatibility Testing")


@pytest.mark.skipif(not HAS_XML_DEPS, reason="pikepdf/lxml/bs4 not installed")
class TestParseXMLData:
    """Test parsing of XFA XML data."""

    def _make_xml(self, **fields):
        """Build a minimal XFA XML string with given fields."""
        parts = ['<?xml version="1.0"?>', '<xfa:datasets xmlns:xfa="http://www.xfa.org/schema/xfa-data/1.0/">', '<xfa:data>', '<form1>']

        if "product_code" in fields:
            parts.append(f'<FDA3514><ProductCode>{fields["product_code"]}</ProductCode></FDA3514>')

        if "applicant_name" in fields:
            parts.append(f'<CoverLetter><ApplicantName>{fields["applicant_name"]}</ApplicantName></CoverLetter>')

        if "ifu" in fields:
            parts.append(f'<FDA3881><IndicationsText>{fields["ifu"]}</IndicationsText></FDA3881>')

        if "predicate_knumber" in fields:
            parts.append(f'<SE><PredicateDevice0><KNumber>{fields["predicate_knumber"]}</KNumber></PredicateDevice0></SE>')

        if "description" in fields:
            parts.append(f'<DeviceDescription><DescriptionText>{fields["description"]}</DescriptionText></DeviceDescription>')

        parts.extend(['</form1>', '</xfa:data>', '</xfa:datasets>'])
        return '\n'.join(parts)

    def test_extracts_product_code(self):
        xml = self._make_xml(product_code="OVE")
        result = parse_xml_data(xml)
        assert result["classification"].get("product_code") == "OVE"

    def test_extracts_applicant(self):
        xml = self._make_xml(applicant_name="ACME Medical")
        result = parse_xml_data(xml)
        assert result["applicant"].get("applicant_name") == "ACME Medical"

    def test_extracts_ifu(self):
        xml = self._make_xml(ifu="For intervertebral body fusion")
        result = parse_xml_data(xml)
        assert "intervertebral" in result["indications_for_use"].get("indications_for_use", "")

    def test_extracts_predicate_knumber(self):
        xml = self._make_xml(predicate_knumber="K192345")
        result = parse_xml_data(xml)
        knumbers = [p["k_number"] for p in result["predicates"]]
        assert "K192345" in knumbers

    def test_extracts_device_description(self):
        xml = self._make_xml(description="A PEEK interbody fusion device with titanium endplates for lumbar spine fusion.")
        result = parse_xml_data(xml)
        assert "PEEK" in result["sections"].get("device_description_text", "") or \
               "PEEK" in result.get("raw_fields", {}).get("form1.DeviceDescription.DescriptionText", "")

    def test_metadata_present(self):
        xml = self._make_xml(product_code="OVE")
        result = parse_xml_data(xml)
        assert "metadata" in result
        assert "extracted_at" in result["metadata"]
        assert result["metadata"]["source_format"] == "xfa_xml"

    def test_empty_xml(self):
        xml = '<?xml version="1.0"?><root></root>'
        result = parse_xml_data(xml)
        assert result["predicates"] == []
        assert result["classification"] == {}

    def test_raw_fields_populated(self):
        xml = self._make_xml(product_code="OVE", applicant_name="Test Corp")
        result = parse_xml_data(xml)
        assert len(result["raw_fields"]) > 0
