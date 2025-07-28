@echo off
setlocal enabledelayedexpansion

echo ===============================================
echo     TOOL KIEM TRA CO CHE UPGRADE MOI
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

echo 🔧 Chọn chế độ kiểm tra:
echo   1. Kiểm tra toàn bộ cơ chế upgrade
echo   2. Mô phỏng upgrade session (nhiều lần)
echo   3. Xem phân tích độ khó
echo   4. Thoát
echo.

set /p choice="Nhập lựa chọn (1/2/3/4): "

if "%choice%"=="1" (
    echo.
    echo 🔍 Đang chạy kiểm tra toàn bộ...
    python test_upgrade_mechanism.py
) else if "%choice%"=="2" (
    echo.
    echo 🎮 Đang mô phỏng nhiều session upgrade...
    echo Bạn sẽ thấy 5 session khác nhau:
    echo.
    
    for /L %%i in (1,1,5) do (
        echo ----------------------------------------
        echo SESSION %%i:
        python -c "
import sys
sys.path.append('.')
from test_upgrade_mechanism import *
equipment_data, items_data = load_data()
if equipment_data and items_data:
    test_item = None
    for item in items_data:
        if item['item_id'] == 'iron-sword':
            test_item = item
            break
    if test_item:
        current_level = 0
        total_spent = 0
        attempts = 0
        print(f'🗡️  {test_item[\"name\"]} từ Level 0 -> 5')
        while current_level < 5 and attempts < 50:
            attempts += 1
            result = simulate_upgrade(test_item, current_level, equipment_data)
            total_spent += result['gold_cost']
            current_level = result['new_level']
            status = '✅' if result['success'] else '❌'
            print(f'  {attempts:2d}. Level {current_level-1 if result[\"success\"] else current_level+1}→{current_level} {status} ({result[\"random_roll\"]}/{result[\"success_rate\"]}%%)')
            if current_level >= 5:
                break
        print(f'💰 Chi phí: {total_spent} vàng sau {attempts} lần')
        print()
"
    )
) else if "%choice%"=="3" (
    echo.
    echo 📊 Đang hiển thị phân tích độ khó...
    python -c "
import sys
sys.path.append('.')
from test_upgrade_mechanism import *
analyze_upgrade_difficulty()
print()
print('📈 NHẬN XÉT:')
print('- Level 1-3: Dễ dàng (80-100%% thành công)')
print('- Level 4-6: Trung bình (55-75%% thành công)')  
print('- Level 7-10: Khó (10-50%% thành công)')
print()
print('💡 Chi phí kỳ vọng tăng cấp số nhân ở level cao!')
"
) else if "%choice%"=="4" (
    echo.
    echo 👋 Cảm ơn bạn đã sử dụng tool!
    exit /b 0
) else (
    echo.
    echo ❌ Lựa chọn không hợp lệ!
)

echo.
echo ===============================================
pause
