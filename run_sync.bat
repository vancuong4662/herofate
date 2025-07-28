@echo off
setlocal enabledelayedexpansion

echo ===============================================
echo   TOOL DONG BO HOA UNDERSCORE SANG DASH
echo ===============================================
echo.

:: Kiểm tra xem Python có sẵn không
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python khong duoc tim thay!
    echo Vui long cai dat Python truoc khi chay tool nay.
    pause
    exit /b 1
)

echo 🔍 Chọn chế độ thực hiện:
echo   1. Kiểm tra trước (Dry-run)
echo   2. Thực hiện đồng bộ hóa
echo   3. Chỉ kiểm tra tính đồng bộ
echo.

set /p choice="Nhập lựa chọn (1/2/3): "

if "%choice%"=="1" (
    echo.
    echo 🔍 Đang chạy chế độ kiểm tra trước...
    python sync_underscore_to_dash.py --dry-run
) else if "%choice%"=="2" (
    echo.
    echo ⚠️  Bạn có chắc chắn muốn thực hiện đồng bộ hóa?
    echo Điều này sẽ đổi tên file hình ảnh và cập nhật items.json
    set /p confirm="Gõ 'yes' để xác nhận: "
    
    if /i "!confirm!"=="yes" (
        echo.
        echo 🔄 Đang thực hiện đồng bộ hóa...
        python sync_underscore_to_dash.py
    ) else (
        echo.
        echo ❌ Đã hủy thao tác.
    )
) else if "%choice%"=="3" (
    echo.
    echo 🔍 Đang kiểm tra tính đồng bộ...
    python sync_underscore_to_dash.py --validate-only
) else (
    echo.
    echo ❌ Lựa chọn không hợp lệ!
)

echo.
echo ===============================================
pause
