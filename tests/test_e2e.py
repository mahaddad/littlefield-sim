"""End-to-end simulation tests.

Validates overall simulation behavior:
  - Default config with seed 42: positive cash, orders completed > 0
  - Deterministic: same seed produces identical results
  - All time-series arrays non-empty and sorted
  - Balanced preset: no warnings, positive final cash
  - Edge cases: very short sim, single machines, zero inventory
"""

from simulation import Simulation


class TestDefaultConfig:

    def test_default_seed42_completes_orders(self):
        """Default config seed 42 should complete orders."""
        cfg = {
            "seed": 42,
            "end_day": 485,
            "start_day": 0,
            "initial_cash": 0.0,
            "lot_size": 60,
            "interarrival_mean": 0.125,
            "stuffers": 3,
            "testers": 2,
            "tuners": 1,
            "contract": 1,
            "initial_inventory": 9600,
            "reorder_point": 1800,
            "order_quantity": 3600,
        }
        result = Simulation(cfg).run()
        assert result["summary"]["orders_completed"] > 0

    def test_default_seed42_positive_cash(self):
        """Default config should generate positive cash over 485 days."""
        cfg = {
            "seed": 42,
            "end_day": 485,
            "start_day": 0,
            "initial_cash": 0.0,
            "lot_size": 60,
            "interarrival_mean": 0.125,
            "stuffers": 3,
            "testers": 2,
            "tuners": 1,
            "contract": 1,
            "initial_inventory": 9600,
            "reorder_point": 1800,
            "order_quantity": 3600,
        }
        result = Simulation(cfg).run()
        assert result["summary"]["final_cash"] > 0

    def test_default_total_revenue_positive(self):
        """Total revenue should be positive."""
        cfg = {
            "seed": 42,
            "end_day": 485,
            "start_day": 0,
            "initial_cash": 0.0,
            "lot_size": 60,
            "interarrival_mean": 0.125,
            "stuffers": 3,
            "testers": 2,
            "tuners": 1,
            "contract": 1,
            "initial_inventory": 9600,
            "reorder_point": 1800,
            "order_quantity": 3600,
        }
        result = Simulation(cfg).run()
        assert result["summary"]["total_revenue"] > 0


class TestDeterminism:

    def test_same_seed_same_results(self):
        """Same seed should produce identical results."""
        cfg = {
            "seed": 42,
            "end_day": 100,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 9600,
            "reorder_point": 1800,
            "order_quantity": 3600,
        }
        result1 = Simulation(cfg).run()
        result2 = Simulation(cfg).run()

        assert result1["summary"]["final_cash"] == result2["summary"]["final_cash"]
        assert result1["summary"]["orders_completed"] == result2["summary"]["orders_completed"]
        assert result1["summary"]["total_revenue"] == result2["summary"]["total_revenue"]
        assert result1["summary"]["avg_lead_time"] == result2["summary"]["avg_lead_time"]

    def test_different_seeds_different_results(self):
        """Different seeds should produce different results."""
        cfg1 = {
            "seed": 42,
            "end_day": 100,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 9600,
            "reorder_point": 1800,
            "order_quantity": 3600,
        }
        cfg2 = dict(cfg1, seed=99)
        result1 = Simulation(cfg1).run()
        result2 = Simulation(cfg2).run()
        # With different seeds, at least one metric should differ
        assert (
            result1["summary"]["final_cash"] != result2["summary"]["final_cash"]
            or result1["summary"]["orders_completed"] != result2["summary"]["orders_completed"]
        )

    def test_determinism_with_timeline(self):
        """Determinism holds even with timeline actions."""
        cfg = {
            "seed": 42,
            "end_day": 100,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 9600,
            "reorder_point": 1800,
            "order_quantity": 3600,
            "timeline": [
                {"day": 20, "action": "buy_tester", "value": 1},
                {"day": 40, "action": "set_contract", "value": 2},
            ],
        }
        result1 = Simulation(cfg).run()
        result2 = Simulation(cfg).run()
        assert result1["summary"]["final_cash"] == result2["summary"]["final_cash"]


class TestTimeSeriesIntegrity:

    def test_all_series_non_empty(self):
        """All time-series arrays should be non-empty after a full run."""
        cfg = {
            "seed": 42,
            "end_day": 100,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 9600,
            "reorder_point": 1800,
            "order_quantity": 3600,
        }
        result = Simulation(cfg).run()
        charts = result["charts"]
        assert len(charts["cash"]) > 0
        assert len(charts["lead_times"]) > 0
        assert len(charts["inventory"]) > 0
        assert len(charts["revenue"]) > 0
        assert len(charts["machines"]) > 0
        for s in range(3):
            assert len(charts[f"util_{s}"]) > 0
            assert len(charts[f"queue_{s}"]) > 0

    def test_cash_series_sorted_by_day(self):
        """Cash time series should be sorted by day."""
        cfg = {
            "seed": 42,
            "end_day": 100,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 9600,
        }
        result = Simulation(cfg).run()
        days = [d for d, _ in result["charts"]["cash"]]
        assert days == sorted(days)

    def test_inventory_series_sorted_by_day(self):
        """Inventory time series should be sorted by day."""
        cfg = {
            "seed": 42,
            "end_day": 100,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 9600,
        }
        result = Simulation(cfg).run()
        days = [d for d, _ in result["charts"]["inventory"]]
        assert days == sorted(days)

    def test_lead_times_sorted_by_time(self):
        """Lead times should be sorted by completion time."""
        cfg = {
            "seed": 42,
            "end_day": 100,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 9600,
        }
        result = Simulation(cfg).run()
        times = [t for t, _ in result["charts"]["lead_times"]]
        assert times == sorted(times)

    def test_utilization_series_sorted(self):
        """Utilization series should be sorted by day."""
        cfg = {
            "seed": 42,
            "end_day": 100,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 9600,
        }
        result = Simulation(cfg).run()
        for s in range(3):
            days = [d for d, _ in result["charts"][f"util_{s}"]]
            assert days == sorted(days)


class TestBalancedPreset:

    def test_balanced_no_warnings(self, balanced_cfg):
        """Balanced preset should produce no warnings."""
        result = Simulation(balanced_cfg).run()
        assert len(result["warnings"]) == 0

    def test_balanced_positive_cash(self, balanced_cfg):
        """Balanced preset should end with positive cash."""
        result = Simulation(balanced_cfg).run()
        assert result["summary"]["final_cash"] > 0

    def test_balanced_completes_many_orders(self, balanced_cfg):
        """Balanced preset should complete a significant number of orders."""
        result = Simulation(balanced_cfg).run()
        # ~8 orders/day * 485 days = ~3880, but not all complete in time
        assert result["summary"]["orders_completed"] > 100


class TestEdgeCases:

    def test_very_short_simulation(self):
        """Very short sim (5 days) should not crash."""
        cfg = {
            "seed": 42,
            "end_day": 5,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 9600,
        }
        result = Simulation(cfg).run()
        assert "summary" in result
        assert "charts" in result

    def test_single_machines_all_stations(self):
        """Running with 1 machine per station should work (slow but valid)."""
        cfg = {
            "seed": 42,
            "end_day": 50,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 9600,
            "stuffers": 1,
            "testers": 1,
            "tuners": 1,
            "reorder_point": 1800,
            "order_quantity": 3600,
        }
        result = Simulation(cfg).run()
        assert result["summary"]["orders_completed"] >= 0

    def test_zero_initial_inventory(self):
        """Starting with zero inventory should work (orders queue for kits)."""
        cfg = {
            "seed": 42,
            "end_day": 50,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 0,
            "reorder_point": 1800,
            "order_quantity": 3600,
        }
        result = Simulation(cfg).run()
        assert "summary" in result

    def test_high_interarrival_mean(self):
        """Very few orders (high interarrival) should still work."""
        cfg = {
            "seed": 42,
            "end_day": 100,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 9600,
            "interarrival_mean": 10.0,   # ~1 order every 10 days
        }
        result = Simulation(cfg).run()
        # Very few orders but should complete some
        assert result["summary"]["orders_completed"] >= 0

    def test_result_structure(self):
        """Result dict should have expected top-level keys."""
        cfg = {
            "seed": 42,
            "end_day": 20,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 9600,
        }
        result = Simulation(cfg).run()
        assert "warnings" in result
        assert "summary" in result
        assert "charts" in result
        assert isinstance(result["warnings"], list)
        assert isinstance(result["summary"], dict)
        assert isinstance(result["charts"], dict)

    def test_summary_keys(self):
        """Summary should contain all expected keys."""
        cfg = {
            "seed": 42,
            "end_day": 20,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 9600,
        }
        result = Simulation(cfg).run()
        expected_keys = {
            "start_day", "final_cash", "total_revenue",
            "orders_completed", "orders_waiting",
            "avg_lead_time", "max_lead_time", "avg_revenue",
        }
        assert expected_keys == set(result["summary"].keys())

    def test_charts_keys(self):
        """Charts should contain all expected keys."""
        cfg = {
            "seed": 42,
            "end_day": 20,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 9600,
        }
        result = Simulation(cfg).run()
        expected_keys = {
            "cash", "lead_times", "inventory", "revenue", "machines",
            "util_0", "util_1", "util_2",
            "queue_0", "queue_1", "queue_2",
        }
        assert expected_keys == set(result["charts"].keys())
