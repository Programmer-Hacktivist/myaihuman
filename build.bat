pip install -r requirements.txt
pip install pyinstaller

:: Build GUI app
pyinstaller --noconfirm --onefile --windowed app.py

:: Build background service
pyinstaller --noconfirm --onefile service.py

pip install pywin32

pause
