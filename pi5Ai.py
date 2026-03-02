import fiftyone.zoo as foz
import fiftyone as fo
import shutil
import os

indoor_classes = ["book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]

# Delete old dataset if exists
if fo.dataset_exists("coco-indoor"):
    fo.delete_dataset("coco-indoor")

dataset = foz.load_zoo_dataset(
    "coco-2017",
    split="validation",
    label_types=["detections"],
    classes=indoor_classes,
    max_samples=500,
    dataset_name="coco-indoor"
)

print(f"Dataset has {len(dataset)} samples")

# Base output folder
output_folder = r"C:\Users\oscar\Downloads\coco_indoor"

# Create a subfolder for each class
for cls in indoor_classes:
    os.makedirs(os.path.join(output_folder, cls), exist_ok=True)

# Copy each image into the correct class folder
for sample in dataset:
    if sample.ground_truth is None:
        continue

    # Get all class labels in this image
    labels = [det.label for det in sample.ground_truth.detections]

    # Copy image to each class folder it belongs to
    for label in set(labels):  # use set() to avoid copying twice
        if label in indoor_classes:
            dest_folder = os.path.join(output_folder, label)
            shutil.copy(sample.filepath, dest_folder)

print("Images organized by class!")
