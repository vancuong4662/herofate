# Hero Fate - Web Game Online

> **📚 Documentation đã được tổ chức lại!** Thay vì một file README dài 1200+ dòng, giờ đây documentation được chia thành các file chuyên biệt trong thư mục `markdown/` để dễ quản lý và tra cứu.

## 🎮 Giới thiệu

**Hero Fate** là một web game online đơn giản, được thiết kế như một dự án học tập để học viên mới bắt đầu học lập trình có thể thực hành theo. Game có lối chơi nhẹ nhàng, gồm hai phần chính: **xây dựng thị trấn** và **chiến đấu theo lượt**.

## 🛠️ Công nghệ chính

- **Backend**: Python + Flask + MongoDB
- **Frontend**: HTML/CSS/JavaScript + Custom GML.js Animation Library
- **Game Engine**: Turn-based combat + Town building mechanics
- **Authentication**: Session-based với Flask-Login

## 📚 Documentation Structure

Toàn bộ documentation đã được tổ chức trong thư mục `markdown/`:

- **[Tổng quan dự án](markdown/01_overview.md)** - Tổng quan, mục tiêu và công nghệ sử dụng
- **[Frontend Architecture](markdown/02_frontend.md)** - UI/UX, routing, animation system và components
- **[Backend & API](markdown/03_backend.md)** - API design, database schema và authentication
- **[Game Mechanics](markdown/04_game_mechanics.md)** - Combat system, quests, buildings và progression
- **[Data Structure](markdown/05_data_structure.md)** - JSON schemas, data models và relationships
- **[Development Guide](markdown/06_development.md)** - Setup, testing, debugging và deployment

## 🚀 Quick Start

1. **Setup Environment**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Application**:
   ```bash
   python app.py
   ```

3. **Access Game**:
   ```
   http://localhost:5000
   ```

## 📖 Đọc thêm

- 📋 [Xem tất cả documentation](markdown/README.md)
- 🔧 [Upgrade Equipment Mechanism](markdown/UPGRADE_MECHANISM.md)
- 🎯 [Development Tools & Scripts](markdown/06_development.md)

---

> **💡 Tip**: Bắt đầu với [Overview](markdown/01_overview.md) để hiểu tổng quan dự án, sau đó đọc theo thứ tự các file documentation khác.
