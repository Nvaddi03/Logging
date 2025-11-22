"""
User Service - Flask Application
Handles user authentication and profile management
"""

from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Some logging configured
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/api/users/register', methods=['POST'])
def register_user():
    """Register a new user - HAS LOGGING"""
    logger.info("User registration endpoint called")
    
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # Validation
        if not username or not email or not password:
            logger.warning(f"Invalid registration data for email: {email}")
            return jsonify({"error": "Missing required fields"}), 400
        
        # Database operation (simulated)
        user_id = create_user_in_db(username, email, password)
        
        logger.info(f"User registered successfully: {user_id}")
        return jsonify({"user_id": user_id, "message": "User registered"}), 201
        
    except Exception as e:
        logger.error(f"Error during user registration: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user profile - MISSING LOGGING"""
    # NO LOGGING HERE - GAP!
    try:
        user = fetch_user_from_db(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user), 200
    except Exception as e:
        # NO ERROR LOGGING - GAP!
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user profile - PARTIAL LOGGING"""
    data = request.get_json()
    
    # Entry point has no logging - GAP!
    try:
        user = fetch_user_from_db(user_id)
        if not user:
            logger.warning(f"Attempted to update non-existent user: {user_id}")
            return jsonify({"error": "User not found"}), 404
        
        # Update user (no logging of what changed - GAP!)
        updated_user = update_user_in_db(user_id, data)
        
        return jsonify(updated_user), 200
    except Exception as e:
        # Has error logging
        logger.error(f"Failed to update user {user_id}: {str(e)}")
        return jsonify({"error": "Update failed"}), 500


@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user - NO LOGGING AT ALL"""
    # CRITICAL: No logging for user deletion - MAJOR GAP!
    try:
        result = delete_user_from_db(user_id)
        if result:
            return jsonify({"message": "User deleted"}), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": "Deletion failed"}), 500


def create_user_in_db(username, email, password):
    """Database operation - MISSING LOGGING"""
    # Database query with no logging - GAP!
    import hashlib
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Simulated DB insert
    user_id = f"user_{hash(email)}"
    return user_id


def fetch_user_from_db(user_id):
    """Fetch user from database - NO LOGGING"""
    # Database read with no logging - GAP!
    return {
        "id": user_id,
        "username": "john_doe",
        "email": "john@example.com"
    }


def update_user_in_db(user_id, data):
    """Update user in database - NO LOGGING"""
    # Database update with no logging - GAP!
    return {"id": user_id, **data}


def delete_user_from_db(user_id):
    """Delete user from database - CRITICAL MISSING LOGGING"""
    # CRITICAL: Deleting data with no audit trail - MAJOR GAP!
    return True


@app.route('/api/users/login', methods=['POST'])
def login():
    """User login - PARTIAL LOGGING"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Entry logging present
    logger.info(f"Login attempt for email: {email}")
    
    try:
        user = authenticate_user(email, password)
        if user:
            # Success logging
            logger.info(f"Successful login for user: {user['id']}")
            token = generate_auth_token(user['id'])
            return jsonify({"token": token}), 200
        else:
            # Failed login has logging
            logger.warning(f"Failed login attempt for email: {email}")
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({"error": "Login failed"}), 500


def authenticate_user(email, password):
    """Authenticate user - NO LOGGING"""
    # Authentication logic with no logging - GAP!
    import hashlib
    hashed = hashlib.sha256(password.encode()).hexdigest()
    # Simulated check
    return {"id": "user_123", "email": email}


def generate_auth_token(user_id):
    """Generate JWT token - NO LOGGING"""
    # Token generation with no logging - SECURITY GAP!
    import time
    return f"token_{user_id}_{int(time.time())}"


if __name__ == '__main__':
    logger.info("Starting User Service on port 5001")
    app.run(host='0.0.0.0', port=5001, debug=True)
