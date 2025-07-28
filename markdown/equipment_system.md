# Equipment System Documentation

## Tổng quan hệ thống
Hệ thống equipment trong HeroFate là một phần quan trọng của gameplay, cho phép người chơi trang bị và nâng cấp vũ khí, giáp để tăng sức mạnh.

## Kiến trúc hệ thống

### 1. Equipment Slots
Người chơi có 4 slot trang bị chính:
- **Helmet** (Mũ): Tăng defense và các stat phụ
- **Armor** (Giáp): Tăng defense và vitality 
- **Weapon** (Vũ khí): Tăng attack và strength
- **Ring** (Nhẫn): Tăng các stat đặc biệt như crit rate

### 2. Equipment Levels
Mỗi equipment có thể được nâng cấp từ level 0 đến level 10:
- **Level 0**: Base stats (không có bonus)
- **Level 1-10**: Stats được nhân với level multipliers

### 3. Level Multipliers
```javascript
const levelMultipliers = {
  "0": 1.0,   // Không có bonus
  "1": 1.0,   // Không có bonus
  "2": 1.2,   // +20% stats
  "3": 1.5,   // +50% stats
  "4": 1.8,   // +80% stats
  "5": 2.2,   // +120% stats
  "6": 2.7,   // +170% stats
  "7": 3.3,   // +230% stats
  "8": 4.0,   // +300% stats
  "9": 4.8,   // +380% stats
  "10": 5.7   // +470% stats
};
```

## Data Structure

### Equipment trong User Data
```javascript
userData.equipment = {
  "helmet": {
    "item_id": "iron_helmet",
    "level": 3
  },
  "armor": {
    "item_id": "iron_armor", 
    "level": 2
  },
  "weapon": {
    "item_id": "iron_sword",
    "level": 5
  },
  "ring": null
};
```

### Equipment Item Definition
```javascript
// Từ items.json
{
  "item_id": "iron_sword",
  "name": "Iron Sword",
  "type": "equipment",
  "equipment_slot": "weapon",
  "stat": {
    "STR": 8,
    "crit_rate": 0.05
  },
  "level_require": 5,
  "price": 100,
  "description": "A sturdy iron sword"
}
```

## API Endpoints

### 1. Get Equipment Status
```
GET /api/equipment
Headers: X-Username: player_username

Response:
{
  "success": true,
  "equipment": {
    "helmet": {"item_id": "iron_helmet", "level": 3},
    "armor": null,
    "weapon": {"item_id": "iron_sword", "level": 2},
    "ring": null
  },
  "equipped_items": {
    "helmet": {"item_id": "iron_helmet", "name": "Iron Helmet", ...},
    "weapon": {"item_id": "iron_sword", "name": "Iron Sword", ...}
  },
  "total_stats": {
    "STR": 12,
    "AGI": 5,
    "crit_rate": 0.08
  },
  "equipment_config": {
    "level_multipliers": {...}
  }
}
```

### 2. Equip Item
```
POST /api/equipment/equip
Body: {"item_id": "iron_sword"}

Response:
{
  "success": true,
  "message": "Đã trang bị Iron Sword",
  "equipment": {...},
  "inventory": [...]
}
```

### 3. Unequip Item
```
POST /api/equipment/unequip  
Body: {"slot": "weapon"}

Response:
{
  "success": true,
  "message": "Đã gỡ trang bị Iron Sword",
  "equipment": {...},
  "inventory": [...]
}
```

## Frontend Implementation

### 1. Equipment Configuration Loading
```javascript
// Load equipment config từ server
async function loadEquipmentConfig() {
  try {
    const response = await apiCall('/api/equipment');
    if (response.success && response.equipment_config) {
      equipmentMultipliers = {
        "0": 1.0,
        ...response.equipment_config.level_multipliers
      };
    }
  } catch (error) {
    console.warn('Could not load equipment config, using defaults');
  }
}
```

### 2. Stat Calculation với Level Multipliers
```javascript
function getLevelMultiplier(level) {
  return equipmentMultipliers[level.toString()] || 1.0;
}

// Tính toán final stats
function calculateEquipmentStats(baseStats, equipmentLevel) {
  const multiplier = getLevelMultiplier(equipmentLevel);
  const finalStats = {};
  
  Object.entries(baseStats).forEach(([key, value]) => {
    if (key === 'crit_rate') {
      // Crit rate tính theo phần trăm
      finalStats[key] = value * multiplier;
    } else {
      // Các stat khác làm tròn
      finalStats[key] = Math.round(value * multiplier);
    }
  });
  
  return finalStats;
}
```

### 3. UI Display Logic

#### Equipment Slots Display
```javascript
async function updateEquipmentDisplay(equipmentData) {
  const slots = ['helmet', 'armor', 'weapon', 'ring'];
  
  slots.forEach(slot => {
    const slotElement = document.getElementById(`equipmentSlot-${slot}`);
    const equipment = equipmentData.equipment[slot];
    const equippedItem = equipmentData.equipped_items[slot];
    
    if (equipment && equippedItem) {
      // Item được trang bị
      slotElement.classList.add('equipped');
      
      // Hiển thị level bằng stars
      if (equipment.level > 0) {
        let levelHtml = '';
        for (let i = 0; i < Math.min(equipment.level, 3); i++) {
          levelHtml += '⭐';
        }
        if (equipment.level > 3) {
          levelHtml += `+${equipment.level - 3}`;
        }
        levelElement.innerHTML = levelHtml;
      }
    } else {
      // Slot trống
      slotElement.classList.remove('equipped');
      iconElement.src = '/static/img/icon/item/cube.png';
      nameElement.textContent = 'Trống';
    }
  });
}
```

#### Inventory Equipment Display
```javascript
// Hiển thị level stars trong inventory slots
if (itemData.type === 'equipment') {
  let currentLevel = item.level || 0;
  
  // Kiểm tra nếu item đang được equip
  if (currentLevel === 0) {
    const equipmentSlot = itemData.equipment_slot;
    const equipmentData = userData.equipment && userData.equipment[equipmentSlot];
    if (equipmentData && equipmentData.item_id === item.item_id) {
      currentLevel = equipmentData.level || 0;
    }
  }
  
  if (currentLevel > 0) {
    levelIndicator = `<div class="item-level-stars">`;
    levelIndicator += `<span>${currentLevel}</span>`;
    levelIndicator += `<img src="/static/img/icon/info/star.png" style="width: 10px; height: 10px;">`;
    levelIndicator += '</div>';
  }
}
```

#### Item Detail với Upgraded Stats
```javascript
function updateItemDetail(itemData, selectedItemId = null) {
  if (itemData.type === 'equipment') {
    // Lấy level của equipment
    const userData = getUserData();
    let currentLevel = 0;
    
    // Priority: selected item > equipped item
    if (selectedItemId) {
      const inventory = userData.inventory || [];
      const inventoryItem = inventory.find(item => item.item_id === selectedItemId);
      if (inventoryItem && inventoryItem.level !== undefined) {
        currentLevel = inventoryItem.level;
      } else {
        // Kiểm tra nếu đang được equip
        const equipmentSlot = itemData.equipment_slot;
        const equipmentData = userData.equipment && userData.equipment[equipmentSlot];
        if (equipmentData && equipmentData.item_id === selectedItemId) {
          currentLevel = equipmentData.level || 0;
        }
      }
    }
    
    // Hiển thị stats với level multipliers
    if (itemData.stat && Object.keys(itemData.stat).length > 0) {
      const levelMultiplier = getLevelMultiplier(currentLevel);
      
      Object.entries(itemData.stat).forEach(([key, value]) => {
        let displayValue = value;
        
        if (currentLevel > 0) {
          displayValue = Math.round(value * levelMultiplier);
        }
        
        if (key === 'crit_rate') {
          const basePercent = Math.round(value * 100);
          const upgradePercent = Math.round(displayValue * 100);
          displayValue = upgradePercent + '%';
          
          if (currentLevel > 0 && upgradePercent > basePercent) {
            displayValue += ` <span style="color: #27ae60;">(+${upgradePercent - basePercent}%)</span>`;
          }
        } else {
          if (currentLevel > 0 && displayValue > value) {
            displayValue = `${displayValue} <span style="color: #27ae60;">(+${displayValue - value})</span>`;
          } else {
            displayValue = '+' + displayValue;
          }
        }
      });
    }
  }
}
```

## Equipment Actions

### 1. Equip Equipment
```javascript
async function useSelectedItem() {
  if (currentTab === 'equipment') {
    try {
      const response = await apiCall('/api/equipment/equip', 'POST', {
        item_id: selectedItem
      });
      
      if (response.success) {
        // Update user data với equipment mới
        const userData = getUserData();
        userData.equipment = response.equipment;
        userData.inventory = response.inventory;
        updateUserData(userData);
        
        // Update UI
        updateUserInfoDisplay(userData);
        
        // Chuyển sang player info modal để xem equipment
        document.getElementById('inventoryModal').style.display = 'none';
        setTimeout(async () => {
          await showPlayerInfo();
        }, 200);
      }
    } catch (error) {
      console.error('Error equipping item:', error);
      showToast('Lỗi khi trang bị item', 'error');
    }
  }
}
```

### 2. Unequip Equipment
```javascript
async function unequipItem(slot) {
  const userData = getUserData();
  const equipment = userData.equipment || {};
  
  if (!equipment[slot]) {
    showToast('Không có trang bị nào trong slot này', 'info');
    return;
  }
  
  try {
    const response = await apiCall('/api/equipment/unequip', 'POST', {
      slot: slot
    });
    
    if (response.success) {
      // Update user data
      userData.equipment = response.equipment;
      userData.inventory = response.inventory;
      updateUserData(userData);
      
      // Chuyển sang inventory modal để xem item đã unequip
      document.getElementById('playerInfoModal').style.display = 'none';
      
      setTimeout(async () => {
        // Fetch fresh inventory data
        const freshResponse = await fetch('/api/user/inventory', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'X-Username': userData.username
          }
        });
        const freshData = await freshResponse.json();
        
        if (freshData.success) {
          const currentUserData = getUserData();
          currentUserData.inventory = freshData.inventory;
          updateUserData(currentUserData);
        }
        
        // Show inventory với equipment tab
        const modal = document.getElementById('inventoryModal');
        modal.style.display = 'block';
        await showInventoryTab('equipment');
      }, 200);
    }
  } catch (error) {
    console.error('Error unequipping item:', error);
    showToast('Lỗi khi gỡ trang bị', 'error');
  }
}
```

## Stat System Integration

### 1. Player Stats Calculation
```javascript
async function updateStatsWithEquipment(userData, equipmentData) {
  const baseStats = userData.stats || {};
  const equipmentStats = equipmentData.total_stats || {};
  
  // Tính final stats (base + equipment)
  const finalStats = {
    STR: (baseStats.STR || 10) + (equipmentStats.STR || 0),
    AGI: (baseStats.AGI || 10) + (equipmentStats.AGI || 0),
    INT: (baseStats.INT || 10) + (equipmentStats.INT || 0),
    VIT: (baseStats.VIT || 10) + (equipmentStats.VIT || 0),
    WIS: (baseStats.WIS || 10) + (equipmentStats.WIS || 0),
    crit_rate: (baseStats.crit_rate || 0.05) + (equipmentStats.crit_rate || 0)
  };
  
  updateStatsDisplay(finalStats, baseStats, equipmentStats);
}
```

### 2. Stats Display với Equipment Bonus
```javascript
function formatStatValue(statKey, finalValue, baseStats, equipmentStats) {
  if (!baseStats || !equipmentStats) {
    return finalValue;
  }
  
  const baseValue = baseStats[statKey] || (statKey === 'crit_rate' ? 0.05 : 10);
  const equipValue = equipmentStats[statKey] || 0;
  
  if (equipValue > 0) {
    if (statKey === 'crit_rate') {
      const baseCrit = Math.round(baseValue * 100);
      const equipCrit = Math.round(equipValue * 100);
      return `${baseCrit + equipCrit}% <span style="color: #27ae60;">(+${equipCrit}%)</span>`;
    } else {
      return `${finalValue} <span style="color: #27ae60;">(+${equipValue})</span>`;
    }
  }
  
  return finalValue;
}
```

## LocalStorage Data Management

### 1. Data Consistency
```javascript
// Luôn sử dụng getUserData() để lấy data fresh
function getUserData() {
  const userData = localStorage.getItem('user_data');
  return userData ? JSON.parse(userData) : null;
}

// Luôn sử dụng updateUserData() để lưu data
function updateUserData(newData) {
  localStorage.setItem('user_data', JSON.stringify(newData));
}
```

### 2. Fresh Data Policy
- **Inventory modal**: Luôn fetch fresh data từ server trước khi mở
- **Equipment actions**: Update localStorage ngay sau khi API success
- **UI updates**: Re-render sau mỗi equipment change

## Error Handling

### 1. API Error Handling
```javascript
try {
  const response = await apiCall('/api/equipment/equip', 'POST', data);
  if (response.success) {
    // Success handling
  } else {
    showToast(response.message, 'error');
  }
} catch (error) {
  console.error('Error equipping item:', error);
  showToast('Lỗi khi trang bị item', 'error');
}
```

### 2. Fallback Mechanisms
- **Equipment config**: Sử dụng default multipliers nếu load failed
- **Icons**: Fallback to cube.png nếu item icon không load được
- **Stats**: Hiển thị base stats nếu không có equipment data

## Performance Considerations

### 1. API Optimization
- **Equipment config**: Load một lần khi page load
- **Inventory data**: Chỉ fetch khi cần thiết
- **Stat calculation**: Cache results cho cùng một level

### 2. DOM Optimization
- **Grid rendering**: Clear và re-render thay vì update từng slot
- **Event handlers**: Sử dụng event delegation
- **Image loading**: Lazy loading cho item icons

## Future Enhancements

### 1. Equipment Upgrade System
- **Materials requirement**: Cần materials để upgrade level
- **Success rate**: Có thể fail khi upgrade high level
- **Destruction**: Risk of losing equipment khi upgrade fail

### 2. Equipment Sets
- **Set bonuses**: Bonus khi equip full set
- **Set effects**: Special abilities khi có set bonus

### 3. Equipment Enhancement
- **Enchantments**: Thêm special effects
- **Gems/Stones**: Socket system để enhance stats
- **Reforging**: Change stat distribution

---

> **🎮 Equipment System**: Complete documentation của hệ thống equipment với level multipliers, star display, và full UI/UX integration.
