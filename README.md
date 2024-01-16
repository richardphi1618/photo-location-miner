# photo-location-miner
Scans the EXIF data in each photo, logs the information I want to a CSV, and then quits. If the photo does not have EXIF data it logs it in the CSV with a special place holder.

# pyinstaller
```bash
pip install pyinstaller
pyinstaller --onefile main.py
```
note: probably need to run in windows