"""Tests for openFDA API field names and response shapes.

Verifies that the API endpoints we depend on still return expected field structures.
These tests make real API calls — skip with `pytest -m "not api"` for offline testing.

NOTE: Tests use real openFDA API endpoints without an API key (1K/day limit).
Rate limit: 5 calls/minute without key. Tests include delays.
"""

import json
import time
import urllib.request
import urllib.parse
import pytest


# Mark all tests in this module as requiring API access
pytestmark = pytest.mark.api

BASE_URL = "https://api.fda.gov/device"
HEADERS = {"User-Agent": "Mozilla/5.0 (FDA-Plugin-Test/1.0)"}
TIMEOUT = 15


def _api_get(endpoint, search, limit=1):
    """Make an openFDA API request and return parsed JSON."""
    params = {"search": search, "limit": str(limit)}
    url = f"{BASE_URL}/{endpoint}.json?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read())


class Test510kEndpoint:
    """Verify /device/510k response shape."""

    @pytest.fixture(autouse=True)
    def _rate_limit(self):
        yield
        time.sleep(1)

    def test_510k_has_k_number(self):
        data = _api_get("510k", 'product_code:"OVE"')
        result = data["results"][0]
        assert "k_number" in result

    def test_510k_has_device_name(self):
        data = _api_get("510k", 'product_code:"OVE"')
        result = data["results"][0]
        assert "device_name" in result

    def test_510k_has_applicant(self):
        data = _api_get("510k", 'product_code:"OVE"')
        result = data["results"][0]
        assert "applicant" in result

    def test_510k_has_decision_date(self):
        data = _api_get("510k", 'product_code:"OVE"')
        result = data["results"][0]
        assert "decision_date" in result

    def test_510k_has_product_code(self):
        data = _api_get("510k", 'product_code:"OVE"')
        result = data["results"][0]
        assert "product_code" in result

    def test_510k_meta_has_total(self):
        data = _api_get("510k", 'product_code:"OVE"')
        assert "meta" in data
        assert "results" in data["meta"]
        assert "total" in data["meta"]["results"]


class TestClassificationEndpoint:
    """Verify /device/classification response shape."""

    @pytest.fixture(autouse=True)
    def _rate_limit(self):
        yield
        time.sleep(1)

    def test_classification_has_device_name(self):
        data = _api_get("classification", 'product_code:"OVE"')
        result = data["results"][0]
        assert "device_name" in result

    def test_classification_has_device_class(self):
        data = _api_get("classification", 'product_code:"OVE"')
        result = data["results"][0]
        assert "device_class" in result

    def test_classification_has_regulation_number(self):
        data = _api_get("classification", 'product_code:"OVE"')
        result = data["results"][0]
        assert "regulation_number" in result

    def test_classification_has_product_code(self):
        data = _api_get("classification", 'product_code:"OVE"')
        result = data["results"][0]
        assert "product_code" in result


class TestEventEndpoint:
    """Verify /device/event (MAUDE) response shape."""

    @pytest.fixture(autouse=True)
    def _rate_limit(self):
        yield
        time.sleep(1)

    def test_event_has_event_type(self):
        data = _api_get("event", 'device.device_report_product_code:"KGN"')
        result = data["results"][0]
        assert "event_type" in result

    def test_event_has_device_array(self):
        data = _api_get("event", 'device.device_report_product_code:"KGN"')
        result = data["results"][0]
        assert "device" in result
        assert isinstance(result["device"], list)


class TestRecallEndpoint:
    """Verify /device/recall response shape."""

    @pytest.fixture(autouse=True)
    def _rate_limit(self):
        yield
        time.sleep(1)

    def test_recall_has_product_code(self):
        data = _api_get("recall", 'product_code:"KGN"')
        result = data["results"][0]
        assert "product_code" in result

    def test_recall_has_event_type(self):
        data = _api_get("recall", 'product_code:"KGN"')
        result = data["results"][0]
        assert "event_type" in result or "res_event_number" in result


class TestGoldenFileReviewJSON:
    """Test that review.json fixture matches expected structure."""

    @pytest.fixture
    def review_data(self):
        fixture_path = os.path.join(
            os.path.dirname(__file__), "fixtures", "sample_review.json"
        )
        with open(fixture_path) as f:
            return json.load(f)

    def test_has_project(self, review_data):
        assert "project" in review_data

    def test_has_product_code(self, review_data):
        assert "product_code" in review_data
        assert review_data["product_code"] == "OVE"

    def test_has_predicates(self, review_data):
        assert "predicates" in review_data
        assert len(review_data["predicates"]) == 3

    def test_predicate_has_required_fields(self, review_data):
        for kn, pred in review_data["predicates"].items():
            assert "device_name" in pred
            assert "decision" in pred
            assert "confidence_score" in pred
            assert pred["decision"] in ("accepted", "rejected")

    def test_accepted_predicates_have_scores(self, review_data):
        for kn, pred in review_data["predicates"].items():
            if pred["decision"] == "accepted":
                assert pred["confidence_score"] >= 50

    def test_summary_counts_match(self, review_data):
        summary = review_data["summary"]
        preds = review_data["predicates"]
        accepted = sum(1 for p in preds.values() if p["decision"] == "accepted")
        rejected = sum(1 for p in preds.values() if p["decision"] == "rejected")
        assert summary["accepted"] == accepted
        assert summary["rejected"] == rejected
        assert summary["total_evaluated"] == len(preds)


# Need os import for fixture path
import os
