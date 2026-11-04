from rooms_csv import load_rooms

room_objects, valid_rooms, invalid_rooms = load_rooms()

for room in room_objects():
    print("\nRoom Number:", room.room_no)
    print("Room Type:", room.room_type)
    print("Floor:", room.floor)
    print("Base Rate:", room.base_rate())
    print("Maximum Guests:", room.maximum_guests())