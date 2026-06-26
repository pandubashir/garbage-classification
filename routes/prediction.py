"""
routes/prediction.py
--------------------
Blueprint for all prediction-related routes.
Delegates file handling to file_handler and inference to predictor.
"""

import os
from flask import Blueprint, request, render_template, current_app
from utils.file_handler import validate_and_save
from utils.predictor import predict

prediction_bp = Blueprint('prediction', __name__)


@prediction_bp.route('/', methods=['GET', 'POST'])
def index():
    """Main page: renders upload form on GET, runs prediction on POST."""
    if request.method == 'GET':
        return render_template('index.html')

    # ── Handle upload ─────────────────────────────────────────────────────
    upload_folder = current_app.config['UPLOAD_FOLDER']
    file          = request.files.get('file')

    filepath, error = validate_and_save(file, upload_folder)

    if error:
        return render_template('index.html', error=error)

    # ── Run inference ─────────────────────────────────────────────────────
    try:
        result = predict(filepath)
    except Exception as e:
        current_app.logger.error(f'Prediction failed for {filepath}: {e}')
        return render_template(
            'index.html',
            error='Prediction failed. The image may be corrupted or in an unsupported format.'
        )

    # Derive the relative URL for the uploaded image (for display in template)
    filename    = os.path.basename(filepath)
    image_url   = f'/static/uploads/{filename}'

    return render_template(
        'index.html',
        image_url=image_url,
        result=result,
    )
