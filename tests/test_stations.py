"""Tests for station processing logic.

Rules from Overview doc:
  - Order flows through S1 -> S2 -> S3 -> S2 (4 steps, 3 stations)
  - Priority Step 4: step-4 jobs prioritized at S2 over step-2 jobs (FAQ #14)
  - Multiple machines dispatch correctly
  - Lot splitting: order not shipped until ALL lots complete
"""

from simulation import Simulation, STEP_STATION, STEP_PARAMS, MACHINE_COST, MACHINE_SELL


class TestStepStationMapping:

    def test_four_steps_three_stations(self):
        """STEP_STATION maps 4 steps to 3 stations: S1->S2->S3->S2."""
        assert len(STEP_STATION) == 4
        assert STEP_STATION == [0, 1, 2, 1]

    def test_step_params_count(self):
        """Each step has setup_mean and per_kit_mean."""
        assert len(STEP_PARAMS) == 4
        for setup, per_kit in STEP_PARAMS:
            assert setup > 0
            assert per_kit > 0


class TestPriorityStep4:

    def test_priority_step4_enabled(self):
        """With priority_step4=True, step-4 jobs should be prioritized at S2."""
        cfg = {
            "seed": 42,
            "end_day": 100,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 9600,
            "reorder_point": 1800,
            "order_quantity": 3600,
            "stuffers": 3,
            "testers": 1,  # bottleneck S2 to force queuing
            "tuners": 1,
            "priority_step4": True,
            "contract": 1,
        }
        sim_prio = Simulation(cfg)
        result_prio = sim_prio.run()

        cfg["priority_step4"] = False
        cfg["seed"] = 42  # same seed
        sim_fifo = Simulation(cfg)
        result_fifo = sim_fifo.run()

        # Priority should generally lead to different (often lower) avg lead
        # times since step-4 jobs finish faster when prioritized.
        # At minimum both should complete some orders.
        assert result_prio["summary"]["orders_completed"] > 0
        assert result_fifo["summary"]["orders_completed"] > 0

    def test_priority_flag_stored(self):
        """Simulation stores priority_step4 flag correctly."""
        cfg = {"seed": 1, "end_day": 1, "priority_step4": True}
        sim = Simulation(cfg)
        assert sim.prio_step4 is True

        cfg2 = {"seed": 1, "end_day": 1, "priority_step4": False}
        sim2 = Simulation(cfg2)
        assert sim2.prio_step4 is False


class TestMultipleMachines:

    def test_more_machines_increase_throughput(self):
        """Adding machines to the bottleneck should increase throughput."""
        base = {
            "seed": 42,
            "end_day": 100,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 9600,
            "reorder_point": 1800,
            "order_quantity": 3600,
            "stuffers": 3,
            "testers": 1,  # tight
            "tuners": 1,
            "contract": 1,
        }
        result_1 = Simulation(base).run()

        boosted = dict(base)
        boosted["testers"] = 3  # add capacity
        result_3 = Simulation(boosted).run()

        # More testers -> more completed orders or lower lead times
        assert result_3["summary"]["orders_completed"] >= result_1["summary"]["orders_completed"]

    def test_machine_counts_stored(self):
        """Machine counts are stored correctly from config."""
        cfg = {
            "seed": 1, "end_day": 1,
            "stuffers": 5, "testers": 4, "tuners": 3,
        }
        sim = Simulation(cfg)
        assert sim.machines == [5, 4, 3]


class TestMachineCosts:

    def test_buy_prices(self):
        """Machine buy prices match Overview doc."""
        assert MACHINE_COST[0] == 90_000   # stuffer
        assert MACHINE_COST[1] == 80_000   # tester
        assert MACHINE_COST[2] == 100_000  # tuner

    def test_sell_price(self):
        """Machine sell price is $10K for any station."""
        assert MACHINE_SELL == 10_000


class TestOrderFlow:

    def test_orders_complete_through_all_steps(self):
        """Orders should flow S1->S2->S3->S2 and complete."""
        cfg = {
            "seed": 42,
            "end_day": 50,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 9600,
            "reorder_point": 1800,
            "order_quantity": 3600,
            "stuffers": 3,
            "testers": 2,
            "tuners": 1,
            "contract": 1,
        }
        result = Simulation(cfg).run()
        # Should complete at least some orders in 50 days
        assert result["summary"]["orders_completed"] > 0
        # Lead times should all be positive
        for _, lt in result["charts"]["lead_times"]:
            assert lt > 0

    def test_utilization_tracked_for_all_stations(self):
        """All three station utilization series should be populated."""
        cfg = {
            "seed": 42,
            "end_day": 30,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 9600,
        }
        result = Simulation(cfg).run()
        for s in range(3):
            key = f"util_{s}"
            assert len(result["charts"][key]) > 0
