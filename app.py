import webbrowser
import threading
import os
from flask import Flask, render_template, request, jsonify, session, redirect
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

@app.route("/")
def index():
    # Nếu user đã đăng nhập, redirect sang town
    if current_user.is_authenticated:
        return redirect('/town')
    return render_template("index.html")

@app.route("/town")
@login_required
def town():
    return render_template("town.html")

@app.route("/quests")
@login_required
def quests():
    return render_template("quests.html")

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
def api_quests():
    try:
        with open("data/quests.json", "r", encoding="utf-8") as f:
            quests = json.load(f)
        return jsonify({"success": True, "quests": quests})
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


# Chỉ mở trình duyệt nếu đây là tiến trình chính (tránh auto-reload)
def open_browser():
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":  # Chỉ chạy khi Flask khởi động lần đầu
        webbrowser.open(f"http://{HOST}:{PORT}/", new=2)

if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
    app.run(host=HOST, port=PORT)