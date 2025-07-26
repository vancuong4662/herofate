#!/usr/bin/env python3
"""
Tool để chuyển đổi các file webp thành png trong thư mục static/img/icon/item
"""

import os
import sys
from PIL import Image
import argparse

def convert_webp_to_png(input_dir, output_dir=None, remove_original=False):
    """
    Chuyển đổi tất cả file .webp trong thư mục thành .png
    
    Args:
        input_dir (str): Thư mục chứa file webp
        output_dir (str): Thư mục đầu ra (mặc định là cùng thư mục)
        remove_original (bool): Có xóa file gốc sau khi chuyển đổi
    """
    if output_dir is None:
        output_dir = input_dir
    
    # Đảm bảo thư mục đầu ra tồn tại
    os.makedirs(output_dir, exist_ok=True)
    
    # Tìm tất cả file .webp
    webp_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.webp')]
    
    if not webp_files:
        print(f"Không tìm thấy file .webp nào trong {input_dir}")
        return
    
    print(f"Tìm thấy {len(webp_files)} file .webp")
    
    converted_count = 0
    failed_count = 0
    
    for webp_file in webp_files:
        try:
            # Đường dẫn file đầu vào
            input_path = os.path.join(input_dir, webp_file)
            
            # Tạo tên file đầu ra (.png)
            png_filename = os.path.splitext(webp_file)[0] + '.png'
            output_path = os.path.join(output_dir, png_filename)
            
            # Mở và chuyển đổi
            with Image.open(input_path) as img:
                # Chuyển đổi sang RGBA nếu cần (để hỗ trợ transparency)
                if img.mode in ('RGBA', 'LA'):
                    # Giữ nguyên alpha channel
                    rgba_img = img
                else:
                    # Chuyển sang RGBA
                    rgba_img = img.convert('RGBA')
                
                # Lưu thành PNG
                rgba_img.save(output_path, 'PNG', optimize=True)
                
            print(f"✓ Chuyển đổi: {webp_file} → {png_filename}")
            converted_count += 1
            
            # Xóa file gốc nếu được yêu cầu
            if remove_original:
                os.remove(input_path)
                print(f"  Đã xóa file gốc: {webp_file}")
                
        except Exception as e:
            print(f"✗ Lỗi khi chuyển đổi {webp_file}: {str(e)}")
            failed_count += 1
    
    print(f"\nKết quả:")
    print(f"- Chuyển đổi thành công: {converted_count} file")
    print(f"- Thất bại: {failed_count} file")
    
    if converted_count > 0:
        print(f"\nCác file PNG đã được lưu tại: {output_dir}")

def main():
    parser = argparse.ArgumentParser(description='Chuyển đổi file WebP thành PNG')
    parser.add_argument('--input', '-i', 
                       default='static/img/icon/item',
                       help='Thư mục chứa file WebP (mặc định: static/img/icon/item)')
    parser.add_argument('--output', '-o',
                       help='Thư mục đầu ra (mặc định: cùng với input)')
    parser.add_argument('--remove-original', '-r',
                       action='store_true',
                       help='Xóa file WebP gốc sau khi chuyển đổi')
    parser.add_argument('--dry-run', '-d',
                       action='store_true',
                       help='Chỉ hiển thị danh sách file sẽ được chuyển đổi')
    
    args = parser.parse_args()
    
    # Kiểm tra thư mục đầu vào
    if not os.path.exists(args.input):
        print(f"Lỗi: Thư mục '{args.input}' không tồn tại!")
        sys.exit(1)
    
    # Kiểm tra Pillow có được cài đặt
    try:
        from PIL import Image
    except ImportError:
        print("Lỗi: Cần cài đặt Pillow để chuyển đổi hình ảnh")
        print("Chạy: pip install Pillow")
        sys.exit(1)
    
    if args.dry_run:
        # Chỉ hiển thị danh sách file
        webp_files = [f for f in os.listdir(args.input) if f.lower().endswith('.webp')]
        print(f"Tìm thấy {len(webp_files)} file .webp trong '{args.input}':")
        for webp_file in webp_files:
            png_filename = os.path.splitext(webp_file)[0] + '.png'
            print(f"  {webp_file} → {png_filename}")
    else:
        # Thực hiện chuyển đổi
        convert_webp_to_png(args.input, args.output, args.remove_original)

if __name__ == '__main__':
    main()
