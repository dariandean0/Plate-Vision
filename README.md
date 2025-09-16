# Plate-Vision: License Plate Detection and Recognition

Plate-Vision is a web application that detects and recognizes license plates from images using YOLOv5 for object detection and Tesseract OCR for text recognition.

## Features
- **License Plate Detection**: Detects license plates in images using a YOLOv5 model.
- **Text Recognition**: Extracts and displays the text from detected license plates using Tesseract OCR.
- **Web Interface**: Provides a user-friendly web interface for uploading images and viewing results.

---

## Repository Structure
Plate-Vision/ ├── backend/ # Backend code (Flask app) │ ├── app.py # Flask app entry point │ ├── models/ # Model-related code │ │ ├── plate_recognition_model.py │ │ └── init.py ├── frontend/ # Frontend code (HTML, CSS, JS) │ ├── index.html # Frontend HTML │ ├── app.js # Frontend JavaScript │ ├── styles.css # Frontend CSS ├── yolov5/ # YOLOv5 code (submodule or included) ├── car_plates_dataset/ # Dataset directory │ ├── annotations/ # Pascal VOC XML files │ ├── images/ # Raw images │ ├── labels/ # YOLO-format labels │ ├── dataset.yaml # YOLOv5 dataset configuration ├── uploads/ # Temporary directory for uploaded images ├── runs/ # YOLOv5 output directory (ignored in public repo) ├── LICENSE # License for your project ├── README.md # Project documentation ├── requirements.txt # Python dependencies └── download_dataset.py # Script to download the dataset

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Tesseract OCR installed on your system ([Installation Guide](https://github.com/tesseract-ocr/tesseract))

1. Clone the Repository:
```bash
git clone https://github.com/your-username/Plate-Vision.git
cd Plate-Vision
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Download the dataset:
```bash
python download_dataset.py
```
4. Train the YOLOv5 model:
```bash
python yolov5/train.py --img 416 --batch 16 --epochs 50 --data car_plates_dataset/dataset.yaml --weights yolov5s.pt
```

### Usage
1. Start the Flask backend:
```bash
python backend/app.py
```
2. Open frontend/index.html in your browser or start a server:
```bash
python -m http.server 8000
```
3. Upload an image to detect and read license plates.

---

## Dataset
The dataset used for training the YOLOv5 model contains images of cars with visible license plates. The dataset includes:

* Annotations: Pascal VOC XML files and YOLO-format labels.
* Images: Raw images of cars.
If the dataset is not included in this repository, use the download_dataset.py script to download it.

---

## Acknowledgments
* YOLOv5 for object detection
* Tesseract OCR for text recognition

---

## License
This project is licensed under the MIT License