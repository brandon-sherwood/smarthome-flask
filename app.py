from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import re

app = Flask(__name__)
CORS(app)


@app.route("/ping")
def ping():
    return "pong", 200


# Folder where videos stored
UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Find next available practice number


def next_number(gesture, last):
    gesture_u = gesture.upper()
    last_u = last.upper()
    prefix = f"{gesture_u}_PRACTICE_"
    suffix = f"_{last_u}.mp4"

    nums = set()
    for name in os.listdir(UPLOAD_DIR):
        if name.startswith(prefix) and name.endswith(suffix):
            m = re.search(r"_PRACTICE_(\d+)_", name)
            if m:
                nums.add(int(m.group(1)))

    n = 1
    while n in nums:
        n += 1
    return n

# Server decides the filename/number


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "missing 'file' field"}), 400

    f = request.files["file"]
    gesture = (request.form.get("gestureName") or "").strip()
    last = (request.form.get("lastName") or "").strip()

    if not f or not f.filename:
        return jsonify({"error": "empty file"}), 400
    if not gesture or not last:
        return jsonify({"error": "missing fields (gestureName, lastName)"}), 400

    # Let server decide practice number
    practice_num = next_number(gesture, last)
    target_name = f"{gesture.upper()}_PRACTICE_{practice_num}_{last.upper()}.mp4"

    safe_name = secure_filename(target_name)
    out_path = os.path.join(UPLOAD_DIR, safe_name)

    f.save(out_path)
    return jsonify({"saved_as": safe_name, "n": practice_num}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
