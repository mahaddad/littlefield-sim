"""Littlefield Simulator — Flask web server."""

from flask import Flask, render_template, request, jsonify
from simulation import Simulation

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/guide")
def guide():
    return render_template("guide.html")


@app.route("/simulate", methods=["POST"])
def simulate():
    try:
        cfg = request.get_json(force=True)
        sim = Simulation(cfg)
        return jsonify(sim.run())
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port, debug=True)
