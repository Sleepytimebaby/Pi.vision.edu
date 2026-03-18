#!/bin/bash
echo "===== AI Camera Setup ====="

echo "Installing system packages..."
sudo apt update
sudo apt install -y python3-venv python3-picamera2 libcap-dev

mkdir -p ~/ai-camera
cd ~/ai-camera

echo "Extracting files..."
tar xzf ~/ai-camera-package.tar.gz -C ~/ai-camera

echo "Creating virtual environment..."
python3 -m venv ~/ai-camera-env

source ~/ai-camera-env/bin/activate
echo "Installing Python packages..."
pip install numpy tensorflow opencv-python-headless picamera2 --break-system-packages

SITE_PACKAGES=$(python3 -c "import site; print(site.getsitepackages()[0])")
ln -sf /usr/lib/python3/dist-packages/libcamera "$SITE_PACKAGES/" 2>/dev/null
ln -sf /usr/lib/python3/dist-packages/pykms* "$SITE_PACKAGES/" 2>/dev/null
ln -sf /usr/lib/python3/dist-packages/kms* "$SITE_PACKAGES/" 2>/dev/null

echo ""
echo "===== Setup Complete! ====="
echo "To run:"
echo "  cd ~/ai-camera"
echo "  source ~/ai-camera-env/bin/activate"
echo "  python camera_detect.py"
```

Save with Ctrl+O, Enter, Ctrl+X. Then:
```
chmod +x ~/setup-ai-camera.sh
```

**Step 3: Copy both files to a USB drive**

Plug a USB drive into your current Pi. It will probably mount automatically. Find it:
```
lsblk
```

Look for the USB drive (usually something like `/media/sleepytimebaby/USBNAME`). Then copy:
```
cp ~/ai-camera-package.tar.gz /media/sleepytimebaby/USBNAME/
cp ~/setup-ai-camera.sh /media/sleepytimebaby/USBNAME/
```

Safely eject:
```
sync
sudo umount /media/sleepytimebaby/USBNAME
```

**Step 4: On the NEW Pi**

Plug the USB drive into the new Pi. Find where it mounted:
```
lsblk
```

Copy the files to the home folder:
```
cp /media/YOURUSERNAME/USBNAME/ai-camera-package.tar.gz ~/
cp /media/YOURUSERNAME/USBNAME/setup-ai-camera.sh ~/
```

Run the setup:
```
bash ~/setup-ai-camera.sh
```

**Step 5: Run it on the NEW Pi**
```
cd ~/ai-camera
source ~/ai-camera-env/bin/activate
python camera_detect.py
