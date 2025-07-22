import pymongo
from pymongo import MongoClient
from datetime import datetime
import json
import os

class Database:
    def __init__(self, connection_string=None, database_name="herofate"):
        # Sử dụng connection string từ environment variable hoặc tham số
        if not connection_string:
            connection_string = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        
        self.environment = os.getenv('ENVIRONMENT', 'development')
        
        try:
            self.client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)  # 5 second timeout
            self.db = self.client[database_name]
            self.users = self.db.users
            
            # Test connection
            self.client.admin.command('ping')
            
            # Determine connection type
            if 'localhost' in connection_string or '127.0.0.1' in connection_string:
                print("✅ Connected to MongoDB Local successfully!")
                print(f"🏠 Database: {database_name} (Local Development)")
            else:
                print("✅ Connected to MongoDB Atlas successfully!")
                print(f"☁️ Database: {database_name} (Cloud Production)")
            
        except Exception as e:
            print(f"❌ Error connecting to MongoDB: {e}")
            print("📁 Falling back to file-based storage...")
            print("💡 Tip: Make sure MongoDB service is running locally")
            # Fallback to file-based storage for development
            self.client = None
            self.db = None
            self.users = None
            self._init_file_storage()

    def _init_file_storage(self):
        """Initialize file-based storage as fallback"""
        self.users_file = "data/users.json"
        
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
        print("📁 Using file-based storage for users")

    def _load_users_from_file(self):
        """Load users from JSON file"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []

    def _save_users_to_file(self, users):
        """Save users to JSON file"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(users, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False

    def create_user(self, username, password, gender):
        """Create a new user"""
        user_data = {
            "username": username,
            "password": password,  # In production, this should be hashed
            "created_at": datetime.now().isoformat(),
            "gender": gender,
            "buildings": {
                "town_hall": 1,   # Start with level 1 town hall
                "storage": 1,     # Đổi từ "inventory" thành "storage"
                "blacksmith": 0,  # Đổi từ "forge" thành "blacksmith"
                "market": 0,      # Đổi từ "shop" thành "market"
                "mage_tower": 0
            },
            "quests": [],
            "dialogs_seen": [],
            "inventory": [],
            "gold": 1000,
            "exp": 0,
            "reputation": 0,
            "stats": {
                "STR": 10,
                "AGI": 10,
                "INT": 10,
                "VIT": 10,
                "WIS": 10,
                "crit_rate": 0.05
            },
            "skills": [
                {"skill_id": 1001, "level": 1}  # Basic attack skill
            ]
        }

        if self.users is not None:
            # MongoDB storage
            try:
                result = self.users.insert_one(user_data)
                return result.inserted_id is not None
            except Exception as e:
                print(f"Error creating user in MongoDB: {e}")
                return False
        else:
            # File storage
            users = self._load_users_from_file()
            users.append(user_data)
            return self._save_users_to_file(users)

    def find_user(self, username):
        """Find user by username"""
        if self.users is not None:
            # MongoDB storage
            try:
                return self.users.find_one({"username": username})
            except Exception as e:
                print(f"Error finding user in MongoDB: {e}")
                return None
        else:
            # File storage
            users = self._load_users_from_file()
            for user in users:
                if user["username"] == username:
                    return user
            return None

    def update_user(self, username, update_data):
        """Update user data"""
        if self.users is not None:
            # MongoDB storage
            try:
                result = self.users.update_one(
                    {"username": username},
                    {"$set": update_data}
                )
                return result.modified_count > 0
            except Exception as e:
                print(f"Error updating user in MongoDB: {e}")
                return False
        else:
            # File storage
            users = self._load_users_from_file()
            for i, user in enumerate(users):
                if user["username"] == username:
                    users[i].update(update_data)
                    return self._save_users_to_file(users)
            return False

    def user_exists(self, username):
        """Check if user exists"""
        return self.find_user(username) is not None

    def authenticate_user(self, username, password):
        """Authenticate user login"""
        user = self.find_user(username)
        if user and user["password"] == password:  # In production, use proper password hashing
            return user
        return None

    def get_user_buildings(self, username):
        """Get user's building levels"""
        user = self.find_user(username)
        if user:
            return user.get("buildings", {})
        return {}

    def update_user_buildings(self, username, building_id, level):
        """Update a specific building level"""
        user = self.find_user(username)
        if user:
            buildings = user.get("buildings", {})
            buildings[building_id] = level
            return self.update_user(username, {"buildings": buildings})
        return False

    def get_user_inventory(self, username):
        """Get user's inventory"""
        user = self.find_user(username)
        if user:
            return user.get("inventory", [])
        return []

    def update_user_inventory(self, username, inventory):
        """Update user's inventory"""
        return self.update_user(username, {"inventory": inventory})

    def add_item_to_inventory(self, username, item_id, quantity=1):
        """Add item to user's inventory"""
        user = self.find_user(username)
        if not user:
            return False

        inventory = user.get("inventory", [])
        
        # Check if item already exists
        for item in inventory:
            if item["item_id"] == item_id:
                item["quantity"] += quantity
                break
        else:
            # Item doesn't exist, add new
            inventory.append({"item_id": item_id, "quantity": quantity})

        return self.update_user_inventory(username, inventory)

    def remove_item_from_inventory(self, username, item_id, quantity=1):
        """Remove item from user's inventory"""
        user = self.find_user(username)
        if not user:
            return False

        inventory = user.get("inventory", [])
        
        for i, item in enumerate(inventory):
            if item["item_id"] == item_id:
                if item["quantity"] <= quantity:
                    # Remove item completely
                    inventory.pop(i)
                else:
                    # Decrease quantity
                    item["quantity"] -= quantity
                break

        return self.update_user_inventory(username, inventory)

    def update_user_gold(self, username, gold_change):
        """Update user's gold (can be positive or negative)"""
        user = self.find_user(username)
        if user:
            current_gold = user.get("gold", 0)
            new_gold = max(0, current_gold + gold_change)  # Ensure gold doesn't go negative
            return self.update_user(username, {"gold": new_gold})
        return False

    def close_connection(self):
        """Close database connection"""
        if self.client is not None:
            self.client.close()
            print("📝 Database connection closed")


# Global database instance
db = Database()

def get_database():
    """Get database instance"""
    return db
