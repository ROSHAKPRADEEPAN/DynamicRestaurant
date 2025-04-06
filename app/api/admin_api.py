from flask import Blueprint, jsonify, request

admin_api = Blueprint('admin_api', __name__)

@admin_api.route('/users', methods=['GET'])
def get_all_users():
    """
    Fetch a list of all users.
    """
    # Example response (replace with actual database query)
    users = [
        {"id": 1, "username": "john_doe", "email": "john@example.com"},
        {"id": 2, "username": "jane_doe", "email": "jane@example.com"}
    ]
    return jsonify(users)

@admin_api.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user by ID.
    """
    # Example: Perform deletion in the database
    return jsonify({"message": f"User with ID {user_id} deleted successfully"})