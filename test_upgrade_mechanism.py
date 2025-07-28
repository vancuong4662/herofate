#!/usr/bin/env python3
"""
Tool kiểm tra và mô phỏng cơ chế upgrade equipment mới
"""

import json
import random
import os

def load_data():
    """Load dữ liệu từ các file JSON"""
    try:
        with open('data/equipment.json', 'r', encoding='utf-8') as f:
            equipment_data = json.load(f)
        
        with open('data/items.json', 'r', encoding='utf-8') as f:
            items_data = json.load(f)
        
        return equipment_data, items_data
    except Exception as e:
        print(f"❌ Lỗi đọc file: {e}")
        return None, None

def get_equipment_items(items_data):
    """Lấy danh sách tất cả equipment items"""
    equipment_items = []
    for item in items_data:
        if item.get('type') == 'equipment':
            equipment_items.append(item)
    return equipment_items

def simulate_upgrade(item, current_level, equipment_data):
    """Mô phỏng quá trình upgrade"""
    if current_level >= 10:
        return {
            'success': False,
            'message': 'Đã đạt level tối đa',
            'new_level': current_level
        }
    
    next_level = current_level + 1
    
    # Lấy thông tin upgrade
    gold_cost = equipment_data['equipment_upgrade_rates']['upgrade_costs'][str(next_level)]['gold']
    success_rate = equipment_data['equipment_upgrade_rates']['upgrade_success_rates'][str(next_level)]
    materials = item.get('upgrade_material', [])
    
    # Random thành công/thất bại
    random_roll = random.randint(1, 100)
    success = random_roll <= success_rate
    
    if success:
        new_level = next_level
        multiplier = equipment_data['equipment_upgrade_rates']['level_multipliers'][str(new_level)]
        message = f"✅ THÀNH CÔNG! {item['name']} lên Level {new_level} (x{multiplier})"
    else:
        new_level = max(0, current_level - 1)
        message = f"❌ THẤT BẠI! {item['name']} giảm xuống Level {new_level}"
    
    return {
        'success': success,
        'new_level': new_level,
        'gold_cost': gold_cost,
        'materials': materials,
        'success_rate': success_rate,
        'random_roll': random_roll,
        'message': message
    }

def calculate_expected_cost(item, target_level, equipment_data, iterations=10000):
    """Tính toán chi phí kỳ vọng để đạt target level"""
    total_cost = 0
    successful_runs = 0
    
    for _ in range(iterations):
        current_level = 0
        run_cost = 0
        attempts = 0
        max_attempts = 1000  # Tránh vòng lặp vô hạn
        
        while current_level < target_level and attempts < max_attempts:
            attempts += 1
            result = simulate_upgrade(item, current_level, equipment_data)
            
            if result['success'] is False and 'Đã đạt level tối đa' in result['message']:
                break
                
            run_cost += result['gold_cost']
            current_level = result['new_level']
        
        if current_level >= target_level:
            total_cost += run_cost
            successful_runs += 1
    
    if successful_runs > 0:
        return total_cost / successful_runs
    else:
        return float('inf')

def analyze_upgrade_difficulty():
    """Phân tích độ khó của từng level upgrade"""
    equipment_data, items_data = load_data()
    if not equipment_data or not items_data:
        return
    
    print("🔍 PHÂN TÍCH ĐỘ KHÓ UPGRADE")
    print("=" * 60)
    
    success_rates = equipment_data['equipment_upgrade_rates']['upgrade_success_rates']
    costs = equipment_data['equipment_upgrade_rates']['upgrade_costs']
    
    print(f"{'Level':<8}{'Tỷ lệ':<12}{'Chi phí':<12}{'Kỳ vọng chi phí':<15}")
    print("-" * 60)
    
    for level in range(1, 11):
        success_rate = success_rates[str(level)]
        cost = costs[str(level)]['gold']
        expected_cost = cost / (success_rate / 100)  # Chi phí kỳ vọng cho 1 lần thành công
        
        print(f"{level:<8}{success_rate}%{'':<7}{cost:<12}{expected_cost:.0f}")

def test_specific_item():
    """Test upgrade cho một item cụ thể"""
    equipment_data, items_data = load_data()
    if not equipment_data or not items_data:
        return
    
    equipment_items = get_equipment_items(items_data)
    
    print("\n🎯 TEST UPGRADE CHO ITEM CỤ THỂ")
    print("=" * 60)
    
    # Chọn một vài item tiêu biểu
    test_items = []
    for item in equipment_items:
        if item['item_id'] in ['bronze-sword', 'iron-sword', 'phoenix-sword', 'terror-blade']:
            test_items.append(item)
    
    for item in test_items:
        print(f"\n📦 {item['name']} ({item['item_id']})")
        print(f"   Nguyên liệu: {', '.join(item.get('upgrade_material', []))}")
        
        # Thử upgrade từ level 0 lên level 1
        result = simulate_upgrade(item, 0, equipment_data)
        print(f"   Level 0→1: {result['message']}")
        print(f"   Chi phí: {result['gold_cost']} vàng, Tỷ lệ: {result['success_rate']}%")
        
        # Tính chi phí kỳ vọng để đạt level 5
        expected_cost = calculate_expected_cost(item, 5, equipment_data, 1000)
        if expected_cost != float('inf'):
            print(f"   Chi phí kỳ vọng đạt Level 5: {expected_cost:.0f} vàng")

def simulate_upgrade_session():
    """Mô phỏng một session upgrade"""
    equipment_data, items_data = load_data()
    if not equipment_data or not items_data:
        return
    
    print("\n🎮 MÔ PHỎNG SESSION UPGRADE")
    print("=" * 60)
    
    # Chọn iron-sword làm ví dụ
    test_item = None
    for item in items_data:
        if item['item_id'] == 'iron-sword':
            test_item = item
            break
    
    if not test_item:
        print("❌ Không tìm thấy iron-sword")
        return
    
    current_level = 0
    total_spent = 0
    attempts = 0
    max_attempts = 50
    
    print(f"🗡️  Bắt đầu upgrade {test_item['name']} từ Level {current_level}")
    print(f"   Nguyên liệu cần: {', '.join(test_item.get('upgrade_material', []))}")
    print()
    
    while current_level < 5 and attempts < max_attempts:
        attempts += 1
        result = simulate_upgrade(test_item, current_level, equipment_data)
        
        total_spent += result['gold_cost']
        current_level = result['new_level']
        
        print(f"Lần {attempts}: {result['message']}")
        print(f"   Roll: {result['random_roll']}/{result['success_rate']} | Chi phí: {result['gold_cost']} vàng")
        
        if current_level >= 5:
            print(f"\n🎉 ĐẠT MỤC TIÊU! Level {current_level} sau {attempts} lần thử")
            break
    
    print(f"\n💰 Tổng chi phí: {total_spent} vàng")
    print(f"🎯 Level cuối: {current_level}")

def validate_data_consistency():
    """Kiểm tra tính nhất quán của dữ liệu"""
    equipment_data, items_data = load_data()
    if not equipment_data or not items_data:
        return
    
    print("\n✅ KIỂM TRA TÍNH NHẤT QUÁN DỮ LIỆU")
    print("=" * 60)
    
    # Kiểm tra upgrade_material có item nào không tồn tại
    all_item_ids = set(item['item_id'] for item in items_data)
    
    equipment_items = get_equipment_items(items_data)
    missing_materials = set()
    
    for item in equipment_items:
        materials = item.get('upgrade_material', [])
        for material in materials:
            if material not in all_item_ids:
                missing_materials.add(material)
    
    if missing_materials:
        print(f"❌ Nguyên liệu không tồn tại: {', '.join(missing_materials)}")
    else:
        print("✅ Tất cả upgrade_material đều tồn tại trong items.json")
    
    # Kiểm tra equipment slots
    equipment_slots = equipment_data.get('equipment_slots', {})
    slot_types = set(equipment_slots.keys())
    
    used_slots = set()
    for item in equipment_items:
        slot = item.get('equipment_slot')
        if slot:
            used_slots.add(slot)
    
    undefined_slots = used_slots - slot_types
    if undefined_slots:
        print(f"❌ Equipment slot chưa định nghĩa: {', '.join(undefined_slots)}")
    else:
        print("✅ Tất cả equipment_slot đều được định nghĩa")
    
    print(f"📊 Tổng số equipment: {len(equipment_items)}")
    print(f"📊 Số loại slot: {len(slot_types)}")

def main():
    """Hàm main"""
    print("🔧 TOOL KIỂM TRA Cơ CHẾ UPGRADE MỚI")
    print("=" * 60)
    
    if not os.path.exists('data/equipment.json'):
        print("❌ Không tìm thấy data/equipment.json")
        return
    
    if not os.path.exists('data/items.json'):
        print("❌ Không tìm thấy data/items.json")
        return
    
    # Chạy các test
    validate_data_consistency()
    analyze_upgrade_difficulty()
    test_specific_item()
    simulate_upgrade_session()
    
    print("\n" + "=" * 60)
    print("🎉 Hoàn thành kiểm tra cơ chế upgrade!")

if __name__ == "__main__":
    main()
