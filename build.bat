@echo off
REM ============================================
REM  Script dong goi Quan Ly Chi Tieu Ca Nhan
REM  (ban giao dien cua so) thanh file .exe
REM ============================================

echo Dang cai dat PyInstaller (neu chua co)...
pip install -r requirements.txt

echo.
echo Dang dong goi thanh file .exe (giao dien cua so, khong co man hinh den)...
pyinstaller --onefile --windowed --name QuanLyChiTieu gui.py

echo.
echo ================================================
echo  XONG! File .exe nam trong thu muc: dist\QuanLyChiTieu.exe
echo ================================================
pause
