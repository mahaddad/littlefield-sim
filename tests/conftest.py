"""Shared fixtures for Littlefield simulation tests."""

import sys
import os
import pytest

# Ensure the project root is on sys.path so `import simulation` works
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def default_cfg():
    """Default game configuration matching Day-0 factory state."""
    return {
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
        "priority_step4": False,
        "defer_buys": False,
        "timeline": [],
    }


@pytest.fixture
def minimal_cfg():
    """Minimal short simulation for fast tests."""
    return {
        "seed": 42,
        "end_day": 30,
        "start_day": 0,
        "initial_cash": 500_000.0,
        "lot_size": 60,
        "interarrival_mean": 0.125,
        "stuffers": 3,
        "testers": 2,
        "tuners": 1,
        "contract": 1,
        "initial_inventory": 9600,
        "reorder_point": 1800,
        "order_quantity": 3600,
        "priority_step4": False,
        "defer_buys": False,
        "timeline": [],
    }


@pytest.fixture
def balanced_cfg():
    """Balanced preset: extra capacity, Contract 1, generous inventory."""
    return {
        "seed": 42,
        "end_day": 485,
        "start_day": 0,
        "initial_cash": 1_000_000.0,
        "lot_size": 60,
        "interarrival_mean": 0.125,
        "stuffers": 3,
        "testers": 3,
        "tuners": 2,
        "contract": 1,
        "initial_inventory": 9600,
        "reorder_point": 1800,
        "order_quantity": 3600,
        "priority_step4": False,
        "defer_buys": False,
        "timeline": [],
    }


@pytest.fixture
def midgame_cfg():
    """Mid-game start: begins at day 50 with cash on hand."""
    return {
        "seed": 42,
        "end_day": 485,
        "start_day": 50,
        "initial_cash": 200_000.0,
        "lot_size": 60,
        "interarrival_mean": 0.125,
        "stuffers": 3,
        "testers": 2,
        "tuners": 1,
        "contract": 1,
        "initial_inventory": 9600,
        "reorder_point": 1800,
        "order_quantity": 3600,
        "priority_step4": False,
        "defer_buys": False,
        "timeline": [],
    }
