"""
Migration script to update building names in existing user data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from database import get_database

def migrate_building_names():
    print("=" * 60)
    print("Migrating Building Names")
    print("=" * 60)
    
    # Mapping từ tên cũ sang tên mới
    building_mapping = {
        "inventory": "storage",
        "forge": "blacksmith", 
        "shop": "market",
        "potion": None  # Xóa potion building không còn sử dụng
    }
    
    try:
        db = get_database()
        
        if db.users is not None:
            # MongoDB migration
            print("Migrating MongoDB users...")
            users = list(db.users.find({}))
            
            for user in users:
                username = user.get('username', 'unknown')
                buildings = user.get('buildings', {})
                updated_buildings = {}
                has_changes = False
                
                print(f"Processing user: {username}")
                print(f"  Current buildings: {buildings}")
                
                # Copy existing buildings và apply mapping
                for building_id, level in buildings.items():
                    if building_id in building_mapping:
                        new_name = building_mapping[building_id]
                        if new_name:  # Nếu không phải None (tức là không xóa)
                            updated_buildings[new_name] = level
                            has_changes = True
                            print(f"    {building_id} -> {new_name} (level {level})")
                        else:
                            print(f"    Removing {building_id}")
                            has_changes = True
                    else:
                        # Giữ nguyên buildings không thay đổi
                        updated_buildings[building_id] = level
                
                if has_changes:
                    # Update user in database
                    result = db.users.update_one(
                        {"username": username},
                        {"$set": {"buildings": updated_buildings}}
                    )
                    
                    if result.modified_count > 0:
                        print(f"  ✅ Updated buildings: {updated_buildings}")
                    else:
                        print(f"  ❌ Failed to update user {username}")
                else:
                    print(f"  ✅ No changes needed")
                    
                print()
                    
        else:
            # File-based migration
            print("Migrating file-based users...")
            import json
            
            try:
                with open('data/users.json', 'r', encoding='utf-8') as f:
                    users_data = json.load(f)
                    
                has_file_changes = False
                
                for i, user in enumerate(users_data):
                    username = user.get('username', f'user_{i}')
                    buildings = user.get('buildings', {})
                    updated_buildings = {}
                    has_changes = False
                    
                    print(f"Processing user: {username}")
                    print(f"  Current buildings: {buildings}")
                    
                    for building_id, level in buildings.items():
                        if building_id in building_mapping:
                            new_name = building_mapping[building_id]
                            if new_name:
                                updated_buildings[new_name] = level
                                has_changes = True
                                print(f"    {building_id} -> {new_name} (level {level})")
                            else:
                                print(f"    Removing {building_id}")
                                has_changes = True
                        else:
                            updated_buildings[building_id] = level
                    
                    if has_changes:
                        users_data[i]['buildings'] = updated_buildings
                        has_file_changes = True
                        print(f"  ✅ Updated buildings: {updated_buildings}")
                    else:
                        print(f"  ✅ No changes needed")
                    print()
                
                if has_file_changes:
                    # Save updated data back to file
                    with open('data/users.json', 'w', encoding='utf-8') as f:
                        json.dump(users_data, f, ensure_ascii=False, indent=2)
                    print("✅ File saved successfully!")
                    
            except FileNotFoundError:
                print("users.json file not found - no file migration needed")
                
    except Exception as e:
        print(f"❌ Migration error: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)
    print("Migration completed!")

if __name__ == "__main__":
    migrate_building_names()
    input("Press Enter to exit...")
