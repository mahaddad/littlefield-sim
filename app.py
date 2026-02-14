"""Littlefield Simulator — Flask web server."""

from flask import Flask, render_template, request, jsonify
from simulation import Simulation

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/simulate", methods=["POST"])
def simulate():
    try:
        cfg = request.get_json(force=True)
        sim = Simulation(cfg)
        return jsonify(sim.run())
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5050)
