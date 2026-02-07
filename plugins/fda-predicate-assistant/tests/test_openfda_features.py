"""Tests for openFDA API features: wildcard, sort, skip, OR batch, _missing_/_exists_.

Validates that the API reference, commands, and FDAClient all leverage the full
set of openFDA query parameters (sort, skip, search_after, OR batching, wildcards).

These tests do NOT require API access unless marked @pytest.mark.api.
"""

import os
import sys
import pytest

# Add scripts directory to path for import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

# Paths to plugin files
PLUGIN_ROOT = os.path.join(os.path.dirname(__file__), "..")
REF_PATH = os.path.join(PLUGIN_ROOT, "skills", "fda-510k-knowledge", "references", "openfda-api.md")
EXTRACT_PATH = os.path.join(PLUGIN_ROOT, "commands", "extract.md")
SAFETY_PATH = os.path.join(PLUGIN_ROOT, "commands", "safety.md")
RESEARCH_PATH = os.path.join(PLUGIN_ROOT, "commands", "research.md")
VALIDATE_PATH = os.path.join(PLUGIN_ROOT, "commands", "validate.md")
MONITOR_PATH = os.path.join(PLUGIN_ROOT, "commands", "monitor.md")
CLIENT_PATH = os.path.join(PLUGIN_ROOT, "scripts", "fda_api_client.py")


def _read(path):
    with open(path) as f:
        return f.read()


# ──────────────────────────────────────────────
# Reference content tests
# ──────────────────────────────────────────────

class TestReferenceWildcard:
    """Wildcard should be documented as supported, not 'Not supported'."""

    def test_wildcard_documented_as_supported(self):
        content = _read(REF_PATH)
        assert "Not supported" not in content, "Wildcard should not say 'Not supported'"

    def test_wildcard_syntax_shown(self):
        content = _read(REF_PATH)
        assert "field:prefix*" in content or "prefix*" in content


class TestReferenceTemplate:
    """The fda_api() template function should include sort and skip params."""

    def test_template_has_sort_parameter(self):
        content = _read(REF_PATH)
        assert "sort=None" in content

    def test_template_has_skip_parameter(self):
        content = _read(REF_PATH)
        assert "skip=0" in content

    def test_template_passes_sort_to_params(self):
        content = _read(REF_PATH)
        assert 'params["sort"] = sort' in content

    def test_template_passes_skip_to_params(self):
        content = _read(REF_PATH)
        assert 'params["skip"]' in content


class TestReferenceSearchSyntax:
    """Search syntax section should document OR batch, _missing_/_exists_, grouping, sort."""

    def test_has_missing_exists(self):
        content = _read(REF_PATH)
        assert "_missing_" in content
        assert "_exists_" in content

    def test_has_parenthetical_grouping(self):
        content = _read(REF_PATH)
        assert "Parenthetical grouping" in content

    def test_has_or_batch_query(self):
        content = _read(REF_PATH)
        assert "OR batch query" in content

    def test_has_sort_entry(self):
        content = _read(REF_PATH)
        assert "sort=field:asc" in content or "sort=field:desc" in content


class TestReferencePagination:
    """Pagination section should mention search_after for deep paging."""

    def test_has_search_after(self):
        content = _read(REF_PATH)
        assert "search_after" in content

    def test_has_deep_paging_note(self):
        content = _read(REF_PATH)
        assert "Deep paging" in content or "26,000" in content


# ──────────────────────────────────────────────
# Command content tests
# ──────────────────────────────────────────────

class TestExtractBatching:
    """extract.md should use OR batch pattern for safety scan."""

    def test_extract_has_or_batch(self):
        content = _read(EXTRACT_PATH)
        assert "+OR+" in content, "extract.md should use OR batch queries"

    def test_extract_no_individual_loop(self):
        """Should not loop over top_5 with individual API calls."""
        content = _read(EXTRACT_PATH)
        # The old pattern was 'for knumber in top_5:' with individual URL per K
        # New pattern does batch lookup then iterates results
        assert "batch_search" in content or 'batch_search = "+OR+"' in content


class TestSafetyBatching:
    """safety.md should use OR batch for peer events and count_field for year trends."""

    def test_peer_benchmark_uses_or_or_count(self):
        content = _read(SAFETY_PATH)
        # Should use either OR query or count_field for peer benchmarking
        assert ("+OR+" in content or
                'count_field="device.device_report_product_code.exact"' in content)

    def test_events_by_year_uses_count_field(self):
        content = _read(SAFETY_PATH)
        assert 'count_field="date_received"' in content, \
            "safety.md should use count_field for year trend (not year-by-year loop)"

    def test_no_year_range_loop(self):
        """Year-by-year loop should be replaced with single count query."""
        content = _read(SAFETY_PATH)
        # Old pattern was 'for year in range(2020, 2027)' with individual calls
        assert "year_totals" in content, "Should aggregate daily buckets into year_totals"

    def test_narrative_fetch_has_sort(self):
        content = _read(SAFETY_PATH)
        assert "date_received:desc" in content, \
            "Narrative fetch should sort by date_received:desc"

    def test_recall_fetch_has_sort(self):
        content = _read(SAFETY_PATH)
        assert "event_date_terminated:desc" in content, \
            "Recent recalls should sort by event_date_terminated:desc"


class TestResearchBatching:
    """research.md should use OR batch for predicate lookups."""

    def test_research_has_or_batch(self):
        content = _read(RESEARCH_PATH)
        assert "+OR+" in content, "research.md should use OR batch queries"

    def test_research_batch_search_pattern(self):
        content = _read(RESEARCH_PATH)
        assert "batch_search" in content


class TestValidateSort:
    """validate.md --search mode should include sort parameter."""

    def test_validate_has_sort_parameter(self):
        content = _read(VALIDATE_PATH)
        assert "decision_date:desc" in content

    def test_validate_argument_hint_shows_sort(self):
        content = _read(VALIDATE_PATH)
        assert "--sort" in content


class TestMonitorBatching:
    """monitor.md should use OR batch for product code checks."""

    def test_monitor_has_or_batch(self):
        content = _read(MONITOR_PATH)
        assert "+OR+" in content, "monitor.md should use OR batch queries"


# ──────────────────────────────────────────────
# FDAClient tests
# ──────────────────────────────────────────────

class TestFDAClientFeatures:
    """FDAClient should have batch_510k, sort passthrough, and correct version."""

    @pytest.fixture
    def client(self, tmp_path):
        from fda_api_client import FDAClient
        c = FDAClient(cache_dir=str(tmp_path / "cache"))
        c.enabled = False
        return c

    def test_batch_510k_method_exists(self, client):
        assert hasattr(client, "batch_510k"), "FDAClient should have batch_510k method"

    def test_batch_510k_empty_list(self, client):
        result = client.batch_510k([])
        assert result["results"] == []
        assert result["meta"]["results"]["total"] == 0

    def test_search_510k_has_sort_param(self):
        """search_510k should accept sort parameter."""
        from fda_api_client import FDAClient
        import inspect
        sig = inspect.signature(FDAClient.search_510k)
        assert "sort" in sig.parameters

    def test_get_clearances_has_sort_param(self):
        """get_clearances should accept sort parameter."""
        from fda_api_client import FDAClient
        import inspect
        sig = inspect.signature(FDAClient.get_clearances)
        assert "sort" in sig.parameters

    def test_get_clearances_default_sort(self):
        """get_clearances should default to decision_date:desc."""
        from fda_api_client import FDAClient
        import inspect
        sig = inspect.signature(FDAClient.get_clearances)
        default = sig.parameters["sort"].default
        assert default == "decision_date:desc"

    def test_user_agent_version(self):
        from fda_api_client import USER_AGENT
        assert "5.4.0" in USER_AGENT, f"USER_AGENT should be 5.4.0, got: {USER_AGENT}"


# ──────────────────────────────────────────────
# API tests (require network)
# ──────────────────────────────────────────────

@pytest.mark.api
class TestAPIFeatures:
    """Live API tests — require network access. Run with: pytest -m api"""

    def test_sort_returns_ordered_results(self):
        from fda_api_client import FDAClient
        client = FDAClient()
        result = client.get_clearances("OVE", limit=5, sort="decision_date:desc")
        if result.get("degraded"):
            pytest.skip("API unavailable")
        results = result.get("results", [])
        if len(results) >= 2:
            dates = [r.get("decision_date", "") for r in results]
            assert dates == sorted(dates, reverse=True), \
                f"Results should be sorted desc: {dates}"

    def test_or_batch_returns_multiple(self, tmp_path):
        from fda_api_client import FDAClient
        client = FDAClient(cache_dir=str(tmp_path / "api_test_cache"))
        result = client.batch_510k(["K241335", "K232318"])
        if result.get("degraded"):
            pytest.skip("API unavailable")
        total = result.get("meta", {}).get("results", {}).get("total", 0)
        assert total >= 1, "OR batch should return at least 1 result"
