@echo off
REM ============================================
REM  Script dong goi Quan Ly Chi Tieu Ca Nhan
REM  thanh file .exe chay tren Windows
REM ============================================

echo Dang cai dat PyInstaller (neu chua co)...
pip install -r requirements.txt

echo.
echo Dang dong goi thanh file .exe ...
pyinstaller --onefile --console --name QuanLyChiTieu main.py

echo.
echo ================================================
echo  XONG! File .exe nam trong thu muc: dist\QuanLyChiTieu.exe
echo ================================================
pause
