"""
User model for Flask-Login
"""

from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_data):
        """Initialize User object from database user data"""
        self.id = str(user_data.get('_id', '')) if user_data.get('_id') else user_data.get('username', '')
        self.username = user_data.get('username', '')
        self.gender = user_data.get('gender', '')
        self.gold = user_data.get('gold', 0)
        self.buildings = user_data.get('buildings', {})
        self.inventory = user_data.get('inventory', [])
        self.quests = user_data.get('quests', [])
        self.equipped_items = user_data.get('equipped_items', {})
        
    def get_id(self):
        """Required by Flask-Login"""
        return self.username  # Use username as unique identifier
        
    def to_dict(self):
        """Convert User object to dictionary for JSON serialization"""
        return {
            'username': self.username,
            'gender': self.gender,
            'gold': self.gold,
            'buildings': self.buildings,
            'inventory': self.inventory,
            'quests': self.quests,
            'equipped_items': self.equipped_items
        }
        
    @staticmethod
    def get(username, db):
        """Get user by username from database"""
        user_data = db.find_user(username)
        if user_data:
            return User(user_data)
        return None
