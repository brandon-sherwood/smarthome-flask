# SmartHome Flask Server

This is a simple Flask server that accepts video uploads from a companion SmartHome app.  
Uploaded videos are stored in the `uploads/` directory and automatically named following a strict convention.

---

## Features

- Accepts video uploads via `/upload`
- Automatically names files in the format:
[GESTURE NAME]PRACTICE[practice number]_[LASTNAME].mp4
- Ensures practice numbers increment automatically without overwriting existing files
- Provides a test endpoint at `/ping` for connectivity checks

---

## Requirements

- Python 3.10+ (tested with 3.13.5)
- Flask
- Flask-CORS
- Werkzeug

Install dependencies with:

```bash
pip install flask flask-cors
