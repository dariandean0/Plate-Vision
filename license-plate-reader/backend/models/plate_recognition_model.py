from pathlib import Path
import cv2
import pytesseract
import subprocess
import os
import glob
from dotenv import load_dotenv

# pytesseract.pytesseract.tesseract_cmd = r"C:\msys64\mingw64\bin\tesseract.exe"

# Load environment variables
load_dotenv()

# Get Tesseract path from environment variable or use default
TESSERACT_CMD = os.getenv('TESSERACT_CMD', r"C:\msys64\mingw64\bin\tesseract.exe")
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.absolute()
YOLO_DIR = PROJECT_ROOT / "yolov5"
WEIGHTS_DIR = PROJECT_ROOT / "weights"
RUNS_DIR = PROJECT_ROOT / "runs"

def run_yolov5(image_path):
    #yolov5_script = r"c:\Users\Daria\OneDrive\proj\Plate-Vision\yolov5\detect.py"
    yolov5_script = str(YOLO_DIR / "detect.py")
    weights_path = str(WEIGHTS_DIR / "best.pt")
    command = [
        "python",
        yolov5_script,
        "--weights",
        weights_path,
        "--source",
        str(image_path),
        "--save-txt",
        "--project",
        str(RUNS_DIR / "detect"),
        "--name",
        "exp",
        "--conf-thres",
        "0.25"
    ]
    subprocess.run(command, check=True)

def parse_yolo_output(image_name):
    # Dynamically find the latest experiment folder
    output_dir = RUNS_DIR / "detect"
    exp_folders = list(output_dir.glob("exp*"))
    if not exp_folders:
        print("No experiment folders found in YOLOv5 output directory.")
        return []

    # Get the latest experiment folder
    latest_exp_folder = max(exp_folders, key=os.path.getmtime)
    label_file = latest_exp_folder / "labels" / f"{Path(image_name).stem}.txt"

    if not label_file.exists():
        print(f"No detections found for {image_name} in {latest_exp_folder}")
        return []

    detected_plates = []
    with open(label_file, "r") as f:
        for line in f:
            parts = line.strip().split()
            class_id, x_center, y_center, width, height = map(float, parts[0:5])
            detected_plates.append((class_id, x_center, y_center, width, height))
    return detected_plates

def detect_and_read_plate(image_path):
    # Run YOLOv5
    run_yolov5(image_path)

    # Parse YOLOv5 output
    image_name = os.path.basename(image_path)
    detections = parse_yolo_output(image_name)

    # Read the image
    image = cv2.imread(image_path)
    h, w, _ = image.shape

    detected_texts = []
    for _, x_center, y_center, width, height in detections:
        # Convert normalized coordinates to pixel values
        x1 = int((x_center - width / 2) * w)
        y1 = int((y_center - height / 2) * h)
        x2 = int((x_center + width / 2) * w)
        y2 = int((y_center + height / 2) * h)

        # Crop the detected plate
        cropped_plate = image[y1:y2, x1:x2]

        # Perform OCR
        gray_plate = cv2.cvtColor(cropped_plate, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray_plate, config="--psm 7")
        detected_texts.append(text.strip())

    return detected_texts