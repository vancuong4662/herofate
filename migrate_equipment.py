#!/usr/bin/env python3
"""
Migration script để thêm equipment field cho users hiện tại
"""

import os
from database import get_database

def migrate_add_equipment():
    """Add equipment field to existing users"""
    print("Starting equipment migration...")
    
    db = get_database()
    
    # Get all users
    if hasattr(db, 'users') and db.users is not None:
        # MongoDB
        users = list(db.users.find({}))
        print(f"Found {len(users)} users in MongoDB")
        
        updated_count = 0
        for user in users:
            if 'equipment' not in user:
                # Add equipment field
                equipment = {
                    "helmet": None,
                    "armor": None,
                    "weapon": None,
                    "ring": None
                }
                
                # Update user
                result = db.users.update_one(
                    {"username": user["username"]},
                    {"$set": {"equipment": equipment}}
                )
                
                if result.modified_count > 0:
                    updated_count += 1
                    print(f"✓ Updated user: {user['username']}")
        
        print(f"Migration completed. Updated {updated_count} users.")
        
    else:
        print("Using file-based storage - migration not needed")

if __name__ == "__main__":
    migrate_add_equipment()
