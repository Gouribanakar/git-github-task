from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route("/api")
def api():
    with open("data.json") as f:
        return jsonify(json.load(f))

if __name__ == "__main__":
    app.run(debug=True)