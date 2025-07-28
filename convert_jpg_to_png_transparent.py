#!/usr/bin/env python3
"""
Tool chuyển đổi JPG sang PNG với nền trong suốt (Phiên bản AI nâng cao)
Chuyển đổi tất cả file .jpg trong static/img/icon/item thành .png
và xóa nền bằng AI deep learning (rembg) hoặc phương pháp truyền thống
"""

import os
import sys
from PIL import Image
import numpy as np

try:
    from rembg import remove, new_session
    REMBG_AVAILABLE = True
    print("🤖 Đã tìm thấy thư viện rembg - sẽ sử dụng AI để xóa nền")
except ImportError:
    REMBG_AVAILABLE = False
    print("⚠️  Không tìm thấy thư viện rembg - sẽ sử dụng phương pháp truyền thống")

def remove_background_ai(image):
    """
    Xóa nền bằng AI (rembg) - phương pháp tốt nhất
    
    Args:
        image: PIL Image object
    
    Returns:
        PIL Image object với nền trong suốt
    """
    try:
        # Chuyển về RGB trước khi xử lý
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Sử dụng model u2net cho các đối tượng nhỏ (items/icons)
        session = new_session('u2net')
        
        # Xóa nền bằng AI
        output = remove(image, session=session)
        
        return output
        
    except Exception as e:
        print(f"   ⚠️  Lỗi AI background removal: {str(e)}")
        print(f"   🔄 Chuyển sang phương pháp truyền thống...")
        return remove_background_traditional(image)

def remove_background_traditional(image, tolerance=30):
    """
    Xóa nền truyền thống dựa trên màu pixel góc trên trái
    
    Args:
        image: PIL Image object
        tolerance: Độ chênh lệch màu cho phép (0-255)
    
    Returns:
        PIL Image object với nền trong suốt
    """
    # Chuyển sang RGBA nếu chưa phải
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # Lấy dữ liệu pixel
    data = np.array(image)
    
    # Lấy màu pixel góc trên trái (0,0)
    bg_color = data[0, 0, :3]  # RGB values
    print(f"   🎨 Màu nền phát hiện: RGB{tuple(bg_color)}")
    
    # Tạo mask cho các pixel có màu gần giống màu nền
    # Tính khoảng cách Euclidean giữa các pixel và màu nền
    diff = np.sqrt(np.sum((data[:, :, :3] - bg_color) ** 2, axis=2))
    
    # Tạo mask: True cho các pixel cần giữ lại (khác màu nền)
    mask = diff > tolerance
    
    # Thiết lập alpha channel
    data[:, :, 3] = mask * 255  # 255 cho pixel giữ lại, 0 cho pixel trong suốt
    
    # Tạo ảnh mới từ dữ liệu đã chỉnh sửa
    result = Image.fromarray(data, 'RGBA')
    return result

def remove_background(image, method='auto', tolerance=30):
    """
    Xóa nền của ảnh với nhiều phương pháp khác nhau
    
    Args:
        image: PIL Image object
        method: 'auto', 'ai', 'traditional'
        tolerance: Độ chênh lệch màu cho phương pháp truyền thống (0-255)
    
    Returns:
        PIL Image object với nền trong suốt
    """
    if method == 'auto':
        # Tự động chọn phương pháp tốt nhất
        if REMBG_AVAILABLE:
            print(f"   🤖 Sử dụng AI để xóa nền...")
            return remove_background_ai(image)
        else:
            print(f"   🎨 Sử dụng phương pháp truyền thống...")
            return remove_background_traditional(image, tolerance)
    elif method == 'ai':
        if REMBG_AVAILABLE:
            return remove_background_ai(image)
        else:
            print(f"   ❌ Không có thư viện rembg, chuyển sang phương pháp truyền thống")
            return remove_background_traditional(image, tolerance)
    elif method == 'traditional':
        return remove_background_traditional(image, tolerance)
    else:
        raise ValueError(f"Phương pháp không hợp lệ: {method}")

def remove_background_legacy(image, tolerance=30):
    """
    LEGACY: Phương pháp cũ - giữ lại để tương thích
    """
    return remove_background_traditional(image, tolerance)

def convert_jpg_to_png_transparent(source_dir, method='auto', tolerance=30, remove_originals=False):
    """
    Chuyển đổi tất cả file JPG trong thư mục thành PNG với nền trong suốt
    
    Args:
        source_dir: Thư mục chứa file JPG
        method: Phương pháp xóa nền ('auto', 'ai', 'traditional')
        tolerance: Độ chênh lệch màu cho phương pháp truyền thống
        remove_originals: Có xóa file JPG gốc hay không
    """
    if not os.path.exists(source_dir):
        print(f"❌ Thư mục không tồn tại: {source_dir}")
        return
    
    print(f"🔍 Đang quét thư mục: {source_dir}")
    print(f"🎯 Phương pháp: {method.upper()}")
    if method in ['traditional', 'auto']:
        print(f"🎨 Tolerance: {tolerance}")
    print(f"🗑️  Xóa file gốc: {'Có' if remove_originals else 'Không'}")
    print("-" * 50)
    
    # Tìm tất cả file JPG
    jpg_files = []
    for file in os.listdir(source_dir):
        if file.lower().endswith(('.jpg', '.jpeg')):
            jpg_files.append(file)
    
    if not jpg_files:
        print("❌ Không tìm thấy file JPG nào trong thư mục")
        return
    
    print(f"📁 Tìm thấy {len(jpg_files)} file JPG")
    print("-" * 50)
    
    converted_count = 0
    error_count = 0
    
    for jpg_file in jpg_files:
        jpg_path = os.path.join(source_dir, jpg_file)
        png_file = os.path.splitext(jpg_file)[0] + '.png'
        png_path = os.path.join(source_dir, png_file)
        
        try:
            print(f"🔄 Đang xử lý: {jpg_file}")
            
            # Mở ảnh JPG
            with Image.open(jpg_path) as img:
                print(f"   📏 Kích thước: {img.size}")
                print(f"   🎨 Chế độ màu: {img.mode}")
                
                # Xóa nền bằng phương pháp được chọn
                transparent_img = remove_background(img, method=method, tolerance=tolerance)
                
                # Lưu thành PNG
                transparent_img.save(png_path, 'PNG')
                print(f"   ✅ Đã lưu: {png_file}")
                
                # Xóa file JPG gốc nếu được yêu cầu
                if remove_originals:
                    os.remove(jpg_path)
                    print(f"   🗑️  Đã xóa: {jpg_file}")
                
                converted_count += 1
                
        except Exception as e:
            print(f"   ❌ Lỗi: {str(e)}")
            error_count += 1
        
        print()
    
    # Tổng kết
    print("=" * 50)
    print("📊 KẾT QUẢ CHUYỂN ĐỔI:")
    print(f"✅ Thành công: {converted_count} file")
    print(f"❌ Lỗi: {error_count} file")
    print(f"📁 Tổng số file xử lý: {len(jpg_files)} file")
    
    if converted_count > 0:
        print(f"\n🎉 Hoàn thành! Đã chuyển đổi {converted_count} file JPG thành PNG với nền trong suốt")
        if remove_originals:
            print(f"🗑️  Đã xóa {converted_count} file JPG gốc")
        
        if method == 'auto' and REMBG_AVAILABLE:
            print(f"🤖 Đã sử dụng AI để xóa nền cho chất lượng tốt nhất")
        elif method == 'ai' and REMBG_AVAILABLE:
            print(f"🤖 Đã sử dụng AI model u2net để xóa nền")

def main():
    """Hàm main với tùy chọn dòng lệnh"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Chuyển đổi JPG sang PNG với nền trong suốt (AI nâng cao)')
    parser.add_argument('--dir', default='static/img/icon/item', 
                       help='Thư mục chứa file JPG (mặc định: static/img/icon/item)')
    parser.add_argument('--method', choices=['auto', 'ai', 'traditional'], default='auto',
                       help='Phương pháp xóa nền: auto (tự động chọn tốt nhất), ai (dùng rembg), traditional (dựa trên màu nền)')
    parser.add_argument('--tolerance', type=int, default=30,
                       help='Độ chênh lệch màu cho phương pháp truyền thống (0-255, mặc định: 30)')
    parser.add_argument('--remove-originals', action='store_true',
                       help='Xóa file JPG gốc sau khi chuyển đổi')
    parser.add_argument('--install-deps', action='store_true',
                       help='Cài đặt thư viện rembg để sử dụng AI')
    
    args = parser.parse_args()
    
    # Kiểm tra nếu người dùng muốn cài đặt dependencies
    if args.install_deps:
        print("📦 Đang cài đặt thư viện rembg...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "rembg[gpu]" if os.name != 'nt' else "rembg"])
            print("✅ Đã cài đặt thành công! Chạy lại script để sử dụng AI.")
            return
        except Exception as e:
            print(f"❌ Lỗi cài đặt: {e}")
            print("💡 Thử chạy: pip install rembg")
            return
    
    print("🖼️  TOOL CHUYỂN ĐỔI JPG SANG PNG VỚI NỀN TRONG SUỐT (AI NÂNG CAO)")
    print("=" * 70)
    
    # Hiển thị thông tin phương pháp
    if args.method == 'auto':
        if REMBG_AVAILABLE:
            print("🤖 Chế độ AUTO: Sẽ sử dụng AI (rembg) để có chất lượng tốt nhất")
        else:
            print("🎨 Chế độ AUTO: Sẽ sử dụng phương pháp truyền thống (chưa cài rembg)")
            print("💡 Để cài đặt AI: python script.py --install-deps")
    elif args.method == 'ai':
        if not REMBG_AVAILABLE:
            print("❌ Không thể sử dụng AI - chưa cài đặt rembg")
            print("💡 Cài đặt: python script.py --install-deps")
            return
        print("🤖 Chế độ AI: Sử dụng deep learning để xóa nền")
    else:
        print("🎨 Chế độ TRUYỀN THỐNG: Dựa trên màu pixel góc trên trái")
    
    print()
    
    # Chuyển đổi đường dẫn tương đối thành tuyệt đối
    source_dir = os.path.abspath(args.dir)
    
    convert_jpg_to_png_transparent(
        source_dir=source_dir,
        method=args.method,
        tolerance=args.tolerance,
        remove_originals=args.remove_originals
    )

if __name__ == "__main__":
    main()
