"""
file_handler.py
---------------
Handles file validation and safe upload to disk.
"""

import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

# ── Constants ────────────────────────────────────────────────────────────────

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE_MB   = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# ── Public API ────────────────────────────────────────────────────────────────

def validate_and_save(file: FileStorage, upload_folder: str) -> tuple[str, str | None]:
    """
    Validate an uploaded file and save it to disk.

    Parameters
    ----------
    file          : FileStorage — the uploaded file object from Flask request
    upload_folder : str         — destination folder path

    Returns
    -------
    (filepath, error_message)
        filepath      : str | None — full path to saved file, or None on error
        error_message : str | None — human-readable error, or None on success
    """
    # Check file was actually selected
    if not file or file.filename == '':
        return None, 'No file selected. Please choose an image to upload.'

    # Check file extension
    if not _is_allowed_extension(file.filename):
        return None, (
            f'Invalid file format. '
            f'Allowed formats: {", ".join(sorted(ALLOWED_EXTENSIONS)).upper()}.'
        )

    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    if file_size > MAX_FILE_SIZE_BYTES:
        return None, (
            f'File is too large ({file_size / (1024*1024):.1f} MB). '
            f'Maximum allowed size is {MAX_FILE_SIZE_MB} MB.'
        )

    if file_size == 0:
        return None, 'The uploaded file is empty or corrupted.'

    # Save to disk
    filename = secure_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)

    os.makedirs(upload_folder, exist_ok=True)
    file.save(filepath)

    return filepath, None


# ── Internal Helpers ──────────────────────────────────────────────────────────

def _is_allowed_extension(filename: str) -> bool:
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )
