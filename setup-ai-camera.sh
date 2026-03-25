#!/bin/bash
echo "===== AI Camera Setup ====="

echo "Installing system packages..."
sudo apt update
sudo apt install -y python3-venv python3-picamera2 libcap-dev libgtk-3-dev

mkdir -p ~/ai-camera
cd ~/ai-camera

echo "Creating virtual environment..."
python3 -m venv ~/ai-camera-env

source ~/ai-camera-env/bin/activate
echo "Installing Python packages..."
pip install numpy tensorflow opencv-python picamera2 flatbuffers==24.3.25 --break-system-packages

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

Save with Ctrl+O, Enter, Ctrl+X. Then push to GitHub:
```
git add setup-ai-camera.sh
git commit -m "Fix setup script - clean version with correct dependencies"
git push
```

Now on the **new Pi** (haileydrnts), fix the immediate issue:
```
pip install opencv-python --break-system-packages
cd ~/ai-camera
python camera_detect.py
