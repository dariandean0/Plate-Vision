# from flask import Flask, request, jsonify
# from models.plate_recognition_model import detect_and_read_plate
# import os

# app = Flask(__name__)

# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route("/upload", methods=["POST"])
# def upload_image():
#     if "image" not in request.files:
#         return jsonify({"error": "No image uploaded"}), 400

#     file = request.files["image"]
#     file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#     file.save(file_path)

#     # Process the image
#     try:
#         plates = detect_and_read_plate(file_path)
#         return jsonify({"plates": plates})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True)



# filepath: c:\Users\Daria\OneDrive\proj\Plate-Vision\license-plate-reader\backend\app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from models.plate_recognition_model import detect_and_read_plate
import os

app = Flask(__name__)
CORS(app)  # Enable CORS

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Process the image
    try:
        plates = detect_and_read_plate(file_path)
        return jsonify({"plates": plates})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)