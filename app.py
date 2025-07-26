import webbrowser
import threading
import os
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import json
from bson import ObjectId
from database import get_database
from models import User

def serialize_user(user):
    """Convert MongoDB user document to JSON-serializable format"""
    if not user:
        return None
    
    serialized = {}
    for key, value in user.items():
        if key == "_id":
            # Convert ObjectId to string
            serialized[key] = str(value)
        elif key == "password":
            # Skip password for security
            continue
        else:
            serialized[key] = value
    return serialized

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', "4460")  # Use secret key from .env
# Bật chế độ debug
app.config['DEBUG'] = os.getenv('DEBUG', 'True') == 'True'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'  # Redirect to index page when login required
login_manager.login_message = 'Vui lòng đăng nhập để tiếp tục.'

# Debug: Print environment info
print("=" * 60)
print("Flask App Starting...")
print(f"Environment: {os.getenv('ENVIRONMENT', 'not set')}")
print(f"MongoDB URI: {os.getenv('MONGODB_URI', 'not set')}")
print(f"Database Name: {os.getenv('DATABASE_NAME', 'not set')}")
print("=" * 60)

# Địa chỉ server Flask
HOST = "127.0.0.1"
PORT = 2301

# Initialize database
db = get_database()
print(f"Database initialized: {'MongoDB' if db.users is not None else 'File-based'}")
if db.users is not None:
    print(f"MongoDB Database: {db.users.database.name}")
    print(f"MongoDB Collection: {db.users.name}")
print("=" * 60)

@login_manager.user_loader
def load_user(username):
    """Load user for Flask-Login"""
    return User.get(username, db)

def assign_random_quests(username):
    """Assign random quests to user if they have less than 3 active quests"""
    try:
        # Set random seed based on current time and username for better randomness
        import time
        random.seed(int(time.time() * 1000) + hash(username))
        
        user = db.find_user(username)
        if not user:
            print(f"User {username} not found")
            return
        
        # Get current active quests
        user_quests = user.get('quests', [])
        active_quests = [q for q in user_quests if q.get('state') == 'active']
        
        print(f"User {username} has {len(active_quests)} active quests")
        
        # If user already has 3 or more active quests, return
        if len(active_quests) >= 3:
            print(f"User {username} already has 3 or more active quests")
            return
        
        # Load all available quests
        with open('data/quests.json', 'r', encoding='utf-8') as f:
            all_quests = json.load(f)
        
        print(f"Total quests in database: {len(all_quests)}")
        
        # Filter quests that user doesn't have and meets level requirement
        user_level = user.get('level', 1)
        existing_quest_ids = [q['quest_id'] for q in user_quests]
        
        print(f"User level: {user_level}")
        print(f"Existing quest IDs: {existing_quest_ids}")
        
        available_quests = [
            quest for quest in all_quests 
            if quest['quest_id'] not in existing_quest_ids 
            and quest['level_required'] <= user_level
        ]
        
        print(f"Available quests for user: {[q['quest_id'] for q in available_quests]}")
        
        # Calculate how many quests to assign
        quests_needed = 3 - len(active_quests)
        quests_to_assign = min(quests_needed, len(available_quests))
        
        print(f"Quests needed: {quests_needed}, Available: {len(available_quests)}, Will assign: {quests_to_assign}")
        
        if quests_to_assign > 0:
            # Ensure we have enough quests to sample from
            if len(available_quests) < quests_to_assign:
                print(f"Not enough available quests. Only {len(available_quests)} available")
                quests_to_assign = len(available_quests)
            
            # Randomly select quests using random.shuffle for better randomness
            available_quest_copy = available_quests.copy()
            random.shuffle(available_quest_copy)
            selected_quests = available_quest_copy[:quests_to_assign]
            
            print(f"Selected quests: {[q['quest_id'] for q in selected_quests]}")
            
            # Add selected quests to user
            for quest in selected_quests:
                new_quest = {
                    'quest_id': quest['quest_id'],
                    'state': 'active',
                    'assigned_at': str(datetime.utcnow()),
                    'progress': {}
                }
                user_quests.append(new_quest)
                print(f"Added quest {quest['quest_id']} to user {username}")
            
            # Update user in database
            db.update_user(username, {'quests': user_quests})
            print(f"Successfully assigned {quests_to_assign} random quests to user {username}")
        else:
            print(f"No quests to assign to user {username}")
        
    except Exception as e:
        print(f"Error assigning random quests to {username}: {e}")
        import traceback
        traceback.print_exc()

def assign_random_market_items(username):
    """Assign random market items to user based on market building level"""
    try:
        import time
        random.seed(int(time.time() * 1000) + hash(username))
        
        user = db.find_user(username)
        if not user:
            print(f"User {username} not found")
            return
        
        # Get market building level (default to 0 if not built)
        buildings = user.get('buildings', {})
        market_level = buildings.get('market', 0)
        
        # If market is not built, no items to assign
        if market_level == 0:
            print(f"User {username} has no market building")
            return
        
        # Calculate number of items based on market level (base 3 + level)
        base_items = 3
        items_count = base_items + market_level
        max_items = 8  # Cap at 8 items
        items_count = min(items_count, max_items)
        
        print(f"User {username} market level: {market_level}, will assign {items_count} items")
        
        # Check if user already has market items (refresh daily)
        current_market = user.get('market', [])
        current_time = datetime.utcnow()
        
        # Remove expired items (older than 24 hours)
        valid_items = []
        for item in current_market:
            item_time = datetime.fromisoformat(item.get('timestamp', ''))
            if (current_time - item_time).total_seconds() < 86400:  # 24 hours
                valid_items.append(item)
        
        # If we still have enough valid items, don't assign new ones
        if len(valid_items) >= items_count:
            print(f"User {username} already has {len(valid_items)} valid market items")
            return
        
        # Load all items
        with open('data/items.json', 'r', encoding='utf-8') as f:
            all_items = json.load(f)
        
        # Separate items by type
        equipment_items = [item for item in all_items if item['type'] == 'equipment']
        material_items = [item for item in all_items if item['type'] == 'material']
        
        print(f"Available equipment items: {len(equipment_items)}")
        print(f"Available material items: {len(material_items)}")
        
        # Calculate how many of each type to assign
        items_needed = items_count - len(valid_items)
        equipment_count = int(items_needed * 0.2)  # 20% equipment
        material_count = int(items_needed * 0.8)   # 80% materials
        
        # Ensure we have at least some of each if possible
        if equipment_count == 0 and len(equipment_items) > 0 and items_needed > 0:
            equipment_count = 1
            material_count = items_needed - 1
        
        print(f"Will assign {equipment_count} equipment and {material_count} materials")
        
        new_market_items = valid_items.copy()
        
        # Add equipment items
        if equipment_count > 0 and len(equipment_items) > 0:
            selected_equipment = random.sample(equipment_items, min(equipment_count, len(equipment_items)))
            for item in selected_equipment:
                market_item = {
                    'item_id': item['item_id'],
                    'quantity': random.randint(1, 3),
                    'price': int(item['price'] * random.uniform(0.9, 1.1)),  # Price variation ±10%
                    'timestamp': current_time.isoformat()
                }
                new_market_items.append(market_item)
                print(f"Added equipment item {item['item_id']} to market")
        
        # Add material items
        if material_count > 0 and len(material_items) > 0:
            selected_materials = random.sample(material_items, min(material_count, len(material_items)))
            for item in selected_materials:
                market_item = {
                    'item_id': item['item_id'],
                    'quantity': random.randint(5, 20),  # More quantity for materials
                    'price': int(item['price'] * random.uniform(0.85, 1.05)),  # Less price variation for materials
                    'timestamp': current_time.isoformat()
                }
                new_market_items.append(market_item)
                print(f"Added material item {item['item_id']} to market")
        
        # Update user market data
        db.update_user(username, {'market': new_market_items})
        print(f"Successfully assigned {len(new_market_items)} market items to user {username}")
        
    except Exception as e:
        print(f"Error assigning random market items to {username}: {e}")
        import traceback
        traceback.print_exc()

@app.route("/")
def index():
    # Nếu user đã đăng nhập, redirect sang town
    if current_user.is_authenticated:
        return redirect('/town')
    return render_template("index.html")

@app.route("/not-implemented")
def not_implemented():
    return render_template("not-implemented.html")

@app.route("/town")
@login_required
def town():
    return render_template("town.html")

@app.route('/dialog')
@login_required
def dialog():
    quest_id = request.args.get('quest')
    dialog_type = request.args.get('type', 'start')  # start or complete
    
    if not quest_id:
        flash('Không tìm thấy quest ID!')
        return redirect(url_for('quests'))
    
    return render_template('dialog.html', quest_id=quest_id, dialog_type=dialog_type)

@app.route('/quests')
@login_required
def quests():
    return render_template("quests.html")

@app.route('/market')
@login_required
def market():
    return render_template("market.html")

# API Routes
@app.route("/api/register", methods=["POST"])
def api_register():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        gender = data.get("gender")
        
        if not username or not password or not gender:
            return jsonify({"success": False, "message": "Thiếu thông tin bắt buộc"}), 400
        
        if db.user_exists(username):
            return jsonify({"success": False, "message": "Tên đăng nhập đã tồn tại"}), 400
        
        if db.create_user(username, password, gender):
            return jsonify({"success": True, "message": "Đăng ký thành công"})
        else:
            return jsonify({"success": False, "message": "Lỗi tạo tài khoản"}), 500
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/login", methods=["POST"])
def api_login():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            return jsonify({"success": False, "message": "Thiếu tên đăng nhập hoặc mật khẩu"}), 400
        
        user_data = db.authenticate_user(username, password)
        if user_data:
            # Create User object and login
            user = User(user_data)
            login_user(user)
            
            # Assign random quests if user has less than 3 active quests
            assign_random_quests(username)
            
            # Assign random market items based on market building level
            assign_random_market_items(username)
            
            # Reload user data after quest and market assignment
            updated_user_data = db.find_user(username)
            user = User(updated_user_data)
            
            # Return user data (password already excluded by User.to_dict())
            return jsonify({"success": True, "user": user.to_dict(), "message": "Đăng nhập thành công"})
        else:
            return jsonify({"success": False, "message": "Tên đăng nhập hoặc mật khẩu không đúng"}), 401
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/logout", methods=["POST"])
@login_required
def api_logout():
    try:
        logout_user()
        return jsonify({"success": True, "message": "Đăng xuất thành công"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/auth-status", methods=["GET"])
def api_auth_status():
    """Check if user is authenticated"""
    try:
        if current_user.is_authenticated:
            return jsonify({
                "success": True, 
                "authenticated": True,
                "user": current_user.to_dict()
            })
        else:
            return jsonify({
                "success": True,
                "authenticated": False
            })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/buildings", methods=["GET"])
def api_buildings():
    try:
        with open("data/buildings.json", "r", encoding="utf-8") as f:
            buildings = json.load(f)
        return jsonify({"success": True, "buildings": buildings})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/upgrade-building", methods=["POST"])
@login_required
def api_upgrade_building():
    try:
        data = request.get_json()
        building_id = data.get("building_id")
        level = data.get("level")
        cost = data.get("cost")
        
        username = current_user.username
        user = db.find_user(username)
        if not user:
            return jsonify({"success": False, "message": "Không tìm thấy người dùng"}), 404
        
        # Check if user has enough gold
        if user.get("gold", 0) < cost.get("gold", 0):
            return jsonify({"success": False, "message": "Không đủ vàng"}), 400
        
        # Check if user has enough materials
        user_inventory = user.get("inventory", [])
        for material in cost.get("materials", []):
            user_item = next((item for item in user_inventory if item["item_id"] == material["item_id"]), None)
            if not user_item or user_item["quantity"] < material["quantity"]:
                return jsonify({"success": False, "message": f"Không đủ {material['item_id']}"}), 400
        
        # Perform upgrade
        # Update building level
        buildings = user.get("buildings", {})
        buildings[building_id] = level
        
        # Deduct gold
        new_gold = user.get("gold", 0) - cost.get("gold", 0)
        
        # Remove materials from inventory
        new_inventory = user_inventory.copy()
        for material in cost.get("materials", []):
            for item in new_inventory:
                if item["item_id"] == material["item_id"]:
                    item["quantity"] -= material["quantity"]
                    if item["quantity"] <= 0:
                        new_inventory.remove(item)
                    break
        
        # Update user data
        update_data = {
            "buildings": buildings,
            "gold": new_gold,
            "inventory": new_inventory
        }
        
        if db.update_user(username, update_data):
            return jsonify({"success": True, "message": "Nâng cấp thành công"})
        else:
            return jsonify({"success": False, "message": "Lỗi cập nhật dữ liệu"}), 500
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/items", methods=["GET"])
def api_items():
    try:
        with open("data/items.json", "r", encoding="utf-8") as f:
            items = json.load(f)
        return jsonify({"success": True, "items": items})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/quests", methods=["GET"])
@login_required
def api_quests():
    try:
        # Load all quest data
        with open("data/quests.json", "r", encoding="utf-8") as f:
            all_quests = json.load(f)
        
        # Get user's assigned quests
        username = current_user.username
        user = db.find_user(username)
        
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        user_quests = user.get('quests', [])
        
        # Filter to only return user's assigned quests with full quest data
        user_quest_data = []
        for user_quest in user_quests:
            # Find the full quest data
            full_quest = next((q for q in all_quests if q['quest_id'] == user_quest['quest_id']), None)
            if full_quest:
                # Merge quest data with user's quest state
                quest_with_state = full_quest.copy()
                quest_with_state['state'] = user_quest.get('state', 'active')
                quest_with_state['assigned_at'] = user_quest.get('assigned_at')
                quest_with_state['progress'] = user_quest.get('progress', {})
                user_quest_data.append(quest_with_state)
        
        return jsonify({"success": True, "quests": user_quest_data})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/user", methods=["GET"])
@login_required
def api_user():
    try:
        username = current_user.username
        user = db.find_user(username)
        if user:
            # Return current user data
            return jsonify({"success": True, "user": current_user.to_dict()})
        else:
            return jsonify({"success": False, "message": "Không tìm thấy người dùng"}), 404
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/shop", methods=["GET"])
def api_shop():
    try:
        # Load available items for shop
        with open("data/items.json", "r", encoding="utf-8") as f:
            all_items = json.load(f)
        
        # Filter items that can be bought (materials and low-level equipment)
        shop_items = []
        for item in all_items:
            if item["type"] == "material":
                shop_items.append(item)
            elif item["type"] == "equipment" and item.get("level_require", 0) <= 5:
                shop_items.append(item)
        
        return jsonify({"success": True, "items": shop_items})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/market", methods=["GET"])
@login_required
def api_market():
    try:
        username = current_user.username
        user = db.find_user(username)
        
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        # Get user's market items
        market_items = user.get('market', [])
        
        # Load item details
        with open("data/items.json", "r", encoding="utf-8") as f:
            all_items = json.load(f)
        
        # Combine market data with item details
        market_data = []
        for market_item in market_items:
            item_details = next((item for item in all_items if item['item_id'] == market_item['item_id']), None)
            if item_details:
                combined_item = {
                    'item_id': market_item['item_id'],
                    'name': item_details['name'],
                    'description': item_details['description'],
                    'type': item_details['type'],
                    'quantity': market_item['quantity'],
                    'price': market_item['price'],
                    'original_price': item_details['price'],
                    'timestamp': market_item['timestamp']
                }
                market_data.append(combined_item)
        
        return jsonify({"success": True, "market": market_data})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/buy-item", methods=["POST"])
@login_required
def api_buy_item():
    try:
        data = request.get_json()
        item_id = data.get("item_id")
        quantity = data.get("quantity", 1)
        
        username = current_user.username
        
        # Load item data
        with open("data/items.json", "r", encoding="utf-8") as f:
            all_items = json.load(f)
        
        item_data = next((item for item in all_items if item["item_id"] == item_id), None)
        if not item_data:
            return jsonify({"success": False, "message": "Item không tồn tại"}), 404
        
        # Calculate total cost (buy price = base price + 15%)
        buy_price = int(item_data["price"] * 1.15)
        total_cost = buy_price * quantity
        
        user = db.find_user(username)
        if not user:
            return jsonify({"success": False, "message": "Không tìm thấy người dùng"}), 404
        
        if user.get("gold", 0) < total_cost:
            return jsonify({"success": False, "message": "Không đủ vàng"}), 400
        
        # Add item to inventory
        inventory = user.get("inventory", [])
        existing_item = next((item for item in inventory if item["item_id"] == item_id), None)
        
        if existing_item:
            existing_item["quantity"] += quantity
        else:
            new_item = {"item_id": item_id, "quantity": quantity}
            if item_data["type"] == "equipment":
                new_item["level"] = 1
            inventory.append(new_item)
        
        # Update user data
        new_gold = user.get("gold", 0) - total_cost
        update_data = {
            "inventory": inventory,
            "gold": new_gold
        }
        
        if db.update_user(username, update_data):
            return jsonify({
                "success": True, 
                "message": f"Đã mua {quantity} {item_data['name']}",
                "cost": total_cost
            })
        else:
            return jsonify({"success": False, "message": "Lỗi cập nhật dữ liệu"}), 500
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/buy-market-item", methods=["POST"])
@login_required
def api_buy_market_item():
    try:
        data = request.get_json()
        item_id = data.get("item_id")
        quantity = data.get("quantity", 1)
        
        username = current_user.username
        user = db.find_user(username)
        
        if not user:
            return jsonify({"success": False, "message": "Không tìm thấy người dùng"}), 404
        
        # Find item in user's market
        market_items = user.get('market', [])
        market_item = next((item for item in market_items if item['item_id'] == item_id), None)
        
        if not market_item:
            return jsonify({"success": False, "message": "Item không có trong chợ"}), 404
        
        if market_item['quantity'] < quantity:
            return jsonify({"success": False, "message": "Không đủ số lượng"}), 400
        
        # Calculate total cost
        total_cost = market_item['price'] * quantity
        
        if user.get("gold", 0) < total_cost:
            return jsonify({"success": False, "message": "Không đủ vàng"}), 400
        
        # Add item to inventory
        inventory = user.get("inventory", [])
        existing_item = next((item for item in inventory if item["item_id"] == item_id), None)
        
        if existing_item:
            existing_item["quantity"] += quantity
        else:
            new_item = {"item_id": item_id, "quantity": quantity}
            inventory.append(new_item)
        
        # Update market item quantity or remove if 0
        market_item['quantity'] -= quantity
        if market_item['quantity'] <= 0:
            market_items.remove(market_item)
        
        # Update user data
        new_gold = user.get("gold", 0) - total_cost
        update_data = {
            "inventory": inventory,
            "market": market_items,
            "gold": new_gold
        }
        
        if db.update_user(username, update_data):
            # Load item name for response
            with open("data/items.json", "r", encoding="utf-8") as f:
                all_items = json.load(f)
            item_data = next((item for item in all_items if item["item_id"] == item_id), None)
            item_name = item_data['name'] if item_data else item_id
            
            return jsonify({
                "success": True, 
                "message": f"Đã mua {quantity} {item_name} từ chợ",
                "cost": total_cost,
                "new_gold": new_gold
            })
        else:
            return jsonify({"success": False, "message": "Lỗi cập nhật dữ liệu"}), 500
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/dialog/<int:dialog_id>')
@login_required
def get_dialog(dialog_id):
    """Get dialog data by ID"""
    try:
        with open('data/dialogs.json', 'r', encoding='utf-8') as f:
            dialogs = json.load(f)
        
        dialog = next((d for d in dialogs if d['dialog_id'] == dialog_id), None)
        
        if not dialog:
            return jsonify({"success": False, "message": "Dialog not found"}), 404
        
        return jsonify({"success": True, "dialog": dialog})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/dialog')
@login_required
def dialog_page():
    """Dialog system page"""
    quest_id = request.args.get('quest')
    dialog_type = request.args.get('type', 'start')  # start or complete
    
    if not quest_id:
        flash('Không tìm thấy quest ID!')
        return redirect(url_for('quests'))
    
    return render_template('dialog.html', quest_id=quest_id, dialog_type=dialog_type)

@app.route('/data/dialogs.json')
def get_dialogs():
    """API endpoint to get dialog data"""
    try:
        with open('data/dialogs.json', 'r', encoding='utf-8') as f:
            dialogs = json.load(f)
        return jsonify(dialogs)
    except FileNotFoundError:
        return jsonify([]), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/dialog/complete', methods=['POST'])
@login_required
def complete_dialog():
    """Handle dialog completion"""
    try:
        data = request.get_json()
        dialog_id = data.get('dialog_id')
        dialog_type = data.get('type')
        
        username = current_user.username
        user = db.find_user(username)
        
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        # Initialize completed_dialogs if not exists
        completed_dialogs = user.get('completed_dialogs', [])
        
        # Add dialog to completed list if not already there
        if dialog_id not in completed_dialogs:
            completed_dialogs.append(dialog_id)
            
            # Update user in database
            db.update_user(username, {"completed_dialogs": completed_dialogs})
            
            # Give rewards based on dialog type
            rewards = {}
            if dialog_type == 'end':
                # End dialogs give rewards
                rewards = {
                    'gold': 100,
                    'exp': 50
                }
                
                # Update user stats
                new_gold = user.get('gold', 0) + rewards['gold']
                new_exp = user.get('exp', 0) + rewards['exp']
                
                db.update_user(username, {
                    'gold': new_gold,
                    'exp': new_exp
                })
                
                rewards['new_gold'] = new_gold
                rewards['new_exp'] = new_exp
            
            return jsonify({
                "success": True, 
                "message": f"Dialog {dialog_id} completed",
                "rewards": rewards
            })
        else:
            return jsonify({
                "success": True, 
                "message": f"Dialog {dialog_id} already completed"
            })
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/start-quest', methods=['POST'])
@login_required
def start_quest():
    try:
        data = request.get_json()
        quest_id = data.get('quest_id')
        
        if not quest_id:
            return jsonify({'success': False, 'message': 'Thiếu quest ID!'})
        
        # Get user from database
        user = db.find_user(current_user.username)
        if not user:
            return jsonify({'success': False, 'message': 'Không tìm thấy người dùng!'})
        
        # Check if quest is assigned to user and in 'active' state
        user_quests = user.get('quests', [])
        quest_found = False
        
        for i, quest in enumerate(user_quests):
            if quest['quest_id'] == quest_id:
                if quest['state'] == 'active':
                    # Update quest state to 'doing'
                    user_quests[i]['state'] = 'doing'
                    quest_found = True
                    break
                else:
                    return jsonify({'success': False, 'message': 'Quest không ở trạng thái có thể bắt đầu!'})
        
        if not quest_found:
            return jsonify({'success': False, 'message': 'Quest không được gán cho người chơi này!'})
        
        # Update user in database
        db.update_user(current_user.username, {'quests': user_quests})
        
        return jsonify({
            'success': True,
            'message': 'Đã bắt đầu quest!'
        })
        
    except Exception as e:
        print(f"Error starting quest: {e}")
        return jsonify({'success': False, 'message': 'Lỗi server khi bắt đầu quest!'})

@app.route('/api/complete-quest', methods=['POST'])
@login_required
def complete_quest():
    """Complete a quest for the user"""
    try:
        data = request.get_json()
        quest_id = data.get('quest_id')
        
        if not quest_id:
            return jsonify({"success": False, "message": "Quest ID required"}), 400
        
        username = current_user.username
        user = db.find_user(username)
        
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        # Load quest data
        with open('data/quests.json', 'r', encoding='utf-8') as f:
            quests = json.load(f)
        
        quest = next((q for q in quests if q['quest_id'] == quest_id), None)
        if not quest:
            return jsonify({"success": False, "message": "Quest not found"}), 404
        
        # Find user's quest
        user_quests = user.get('quests', [])
        user_quest = next((uq for uq in user_quests if uq['quest_id'] == quest_id), None)
        
        if not user_quest or user_quest['state'] not in ['active', 'doing']:
            return jsonify({"success": False, "message": "Quest not active or doing"}), 400
        
        # Mark quest as completed
        user_quest['state'] = 'completed'
        user_quest['completed_at'] = str(datetime.utcnow())
        
        # Give rewards
        rewards = quest['reward']
        new_gold = user.get('gold', 0) + rewards['gold']
        new_exp = user.get('exp', 0) + rewards['exp']
        
        # Add items to inventory
        inventory = user.get('inventory', [])
        for item_reward in rewards.get('items', []):
            existing_item = next((item for item in inventory if item['item_id'] == item_reward['item_id']), None)
            if existing_item:
                existing_item['quantity'] += item_reward['quantity']
            else:
                inventory.append({
                    'item_id': item_reward['item_id'],
                    'quantity': item_reward['quantity']
                })
        
        # Update user
        update_data = {
            'quests': user_quests,
            'gold': new_gold,
            'exp': new_exp,
            'inventory': inventory
        }
        
        db.update_user(username, update_data)
        
        return jsonify({
            "success": True,
            "message": f"Quest {quest_id} completed",
            "rewards": {
                "gold": rewards['gold'],
                "exp": rewards['exp'],
                "items": rewards.get('items', []),
                "new_gold": new_gold,
                "new_exp": new_exp
            }
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# Chỉ mở trình duyệt nếu đây là tiến trình chính (tránh auto-reload)
def open_browser():
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":  # Chỉ chạy khi Flask khởi động lần đầu
        webbrowser.open(f"http://{HOST}:{PORT}/", new=2)

if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
    app.run(host=HOST, port=PORT)