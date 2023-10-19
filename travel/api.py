from flask import Blueprint, jsonify, request
from travel.models import Hotel, Room
from travel import db

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Get a list of hotels
@api_bp.route('/hotels', methods=['GET'])
def get_hotels():
    hotels = Hotel.query.all()
    hotel_list = [h.to_dict() for h in hotels]
    return jsonify(hotels=hotel_list)

# Create a new hotel
@api_bp.route('/hotels', methods=['POST'])
def create_hotel():
    json_data = request.get_json()

    # Check if the request body contains valid JSON data
    if not json_data:
        return jsonify(message="No input data provided!"), 400

    # Create a new Hotel object from the JSON data
    hotel = Hotel(
        name=json_data['name'],
        description=json_data['description'],
        destination_id=json_data['destination_id']
    )

    # Create Room objects associated with the hotel
    rooms = []
    for room_json in json_data.get('rooms', []):
        room = Room(
            type=room_json['room_type'],
            num_rooms=room_json['num_rooms'],
            description=room_json['room_description'],
            rate=room_json['room_rate'],
            hotel=hotel
        )
        rooms.append(room)

    # Add the hotel and rooms to the database
    db.session.add(hotel)
    db.session.add_all(rooms)
    db.session.commit()

    return jsonify(message='Successfully created a new hotel!'), 201

# Delete an existing hotel by ID (also deletes related rooms)
@api_bp.route('/hotels/<int:hotel_id>', methods=['DELETE'])
def delete_hotel(hotel_id):
    hotel = Hotel.query.get(hotel_id)

    if not hotel:
        return jsonify(message='Hotel not found!'), 404

    db.session.delete(hotel)
    db.session.commit()

    return jsonify(message='Record deleted!'), 200

# Update an existing hotel by ID
@api_bp.route('/hotels/<int:hotel_id>', methods=['PUT'])
def update_hotel(hotel_id):
    json_data = request.get_json()
    hotel = Hotel.query.get(hotel_id)

    if not hotel:
        return jsonify(message='Hotel not found!'), 404

    hotel.name = json_data['name']
    hotel.description = json_data['description']
    db.session.commit()

    return jsonify(message='Record updated!'), 200
