# Frontend Architecture

> Được tách ra từ README.md chính để dễ quản lý và tra cứu

## 1. Giới thiệu chung

**Hero Fate** là một web game online đơn giản, được thiết kế như một dự án học tập để học viên mới bắt đầu học lập trình có thể thực hành theo. Game có lối chơi nhẹ nhàng, gồm hai phần chính: **xây dựng thị trấn** và **chiến đấu theo lượt (turn-based)**.

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


## 4. Frontend Libraries & Animation System

### 4.1. GML.js - Game Maker Language JavaScript
**GML.js** là thư viện sprite animation tự phát triển, lấy cảm hứng từ GameMaker Studio:

```javascript
// Tạo sprite với 4 frames animation
const playerSprite = spriteCreate(
    '/static/img/player/male_idle.png', 
    128,    // sprite width
    128,    // sprite height  
    4,      // number of frames
    64,     // origin x
    64      // origin y
);

// Tạo instance của sprite
const playerInstance = instCreate(x, y, 0, playerSprite);
playerInstance.imageSpeed = 0.15;  // Animation speed
playerInstance.imageLoop = true;   // Loop animation
```

**Tính năng chính:**
- **Sprite Management**: Load và quản lý sprite sheets
- **Frame Animation**: Hỗ trợ multi-frame animation với tốc độ có thể điều chỉnh
- **Instance System**: Tạo và quản lý multiple instances của cùng một sprite
- **Canvas Rendering**: Render sprites lên HTML5 Canvas
- **Performance Optimized**: Chỉ render khi cần thiết

### 4.2. Support.js - Utility Functions
**Support.js** chứa các helper functions và utilities:

```javascript
// Toast notification system
showToast(message, type);  // 'success', 'error', 'warning', 'info'

// API call wrapper với error handling
apiCall(endpoint, options);

// User data management
getUserData();
updateUserInfoDisplay(userData);

// Level calculation từ EXP
calculateLevel(exp);

// Modal management
closeModal();
```

**Chức năng chính:**
- **Toast System**: Thông báo user-friendly
- **API Wrapper**: Xử lý HTTP requests với error handling
- **Data Management**: LocalStorage và session management  
- **UI Utilities**: Modal controls, form validation
- **Game Logic**: Level calculation, stat management

### 4.3. Player Animation Integration
```javascript
// Animation control functions
setAnimationSpeed(speed);        // 0.05 - 0.3
setAnimationPreset(preset);      // 'slow', 'normal', 'fast'
getAnimationSpeed();             // Get current speed
startPlayerAnimation();          // Start animation
stopPlayerAnimation();           // Stop animation

// Configuration object
const ANIMATION_CONFIG = {
    FRAME_SPEED: 0.1,
    FRAME_COUNT: 4,
    CANVAS_SIZE: 128,
    SPRITE_SIZE: 128,
    AUTO_START: false
};
```

---


## 5. Modal System & UI Standards

### 5.1. Modal Structure Standards
Tất cả modals trong game tuân theo cấu trúc 3 phần chuẩn:

```html
<div id="modalName" class="modal">
    <div class="modal-content">
        <!-- Modal Header -->
        <div class="modal-header">
            <h2 class="modal-title">
                <i class="fas fa-icon"></i> Tiêu đề Modal
            </h2>
            <button class="modal-close" onclick="closeModal()">
                <i class="fas fa-times"></i>
            </button>
        </div>
        
        <!-- Modal Body -->
        <div class="modal-body">
            <!-- Nội dung chính của modal -->
        </div>
        
        <!-- Modal Footer -->
        <div class="modal-footer">
            <button class="btn btn-primary">Hành động chính</button>
            <button class="btn btn-secondary" onclick="closeModal()">Đóng</button>
        </div>
    </div>
</div>
```

### 5.2. Modal Sizing Standards
```css
/* Standard modal */
.modal-content {
    max-width: 700px;
    width: 85%;
}

/* Large modal (cho inventory, player info) */
.inventory-modal .modal-content {
    max-width: 900px;
    width: 95%;
}

/* Player info modal */
.player-info-modal {
    max-width: 750px;
    width: 90%;
}
```

### 5.3. Button Consistency
```css
/* Modal footer buttons luôn được căn giữa và có khoảng cách đều */
.modal-footer {
    display: flex;
    justify-content: center;
    gap: var(--spacing-md);
}

/* Button styling standards */
.btn-primary {
    background: var(--primary-color);
}

.btn-secondary {
    background: var(--primary-color-light);
}
```

---


## 8. UI/UX Improvements

### 8.1. Visual Design
- **Header**: Background image từ `static/img/background/1.jpg`
- **Building System**: 
  - Hình ảnh building từ `static/img/building/{building_id}.png`
  - Ground texture: `static/img/building/ground.png`
  - Building images được scale 2x để nổi bật
- **Visual States**: 
  - Đã xây: Màu bình thường + level badge xanh
  - Chưa xây: Grayscale filter + level badge đỏ

### 8.2. Desktop-Only Experience
- **Platform Support**: Chỉ hỗ trợ máy tính để bàn và laptop
- **Screen Requirements**: Độ phân giải tối thiểu 1024x768
- **Mobile Detection**: Tự động redirect thiết bị mobile đến `/not-implemented`
- **Optimized Layout**: 3 cột buildings được tối ưu cho màn hình lớn

### 8.3. Mobile Not Supported
- **Auto Detection**: JavaScript kiểm tra User Agent và screen size
- **Redirect Logic**: Mobile users → `/not-implemented` page
- **Clear Messaging**: Thông báo rõ ràng về yêu cầu hệ thống
- **No Responsive CSS**: Đã loại bỏ toàn bộ mobile responsive để tối ưu performance

---


## 12. Giao diện & User Experience

### 12.1. Desktop-Only Design
- **Container**: Width 70% tối ưu cho desktop/laptop
- **Grid System**: 3 cột buildings cố định cho màn hình lớn
- **Navigation**: User Info & Navigation tích hợp thành một bar
- **No Mobile Support**: Loại bỏ responsive CSS để tối ưu performance

### 12.2. Enhanced Navigation  
- **Integrated Bar**: User stats + navigation actions trong cùng một component
- **Direct Actions**: Thị trấn, Nhiệm vụ, Chiến đấu, Kho đồ, Đăng xuất
- **Visual Feedback**: Button states và hover effects
- **Streamlined UX**: Loại bỏ Action Buttons duplicate

### 12.3. Visual Elements  
- **Modals**: W3.CSS modal system cho building upgrades
- **Toasts**: Thông báo success/error với animations
- **Loading states**: Visual feedback cho API calls
- **Hover effects**: Smooth transitions và scale effects

### 12.4. Authentication UX
- **Smart redirects**: Tự động điều hướng based on auth status
- **Session persistence**: Maintain login state across browser sessions
- **Error handling**: User-friendly error messages

### 12.5. Mobile Detection & Redirect
- **Auto Detection**: JavaScript kiểm tra device type và screen size
- **Graceful Fallback**: Redirect đến `/not-implemented` với thông báo rõ ràng
- **System Requirements**: Hiển thị yêu cầu hệ thống cho user

---

---


