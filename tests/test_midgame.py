"""Tests for mid-game start feature.

The simulation supports starting at a day > 0 with initial cash,
mimicking the game's Day 50 handoff.

Rules:
  - start_day>0: clock starts at start_day
  - initial_cash: cash initialized correctly
  - Timeline actions before start_day filtered out
  - Initial snapshot exists at start_day in all time series
  - First arrival at start_day + exp(mean)
"""

from simulation import Simulation


class TestMidGameStartDay:

    def test_clock_starts_at_start_day(self):
        """Simulation clock should begin at start_day."""
        cfg = {
            "seed": 42,
            "end_day": 100,
            "start_day": 50,
            "initial_cash": 200_000.0,
            "initial_inventory": 9600,
        }
        sim = Simulation(cfg)
        assert sim.t == 50.0

    def test_start_day_in_summary(self):
        """Summary should report the correct start_day."""
        cfg = {
            "seed": 42,
            "end_day": 100,
            "start_day": 50,
            "initial_cash": 200_000.0,
            "initial_inventory": 9600,
        }
        result = Simulation(cfg).run()
        assert result["summary"]["start_day"] == 50


class TestMidGameInitialCash:

    def test_initial_cash_set(self):
        """Cash should initialize to the configured initial_cash."""
        cfg = {
            "seed": 42,
            "end_day": 100,
            "start_day": 50,
            "initial_cash": 200_000.0,
            "initial_inventory": 9600,
        }
        sim = Simulation(cfg)
        assert sim.cash == 200_000.0

    def test_zero_start_day_zero_cash(self):
        """Default start (day 0, no cash) matches the original game setup."""
        cfg = {
            "seed": 42,
            "end_day": 100,
            "start_day": 0,
            "initial_cash": 0.0,
        }
        sim = Simulation(cfg)
        assert sim.t == 0.0
        assert sim.cash == 0.0


class TestTimelineFiltering:

    def test_actions_before_start_day_filtered(self):
        """Timeline actions before start_day should be removed."""
        cfg = {
            "seed": 42,
            "end_day": 100,
            "start_day": 50,
            "initial_cash": 500_000.0,
            "initial_inventory": 9600,
            "reorder_point": 0,
            "order_quantity": 0,
            "timeline": [
                {"day": 10, "action": "buy_tester", "value": 1},   # before start
                {"day": 30, "action": "buy_stuffer", "value": 1},  # before start
                {"day": 60, "action": "buy_tuner", "value": 1},    # after start
            ],
        }
        sim = Simulation(cfg)
        # Only the day-60 action should remain
        assert len(sim.timeline) == 1
        assert sim.timeline[0]["day"] == 60

    def test_action_on_start_day_kept(self):
        """Timeline action exactly on start_day should be kept."""
        cfg = {
            "seed": 42,
            "end_day": 100,
            "start_day": 50,
            "initial_cash": 500_000.0,
            "initial_inventory": 9600,
            "reorder_point": 0,
            "order_quantity": 0,
            "timeline": [
                {"day": 50, "action": "buy_tester", "value": 1},
            ],
        }
        sim = Simulation(cfg)
        assert len(sim.timeline) == 1
        assert sim.timeline[0]["day"] == 50


class TestInitialSnapshot:

    def test_cash_snapshot_at_start_day(self):
        """Cash time series should have an initial entry at start_day."""
        cfg = {
            "seed": 42,
            "end_day": 100,
            "start_day": 50,
            "initial_cash": 200_000.0,
            "initial_inventory": 9600,
        }
        result = Simulation(cfg).run()
        cash_series = result["charts"]["cash"]
        assert len(cash_series) > 0
        first_day, first_cash = cash_series[0]
        assert first_day == 50
        assert first_cash == 200_000.0

    def test_inventory_snapshot_at_start_day(self):
        """Inventory time series should have an initial entry at start_day."""
        cfg = {
            "seed": 42,
            "end_day": 100,
            "start_day": 50,
            "initial_cash": 200_000.0,
            "initial_inventory": 9600,
        }
        result = Simulation(cfg).run()
        inv_series = result["charts"]["inventory"]
        assert len(inv_series) > 0
        first_day, first_inv = inv_series[0]
        assert first_day == 50
        assert first_inv == 9600

    def test_utilization_snapshot_at_start_day(self):
        """Utilization time series should have an initial entry at start_day."""
        cfg = {
            "seed": 42,
            "end_day": 100,
            "start_day": 50,
            "initial_cash": 200_000.0,
            "initial_inventory": 9600,
        }
        result = Simulation(cfg).run()
        for s in range(3):
            util_series = result["charts"][f"util_{s}"]
            assert len(util_series) > 0
            first_day, _ = util_series[0]
            assert first_day == 50

    def test_machines_snapshot_at_start_day(self):
        """Machines time series should have an initial entry at start_day."""
        cfg = {
            "seed": 42,
            "end_day": 100,
            "start_day": 50,
            "initial_cash": 200_000.0,
            "initial_inventory": 9600,
            "stuffers": 3,
            "testers": 2,
            "tuners": 1,
        }
        result = Simulation(cfg).run()
        machines_series = result["charts"]["machines"]
        assert len(machines_series) > 0
        first_day, first_machines = machines_series[0]
        assert first_day == 50
        assert first_machines == [3, 2, 1]

    def test_queue_snapshot_at_start_day(self):
        """Queue length time series should have an initial entry at start_day."""
        cfg = {
            "seed": 42,
            "end_day": 100,
            "start_day": 50,
            "initial_cash": 200_000.0,
            "initial_inventory": 9600,
        }
        result = Simulation(cfg).run()
        for s in range(3):
            queue_series = result["charts"][f"queue_{s}"]
            assert len(queue_series) > 0
            first_day, first_qlen = queue_series[0]
            assert first_day == 50
            assert first_qlen == 0


class TestFirstArrival:

    def test_first_arrival_after_start_day(self):
        """First order should arrive after start_day, not before."""
        cfg = {
            "seed": 42,
            "end_day": 100,
            "start_day": 50,
            "initial_cash": 200_000.0,
            "initial_inventory": 9600,
        }
        result = Simulation(cfg).run()
        # Lead times chart shows (time, lt) for completed orders
        # All times should be > 50
        for t, _ in result["charts"]["lead_times"]:
            assert t >= 50.0

    def test_no_events_before_start_day(self):
        """No time-series data should exist before start_day (except initial snapshot)."""
        cfg = {
            "seed": 42,
            "end_day": 100,
            "start_day": 50,
            "initial_cash": 200_000.0,
            "initial_inventory": 9600,
        }
        result = Simulation(cfg).run()
        # Check all chart series: days should be >= start_day
        for key in ["cash", "inventory"]:
            for day, _ in result["charts"][key]:
                assert day >= 50, f"{key} has data before start_day: day={day}"
        for s in range(3):
            for day, _ in result["charts"][f"util_{s}"]:
                assert day >= 50
            for day, _ in result["charts"][f"queue_{s}"]:
                assert day >= 50
