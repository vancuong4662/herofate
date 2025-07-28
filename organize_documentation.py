#!/usr/bin/env python3
"""
Script tách README.md thành các file markdown con
"""

import os
import re

def extract_sections_from_readme():
    """Đọc README.md và tách thành các sections"""
    
    if not os.path.exists('README.md'):
        print("❌ Không tìm thấy README.md")
        return
    
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Tạo thư mục markdown nếu chưa có
    os.makedirs('markdown', exist_ok=True)
    
    sections = {
        'overview': {
            'title': 'Tổng quan dự án',
            'file': 'markdown/01_overview.md',
            'keywords': ['giới thiệu', 'mục tiêu', 'công nghệ', 'cấu trúc']
        },
        'frontend': {
            'title': 'Frontend Architecture',
            'file': 'markdown/02_frontend.md', 
            'keywords': ['frontend', 'navigation', 'routes', 'ui', 'gml.js', 'animation']
        },
        'backend': {
            'title': 'Backend & API',
            'file': 'markdown/03_backend.md',
            'keywords': ['backend', 'api', 'database', 'flask', 'mongodb']
        },
        'game_mechanics': {
            'title': 'Game Mechanics',
            'file': 'markdown/04_game_mechanics.md',
            'keywords': ['chiến đấu', 'battle', 'quest', 'building', 'equipment', 'stats']
        },
        'data_structure': {
            'title': 'Data Structure',
            'file': 'markdown/05_data_structure.md',
            'keywords': ['json', 'items', 'enemies', 'dialogs', 'buildings']
        },
        'development': {
            'title': 'Development Guide',
            'file': 'markdown/06_development.md',
            'keywords': ['setup', 'installation', 'testing', 'debugging']
        }
    }
    
    # Chia nội dung theo header level
    lines = content.split('\n')
    current_section = []
    all_sections = []
    current_header = ""
    
    for line in lines:
        if line.startswith('# ') or line.startswith('## '):
            if current_section:
                all_sections.append({
                    'header': current_header,
                    'content': '\n'.join(current_section)
                })
                current_section = []
            current_header = line
        current_section.append(line)
    
    # Thêm section cuối
    if current_section:
        all_sections.append({
            'header': current_header,
            'content': '\n'.join(current_section)
        })
    
    return all_sections

def categorize_section(header, content, categories):
    """Phân loại section vào category phù hợp"""
    header_lower = header.lower()
    content_lower = content.lower()
    
    scores = {}
    for cat_name, cat_info in categories.items():
        score = 0
        for keyword in cat_info['keywords']:
            score += header_lower.count(keyword) * 3  # Header quan trọng hơn
            score += content_lower.count(keyword)
        scores[cat_name] = score
    
    # Trả về category có điểm cao nhất
    if max(scores.values()) > 0:
        return max(scores, key=scores.get)
    else:
        return 'overview'  # Default

def create_documentation_structure():
    """Tạo cấu trúc documentation mới"""
    
    print("📚 TÁCH README.MD THÀNH CÁC FILE DOCUMENTATION")
    print("=" * 60)
    
    # Đọc và phân tích README
    sections = extract_sections_from_readme()
    if not sections:
        return
    
    # Định nghĩa categories
    categories = {
        'overview': {
            'title': 'Tổng quan dự án',
            'file': 'markdown/01_overview.md',
            'keywords': ['giới thiệu', 'mục tiêu', 'công nghệ', 'fullstack', 'học tập'],
            'sections': []
        },
        'frontend': {
            'title': 'Frontend Architecture', 
            'file': 'markdown/02_frontend.md',
            'keywords': ['frontend', 'navigation', 'routes', 'ui', 'gml.js', 'animation', 'canvas', 'modal'],
            'sections': []
        },
        'backend': {
            'title': 'Backend & API',
            'file': 'markdown/03_backend.md', 
            'keywords': ['backend', 'api', 'flask', 'mongodb', 'database', 'session', 'auth'],
            'sections': []
        },
        'game_mechanics': {
            'title': 'Game Mechanics',
            'file': 'markdown/04_game_mechanics.md',
            'keywords': ['chiến đấu', 'battle', 'quest', 'building', 'equipment', 'stats', 'level', 'exp'],
            'sections': []
        },
        'data_structure': {
            'title': 'Data Structure', 
            'file': 'markdown/05_data_structure.md',
            'keywords': ['json', 'items', 'enemies', 'dialogs', 'buildings', 'skills', 'cấu trúc', 'dữ liệu'],
            'sections': []
        },
        'development': {
            'title': 'Development Guide',
            'file': 'markdown/06_development.md',
            'keywords': ['setup', 'installation', 'testing', 'debug', 'development', 'deploy', 'cài đặt'],
            'sections': []
        }
    }
    
    # Phân loại sections
    for section in sections:
        if not section['header']:
            continue
            
        category = categorize_section(section['header'], section['content'], categories)
        categories[category]['sections'].append(section)
        
        print(f"📄 {section['header'][:50]}... → {categories[category]['title']}")
    
    # Tạo các file documentation
    for cat_name, cat_info in categories.items():
        if not cat_info['sections']:
            continue
            
        content = f"# {cat_info['title']}\n\n"
        content += f"> Được tách ra từ README.md chính để dễ quản lý và tra cứu\n\n"
        
        for section in cat_info['sections']:
            content += section['content'] + '\n\n'
        
        # Ghi file
        with open(cat_info['file'], 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Tạo {cat_info['file']} ({len(cat_info['sections'])} sections)")
    
    # Tạo README mới ngắn gọn
    create_new_readme(categories)
    
    # Tạo index file
    create_index_file(categories)

def create_new_readme(categories):
    """Tạo README.md mới ngắn gọn"""
    
    new_readme = """# Hero Fate - Web Game Online

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

"""
    
    for i, (cat_name, cat_info) in enumerate(categories.items(), 1):
        file_name = cat_info['file'].replace('markdown/', '')
        new_readme += f"- **[{cat_info['title']}]({cat_info['file']})** - {get_category_description(cat_name)}\n"
    
    new_readme += """
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
"""
    
    # Backup README cũ
    os.rename('README.md', 'README.md.backup')
    
    # Ghi README mới
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_readme)
    
    print(f"✅ Tạo README.md mới (ngắn gọn)")
    print(f"📦 Backup README cũ: README.md.backup")

def get_category_description(cat_name):
    """Lấy mô tả ngắn cho từng category"""
    descriptions = {
        'overview': 'Tổng quan, mục tiêu và công nghệ sử dụng',
        'frontend': 'UI/UX, routing, animation system và components',
        'backend': 'API design, database schema và authentication',
        'game_mechanics': 'Combat system, quests, buildings và progression',
        'data_structure': 'JSON schemas, data models và relationships',
        'development': 'Setup, testing, debugging và deployment'
    }
    return descriptions.get(cat_name, 'Documentation')

def create_index_file(categories):
    """Tạo file index cho thư mục markdown"""
    
    index_content = """# Documentation Index

> Tổng hợp toàn bộ documentation của Hero Fate Web Game

## 📑 Danh sách Documentation

"""
    
    for i, (cat_name, cat_info) in enumerate(categories.items(), 1):
        file_name = cat_info['file'].replace('markdown/', '')
        index_content += f"### {i}. [{cat_info['title']}]({file_name})\n"
        index_content += f"{get_category_description(cat_name)}\n\n"
    
    index_content += """## 🔧 Tools & Utilities

- **[Upgrade Mechanism](UPGRADE_MECHANISM.md)** - Equipment upgrade system
- **[Background Removal](BACKGROUND_REMOVAL_README.md)** - AI-powered background removal tool  
- **[Sync Underscore](SYNC_UNDERSCORE_README.md)** - Đồng bộ naming convention

## 📝 Development Notes

- Tất cả file documentation được tạo tự động từ README.md gốc
- Mỗi file tập trung vào một khía cạnh cụ thể của dự án
- Cấu trúc được thiết kế để dễ maintain và mở rộng

---

> **🔄 Last Updated**: Được tạo tự động từ script `organize_documentation.py`
"""
    
    with open('markdown/README.md', 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"✅ Tạo markdown/README.md (index file)")

def main():
    """Hàm main"""
    print("📚 TOOL TỔ CHỨC LẠI DOCUMENTATION")
    print("=" * 60)
    
    if not os.path.exists('README.md'):
        print("❌ Không tìm thấy README.md")
        return
    
    create_documentation_structure()
    
    print("\n" + "=" * 60)
    print("🎉 Hoàn thành tổ chức lại documentation!")
    print("\n📋 Kết quả:")
    print("- README.md mới: Ngắn gọn, dễ đọc")
    print("- README.md.backup: Backup file gốc")
    print("- markdown/: Thư mục chứa documentation chi tiết")
    print("- markdown/README.md: Index file")
    
if __name__ == "__main__":
    main()
