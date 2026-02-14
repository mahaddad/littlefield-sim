# Littlefield Technologies Simulator

A discrete-event simulation of the Littlefield Technologies factory with an interactive web dashboard. Built to support strategy planning for the Yale MGT 422 (Operations Engine) simulation game.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web_UI-000000?logo=flask&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-Visualizations-FF6384?logo=chartdotjs&logoColor=white)

## What It Does

The simulator models the full Littlefield factory: **4 processing steps across 3 stations**, with Station 2 (Testing) as the bottleneck since it handles Steps 2 and 4. You can experiment with different strategies — buying machines, switching contracts, adjusting inventory — and see the impact on cash, lead times, and utilization over the full 485-day simulation.

**Factory Flow:**
```
Order → [S1 Stuffing] → [S2 Testing] → [S3 Tuning] → [S2 Re-test] → Revenue
```

### Key Features

- **Discrete-event simulation engine** — heapq-based DES with exponential interarrivals, gamma processing times, and proper queuing
- **Strategy timeline** — schedule actions at specific days (buy/sell machines, switch contracts, change inventory policy)
- **Three preset strategies** — Conservative, Balanced, and Aggressive with realistic cash flow constraints
- **Contract modeling** — all 3 contracts with exact revenue formulas (quoted lead time, max lead time, linear penalty)
- **Inventory management** — reorder point / order quantity with $10/kit + $1K shipping, 4-day supplier lead time
- **Cash flow enforcement** — can't spend more than you have; machine purchases and kit orders require sufficient cash
- **Interest modeling** — 10%/yr on positive cash, 20%/yr on debt, compounded daily
- **Interactive dark-theme dashboard** — 4 real-time charts (Cash, Lead Times, Utilization, Inventory) with Chart.js

## Quick Start

```bash
pip install flask
python app.py
```

Open **http://localhost:5050** in your browser.

## Project Structure

```
├── simulation.py          # DES engine (~260 lines)
├── app.py                 # Flask server (GET / and POST /simulate)
├── templates/
│   └── index.html         # Web UI (Tailwind CSS + Chart.js)
├── requirements.txt       # Flask
├── Action_Plan_Template.md    # Fill-in-the-blank assignment template
├── Littlefield_Solution_Guide.md  # Comprehensive strategy walkthrough
└── docs/                  # Course lecture PDFs and assignment
```

## Strategy Comparison

| Strategy | Final Cash | Avg Revenue/Order | Key Moves |
|----------|-----------|-------------------|-----------|
| Do nothing | ~$605K | $750 | No changes from defaults |
| Conservative | ~$1.19M | $918 | +1 tester, Contract 2 at day 120 |
| Balanced | ~$1.23M | $927 | +1 tester +1 tuner, Contract 2 at day 90 |
| Aggressive | ~$1.27M | $926 | Staggered machine buys, Contract 3 at day 120 |

## How the Simulation Works

1. **Orders arrive** following an exponential distribution (~8/day by default)
2. Each order consumes 60 kits from inventory and enters the 4-step processing pipeline
3. At each station, orders queue for an available machine; processing time = exponential setup + gamma per-kit time
4. Station 2 processes both Step 2 and Step 4, making it the natural bottleneck (~90% utilization with 2 machines)
5. Completed orders earn revenue based on the active contract and actual lead time
6. Kit inventory triggers reorders when it drops below the reorder point (if cash allows)
7. Daily snapshots capture cash (with interest), utilization, queue lengths, and inventory levels

## Docs

The `docs/` folder contains the course materials:

- **Littlefield Technologies Overview and Assignment 2026.pdf** — the assignment
- **Littlefield FAQ.pdf** — common questions and game mechanics
- **Lectures 05-08** — queuing theory, variability, inventory models (EOQ, newsvendor)
