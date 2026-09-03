@echo off
REM Ban dong dong hanh: dong goi ban dong lenh (CLI) thanh .exe rieng, neu can

echo Dang cai dat PyInstaller (neu chua co)...
pip install -r requirements.txt

echo.
echo Dang dong goi ban CLI thanh file .exe (co man hinh dong lenh)...
pyinstaller --onefile --console --name QuanLyChiTieu_CLI main.py

echo.
echo XONG! File .exe nam trong thu muc: dist\QuanLyChiTieu_CLI.exe
pause
