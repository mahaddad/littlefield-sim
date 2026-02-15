"""Tests for revenue calculation logic.

Revenue = price * max(0, min(1, (max_lt - lead_time) / (max_lt - quoted_lt)))

Contract specs (from Overview doc):
  C1: $750,  quoted 7d,   max 14d
  C2: $1000, quoted 1d,   max 2d
  C3: $1250, quoted 0.5d, max 1d
"""

from simulation import Simulation, CONTRACTS


# ── Helper: extract revenue from a Simulation instance ────────────────────

def _revenue(contract_id, lead_time):
    """Compute revenue for a single order under the given contract."""
    cfg = {
        "seed": 1,
        "end_day": 1,
        "start_day": 0,
        "initial_cash": 0.0,
        "contract": contract_id,
    }
    sim = Simulation(cfg)
    return sim._revenue(lead_time)


# ── Contract 1: $750, 7d quoted, 14d max ─────────────────────────────────

class TestContractC1:

    def test_full_price_at_zero_lt(self):
        assert _revenue(1, 0.0) == 750.0

    def test_full_price_at_quoted_lt(self):
        assert _revenue(1, 7.0) == 750.0

    def test_half_price_at_midpoint(self):
        # midpoint between 7 and 14 is 10.5 -> ratio = (14-10.5)/(14-7) = 0.5
        rev = _revenue(1, 10.5)
        assert abs(rev - 375.0) < 0.01

    def test_zero_at_max_lt(self):
        assert _revenue(1, 14.0) == 0.0

    def test_zero_beyond_max_lt(self):
        assert _revenue(1, 20.0) == 0.0

    def test_linear_interpolation_quarter(self):
        # 25% into the penalty zone: lt = 7 + 0.25*7 = 8.75
        # ratio = (14 - 8.75) / 7 = 0.75
        rev = _revenue(1, 8.75)
        assert abs(rev - 750.0 * 0.75) < 0.01

    def test_linear_interpolation_three_quarter(self):
        # 75% into the penalty zone: lt = 7 + 0.75*7 = 12.25
        # ratio = (14 - 12.25) / 7 = 0.25
        rev = _revenue(1, 12.25)
        assert abs(rev - 750.0 * 0.25) < 0.01


# ── Contract 2: $1000, 1d quoted, 2d max ─────────────────────────────────

class TestContractC2:

    def test_full_price_at_quoted(self):
        assert _revenue(2, 1.0) == 1000.0

    def test_half_price_at_midpoint(self):
        rev = _revenue(2, 1.5)
        assert abs(rev - 500.0) < 0.01

    def test_zero_at_max(self):
        assert _revenue(2, 2.0) == 0.0

    def test_zero_beyond_max(self):
        assert _revenue(2, 5.0) == 0.0

    def test_full_price_below_quoted(self):
        assert _revenue(2, 0.5) == 1000.0


# ── Contract 3: $1250, 0.5d quoted, 1d max ───────────────────────────────

class TestContractC3:

    def test_full_price_at_quoted(self):
        assert _revenue(3, 0.5) == 1250.0

    def test_full_price_below_quoted(self):
        assert _revenue(3, 0.1) == 1250.0

    def test_zero_at_max(self):
        assert _revenue(3, 1.0) == 0.0

    def test_zero_beyond_max(self):
        assert _revenue(3, 2.0) == 0.0

    def test_half_price_at_midpoint(self):
        # midpoint = 0.75, ratio = (1.0-0.75)/(1.0-0.5) = 0.5
        rev = _revenue(3, 0.75)
        assert abs(rev - 625.0) < 0.01


# ── Contract constants match the Overview doc ────────────────────────────

class TestContractConstants:

    def test_c1_values(self):
        price, quoted, maximum = CONTRACTS[1]
        assert price == 750
        assert quoted == 7.0
        assert maximum == 14.0

    def test_c2_values(self):
        price, quoted, maximum = CONTRACTS[2]
        assert price == 1000
        assert quoted == 1.0
        assert maximum == 2.0

    def test_c3_values(self):
        price, quoted, maximum = CONTRACTS[3]
        assert price == 1250
        assert quoted == 0.5
        assert maximum == 1.0
