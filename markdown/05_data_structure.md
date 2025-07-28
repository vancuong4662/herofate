# Data Structure

> Được tách ra từ README.md chính để dễ quản lý và tra cứu

## Cấu trúc Database Users

### MongoDB Schema

```json
{
  "username": "cuongnv",
  "password": "123456",
  "created_at": "2024-01-01T00:00:00Z",
  "gender": "male",
  "buildings": {
    "town_hall": 1,
    "storage": 1,
    "blacksmith": 0,
    "market": 0,
    "mage_tower": 0
  },
  "stats": {
    "level": 1,
    "exp": 0,
    "gold": 1000,
    "reputation": 0,
    "STR": 10,
    "AGI": 10,
    "INT": 10,
    "VIT": 10,
    "WIS": 10
  },
  "equipment": {
    "weapon": null,
    "armor": null,
    "helmet": null,
    "ring": null
  },
  "inventory": [],
  "quests": [],
  "skills": {}
}
```

## Cấu trúc File JSON

### Items (`data/items.json`)

Chứa toàn bộ vật phẩm trong game:

```json
{
  "item_id": "iron-sword",
  "name": "Gươm sắt",
  "type": "equipment",
  "equipment_slot": "weapon",
  "price": 250,
  "description": "Thanh gươm chắc chắn làm từ sắt",
  "level_require": 3,
  "stat": {
    "STR": 6
  },
  "upgrade_material": ["iron", "crystal"]
}
```

**Loại vật phẩm**:
- `material`: Nguyên liệu (wood, stone, iron, diamond, etc.)
- `consumable`: Đồ tiêu hao (banana, chicken, magic-potion, etc.)
- `equipment`: Trang bị (weapon, armor, helmet, ring)

### Equipment (`data/equipment.json`)

Cấu hình hệ thống trang bị:

```json
{
  "equipment_upgrade_rates": {
    "level_multipliers": {
      "1": 1.0, "2": 1.2, "3": 1.5, "4": 1.8, "5": 2.2,
      "6": 2.7, "7": 3.3, "8": 4.0, "9": 4.8, "10": 5.7
    },
    "upgrade_costs": {
      "1": {"gold": 100}, "2": {"gold": 200}, "3": {"gold": 400},
      "4": {"gold": 800}, "5": {"gold": 1600}, "6": {"gold": 3200},
      "7": {"gold": 6400}, "8": {"gold": 12800}, "9": {"gold": 25600},
      "10": {"gold": 51200}
    },
    "upgrade_success_rates": {
      "1": 100, "2": 80, "3": 85, "4": 75, "5": 70,
      "6": 55, "7": 50, "8": 40, "9": 20, "10": 10
    }
  },
  "equipment_slots": {
    "weapon": {"name": "Vũ khí", "description": "Công cụ tấn công chính"},
    "armor": {"name": "Áo giáp", "description": "Bảo vệ thân người"},
    "helmet": {"name": "Mũ", "description": "Bảo vệ đầu khỏi tấn công"},
    "ring": {"name": "Nhẫn", "description": "Phụ kiện tăng cường sức mạnh"}
  }
}
```

### Enemies (`data/enemies.json`)

Dữ liệu quái vật:

```json
{
  "enemy_id": "goblin",
  "name": "Goblin",
  "hp": 50,
  "stats": {
    "STR": 8,
    "AGI": 12,
    "INT": 4,
    "VIT": 6,
    "WIS": 3
  },
  "rewards": {
    "exp": 25,
    "gold": 15,
    "items": [
      {"item_id": "wood", "quantity": 2, "chance": 0.8},
      {"item_id": "iron", "quantity": 1, "chance": 0.3}
    ]
  }
}
```

### Quests (`data/quests.json`)

Cấu trúc nhiệm vụ:

```json
{
  "quest_id": "first_battle",
  "title": "Trận chiến đầu tiên",
  "description": "Hãy chiến đấu với Goblin để bảo vệ thị trấn!",
  "type": "battle",
  "target": "goblin",
  "rewards": {
    "exp": 50,
    "gold": 100,
    "items": [{"item_id": "iron", "quantity": 3}]
  },
  "level_require": 1
}
```

### Buildings (`data/buildings.json`)

Thông tin công trình:

```json
{
  "building_id": "blacksmith",
  "name": "Lò rèn",
  "description": "Nơi để rèn và nâng cấp trang bị",
  "cost": {"gold": 500, "materials": [{"item_id": "iron", "quantity": 10}]},
  "level_require": 3,
  "function": "equipment_upgrade"
}
```

### Dialogs (`data/dialogs.json`)

Hệ thống hội thoại:

```json
{
  "dialog_id": "npc_blacksmith_1",
  "npc_name": "Thợ rèn Garon",
  "content": "Chào mừng đến với lò rèn! Tôi có thể giúp bạn nâng cấp trang bị.",
  "options": [
    {"text": "Nâng cấp trang bị", "action": "open_upgrade"},
    {"text": "Tạm biệt", "action": "close"}
  ]
}
```

## Relationships & References

### Item References
- `upgrade_material` trong items.json phải tham chiếu đến item_id hợp lệ
- `equipment_slot` phải khớp với keys trong equipment_slots
- `type` xác định cách xử lý item (material/consumable/equipment)

### Equipment System
- `level_multipliers`: Nhân stat theo level trang bị
- `upgrade_costs`: Chi phí vàng để upgrade
- `upgrade_success_rates`: Tỷ lệ thành công (giảm dần theo level)
- Nếu upgrade fail → giảm 1 level, vẫn mất vàng và materials

### Quest Flow
- Quest → Dialog → Battle → Rewards
- `target` trong quest phải match với `enemy_id`
- Rewards tự động thêm vào inventory sau khi hoàn thành

### Validation Rules

1. **Item IDs**: Phải unique và sử dụng kebab-case (vd: `iron-sword`)
2. **References**: Tất cả references phải valid (materials, equipment_slots, enemies)
3. **Stats**: Chỉ sử dụng 5 stats chuẩn: STR, AGI, INT, VIT, WIS
4. **Level Requirements**: Phải là số nguyên dương
5. **Prices**: Phải là số nguyên dương

## Migration & Synchronization

Khi có thay đổi data structure:

1. **Items**: Sử dụng script sync để đồng bộ với file hình ảnh
2. **Equipment**: Update migration script cho user data hiện có
3. **Enemies**: Backup trước khi thay đổi stats
4. **Validation**: Chạy test script để verify tính nhất quán

---

> **🔄 Data Sync**: Tất cả item_id phải match với tên file PNG trong `static/img/icon/item/`
