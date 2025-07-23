# Hero Fate – Web Game Online (Dự án học lập trình)

## 1. Giới thiệu chung

**Hero Fate** là một web game online đơn giản, được thiết kế như một dự án học tập để học viên mới bắt đầu học lập tr#### Giao diện `/town`

**🎮 Enhanced Navigation Bar:**
- **User Stats**: Cấp độ, Vàng, EXP, Danh tiếng với icons  
- **Player Info Button**: Nút "Thông tin" mở modal chi tiết về player
- **Navigation Actions**: Thị trấn, Nhiệm vụ, Kho đồ, Đăng xuất
- **Clean Layout**: Streamlined horizontal bar without avatar clutter

**📋 Player Info Modal (NEW):**
- **Trigger**: Click nút "Thông tin" trong navigation bar
- **Layout**: Modal nằm ngang với 2 cột chính
  - **Left Side**: Player avatar (128x128 canvas) + username
  - **Right Side**: Stats grid với 10 thông số (Level, Gold, EXP, Reputation, STR, AGI, INT, VIT, WIS, Crit Rate)
- **Animation**: Configurable idle animation chỉ chạy khi modal mở
- **Auto-close**: Animation tự động dừng khi đóng modal
- **Professional**: Centered layout với proper spacing

**� Player Animation System (ENHANCED):**
- **GML.js Integration**: Sử dụng thư viện tự tạo cho sprite animation
- **Canvas Rendering**: 128x128 canvas với idle animation full-size
- **Configurable Speed**: Animation speed có thể điều chỉnh qua JavaScript
- **Control Functions**:
  - `setAnimationSpeed(speed)`: Điều chỉnh tốc độ (0.05-0.3)
  - `setAnimationPreset(preset)`: Sử dụng preset ('slow', 'normal', 'fast')
  - `getAnimationSpeed()`: Lấy tốc độ hiện tại
  - `startPlayerAnimation()` / `stopPlayerAnimation()`: Control animation
- **On-demand**: Animation chỉ chạy khi Player Info Modal mở
- **Performance**: Efficient memory usage với conditional rendering thể thực hành theo. Game có lối chơi nhẹ nhàng, gồm hai phần chính: **xây dựng thị trấn** và **chiến đấu theo lượt (turn-based)**.
- Khi thiếu nhiệm vụ, hệ thống tự thêm mới từ file JSON
- Nút "Bắt đầu" sẽ chuyển sang `/battle` (thay vì navigation trực tiếp)

### D. Chiến đấu theo lượt (`/battle`) - Protected Route

- Dạng 1 vs 1, luân phiên
- Kẻ địch xác định qua `battle_enemy` (từ localStorage)  
- Gọi API lấy dữ liệu enemy từ JSON
- **Chỉ truy cập từ quests**: Không có direct navigation button

### E. Hội thoại (`/dialog/<id>/<quest_id>`) - Protected Routeation Bar:**
- **Player Avatar**: Canvas animation với male_idle.png (4 frames, 128x128 → 64x64)
- **User Stats**: Cấp độ, Vàng, EXP, Danh tiếng với icons
- **Navigation Actions**: Thị trấn, Nhiệm vụ, Kho đồ, Đăng xuất
- **Integrated Layout**: Single horizontal bar thay vì multiple sections

**🏗️ Buildings Grid:**
- Các công trình được render dạng card theo grid 3 cột
- Hover để xem tên, click mở modal tương ứng
- Tòa thị chính mở `/quests`
- Có nút "Xây dựng" để hiện danh sách công trình có thể xây

**🎨 Player Animation System:**
- **GML.js Integration**: Sử dụng thư viện tự tạo cho sprite animation
- **Canvas Rendering**: 64x64 canvas với idle animation
- **Frame Management**: 4 frames với tốc độ 0.2, loop tự động
- **Fallback**: Icon 👤 nếu không load được spriteới bắt đầu học lập trình có thể thực hành theo. Game có lối chơi nhẹ nhàng, gồm hai phần chính: **xây dựng thị trấn** và **chiến đấu theo lượt (turn-based)**.

Dự án sử dụng công nghệ phổ biến, đơn giản, dễ học và dễ triển khai.

---

## 2. Mục tiêu dự án

- Giúp học viên hiểu được luồng hoạt động của một ứng dụng web fullstack.
- Thực hành sử dụng API, kết nối frontend – backend – database.
- Làm quen với các công nghệ cơ bản: Flask, MongoDB, HTML/CSS, JavaScript (XHR).
- Phát triển kỹ năng tư duy logic, làm việc với dữ liệu JSON, xử lý client-side storage (localStorage).

---

## 3. Công nghệ sử dụng

### Backend

- Python
- Flask (REST API) + Flask-Login (Authentication)
- MongoDB (NoSQL database): chỉ sử dụng cho dữ liệu **user**
  - **Development**: MongoDB Local (nhanh hơn, khuyến nghị)
  - **Production**: MongoDB Atlas (cloud)
- Session-based authentication với Flask-Login
- Các dữ liệu hệ thống khác như **quái vật (enemies), vật phẩm (items), nhiệm vụ (quests), hội thoại (dialogs), công trình (buildings), kỹ năng (skills)** sẽ được lưu trữ trong các file JSON tĩnh trên server, để giúp học viên dễ đọc, dễ chỉnh sửa, dễ hiểu.

#### Cấu trúc database `users`

```json
{
  "username": "cuongnv",
  "password": "123456",
  "created_at": "...",
  "gender": "male",
  "buildings": {
    "town_hall": 1,
    "storage": 1,       // Đã đổi từ "inventory"
    "blacksmith": 0,    // Đã đổi từ "forge"
    "market": 0,        // Đã đổi từ "shop"
    "mage_tower": 0
  },
  "quests": [
    { "quest_id": "q001", "state": "doing" },
    { "quest_id": "q004", "state": "done" }
  ],
  "dialogs_seen": [12],
  "inventory": [
    { "item_id": "sword001", "quantity": 1, "level": 2 },
    { "item_id": "hp_potion", "quantity": 5 }
  ],
  "gold": 1250,
  "exp": 780,
  "reputation": 35,
  "stats": {
    "STR": 12,
    "AGI": 8,
    "INT": 5,
    "VIT": 10,
    "WIS": 7,
    "crit_rate": 0.1
  },
  "skills": [
    { "skill_id": 1, "level": 2 },
    { "skill_id": 3, "level": 1 }
  ]
}
```

- `username`, `password`: thông tin đăng nhập
- `gender`: giới tính người chơi (`male` hoặc `female`) — được sử dụng để chọn hình ảnh nhân vật từ thư mục `static/img/player/`
- `buildings`: lưu cấp độ các công trình đã xây (0 nghĩa là chưa xây)
- `quests`: danh sách các nhiệm vụ người chơi đã nhận (và trạng thái)
- `dialogs_seen`: lưu lại những đoạn hội thoại đã xem
- `inventory`: chứa các item người chơi sở hữu
- `gold`: số tiền hiện có
- `exp`: kinh nghiệm hiện tại (level được tính từ EXP này)
- `reputation`: danh tiếng, ảnh hưởng đến tương tác NPC
- `stats`: chỉ số RPG
- `skills`: kỹ năng đã học và cấp độ tương ứng

### Frontend

- HTML, W3.CSS, CSS tùy chỉnh với background images
- Font Awesome 5.15.4
- JavaScript (dùng Fetch API để gọi API)
- Responsive design với mobile support
- Visual effects và animations

---

## 4. Authentication & Session Management

### 4.1. Flask-Login Integration
- **Session-based authentication**: Sử dụng Flask-Login để quản lý session
- **Protected routes**: Các trang như `/town`, `/quests` yêu cầu đăng nhập
- **Automatic redirects**: 
  - Chưa đăng nhập → redirect đến `/` (trang login)
  - Đã đăng nhập → redirect từ `/` đến `/town`

### 4.2. User Model
```python
class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data.get('username')
        self.username = user_data.get('username')
        # ... other user properties
    
    def get_id(self):
        return self.username
```

### 4.3. API Endpoints
- `POST /api/register` - Đăng ký tài khoản mới
- `POST /api/login` - Đăng nhập (tạo session)
- `POST /api/logout` - Đăng xuất (xóa session)
- `GET /api/auth-status` - Kiểm tra trạng thái đăng nhập
- `GET /api/user` - Lấy thông tin user hiện tại (protected)

---

## 5. UI/UX Improvements

### 5.1. Visual Design
- **Header**: Background image từ `static/img/background/1.jpg`
- **Building System**: 
  - Hình ảnh building từ `static/img/building/{building_id}.png`
  - Ground texture: `static/img/building/ground.png`
  - Building images được scale 2x để nổi bật
- **Visual States**: 
  - Đã xây: Màu bình thường + level badge xanh
  - Chưa xây: Grayscale filter + level badge đỏ

### 5.2. Desktop-Only Experience
- **Platform Support**: Chỉ hỗ trợ máy tính để bàn và laptop
- **Screen Requirements**: Độ phân giải tối thiểu 1024x768
- **Mobile Detection**: Tự động redirect thiết bị mobile đến `/not-implemented`
- **Optimized Layout**: 3 cột buildings được tối ưu cho màn hình lớn

### 5.3. Mobile Not Supported
- **Auto Detection**: JavaScript kiểm tra User Agent và screen size
- **Redirect Logic**: Mobile users → `/not-implemented` page
- **Clear Messaging**: Thông báo rõ ràng về yêu cầu hệ thống
- **No Responsive CSS**: Đã loại bỏ toàn bộ mobile responsive để tối ưu performance

---

## 6. Các Route

### A. Trang chính (`/`)

- **Logic redirect thông minh:**
  - Chưa đăng nhập: Hiển thị form login/register
  - Đã đăng nhập: Tự động redirect đến `/town`
- **Slideshow**: Giới thiệu game với hình ảnh động
- **Responsive layout**: 2 cột (slideshow + auth forms)

### B. Xây dựng thị trấn (`/town`) - Protected Route

| Công trình                   | Tính năng                                        | Cải tiến nâng cấp                                     |
|-----------------------------|--------------------------------------------------|-------------------------------------------------------|
| Thợ rèn (blacksmith)        | Chế tạo và nâng cấp trang bị                     | Tăng giới hạn upgrade level                           |
| Chợ (market)                | Mua bán vật phẩm                                 | Tăng số lượng item xuất hiện trong shop               |
| Tòa thị chính (town_hall)   | Nhận nhiệm vụ phụ tuyến                          | Tăng độ khó nhiệm vụ                                  |
| Kho (storage)               | Quản lý item người chơi                          | Tăng số lượng slot lưu trữ                            |
| Tháp phép thuật (mage_tower)| Học và nâng cấp kỹ năng phép thuật               | Mở bán sách phép, xem và nâng cấp kỹ năng đã học     |

#### Giao diện `/town`

- Các công trình được render dạng card theo grid 3 cột
- Hover để xem tên, click mở modal tương ứng
- Tòa thị chính mở `/quests`
- Có nút “Xây dựng” để hiện danh sách công trình có thể xây

---

### B. Chiến đấu theo lượt (`/battle`)

- Dạng 1 vs 1, luân phiên
- Kẻ địch xác định qua `battle_enemy` (từ localStorage)
- Gọi API lấy dữ liệu enemy từ JSON

---

### D. Nhiệm vụ (`/quests`) - Protected Route

- Tối đa 5 nhiệm vụ đang hoạt động
- Trạng thái: chưa nhận, đang thực hiện, đã hoàn thành
- Khi thiếu nhiệm vụ, hệ thống tự thêm mới từ file JSON
- Nút “Bắt đầu” sẽ chuyển sang minigame hoặc battle

---

### E. Hội thoại (`/dialog/<id>/<quest_id>`) - Protected Route

- Hiện đoạn thoại tương tác (từng dòng)
- Có 2 loại:
  - Dẫn nhập nhiệm vụ
  - Kết thúc nhiệm vụ, nhận thưởng
- Nội dung lấy từ file `dialogs.json` dựa theo `dialog_id`
- Mỗi dòng có nút **"Tiếp tục"** để chuyển sang dòng kế
- Sau khi kết thúc hội thoại sẽ ảnh hưởng đến nhiệm vụ với `quest_id` tương ứng:
  - Nếu là hội thoại bắt đầu nhiệm vụ → đánh dấu nhiệm vụ là `doing`
  - Nếu là hội thoại kết thúc nhiệm vụ → mở modal phần thưởng, xoá nhiệm vụ khỏi database của user, sau đó redirect về `/town`


---

## 7. Gameplay chính

### 7.1. Cấu trúc file `enemies.json`

(Thư mục ảnh: `static/img/enemies/{enemy_id}_attack_{frame}.png`)

```json
{
  "id": 1023,
  "name": "Troll Rừng",
  "stats": {
    "STR": 15,
    "AGI": 6,
    "INT": 3,
    "VIT": 12,
    "WIS": 5,
    "crit_rate": 0.05
  },
  "skills": [
    { "skill_id": 1001, "priority": 0.7 },
    { "skill_id": 1004, "priority": 0.3 }
  ],
  "drop": [
    { "item_id": 1005, "rate": 0.5 },
    { "item_id": 1006, "rate": 0.2 }
  ],
  "exp_reward": 120
}
```

### Ghi chú:

- `id`: định danh duy nhất của quái, cũng dùng để lấy ảnh hoạt ảnh (`{id}_attack_{frame}.png`)
- `name`: tên hiển thị
- `stats`: chỉ số cơ bản (HP và MP sẽ được tính từ VIT và WIS)
- `skills`: danh sách kỹ năng mà quái sử dụng, kèm `priority` (tỉ lệ ưu tiên dùng skill, tổng cộng không nhất thiết là 1.0)
- `drop`: danh sách item có thể rơi, với `item_id` và `rate` (0.0 → 1.0)
- `exp_reward`: số EXP người chơi nhận được nếu tiêu diệt

---

### 7.2. Cấu trúc file `skills.json`

(Thư mục ảnh: `static/img/icon/skill/{skill_id}.png`)

```json
{
  "skill_id": 1001,
  "name": "Tấn công thường",
  "damage_type": "physical",
  "effect_id": 1
}
```

### Ghi chú:

- `skill_id`: bắt đầu từ 1001, quy ước 1001 là đòn đánh thường
- `name`: tên hiển thị
- `damage_type`: kiểu sát thương (`physical` hoặc `magical`) để quyết định công thức tính damage
- `effect_id`: id của hiệu ứng hiển thị trong trận chiến (ví dụ: hiệu ứng chém, bắn lửa...)
- Không có hình ảnh riêng — icon kỹ năng mặc định là `{skill_id}.png` trong thư mục `skill/`
- Công thức tính damage sẽ được viết riêng trên server tùy theo từng skill

---

### 7.3. Cấu trúc file `items.json`

(Thư mục ảnh: `static/img/icon/item/{item_id}.png`)

```json
{
  "item_id": 1001,
  "name": "Gươm đồng",
  "type": "equipment",
  "price": 120,
  "description": "Một thanh gươm đơn giản làm từ đồng",
  "stat": {
    "STR": 3
  },
  "upgrade_material": [1026, 1030, 1041]
}
```

### Ghi chú:

- `item_id`: số nguyên, bắt đầu từ 1001
- `name`: tên item
- `type`: `equipment` hoặc `material`
- `price`: giá **bán ra**; giá mua được tính là `price + 15%`
- `description`: chú thích ngắn gọn
- `stat`: chỉ có ở item dạng `equipment`, là chỉ số cộng thêm
- `upgrade_material`: danh sách `item_id` dùng để nâng cấp (áp dụng cho equipment)

### Hệ thống inventory:

- Chia làm 2 tab: `equipment` và `material`
- Equipment:
  - Không stack
  - Có chỉ số, có thể nâng cấp
- Material:
  - Stack không giới hạn
  - Dùng để xây dựng, nâng cấp, hoặc làm nhiệm vụ
- Game **không có** item hồi phục hay tiêu dùng → hồi phục sẽ được đảm nhiệm bởi **kỹ năng phép thuật**

---

### 7.4. Cấu trúc file `buildings.json`

(Thư mục ảnh: `static/img/icon/building/{building_id}.png` hoặc `static/img/building/{building_id}.png`)

```json
{
  "building_id": 1001,
  "name": "Tòa thị chính",
  "description": "Nơi nhận nhiệm vụ và điều hành thị trấn.",
  "upgrade_material": {
    "1": {
      "gold": 100,
      "materials": [
        { "item_id": 2001, "quantity": 3 },
        { "item_id": 2002, "quantity": 1 }
      ]
    },
    "2": {
      "gold": 250,
      "materials": [
        { "item_id": 2001, "quantity": 5 },
        { "item_id": 2003, "quantity": 2 }
      ]
    }
  }
}
```

### Ghi chú:

- `building_id`: bắt đầu từ 1001, cũng là tên ảnh đại diện
- `name`: tên công trình
- `description`: mô tả công dụng của công trình
- `upgrade_material`: các nguyên liệu và số vàng cần để xây/lên cấp
  - Key `"1"`, `"2"` là cấp độ (string hoặc số nguyên)
  - `gold`: số vàng cần để nâng cấp
  - `materials`: danh sách nguyên liệu yêu cầu (item_id và quantity)
- **Không có thời gian xây dựng** để đơn giản hóa gameplay


---

### 7.5. Cấu trúc file `quests.json`

(Trang hiển thị: `/quests` – danh sách các nhiệm vụ đang hoạt động hoặc có thể nhận)

```json
{
  "quest_id": "q001",
  "name": "Giải cứu dân làng",
  "description": "Một nhóm quái vật đang đe dọa ngôi làng gần thị trấn. Hãy đánh bại chúng!",
  "background": "forest.jpg",
  "enemy_id": 1023,
  "start_dialog_id": 12,
  "complete_dialog_id": -1,
  "required_items": [],
  "reward": {
    "gold": 300,
    "exp": 150,
    "items": [
        {"item_id": 1031, "quantity": 1 },
        {"item_id": 1025, "quantity": 2 }
    ]
  },
  "level_required": 1
}
```

### Ghi chú:

- `quest_id`: chuỗi định danh nhiệm vụ (dạng `"q001"`)
- `name`: tên nhiệm vụ
- `description`: nội dung mô tả nhiệm vụ, hiển thị ở `/quests`
- `background`: tên file ảnh nền mà trận chiến của nhiệm vụ sẽ sử dụng (nằm trong thư mục `static/img/background/`)
- `enemy_id`: id kẻ địch cần tiêu diệt nếu là nhiệm vụ dạng chiến đấu
- `start_dialog_id`: id hội thoại khởi đầu nhiệm vụ. Nếu là -1 thì không có hội thoại dẫn truyện
- `complete_dialog_id`: id hội thoại khi hoàn thành nhiệm vụ. Nếu là -1 thì không có hội thoại kết thúc
- `required_items`: (tuỳ chọn) danh sách item cần giao nộp để hoàn thành nhiệm vụ (dạng `[{ "item_id": 1008, "quantity": 5 }]`)
- `reward`: phần thưởng khi hoàn thành nhiệm vụ
  - `gold`: số vàng nhận được
  - `exp`: số EXP nhận được
  - `items`: danh sách item nhận được (dạng mảng id)
- `level_required`: cấp độ tối thiểu (tính từ EXP) để hiển thị nhiệm vụ

### Ghi chú thêm:

- Nếu `enemy_id` tồn tại → hệ thống hiểu đây là nhiệm vụ chiến đấu, sẽ lưu `battle_enemy` vào localStorage để chuyển qua `/battle`
- Nếu không có `enemy_id` nhưng có `required_items` → là nhiệm vụ thu thập
- `start_dialog_id` và `end_dialog_id` giúp liên kết với file `dialogs.json` để tạo dẫn truyện mượt mà
- Khi login vào game, hệ thống sẽ tự động thêm nhiệm vụ (nếu user có slot trống), bằng cách chọn ngẫu nhiên từ file `quests.json`

---
### 7.6. Cấu trúc file `dialogs.json`

(Trang hiển thị: `/dialog/<dialog_id>` — hiện đoạn hội thoại tương tác)

```json
{
  "dialog_id": 12,
  "type": "start",
  "background": "village.jpg",
  "lines": [
    { "speaker": "elder", "text": "Có phải bạn là một hiệp sĩ?" },
    { "speaker": "elder", "text": "Hiệp sĩ mau giúp đỡ chúng tôi!" },
    { "speaker": "player", "text": "Tôi sẽ giúp ngôi làng này. Nhưng có chuyện gì vậy" },
    { "speaker": "elder", "text": "Có quái vật xuất hiện ở làng phía đông!" },
    { "speaker": "player", "text": "Tôi sẽ đến đó ngay lập tức!" }
  ]
}
```

### Ghi chú:

- `dialog_id`: số nguyên định danh đoạn hội thoại, liên kết với nhiệm vụ
- `type`: `"start"` hoặc `"end"` — phân biệt hội thoại mở đầu hay kết thúc nhiệm vụ
- `background`: tên file ảnh nền hiển thị trong hội thoại (nằm trong thư mục `static/img/background/`)
- `lines`: mảng các dòng hội thoại
  - `speaker`: tên người nói (có thể là `"hero"` hoặc `"npc"`, `"elder"`, v.v...)
  - `text`: nội dung hiển thị từng câu
- Hình ảnh speaker sẽ được lấy từ thư mục `static/img/npc/` hoặc `static/img/player/` (nếu là nhân vật người chơi)

### Luồng hoạt động:

- Khi user truy cập `/dialog/<id>`, hệ thống load đoạn hội thoại tương ứng từ `dialogs.json`
- Mỗi dòng hiển thị lần lượt, có nút **"Tiếp tục"** để chuyển dòng kế
- Sau khi hội thoại kết thúc:
  - Nếu là `type: "start"` → nhiệm vụ được đánh dấu là `doing`, rồi redirect về `/quests`
  - Nếu là `type: "end"` → mở modal phần thưởng, sau đó redirect về `/town`
---

---

## 8. Cấu trúc thư mục dự án

```
herofate/
├── 📄 Core Application
│   ├── app.py                    # Main Flask application với Flask-Login
│   ├── database.py               # Database abstraction layer  
│   ├── models.py                 # User model cho Flask-Login
│   └── .env                      # Environment configuration
│
├── 📊 Data & Assets
│   ├── data/                     # JSON data files
│   │   ├── enemies.json
│   │   ├── skills.json  
│   │   ├── items.json
│   │   ├── buildings.json
│   │   ├── quests.json
│   │   └── dialogs.json
│   ├── static/                   # Frontend assets
│   │   ├── css/
│   │   │   └── style.css         # Main CSS với responsive design
│   │   ├── js/
│   │   │   └── main.js           # JavaScript với Fetch API
│   │   └── img/
│   │       ├── background/       # Background images
│   │       ├── building/         # Building sprites + ground.png
│   │       ├── icon/             # Icons cho UI
│   │       ├── enemies/          # Enemy sprites
│   │       ├── player/           # Player avatars
│   │       └── npc/              # NPC portraits
│   └── templates/                # Jinja2 templates
│       ├── index.html            # Landing page với auth
│       ├── town.html             # Main game interface
│       ├── battle.html           # Combat interface
│       ├── quests.html           # Quest management
│       └── dialog.html           # Dialog system
│
├── 🔧 Scripts & Utils
│   ├── start.bat                 # Main startup script
│   ├── start_local.bat           # Local development
│   ├── switch_db.bat             # Environment switching
│   ├── migrate_buildings.py      # Database migration
│   └── requirements.txt          # Python dependencies
│
├── 📖 Documentation & Config
│   ├── README.md                 # Project documentation
│   ├── .gitignore               # Git ignore rules
│   └── CLEANUP_SUMMARY.md       # Project cleanup log
│
└── 🗃️ Development
    ├── git-push.bat             # Git automation scripts
    ├── git-start.bat
    └── __pycache__/             # Python cache
```

---

---

## 9. Giao diện & User Experience

### 9.1. Desktop-Only Design
- **Container**: Width 70% tối ưu cho desktop/laptop
- **Grid System**: 3 cột buildings cố định cho màn hình lớn
- **Navigation**: User Info & Navigation tích hợp thành một bar
- **No Mobile Support**: Loại bỏ responsive CSS để tối ưu performance

### 9.2. Enhanced Navigation  
- **Integrated Bar**: User stats + navigation actions trong cùng một component
- **Direct Actions**: Thị trấn, Nhiệm vụ, Chiến đấu, Kho đồ, Đăng xuất
- **Visual Feedback**: Button states và hover effects
- **Streamlined UX**: Loại bỏ Action Buttons duplicate

### 9.3. Visual Elements  
- **Modals**: W3.CSS modal system cho building upgrades
- **Toasts**: Thông báo success/error với animations
- **Loading states**: Visual feedback cho API calls
- **Hover effects**: Smooth transitions và scale effects

### 9.4. Authentication UX
- **Smart redirects**: Tự động điều hướng based on auth status
- **Session persistence**: Maintain login state across browser sessions
- **Error handling**: User-friendly error messages

### 9.5. Mobile Detection & Redirect
- **Auto Detection**: JavaScript kiểm tra device type và screen size
- **Graceful Fallback**: Redirect đến `/not-implemented` với thông báo rõ ràng
- **System Requirements**: Hiển thị yêu cầu hệ thống cho user

---

---

## 10. Cài đặt và triển khai

### 10.1. Yêu cầu hệ thống

**🖥️ Platform Support:**
- **Máy tính để bàn hoặc laptop** (bắt buộc)
- **Độ phân giải tối thiểu**: 1024x768 pixels
- **Trình duyệt**: Chrome, Firefox, Safari, Edge (phiên bản mới)
- **Kết nối internet**: Ổn định cho MongoDB và API calls

**📱 Mobile & Tablet:**
- **Không hỗ trợ**: Game tự động redirect mobile users đến `/not-implemented`
- **Lý do**: Gameplay tối ưu cho mouse/keyboard interaction

### 10.2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

**Dependencies chính:**
- `Flask` - Web framework
- `Flask-Login` - Authentication management  
- `PyMongo` - MongoDB driver
- `python-dotenv` - Environment variables

### 10.3. Cấu hình Database

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

### 10.4. Chuyển đổi giữa Local và Cloud

Sử dụng script `switch_db.bat` để chuyển đổi nhanh:

```bash
switch_db.bat
```

**Lựa chọn:**
- **Option 1**: MongoDB Local (Development) - Khuyến nghị
- **Option 2**: MongoDB Atlas (Production)

### 10.5. Cấu trúc file .env

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

### 10.6. Database Migration

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

## 11. Development Workflow

### 11.1. Local Development
```bash
# Khởi động với MongoDB local
start_local.bat

# Hoặc chạy thủ công
python app.py
```

### 11.2. Production Deployment
```bash
# Chuyển sang Atlas
switch_db.bat

# Chọn option 2 (MongoDB Atlas)
# Cập nhật .env với production settings
```

### 11.3. Project Management
```bash
# Git workflow
git-start.bat    # Initialize git repo
git-push.bat     # Automated commit & push
```

---

---

## 12. Tác giả & License

- Dự án phát triển bởi **Gum Code**
- Phiên bản đầu tiên: Tháng 7 năm 2025
