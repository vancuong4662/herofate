@echo off
REM Script tiện ích để chuyển đổi JPG sang PNG với nền trong suốt (AI nâng cao)
REM Sử dụng: run_convert.bat [method] [tolerance] [remove-originals]
REM Methods: auto, ai, traditional

echo ========================================
echo TOOL CHUYỂN ĐỔI JPG SANG PNG (AI NÂNG CAO)
echo Nền trong suốt với AI hoặc phương pháp truyền thống
echo ========================================

set METHOD=%1
set TOLERANCE=%2
set REMOVE_FLAG=%3

if "%METHOD%"=="" set METHOD=auto
if "%TOLERANCE%"=="" set TOLERANCE=30

echo Phương pháp: %METHOD%
echo Tolerance: %TOLERANCE%
echo Xóa file gốc: %REMOVE_FLAG%
echo.

REM Kiểm tra và cài đặt rembg nếu cần
if "%METHOD%"=="ai" (
    echo Kiểm tra thư viện AI...
    python -c "import rembg" 2>nul
    if errorlevel 1 (
        echo Chưa cài đặt thư viện AI. Đang cài đặt...
        python convert_jpg_to_png_transparent.py --install-deps
        pause
        exit /b
    )
)

if "%REMOVE_FLAG%"=="--remove-originals" (
    python convert_jpg_to_png_transparent.py --method %METHOD% --tolerance %TOLERANCE% --remove-originals
) else (
    python convert_jpg_to_png_transparent.py --method %METHOD% --tolerance %TOLERANCE%
)

echo.
echo ========================================
echo HƯỚNG DẪN SỬ DỤNG:
echo.
echo auto     - Tự động chọn phương pháp tốt nhất
echo ai       - Sử dụng AI để xóa nền (chất lượng cao nhất)
echo traditional - Phương pháp truyền thống (nhanh)
echo.
echo Ví dụ: run_convert.bat ai 30 --remove-originals
echo ========================================
echo.
echo Hoàn thành! Nhấn phím bất kỳ để đóng...
pause > nul
