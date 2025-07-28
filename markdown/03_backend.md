# Backend & API

> Được tách ra từ README.md chính để dễ quản lý và tra cứu

## 7. Authentication & Session Management

### 7.1. Flask-Login Integration
- **Session-based authentication**: Sử dụng Flask-Login để quản lý session
- **Protected routes**: Các trang như `/town`, `/quests` yêu cầu đăng nhập
- **Automatic redirects**: 
  - Chưa đăng nhập → redirect đến `/` (trang login)
  - Đã đăng nhập → redirect từ `/` đến `/town`

### 7.2. User Model
```python
class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data.get('username')
        self.username = user_data.get('username')
        # ... other user properties
    
    def get_id(self):
        return self.username
```

### 7.3. API Endpoints
**Authentication:**
- `POST /api/register` - Đăng ký tài khoản mới
- `POST /api/login` - Đăng nhập (tạo session)
- `POST /api/logout` - Đăng xuất (xóa session)
- `GET /api/auth-status` - Kiểm tra trạng thái đăng nhập
- `GET /api/user` - Lấy thông tin user hiện tại (protected)

**Equipment System:**
- `GET /api/equipment` - Lấy thông tin equipment hiện tại và stats
- `POST /api/equipment/equip` - Trang bị item từ inventory
- `POST /api/equipment/unequip` - Gỡ trang bị về inventory
- `POST /api/equipment/upgrade` - Nâng cấp equipment đã trang bị

**Market System:**
- `GET /api/market` - Lấy danh sách item trong market của user
- `POST /api/buy-market-item` - Mua item từ market

---


## 13. Cài đặt và triển khai

### 13.1. Yêu cầu hệ thống

**🖥️ Platform Support:**
- **Máy tính để bàn hoặc laptop** (bắt buộc)
- **Độ phân giải tối thiểu**: 1024x768 pixels
- **Trình duyệt**: Chrome, Firefox, Safari, Edge (phiên bản mới)
- **Kết nối internet**: Ổn định cho MongoDB và API calls

**📱 Mobile & Tablet:**
- **Không hỗ trợ**: Game tự động redirect mobile users đến `/not-implemented`
- **Lý do**: Gameplay tối ưu cho mouse/keyboard interaction

### 13.2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

**Dependencies chính:**
- `Flask` - Web framework
- `Flask-Login` - Authentication management  
- `PyMongo` - MongoDB driver
- `python-dotenv` - Environment variables

### 13.3. Cấu hình Database

#### **MongoDB Local (Development - Khuyến nghị)**

1. **Cài đặt MongoDB Community Server:**
   - Download từ [MongoDB Community Server](https://www.mongodb.com/try/download/community)
   - Cài đặt với thiết lập mặc định
   - MongoDB sẽ chạy như Windows Service

2. **Khởi động dự án:**
   ```bash
   # Cách 1: Sử dụng script tự động
   start_local.bat
   
   # Cách 2: Chạy thủ công
   python app.py
   ```

#### **MongoDB Atlas (Production)**

1. **Tạo cluster trên MongoDB Atlas:**
   - Truy cập [MongoDB Atlas](https://www.mongodb.com/atlas)
   - Tạo cluster miễn phí (M0 Sandbox)
   - Cấu hình Database User và Network Access

2. **Chuyển sang production mode:**
   ```bash
   # Sử dụng script chuyển đổi
   switch_db.bat
   
   # Hoặc chỉnh sửa file .env thủ công
   ```

### 13.4. Chuyển đổi giữa Local và Cloud

Sử dụng script `switch_db.bat` để chuyển đổi nhanh:

```bash
switch_db.bat
```

**Lựa chọn:**
- **Option 1**: MongoDB Local (Development) - Khuyến nghị
- **Option 2**: MongoDB Atlas (Production)

### 13.5. Cấu trúc file .env

```env

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/          # Local (default)

# MONGODB_URI=mongodb+srv://...                 # Atlas (production)
DATABASE_NAME=herofate
ENVIRONMENT=development


# Flask Configuration  
SECRET_KEY=your_secret_key_here
DEBUG=True
```

### 13.6. Database Migration

Nếu cập nhật từ version cũ, chạy migration script:

```bash
python migrate_buildings.py
```

Script này sẽ cập nhật:
- `inventory` → `storage`
- `forge` → `blacksmith`  
- `shop` → `market`
- Xóa `potion` building không sử dụng

---

---


# Khởi động với MongoDB local
start_local.bat


# Chọn option 2 (MongoDB Atlas)

