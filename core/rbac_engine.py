import json, os
from datetime import datetime

ROLES = {
    "viewer": ["dashboard:read", "trades:read"],
    "trader": ["dashboard:read", "trades:read", "bot:start", "bot:stop", "trades:execute"],
    "manager": ["dashboard:read", "trades:read", "bot:start", "bot:stop", "trades:execute", "strategy:write", "risk:write"],
    "admin": ["*"]
}

class AccessControl:
    def __init__(self, user_role):
        self.user_role = user_role
        self.permissions = ROLES.get(user_role, [])

    def has_permission(self, action):
        if "*" in self.permissions:
            return True
        return action in self.permissions

    def authorize(self, action, context=None):
        if not self.has_permission(action):
            return False, "RBAC denied"
        # ABAC rules could be evaluated here using context
        return True, "OK"

def load_users():
    USERS_FILE = "config/users.json"
    if not os.path.exists(USERS_FILE):
        os.makedirs("config", exist_ok=True)
        import bcrypt
        default = {"users": [{"id": "admin", "role": "admin", "email": "admin@slh.local", "password_hash": bcrypt.hashpw("admin".encode(), bcrypt.gensalt()).decode()}]}
        with open(USERS_FILE, "w") as f:
            json.dump(default, f, indent=2)
    with open(USERS_FILE) as f:
        return json.load(f)

def save_users(data):
    with open("config/users.json", "w") as f:
        json.dump(data, f, indent=2)

def add_user(email, role, password_hash):
    data = load_users()
    data["users"].append({"id": email.split("@")[0], "role": role, "email": email, "password_hash": password_hash})
    save_users(data)
