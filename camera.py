import cv2
import numpy as np
import tensorflow as tf

# Load the labels
with open("labels.txt", "r") as f:
    labels = [line.strip() for line in f.readlines()]

# Load the TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Start the camera
cap = cv2.VideoCapture(0)
print("Starting camera... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame to match model input size
    input_shape = input_details[0]["shape"]
    resized_frame = cv2.resize(frame, (input_shape[2], input_shape[1]))
    input_data = np.expand_dims(resized_frame, axis=0).astype(np.float32)

    # Run inference
    interpreter.set_tensor(input_details[0]["index"], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]["index"])
    prediction = np.argmax(output_data)
    confidence = float(output_data[0][prediction])

    # Display result
    label = labels[prediction]
    cv2.putText(
        frame,
        f"{label} ({confidence:.2f})",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )

    cv2.imshow("AI Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
