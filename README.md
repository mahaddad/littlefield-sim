# Littlefield Technologies Simulator

A discrete-event factory simulator with an interactive web dashboard for exploring operations management concepts — capacity planning, inventory policy, contract selection, and queuing dynamics.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web_UI-000000?logo=flask&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-Visualizations-FF6384?logo=chartdotjs&logoColor=white)

## What It Does

The simulator models a multi-station factory where customer orders flow through a 4-step, 3-station pipeline. Station 2 handles two steps (testing and re-testing), creating a natural bottleneck that drives most strategic decisions.

```
Order → [S1 Stuffing] → [S2 Testing] → [S3 Tuning] → [S2 Re-test] → Revenue
```

You configure the factory (machines, contracts, inventory policy), schedule actions on a timeline, run the simulation, and analyze the results through interactive charts and a day-by-day snapshot slider.

## Features

### Simulation Engine
- **Discrete-event simulation** — heapq-based DES with exponential interarrivals and gamma processing times
- **Full queuing model** — per-station machine capacity, FIFO and priority scheduling at Station 2
- **Three revenue contracts** — each with quoted lead time, max lead time, and linear penalty formula
- **Inventory system** — reorder point / order quantity with supplier lead time, kit costs, and cash gating
- **Interest modeling** — daily compounding on positive cash and debt at different rates
- **Cash flow enforcement** — machine purchases blocked if they'd prevent future kit reorders

### Strategy Planning
- **Action timeline** — schedule buy/sell machines, contract switches, inventory policy changes at specific days
- **Preset strategies** — starting points you can customize
- **Deferred purchases** — optionally retry failed machine buys daily until affordable
- **Warnings** — blocked actions explained with reasons (insufficient cash, minimum machine constraints)

### Snapshot & Plan-from-Day
- **Day snapshot slider** — scrub to any day after running a sim to see machines, cash, inventory, and all charts at that point
- **Plan from Day X** — one-click to pre-fill config with the sim's computed state at any day, set it as the new starting point, and plan forward
- **Mid-game start** — run the sim from an arbitrary day with custom starting cash and inventory

### Dashboard
- **4 interactive charts** — Cash, Lead Times, Station Utilization (7-day rolling average), Kit Inventory
- **Summary stats** — final cash, avg lead time, orders completed, avg revenue per order
- **Dark theme** — glassmorphism UI with Tailwind CSS
- **How to Play guide** — built-in reference covering factory mechanics, queuing theory, and the snapshot workflow

## Quick Start

```bash
pip install flask
python app.py
```

Open **http://localhost:5050**

For auto-reload during development:

```bash
# app.py already runs with debug=True
python app.py
```

## Project Structure

```
├── simulation.py                # DES engine
├── app.py                       # Flask server (/, /guide, /simulate)
├── templates/
│   ├── index.html               # Simulator UI
│   └── guide.html               # How to Play guide
├── docs/
│   ├── *.pdf                    # Source documents
│   └── *.md                     # Markdown versions
└── requirements.txt             # flask, gunicorn
```

## How the Simulation Works

1. **Orders arrive** following an exponential distribution at a configurable rate
2. Each order consumes kits from inventory and enters the 4-step processing pipeline
3. At each station, orders queue for an available machine — processing time is exponential setup + gamma per-kit
4. Station 2 handles Steps 2 and 4, making it the natural bottleneck
5. Completed orders earn revenue based on the active contract and actual lead time
6. Inventory triggers reorders when it drops below the reorder point (if cash allows and no order is pending)
7. Daily snapshots capture cash (with compounded interest), utilization, queue lengths, and inventory
8. Timeline actions execute at their scheduled day, modifying factory state in real time

## Built With

This project was built in a few hours using AI-assisted development with [Claude](https://claude.ai). It is intended as an educational tool to help develop intuition about operations management through interactive experimentation.
