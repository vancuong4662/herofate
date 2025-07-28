# 🖼️ Tool Chuyển Đổi JPG sang PNG với Nền Trong Suốt (AI Nâng Cao)

Tool Python chuyên dụng để chuyển đổi hình ảnh JPG thành PNG với nền trong suốt, hỗ trợ cả phương pháp AI và truyền thống.

## ✨ Tính Năng

- 🤖 **AI Background Removal**: Sử dụng deep learning (rembg + u2net) để xóa nền với chất lượng cao nhất
- 🎨 **Traditional Method**: Phương pháp truyền thống dựa trên màu pixel góc trên trái (nhanh, phù hợp với nền đơn sắc)
- 🔄 **Auto Mode**: Tự động chọn phương pháp tốt nhất có sẵn
- 📊 **Quality Comparison**: Tool so sánh chất lượng giữa các phương pháp
- 🗑️ **Safe Processing**: Tùy chọn giữ lại file gốc hoặc xóa sau khi xử lý

## 🚀 Cài Đặt

### Cài đặt thư viện cơ bản:
```bash
pip install Pillow numpy
```

### Cài đặt AI (tùy chọn, để có chất lượng tốt nhất):
```bash
pip install rembg
# hoặc sử dụng tool để cài tự động
python convert_jpg_to_png_transparent.py --install-deps
```

## 📖 Cách Sử Dụng

### 1. Chuyển đổi cơ bản (Auto mode):
```bash
python convert_jpg_to_png_transparent.py
```

### 2. Sử dụng AI để có chất lượng tốt nhất:
```bash
python convert_jpg_to_png_transparent.py --method ai
```

### 3. Sử dụng phương pháp truyền thống (nhanh):
```bash
python convert_jpg_to_png_transparent.py --method traditional --tolerance 30
```

### 4. Chuyển đổi và xóa file gốc:
```bash
python convert_jpg_to_png_transparent.py --method ai --remove-originals
```

### 5. Chỉ định thư mục khác:
```bash
python convert_jpg_to_png_transparent.py --dir "path/to/your/images" --method ai
```

### 6. Sử dụng script Windows (.bat):
```bash
# Auto mode với tolerance 30
run_convert.bat auto 30

# AI mode và xóa file gốc
run_convert.bat ai 30 --remove-originals

# Traditional mode
run_convert.bat traditional 50
```

## 🔬 So Sánh Chất Lượng

### Tạo file so sánh để đánh giá chất lượng:
```bash
# So sánh ngẫu nhiên 5 file
python compare_quality.py

# So sánh file cụ thể
python compare_quality.py --files banana.jpg sword.jpg helmet.jpg

# Chỉ định thư mục output
python compare_quality.py --output my_comparison --count 3
```

Kết quả sẽ được lưu trong thư mục `comparison_samples` với 3 phiên bản mỗi file:
- `filename_original.jpg`: Ảnh gốc
- `filename_traditional.png`: Xóa nền bằng phương pháp truyền thống  
- `filename_ai.png`: Xóa nền bằng AI

## ⚙️ Tham Số

### Tool chính (`convert_jpg_to_png_transparent.py`):
- `--dir`: Thư mục chứa file JPG (mặc định: `static/img/icon/item`)
- `--method`: Phương pháp xóa nền (`auto`, `ai`, `traditional`)
- `--tolerance`: Độ chênh lệch màu cho phương pháp truyền thống (0-255, mặc định: 30)
- `--remove-originals`: Xóa file JPG gốc sau khi chuyển đổi
- `--install-deps`: Cài đặt thư viện rembg

### Tool so sánh (`compare_quality.py`):
- `--dir`: Thư mục chứa file JPG
- `--output`: Thư mục lưu kết quả so sánh
- `--files`: Danh sách file cụ thể để test
- `--count`: Số file ngẫu nhiên để test (nếu không dùng `--files`)

## 🎯 Khuyến Nghị Sử Dụng

### 🤖 AI Mode (Chất lượng cao nhất):
- ✅ Phù hợp với: Hình ảnh phức tạp, nhiều chi tiết, nền không đồng nhất
- ✅ Ưu điểm: Chất lượng xuất sắc, xử lý được mọi loại nền
- ❌ Nhược điểm: Chậm hơn, cần cài đặt thêm thư viện (2GB+)

### 🎨 Traditional Mode (Nhanh):
- ✅ Phù hợp với: Nền đơn sắc, hình ảnh đơn giản, xử lý hàng loạt nhanh
- ✅ Ưu điểm: Rất nhanh, không cần thư viện bổ sung
- ❌ Nhược điểm: Kém hiệu quả với nền phức tạp

### 🔄 Auto Mode (Khuyến nghị):
- ✅ Tự động chọn AI nếu có, fallback về traditional nếu không
- ✅ Cân bằng giữa chất lượng và khả năng tương thích

## 🛠️ Xử Lý Sự Cố

### Lỗi Unicode trên Windows:
```bash
# Chạy với encoding UTF-8
python -X utf8 convert_jpg_to_png_transparent.py
```

### Không thể cài đặt rembg:
```bash
# Thử cài phiên bản cụ thể
pip install rembg==2.0.50

# Hoặc dùng conda
conda install -c conda-forge rembg
```

### AI quá chậm:
```bash
# Sử dụng traditional mode cho tốc độ
python convert_jpg_to_png_transparent.py --method traditional
```

## 📊 Hiệu Suất

| Phương pháp | Tốc độ | Chất lượng | RAM sử dụng | Kích thước model |
|------------|--------|------------|-------------|------------------|
| Traditional | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | ~50MB | 0MB |
| AI (u2net) | ⚡⚡ | ⭐⭐⭐⭐⭐ | ~1GB | ~200MB |

## 🔄 Lịch Sử Phiên Bản

- **v2.0**: Thêm AI background removal với rembg
- **v1.0**: Phương pháp truyền thống dựa trên màu pixel

## 🤝 Đóng Góp

Để cải thiện tool:
1. Test với nhiều loại hình ảnh khác nhau
2. Điều chỉnh tolerance cho phương pháp truyền thống
3. Thử các model AI khác (u2netp, silueta, etc.)
4. Tối ưu hiệu suất

---

Made with ❤️ for **Hero Fate** game project
