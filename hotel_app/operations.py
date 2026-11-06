from datetime import datetime, date, timedelta
from .database import conn, cursor, guest_registration
from .hotel import rooms_objects
from .pricing import calculate_price
def Booking():
    mobile_no = guest_registration()
    if mobile_no is None:
        return
    room_type = input("Enter room type: ").strip().capitalize()
    if room_type not in ("Standard", "Deluxe", "Suite"):
        print("Invalid room type")
        return

    while True:
        try:
            no_of_guests = int(input("Enter number of guests: "))
            if no_of_guests < 1:
                print("At least 1 guest is required")
            else:
                break
        except ValueError:
            print("Please enter a valid number")

    check_in = input("Enter check-in date (DD-MM-YYYY): ").strip()
    check_out = input("Enter check-out date (DD-MM-YYYY): ").strip()

    try:
        check_in_date = datetime.strptime(check_in, "%d-%m-%Y").date()
        check_out_date = datetime.strptime(check_out, "%d-%m-%Y").date()
        today = date.today()
        if check_in_date < today:
            print("Check-in date cannot be in the past")
            return
        if check_in_date > today + timedelta(days=180):
            print("Check-in date cannot be more than 180 days from today")
            return
        if check_out_date <= check_in_date:
            print("Check-out date must be after check-in date")
            return
        no_of_nights = (check_out_date - check_in_date).days
        if no_of_nights > 30:
            print("Maximum stay allowed is 30 nights")
            return
        check_in_db = check_in_date.strftime("%Y-%m-%d")
        check_out_db = check_out_date.strftime("%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please enter dates in DD-MM-YYYY format.")
        return

    available_rooms = []
    for room in rooms_objects:
        if room.room_type == room_type and no_of_guests <= room.maximum_guests():
            cursor.execute("SELECT COUNT(*) FROM Booking WHERE room_no = ? AND check_in < ? AND check_out > ? AND status NOT IN ('CANCELLED','CHECKED_OUT')", (room.room_no, check_out_db, check_in_db))
            cnt = cursor.fetchone()[0]
            if cnt == 0:
                available_rooms.append(room)
    if available_rooms:
        lowest_room = available_rooms[0]
        for room in available_rooms:
            if room.room_no < lowest_room.room_no:
                lowest_room = room
        print("\nRoom allocated successfully")
        print("Room Number:", lowest_room.room_no)
        print("Room Type:", lowest_room.room_type)
    else:
        print("\nNo rooms are available for the guest requested type")
        all_room_types = ["Standard", "Deluxe", "Suite"]
        alternative_rooms = []
        for room in all_room_types:
            if room_type == room:
                continue
            for rooms in rooms_objects:
                if rooms.room_type == room and no_of_guests <= rooms.maximum_guests():
                    cursor.execute("SELECT COUNT(*) FROM Booking WHERE room_no = ? AND check_in < ? AND check_out > ? AND status NOT IN ('CANCELLED','CHECKED_OUT')", (rooms.room_no, check_out_db, check_in_db))
                    cnt = cursor.fetchone()[0]
                    if cnt == 0:
                        alternative_rooms.append(rooms)
        if alternative_rooms:
            print("Available alternative rooms:")
            for room in alternative_rooms:
                print(room.room_type, room.room_no)
        else:
            print("No alternative rooms available")
        return

    print("Number of nights:", no_of_nights)
    
    breakfast_choice = "no"
    if room_type == "Standard":
        breakfast_choice = input("Do you want breakfast? (yes/no): ").strip().lower()

        while breakfast_choice not in ("yes", "no"):
            print("Please enter yes or no")
            breakfast_choice = input("Do you want breakfast? (yes/no): ").strip().lower()
            
    room_charges, gst, total_amount = calculate_price(lowest_room,check_in_date,check_out_date,no_of_guests,mobile_no, breakfast_choice)
    
    print("\n---------- FINAL BILL ----------")
    print("Room Number:", lowest_room.room_no)
    print("Room Type:", lowest_room.room_type)
    print("Number of Guests:", no_of_guests)
    print("Number of Nights:", no_of_nights)
    print("Room Charges:", round(room_charges, 2))
    print("GST:", round(gst, 2))
    print("Total Amount Payable:", round(total_amount, 2))
    
    
    payment = input("\nProceed with full payment? (yes/no): ").strip().lower()

    if payment == "yes":
        cursor.execute("""INSERT INTO Booking(mobile_no, room_no, check_in, check_out, no_of_guests, status, total_amount) VALUES (?, ?, ?, ?, ?, ?, ?)""", (mobile_no, lowest_room.room_no, check_in_db, check_out_db, no_of_guests, "CONFIRMED", round(total_amount, 2)))
        conn.commit()
        booking_id = cursor.lastrowid
        print("\nPayment successful!")
        print("Booking confirmed!")
        print("Booking ID:", booking_id)
    else:
        print("\nPayment cancelled. Booking not confirmed.")
        
     