import boto3
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

# -------------------------------------------------------
# CONFIGURATION — change this to your S3 bucket name
BUCKET_NAME = "image-labels-amirtha"
# -------------------------------------------------------

def upload_image(s3_client, local_path, filename):
    print(f"Uploading {filename} to S3...")
    s3_client.upload_file(local_path, BUCKET_NAME, filename)
    print("Upload complete.")

def detect_labels(rekognition_client, local_path):
    print("Analyzing image with Rekognition...")
    with open(local_path, "rb") as f:
        image_bytes = f.read()
    response = rekognition_client.detect_labels(
        Image={"Bytes": image_bytes},
        MaxLabels=10,
        MinConfidence=75
    )
    return response["Labels"]

def draw_boxes(local_path, labels, output_path):
    image = Image.open(local_path)
    img_width, img_height = image.size

    fig, ax = plt.subplots(1)
    ax.imshow(image)

    colors = ["red", "blue", "green", "orange", "purple", "cyan", "magenta", "yellow"]
    color_index = 0

    for label in labels:
        label_name = label["Name"]
        confidence = round(label["Confidence"], 1)

        # Only draw boxes for labels that have instance locations
        if label["Instances"]:
            for instance in label["Instances"]:
                box = instance["BoundingBox"]

                # Rekognition gives values as percentages (0.0 to 1.0)
                # Multiply by image dimensions to get pixel coordinates
                left   = box["Left"]   * img_width
                top    = box["Top"]    * img_height
                width  = box["Width"]  * img_width
                height = box["Height"] * img_height

                color = colors[color_index % len(colors)]

                rect = patches.Rectangle(
                    (left, top), width, height,
                    linewidth=2,
                    edgecolor=color,
                    facecolor="none"
                )
                ax.add_patch(rect)

                ax.text(
                    left, top - 5,
                    f"{label_name} ({confidence}%)",
                    color=color,
                    fontsize=10,
                    fontweight="bold",
                    backgroundcolor="black"
                )

                color_index += 1
        else:
            # Scene-level label (no bounding box) — just print it
            print(f"  Scene label: {label_name} ({confidence}%)")

    ax.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", dpi=150)
    plt.close()
    print(f"Output saved to: {output_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python detect_labels.py images/sample.jpg")
        sys.exit(1)

    local_path = sys.argv[1]

    if not os.path.exists(local_path):
        print(f"Error: File not found — {local_path}")
        sys.exit(1)

    filename = os.path.basename(local_path)
    output_path = os.path.join("output", f"labeled_{filename}")

    # Create AWS clients
    s3_client          = boto3.client("s3",          region_name="us-east-1")
    rekognition_client = boto3.client("rekognition", region_name="us-east-1")

    # Step 1: Upload image to S3
    upload_image(s3_client, local_path, filename)

    # Step 2: Detect labels using Rekognition
    labels = detect_labels(rekognition_client, local_path)

    print(f"\nDetected {len(labels)} labels:")
    for label in labels:
        print(f"  - {label['Name']} ({round(label['Confidence'], 1)}%)")

    # Step 3: Draw bounding boxes and save output image
    draw_boxes(local_path, labels, output_path)

if __name__ == "__main__":
    main()
