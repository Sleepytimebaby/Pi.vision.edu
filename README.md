# Pi.vision.edu
Raspberry Pi vision project 

OS setup:

Video:
https://www.youtube.com/watch?v=PQKZk3zn7yc&list=PLtQDIsEeKHwYlVok5o6i0LcA9qatN5uMC

Instruction link:
https://core-electronics.com.au/guides/raspberry-pi/raspberry-pi-ai-camera-quickstart-guide/

-----------------------------------------------------------------------------------------------------------------------------------------------------------------

Smart Vision Station: Build Your Own AI Camera with Raspberry Pi

This guide will help you build a cool AI project using a Raspberry Pi 5, an AI Hat+, and an AI Camera.

Step 1: Set Up Your Hardware
	•	Plug the AI Hat+ into the top of your Raspberry Pi 5.
	•	Connect the AI Camera to the camera port on the AI Hat+.
	•	Insert the microSD card and connect a monitor, keyboard, and mouse.
	•	Plug in the power supply to turn it on.

Step 2: Install the Software
	•	When your Raspberry Pi starts, open the terminal.
	•	Type these commands to update your system(Bash):

     sudo apt update && sudo apt upgrade -y
	
  •	Install Python and AI tools(Bash):

      sudo apt install -y python3-full python3-venv
	  python3 -m venv ai-camera-env
	  source ai-camera-env/bin/activate
	  pip install numpy opencv-python tensorflow

run env:

	  source ai-camera-env/bin/activate
     

Step 3: Train Your AI Model
	•	Go to: https://teachablemachine.withgoogle.com
	•	Choose “Image Project” and upload pictures of two objects (like backpack and lunchbox).
	•	Train the model and export it as TensorFlow Lite.
	•	Save the model files to a USB drive and copy them to your Raspberry Pi.

Step 4: Write Your Python Code
	•	Open a text editor and write a Python script to load the model and use the camera.
	•	The script will check what the camera sees and tell you what object it recognizes.

(See camera.py)

Step 5: Test Your Project
	•	Run your Python script.
	•	Hold up an object in front of the camera.
	•	Watch the screen to see what the AI thinks it is!

Step 6: Make It Better
	•	Try adding more objects.
	•	Use a buzzer or LED to make alerts.
	•	Share your project with friends or teachers.

Congratulations! You just built your first AI-powered camera.

--------------------------------------------------------------------------------------------------------------------------------

Updated 12.05.25

1. Training Images on Teachable Machine

For a simple 2-class project (backpack vs lunchbox), you need at least 50-100 images per class, but ideally 100-200 images per class for decent accuracy. The guides recommend varying angles, lighting, and backgrounds.

2. Export the Model Correctly

When you export from Teachable Machine:

Choose "TensorFlow Lite" (not TensorFlow or TensorFlow.js)
Select "Quantized" option
Download - you'll get a zip file with model.tflite and labels.txt

3. File Placement on Raspberry Pi

 - Create a project directory
		
		mkdir ~/ai-camera
		cd ~/ai-camera

 - Unzip your downloaded model (assuming it's in Downloads)
		
		unzip ~/Downloads/converted_tflite.zip -d ~/ai-camera

 Your model files should now be in ~/ai-camera
 They might be named something like "model_unquant.tflite" or just "model.tflite" and "labels.txt"

4. Create Your Python Script

 - Make sure you're in your project directory
		
		cd ~/ai-camera

- Create the Python file
		
		nano camera_detect.py

paste the coprrected code (revised.py)

5. Run It From Terminal 

- Activate your virtual environment
		
		source ~/ai-camera-env/bin/activate

- Run the script
		
		python camera_detect.py
