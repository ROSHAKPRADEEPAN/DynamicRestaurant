from flask import Blueprint, jsonify, request

user_api = Blueprint('user_api', __name__)

@user_api.route('/profile', methods=['GET'])
def get_user_profile():
    """
    Fetch the profile of the logged-in user.
    """
    # Example response (replace with actual database query)
    user_profile = {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "reservations": [
            {"id": 101, "date": "2025-04-10", "table_number": 5},
            {"id": 102, "date": "2025-04-15", "table_number": 3}
        ]
    }
    return jsonify(user_profile)

@user_api.route('/reservation', methods=['POST'])
def create_reservation():
    """
    Create a new reservation for the user.
    """
    data = request.json
    # Example: Validate and save reservation to the database
    reservation = {
        "id": 103,
        "user_id": data.get("user_id"),
        "date": data.get("date"),
        "table_number": data.get("table_number")
    }
    return jsonify({"message": "Reservation created successfully", "reservation": reservation}), 201