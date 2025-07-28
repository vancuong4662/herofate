# Cơ Chế Upgrade Equipment Mới

## Tổng quan
Hệ thống upgrade equipment đã được cải tiến với cơ chế rủi ro và phần thưởng cân bằng hơn.

## Cấu trúc dữ liệu mới

### 1. Chi phí upgrade (`upgrade_costs`)
Chỉ tính bằng vàng, đơn giản hóa việc tính toán:
- Level 1: 100 vàng
- Level 2: 200 vàng  
- Level 3: 400 vàng
- Level 4: 800 vàng
- Level 5: 1,600 vàng
- Level 6: 3,200 vàng
- Level 7: 6,400 vàng
- Level 8: 12,800 vàng
- Level 9: 25,600 vàng
- Level 10: 51,200 vàng

### 2. Nguyên liệu upgrade
- Lấy từ trường `upgrade_material` của từng item equipment
- Mỗi item có nguyên liệu riêng phù hợp với độ hiếm và cấp độ
- VD: `bronze-sword` cần `["iron", "coal"]`, `phoenix-sword` cần `["diamond", "crystal"]`

### 3. Tỷ lệ thành công (`upgrade_success_rates`)
Tỷ lệ giảm dần theo level để tạo thử thách:
- Level 1: 100% (luôn thành công)
- Level 2: 80%
- Level 3: 85%
- Level 4: 75%
- Level 5: 70%
- Level 6: 55%
- Level 7: 50%
- Level 8: 40%
- Level 9: 20%
- Level 10: 10%

## Cơ chế hoạt động

### Khi upgrade thành công:
1. ✅ Item tăng 1 level
2. ✅ Stat được nhân với level multiplier tương ứng
3. 💰 Trừ vàng theo `upgrade_costs`
4. 🔧 Trừ nguyên liệu theo `upgrade_material` của item

### Khi upgrade thất bại:
1. ❌ Item giảm 1 level (trừ khi đang ở level 0)
2. 💰 Vẫn trừ vàng (chi phí thử nghiệm)
3. 🔧 Vẫn trừ nguyên liệu (vật liệu bị hư hỏng)

### Ví dụ cụ thể:
**Item**: `iron-sword` (Level 2) muốn upgrade lên Level 3
- **Chi phí**: 400 vàng
- **Nguyên liệu**: iron, crystal (từ `upgrade_material` của `iron-sword`)
- **Tỷ lệ thành công**: 85%
- **Nếu thành công**: Level 3, stat x1.5
- **Nếu thất bại**: Level 1, mất vàng và nguyên liệu

## Logic implementation

```javascript
function upgradeEquipment(player, itemId, currentLevel) {
    const item = getItemById(itemId);
    const nextLevel = currentLevel + 1;
    
    // Kiểm tra điều kiện
    const goldCost = equipment.upgrade_costs[nextLevel].gold;
    const materials = item.upgrade_material;
    const successRate = equipment.upgrade_success_rates[nextLevel];
    
    if (!canAffordUpgrade(player, goldCost, materials)) {
        return { success: false, message: "Không đủ tài nguyên" };
    }
    
    // Trừ tài nguyên trước
    player.gold -= goldCost;
    removeMaterials(player, materials);
    
    // Random thành công/thất bại
    const random = Math.random() * 100;
    
    if (random <= successRate) {
        // Thành công
        return {
            success: true,
            newLevel: nextLevel,
            message: `Upgrade thành công! ${item.name} đã đạt Level ${nextLevel}`
        };
    } else {
        // Thất bại
        const newLevel = Math.max(0, currentLevel - 1);
        return {
            success: false,
            newLevel: newLevel,
            message: `Upgrade thất bại! ${item.name} giảm xuống Level ${newLevel}`
        };
    }
}
```

## Ưu điểm của cơ chế mới

1. **Đơn giản hóa**: Không cần quản lý materials phức tạp trong equipment.json
2. **Linh hoạt**: Mỗi item có nguyên liệu riêng phù hợp với tính chất
3. **Cân bằng**: Tỷ lệ thành công giảm dần tạo thử thách
4. **Rủi ro**: Penalty khi thất bại khuyến khích người chơi cân nhắc
5. **Nhất quán**: Sử dụng dữ liệu có sẵn trong items.json

## Cân bằng game

- **Level thấp (1-4)**: Tỷ lệ cao, ít rủi ro, khuyến khích thử nghiệm
- **Level trung (5-7)**: Cân bằng risk/reward
- **Level cao (8-10)**: Rủi ro cao, chỉ dành cho người chơi giàu có và dám mạo hiểm
