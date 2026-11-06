from .models import Guest, Room, StandardRoom, DeluxeRoom, SuiteRoom
import csv

def load_rooms():
    rooms=[]
    file_path = r"C:\Users\sunitha.chakravaram\OneDrive - Acuvate Software Private Limited\Desktop\hotel_reservation\rooms.csv"
    with open(file_path, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rooms.append(row)
            print(row)

    valid_rooms=[]
    invalid_rooms=[]
    room_numbers =set()
    for row in rooms:
        errors=[]
        if row["room_no"].strip() =="":
            errors.append("Roomm number must not be emptyy")
        elif not row["room_no"].strip().isdigit():
            errors.append("Room number must be numeric")
        elif row["room_no"].strip() in room_numbers:
            errors.append("Duplicate room number")
        else:
            room_numbers.add(row["room_no"].strip())
        if row["room_type"].strip().capitalize() not in ("Standard", "Deluxe", "Suite"):
            errors.append("NO such type of rooms")
        try:
            floor = int(row["floor"])
            if floor <= 0:
                errors.append("Floor value is invalid")
        except ValueError:
            errors.append("Floor must be a valid integer")
        
        if not errors:
            valid_rooms.append(row)
        else:
            invalid_rooms.append(row)
            with open(r"C:\Users\sunitha.chakravaram\OneDrive - Acuvate Software Private Limited\Desktop\hotel_reservation\app.log", "a", newline="") as error_file:
                for error in errors:
                    error_file.write(f"{row} : {error}\n")
    
    rooms_objects = []
    for row in valid_rooms:
        room_no = int(row["room_no"])
        room_type = row["room_type"].strip().capitalize()
        floor = int(row["floor"])
        
        if room_type == "Standard":
            room = StandardRoom(room_no, room_type, floor)
            
        elif room_type == "Deluxe":
            room = DeluxeRoom(room_no, room_type, floor)
        
        elif room_type == "Suite":
            room = SuiteRoom(room_no, room_type, floor)
            
        rooms_objects.append(room)
    return rooms_objects, valid_rooms, invalid_rooms

rooms_objects, valid_rooms, invalid_rooms = load_rooms()

print("Valid Rooms : ", len(valid_rooms))
print("Invalid Rooms : ", len(invalid_rooms))
for room in rooms_objects:
    print("\nRoom Number:", room.room_no)
    print("Room Type:", room.room_type)
    print("Floor:", room.floor)
    print("Base Rate:", room.base_rate())
    print("Maximum Guests:", room.maximum_guests())
