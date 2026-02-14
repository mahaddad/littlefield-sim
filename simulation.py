"""Littlefield Technologies — Discrete-Event Simulation Engine.

A clean, heapq-based DES that models the 4-step / 3-station factory,
inventory replenishment, contract revenue, cash interest, and a
user-defined strategy timeline.
"""

import heapq
import random
from dataclasses import dataclass, field

# ── Constants ────────────────────────────────────────────────────────────────

CONTRACTS = {
    #       (price, quoted_lt, max_lt)
    1: (750,  7.0, 14.0),
    2: (1000, 1.0,  2.0),
    3: (1250, 0.5,  1.0),
}

STEP_STATION = [0, 1, 2, 1]          # step index  →  station index

STEP_PARAMS = [                       # (setup_mean, per_kit_mean) in days
    (0.015, 0.0010),                  # Step 0  Stuffing   @ Station 0
    (0.010, 0.0014),                  # Step 1  Testing    @ Station 1
    (0.008, 0.0015),                  # Step 2  Tuning     @ Station 2
    (0.010, 0.0020),                  # Step 3  Re-test    @ Station 1
]
# Calibrated for ~8 orders/day (interarrival 0.125 days, lot 60):
#   S1(3): ~20%  |  S2(2): ~90% BOTTLENECK  |  S3(1): ~78%
#   Total processing ≈ 0.40 days → Contract 3 feasible with enough capacity

MACHINE_COST = [90_000, 80_000, 100_000]   # buy price per station
MACHINE_SELL = 10_000                       # sell price (any station)

KIT_UNIT_COST = 10        # $/kit
KIT_SHIP_COST = 1_000     # fixed cost per shipment
KIT_LEAD_DAYS = 4.0       # supplier lead time

INTEREST_POS = 1.10 ** (1 / 365) - 1      # 10 %/yr compounded daily
INTEREST_NEG = 1.20 ** (1 / 365) - 1      # 20 %/yr compounded daily


# ── Event types ──────────────────────────────────────────────────────────────

class E:
    ARRIVAL     = 0
    KIT_DELIVER = 1
    END_PROCESS = 2


# ── Data structures ──────────────────────────────────────────────────────────

@dataclass(order=True)
class Ev:
    time: float
    kind: int   = field(compare=True)
    seq:  int   = field(default=0, compare=True)
    data: dict  = field(default_factory=dict, compare=False)


@dataclass
class Order:
    id:       int
    arrival:  float
    lot_size: int
    step:     int = 0          # 0-3


# ── Simulation ───────────────────────────────────────────────────────────────

class Simulation:

    def __init__(self, cfg: dict):
        self.rng         = random.Random(cfg.get("seed", 42))
        self.end_day     = cfg.get("end_day", 485)
        self.lot_size    = cfg.get("lot_size", 60)
        self.arrival_mean = cfg.get("interarrival_mean", 0.125)

        self.machines = [
            cfg.get("stuffers", 3),
            cfg.get("testers", 2),
            cfg.get("tuners", 1),
        ]

        cid = cfg.get("contract", 1)
        self.price, self.quoted_lt, self.max_lt = CONTRACTS[cid]

        self.inv          = cfg.get("initial_inventory", 9600)
        self.rop          = cfg.get("reorder_point", 1800)
        self.roq          = cfg.get("order_quantity", 3600)
        self.pending_kits = False
        self.prio_step4   = cfg.get("priority_step4", False)

        self.timeline = sorted(cfg.get("timeline", []), key=lambda a: a["day"])

        # ── state ──
        self.t        = 0.0
        self.cash     = 0.0
        self.seq      = 0
        self.heap     = []
        self.n_orders = 0

        self.q    = [[], [], []]      # per-station queues
        self.busy = [0, 0, 0]         # machines currently busy
        self.busy_accum = [0.0, 0.0, 0.0]
        self.kit_wait   = []          # orders waiting for inventory

        # ── metrics ──
        self._last_day  = 0
        self._prev_busy = [0.0, 0.0, 0.0]
        self._prev_t    = 0.0

        self.ts_cash  = []
        self.ts_lt    = []
        self.ts_inv   = []
        self.ts_util  = [[], [], []]
        self.ts_qlen  = [[], [], []]
        self.ts_rev   = []
        self.completed = 0

    # ── RNG helpers ──────────────────────────────────────────────────────

    def _exp(self, mean):
        return self.rng.expovariate(1.0 / mean) if mean > 0 else 0.0

    def _gamma(self, shape, scale):
        return self.rng.gammavariate(shape, scale) if shape > 0 and scale > 0 else 0.0

    def _proc_time(self, step, lot):
        s_mean, k_mean = STEP_PARAMS[step]
        return self._exp(s_mean) + self._gamma(lot, k_mean)

    # ── Event helpers ────────────────────────────────────────────────────

    def _push(self, t, kind, **kw):
        self.seq += 1
        heapq.heappush(self.heap, Ev(t, kind, self.seq, kw))

    def _revenue(self, lead_time):
        span = self.max_lt - self.quoted_lt
        if span <= 0:
            return self.price if lead_time <= self.quoted_lt else 0.0
        ratio = (self.max_lt - lead_time) / span
        return self.price * max(0.0, min(1.0, ratio))

    # ── Strategy timeline ────────────────────────────────────────────────

    def _apply_timeline(self):
        changed = False
        while self.timeline and self.timeline[0]["day"] <= self.t:
            changed = True
            a = self.timeline.pop(0)
            act, val = a["action"], a["value"]
            if act in ("buy_stuffer", "buy_tester", "buy_tuner"):
                idx = {"buy_stuffer": 0, "buy_tester": 1, "buy_tuner": 2}[act]
                n = int(val)
                # only buy what we can afford
                affordable = int(self.cash // MACHINE_COST[idx]) if MACHINE_COST[idx] > 0 else 0
                n = min(n, affordable)
                if n > 0:
                    self.machines[idx] += n
                    self.cash -= MACHINE_COST[idx] * n
            elif act == "sell_stuffer":
                n = min(int(val), self.machines[0] - 1)
                if n > 0:
                    self.machines[0] -= n
                    self.cash += MACHINE_SELL * n
            elif act == "sell_tester":
                n = min(int(val), self.machines[1] - 1)
                if n > 0:
                    self.machines[1] -= n
                    self.cash += MACHINE_SELL * n
            elif act == "sell_tuner":
                n = min(int(val), self.machines[2] - 1)
                if n > 0:
                    self.machines[2] -= n
                    self.cash += MACHINE_SELL * n
            elif act == "set_contract":
                self.price, self.quoted_lt, self.max_lt = CONTRACTS[int(val)]
            elif act == "set_lot_size":
                self.lot_size = int(val)
            elif act == "set_reorder_point":
                self.rop = int(val)
            elif act == "set_order_quantity":
                self.roq = int(val)
            elif act == "set_priority_step4":
                self.prio_step4 = bool(int(val))

        if changed:
            for s in range(3):
                self._dispatch(s)

    # ── Station dispatch ─────────────────────────────────────────────────

    def _dispatch(self, station):
        while self.q[station] and self.busy[station] < self.machines[station]:
            if station == 1 and self.prio_step4:
                idx = next(
                    (i for i, o in enumerate(self.q[station]) if o.step == 3), 0
                )
            else:
                idx = 0
            order = self.q[station].pop(idx)
            self.busy[station] += 1
            dur = self._proc_time(order.step, order.lot_size)
            self._push(
                self.t + dur, E.END_PROCESS,
                order=order, station=station, dur=dur,
            )

    # ── Inventory ────────────────────────────────────────────────────────

    def _check_reorder(self):
        if not self.pending_kits and self.inv <= self.rop and self.roq > 0:
            cost = KIT_SHIP_COST + KIT_UNIT_COST * self.roq
            if self.cash < cost:
                return                    # can't afford it — skip
            self.pending_kits = True
            self.cash -= cost
            self._push(self.t + KIT_LEAD_DAYS, E.KIT_DELIVER, qty=self.roq)

    def _fulfill_waiting(self):
        while self.kit_wait and self.inv >= self.kit_wait[0].lot_size:
            order = self.kit_wait.pop(0)
            self.inv -= order.lot_size
            self.q[STEP_STATION[0]].append(order)
            self._dispatch(STEP_STATION[0])
        self._check_reorder()

    # ── Daily snapshot ───────────────────────────────────────────────────

    def _snapshot(self):
        day = int(self.t)
        if day <= self._last_day:
            return

        # compound interest for elapsed days
        elapsed = day - self._last_day
        for _ in range(elapsed):
            rate = INTEREST_POS if self.cash >= 0 else INTEREST_NEG
            self.cash *= (1 + rate)

        # daily utilization
        dt = self.t - self._prev_t if self._prev_t > 0 else max(self.t, 0.001)
        for s in range(3):
            db  = self.busy_accum[s] - self._prev_busy[s]
            cap = max(self.machines[s], 1)
            u   = db / (dt * cap) if dt > 0 else 0
            self.ts_util[s].append((day, round(min(u, 1.0), 4)))
            self.ts_qlen[s].append((day, len(self.q[s])))

        self.ts_cash.append((day, round(self.cash, 2)))
        self.ts_inv.append((day, self.inv))

        self._prev_busy = list(self.busy_accum)
        self._prev_t    = self.t
        self._last_day  = day

    # ── Event handlers ───────────────────────────────────────────────────

    def _on_arrival(self, d):
        self.n_orders += 1
        order = Order(self.n_orders, self.t, self.lot_size)

        if self.inv >= order.lot_size:
            self.inv -= order.lot_size
            self._check_reorder()
            self.q[STEP_STATION[0]].append(order)
            self._dispatch(STEP_STATION[0])
        else:
            self.kit_wait.append(order)
            self._check_reorder()

        nxt = self.t + self._exp(self.arrival_mean)
        if nxt <= self.end_day:
            self._push(nxt, E.ARRIVAL)

    def _on_kit_deliver(self, d):
        self.inv += d["qty"]
        self.pending_kits = False
        self._fulfill_waiting()

    def _on_end_process(self, d):
        order   = d["order"]
        station = d["station"]
        dur     = d["dur"]

        self.busy[station] -= 1
        self.busy_accum[station] += dur

        order.step += 1

        if order.step >= 4:
            lt  = self.t - order.arrival
            rev = self._revenue(lt)
            self.cash += rev
            self.ts_lt.append((round(self.t, 2), round(lt, 4)))
            self.ts_rev.append((round(self.t, 2), round(rev, 2)))
            self.completed += 1
        else:
            ns = STEP_STATION[order.step]
            self.q[ns].append(order)
            self._dispatch(ns)

        self._dispatch(station)

    # ── Main loop ────────────────────────────────────────────────────────

    def run(self) -> dict:
        self._push(self._exp(self.arrival_mean), E.ARRIVAL)

        _handlers = {
            E.ARRIVAL:     self._on_arrival,
            E.KIT_DELIVER: self._on_kit_deliver,
            E.END_PROCESS: self._on_end_process,
        }

        while self.heap:
            ev = heapq.heappop(self.heap)
            if ev.time > self.end_day:
                break
            self.t = ev.time
            self._apply_timeline()
            _handlers[ev.kind](ev.data)
            self._snapshot()

        # final snapshot
        self._snapshot()

        # ── compile results ──
        lts  = [v for _, v in self.ts_lt]
        revs = [v for _, v in self.ts_rev]

        # day-50 snapshot for comparison with real game
        day50 = {}
        for series_name, series in [("cash", self.ts_cash), ("inventory", self.ts_inv)]:
            for day, val in series:
                if day >= 50:
                    day50[series_name] = val
                    break

        # smooth utilization with a 7-day rolling average
        def _smooth(series, window=7):
            out = []
            vals = [v for _, v in series]
            for i, (day, _) in enumerate(series):
                lo = max(0, i - window + 1)
                avg = sum(vals[lo:i+1]) / (i - lo + 1)
                out.append((day, round(avg, 4)))
            return out

        return {
            "summary": {
                "final_cash":        round(self.cash, 2),
                "total_revenue":     round(sum(revs), 2),
                "orders_completed":  self.completed,
                "orders_waiting":    len(self.kit_wait),
                "avg_lead_time":     round(sum(lts) / len(lts), 3) if lts else 0,
                "max_lead_time":     round(max(lts), 3) if lts else 0,
                "avg_revenue":       round(sum(revs) / len(revs), 2) if revs else 0,
                "day50_cash":        day50.get("cash", 0),
                "day50_inventory":   day50.get("inventory", 0),
            },
            "charts": {
                "cash":       self.ts_cash,
                "lead_times": self.ts_lt,
                "inventory":  self.ts_inv,
                "util_0":     _smooth(self.ts_util[0]),
                "util_1":     _smooth(self.ts_util[1]),
                "util_2":     _smooth(self.ts_util[2]),
                "queue_0":    self.ts_qlen[0],
                "queue_1":    self.ts_qlen[1],
                "queue_2":    self.ts_qlen[2],
            },
        }
