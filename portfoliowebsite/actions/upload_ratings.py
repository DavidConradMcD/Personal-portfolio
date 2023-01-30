import os
from flask import url_for, current_app

def upload_ratings_file(ratings_upload):
    filename = ratings_upload.filename

    # Grab the extension type
    ext_type = filename.split('.')[-1]

    filepath = os.path.join(current_app.root_path, 'static/ratings_files', filename)

    filepath.save(filepath)

    return filename
