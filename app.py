"""
app.py
------
Flask application factory.

Responsibilities:
- Create and configure the Flask app
- Register blueprints
- Handle Railway's dynamic $PORT via environment variable

Usage:
    Local  : python app.py
    Railway: gunicorn app:app --bind 0.0.0.0:$PORT
"""

import os
from flask import Flask
from routes.prediction import prediction_bp


def create_app() -> Flask:
    app = Flask(__name__)

    # ── Configuration ─────────────────────────────────────────────────────
    app.config['UPLOAD_FOLDER']    = os.path.join('static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB hard limit (Flask-level)
    app.config['SECRET_KEY']       = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # ── Template filters ──────────────────────────────────────────────────
    # Adds Python's built-in enumerate() as a Jinja2 filter
    # so templates can do: result.top3 | enumerate
    app.jinja_env.filters['enumerate'] = enumerate

    # ── Blueprints ────────────────────────────────────────────────────────
    app.register_blueprint(prediction_bp)

    return app


app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)