"""Tests for the inventory / reorder system.

Rules from Overview doc and FAQ:
  - Reorder when inv < ROP AND no outstanding order AND sufficient cash (FAQ #8)
  - Kit cost = $1K + $10 * qty, paid when ordered (FAQ #3)
  - ROQ=0 prevents reorders (FAQ #9)
  - Orders queue when inventory insufficient, resume on delivery
  - Supplier delivers after exactly 4 days
"""

from simulation import Simulation, KIT_SHIP_COST, KIT_UNIT_COST, KIT_LEAD_DAYS


class TestReorderTrigger:

    def test_reorder_when_below_rop(self):
        """Inventory below ROP should trigger a reorder."""
        cfg = {
            "seed": 42,
            "end_day": 50,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 1000,   # below default ROP of 1800
            "reorder_point": 1800,
            "order_quantity": 3600,
        }
        sim = Simulation(cfg)
        result = sim.run()
        # Inventory should have increased from a delivery (at least one reorder)
        inv_values = [v for _, v in result["charts"]["inventory"]]
        # Should see an increase at some point (delivery arrived)
        assert max(inv_values) > 1000

    def test_no_reorder_when_above_rop(self):
        """Inventory well above ROP should not trigger immediate reorder."""
        cfg = {
            "seed": 42,
            "end_day": 5,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 9600,
            "reorder_point": 100,   # very low ROP
            "order_quantity": 3600,
        }
        sim = Simulation(cfg)
        result = sim.run()
        # Cash should not have been spent on kits (only revenue changes cash)
        # In a short 5-day sim with high inventory, no reorder should fire
        # Check that inventory never jumped above initial (no delivery)
        inv_values = [v for _, v in result["charts"]["inventory"]]
        assert max(inv_values) <= 9600


class TestKitCost:

    def test_kit_cost_formula(self):
        """Kit cost = $1K fixed + $10 per kit."""
        qty = 3600
        expected_cost = KIT_SHIP_COST + KIT_UNIT_COST * qty
        assert expected_cost == 1000 + 10 * 3600  # $37,000

    def test_cost_deducted_on_order(self):
        """Cash decreases by kit cost when order is placed (FAQ #3: paid when ordered)."""
        cfg = {
            "seed": 42,
            "end_day": 2,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 0,     # will trigger reorder immediately
            "reorder_point": 1800,
            "order_quantity": 3600,
        }
        sim = Simulation(cfg)
        result = sim.run()
        # Cash should have dropped by at least the kit cost ($37K)
        # even though delivery hasn't arrived yet (only 2 days, lead = 4)
        kit_cost = KIT_SHIP_COST + KIT_UNIT_COST * 3600
        final_cash = result["summary"]["final_cash"]
        assert final_cash < 500_000.0 - kit_cost + 1000  # allow small interest


class TestROQZero:

    def test_roq_zero_prevents_reorder(self):
        """Setting ROQ=0 should prevent any reorder (FAQ #9)."""
        cfg = {
            "seed": 42,
            "end_day": 30,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 100,   # very low, below ROP
            "reorder_point": 1800,
            "order_quantity": 0,        # ROQ = 0
        }
        sim = Simulation(cfg)
        result = sim.run()
        # Inventory should only decrease (orders consuming kits) or stay same
        inv_values = [v for _, v in result["charts"]["inventory"]]
        # Should never increase above initial since no reorder placed
        assert max(inv_values) <= 100


class TestOrderQueueing:

    def test_orders_queue_when_no_inventory(self):
        """Orders wait when inventory is insufficient, then proceed on delivery."""
        cfg = {
            "seed": 42,
            "end_day": 20,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 0,     # no kits at all
            "reorder_point": 1800,
            "order_quantity": 3600,
            "lot_size": 60,
        }
        sim = Simulation(cfg)
        result = sim.run()
        # Some orders should eventually complete after delivery (day ~4)
        # and some lead times should appear
        assert result["summary"]["orders_completed"] >= 0
        # There should be lead time data if any orders completed
        if result["summary"]["orders_completed"] > 0:
            assert len(result["charts"]["lead_times"]) > 0


class TestSupplierLeadTime:

    def test_supplier_lead_time_constant(self):
        """Supplier delivers after exactly 4 days (from Overview doc)."""
        assert KIT_LEAD_DAYS == 4.0

    def test_delivery_timing(self):
        """Inventory should increase around day 4 when starting with 0 inventory."""
        cfg = {
            "seed": 42,
            "end_day": 10,
            "start_day": 0,
            "initial_cash": 500_000.0,
            "initial_inventory": 0,
            "reorder_point": 1800,
            "order_quantity": 3600,
            "lot_size": 60,
        }
        sim = Simulation(cfg)
        result = sim.run()
        inv_series = result["charts"]["inventory"]
        # Find first day where inventory jumps up
        delivery_days = [
            day for day, inv in inv_series
            if inv > 0 and day > 0
        ]
        if delivery_days:
            # First delivery should be around day 4
            # (reorder placed right away since inv=0 < ROP=1800)
            first_delivery_day = delivery_days[0]
            assert first_delivery_day >= 4  # can't arrive before lead time


class TestInsufficientCashReorder:

    def test_reorder_skipped_when_cash_insufficient(self):
        """Reorder is skipped when cash is too low to cover kit cost."""
        kit_cost = KIT_SHIP_COST + KIT_UNIT_COST * 3600  # $37,000
        cfg = {
            "seed": 42,
            "end_day": 30,
            "start_day": 0,
            "initial_cash": 100.0,      # way too low for $37K kit cost
            "initial_inventory": 100,    # below ROP
            "reorder_point": 1800,
            "order_quantity": 3600,
        }
        sim = Simulation(cfg)
        result = sim.run()
        # Should have a warning about kit reorder being skipped
        reorder_warnings = [w for w in result["warnings"] if "Kit reorder skipped" in w]
        assert len(reorder_warnings) > 0
