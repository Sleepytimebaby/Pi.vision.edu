import cv2
import numpy as np
import tensorflow as tf
from picamera2 import Picamera2

# Define available models
models = {
    "1": ("Keyboard vs Mouse", "models/keyboard_mouse"),
    "2": ("Laptop vs TV", "models/laptop_tv"),
    "3": ("Baseball Glove vs Book", "models/baseball_book"),
    "4": ("Teddybear vs Suitcase", "models/teddybear_suitcase"),
    "5": ("Fork vs Clock", "models/fork_clock"),
}

# Show menu
print("\n===== AI Camera =====")
print("Select a model:\n")
for key, (name, _) in models.items():
    print(f"  {key}. {name}")

choice = input("\nEnter choice (1-5): ").strip()

if choice not in models:
    print("Invalid choice. Exiting.")
    exit()

model_name, model_dir = models[choice]
print(f"\nLoading model: {model_name}")

# Load the labels (strip number prefixes)
with open(f"{model_dir}/labels.txt", "r") as f:
    labels = [line.strip().split(" ", 1)[-1] for line in f.readlines()]

# Load the TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path=f"{model_dir}/model.tflite")
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print(f"Model input shape: {input_details[0]['shape']}")
print(f"Model input dtype: {input_details[0]['dtype']}")
print(f"Classes: {labels}")

# Start the camera using picamera2
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"})
picam2.configure(config)
picam2.start()

print(f"\nStarting camera with [{model_name}]... Press 'q' to quit.")

while True:
    frame = picam2.capture_array()

    # Convert RGB to BGR for OpenCV display
    display_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Get expected input shape
    input_shape = input_details[0]["shape"]
    height, width = input_shape[1], input_shape[2]

    # Convert to grayscale if model expects 1 channel
    if input_shape[3] == 1:
        processed = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        processed = cv2.resize(processed, (width, height))
        input_data = np.expand_dims(processed, axis=(0, -1))
    else:
        processed = cv2.resize(frame, (width, height))
        input_data = np.expand_dims(processed, axis=0)

    # Match model's expected dtype
    if input_details[0]["dtype"] == np.uint8:
        input_data = input_data.astype(np.uint8)
    else:
        input_data = (np.float32(input_data) - 127.5) / 127.5

    # Run inference
    interpreter.set_tensor(input_details[0]["index"], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]["index"])

    # Get prediction
    scores = output_data[0].astype(np.float32)
    if scores.max() > 1.0:
        scores = scores / 255.0
    prediction = np.argmax(scores)
    confidence = float(scores[prediction])

    # Display result
    label = labels[prediction]
    cv2.putText(
        display_frame,
        f"{label}: {confidence:.2%}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )

    cv2.imshow(f"AI Camera - {model_name}", display_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

picam2.stop()
cv2.destroyAllWindows()
