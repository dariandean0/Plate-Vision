# import cv2
# import pytesseract
# import subprocess
# import os

# def run_yolov5(image_path):
#     yolov5_script = r"c:\Users\Daria\OneDrive\proj\Plate-Vision\yolov5\detect.py"
#     command = [
#         "python",
#         yolov5_script,
#         "--weights",
#         "c:/Users/Daria/OneDrive/proj/Plate-Vision/yolov5/runs/train/exp5/weights/best.pt",
#         "--source",
#         image_path,
#         "--save-txt",  # Save detection results as text files
#         "--project",
#         "runs/detect",  # Output directory
#         "--name",
#         "exp",  # Experiment name
#         "--conf-thres",
#         "0.25"
#     ]
#     subprocess.run(command, check=True)

# def parse_yolo_output(image_name):
#     # Path to YOLOv5 output directory
#     output_dir = r"c:\Users\Daria\OneDrive\proj\Plate-Vision\yolov5\runs\detect\exp\labels"
#     label_file = os.path.join(output_dir, os.path.splitext(image_name)[0] + ".txt")

#     if not os.path.exists(label_file):
#         print(f"No detections found for {image_name}")
#         return []

#     detected_plates = []
#     with open(label_file, "r") as f:
#         for line in f:
#             parts = line.strip().split()
#             class_id, x_center, y_center, width, height = map(float, parts[0:5])
#             detected_plates.append((class_id, x_center, y_center, width, height))
#     return detected_plates

# def detect_and_read_plate(image_path):
#     # Run YOLOv5
#     run_yolov5(image_path)

#     # Parse YOLOv5 output
#     image_name = os.path.basename(image_path)
#     detections = parse_yolo_output(image_name)

#     # Read the image
#     image = cv2.imread(image_path)
#     h, w, _ = image.shape

#     detected_texts = []
#     for _, x_center, y_center, width, height in detections:
#         # Convert normalized coordinates to pixel values
#         x1 = int((x_center - width / 2) * w)
#         y1 = int((y_center - height / 2) * h)
#         x2 = int((x_center + width / 2) * w)
#         y2 = int((y_center + height / 2) * h)

#         # Crop the detected plate
#         cropped_plate = image[y1:y2, x1:x2]

#         # Perform OCR
#         gray_plate = cv2.cvtColor(cropped_plate, cv2.COLOR_BGR2GRAY)
#         text = pytesseract.image_to_string(gray_plate, config="--psm 7")
#         detected_texts.append(text.strip())

#     return detected_texts




import cv2
import pytesseract
import subprocess
import os
import glob

pytesseract.pytesseract.tesseract_cmd = r"C:\msys64\mingw64\bin\tesseract.exe"

def run_yolov5(image_path):
    yolov5_script = r"c:\Users\Daria\OneDrive\proj\Plate-Vision\yolov5\detect.py"
    command = [
        "python",
        yolov5_script,
        "--weights",
        "c:/Users/Daria/OneDrive/proj/Plate-Vision/yolov5/runs/train/exp5/weights/best.pt",
        "--source",
        image_path,
        "--save-txt",  # Save detection results as text files
        "--project",
        "runs/detect",  # Output directory
        "--name",
        "exp",  # Experiment name
        "--conf-thres",
        "0.25"
    ]
    subprocess.run(command, check=True)

def parse_yolo_output(image_name):
    # Dynamically find the latest experiment folder
    output_dir = r"c:\Users\Daria\OneDrive\proj\Plate-Vision\yolov5\runs\detect"
    exp_folders = glob.glob(os.path.join(output_dir, "exp*"))
    if not exp_folders:
        print("No experiment folders found in YOLOv5 output directory.")
        return []

    # Get the latest experiment folder
    latest_exp_folder = max(exp_folders, key=os.path.getmtime)
    label_file = os.path.join(latest_exp_folder, "labels", os.path.splitext(image_name)[0] + ".txt")

    if not os.path.exists(label_file):
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