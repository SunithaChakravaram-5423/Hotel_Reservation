from datetime import datetime, date, timedelta
from .database import conn, cursor, guest_registration
from .hotel import rooms_objects
from .pricing import calculate_price
from .exceptions import RoomUnavailableError, BookingNotFoundError, InvalidStatusChangeError, InvalidDateError

def search_availability():
    room_type = input("Enter room type: ").strip().capitalize()

    if room_type not in ("Standard", "Deluxe", "Suite"):
        print("Invalid room type")
        return
    try:
        no_of_guests = int(input("Enter number of guests: "))
        if no_of_guests < 1:
            print("At least 1 guest is required")
            return
        check_in = input("Enter check-in date (DD-MM-YYYY): ").strip()
        check_out = input("Enter check-out date (DD-MM-YYYY): ").strip()

        check_in_date = datetime.strptime(check_in, "%d-%m-%Y").date()
        check_out_date = datetime.strptime(check_out, "%d-%m-%Y").date()

        today = date.today()
        if check_in_date < today:
            print("Check-in date cannot be in the past")
            return
        if check_in_date > today + timedelta(days=180):
            print("Check-in date cannot be more than 180 days ahead")
            return
        if check_out_date <= check_in_date:
            print("Check-out must be after check-in")
            return
        no_of_nights = (check_out_date - check_in_date).days
        if no_of_nights > 30:
            print("Maximum stay allowed is 30 nights")
            return
        check_in_db = check_in_date.strftime("%Y-%m-%d")
        check_out_db = check_out_date.strftime("%Y-%m-%d")
    except ValueError:
        print("Invalid input. Please enter valid dates and guest count.")
        return
    
    available_rooms = []
    for room in rooms_objects:
        if room.room_type == room_type and no_of_guests <= room.maximum_guests():
            cursor.execute("""
                SELECT COUNT(*)
                FROM Booking
                WHERE room_no = ?
                AND check_in < ?
                AND check_out > ?
                AND status NOT IN ('CANCELLED', 'CHECKED_OUT')
            """, (room.room_no, check_out_db, check_in_db))
            cnt = cursor.fetchone()[0]
            if cnt == 0:
                available_rooms.append(room)

    print("\nRoom Availability")
    if available_rooms:
        print("Available rooms for", room_type)
        for room in available_rooms:
            print("Room Number:", room.room_no)
        print("Total available rooms:", len(available_rooms))
    else:
        print("No rooms available for the requested room type.")
    if not available_rooms:
        alternative_rooms = []
        for room in rooms_objects:
            if room.room_type != room_type and no_of_guests <= room.maximum_guests():
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM Booking
                    WHERE room_no = ?
                    AND check_in < ?
                    AND check_out > ?
                    AND status NOT IN ('CANCELLED', 'CHECKED_OUT')
                """, (room.room_no, check_out_db, check_in_db))
                cnt = cursor.fetchone()[0]
                if cnt == 0:
                    alternative_rooms.append(room)
        if alternative_rooms:
            print("\nAvailable alternative rooms:")
            for room in alternative_rooms:
                print("Room Type:", room.room_type,"     Room Number:", room.room_no)
        else:
            print("No alternative rooms available.")
    print("\nNumber of Nights:", no_of_nights)



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
        raise RoomUnavailableError("No room of the requested type is available for these dates.")

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
        cursor.execute("""INSERT INTO Booking(mobile_no, room_no, check_in, check_out, no_of_guests, breakfast_choice, status, total_amount, room_charges, gst_amount) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (mobile_no, lowest_room.room_no, check_in_db, check_out_db, no_of_guests, breakfast_choice, "CONFIRMED", round(total_amount, 2), round(room_charges, 2), round(gst, 2)))
        conn.commit()
        booking_id = cursor.lastrowid
        display_id = f"BK{booking_id + 999}"
        print("\nPayment successful!")
        print("Booking confirmed!")
        print("Booking ID:", display_id)
    else:
        print("\nPayment cancelled. Booking not confirmed.")
        
        
def check_in():
    booking_id = input("ENter booking Id: ").strip()
    if not booking_id.startswith("BK") or not booking_id[2:].isdigit():
        print("Invalid booking ID")
        return
    db_booking_id = int(booking_id[2:])-999
    if db_booking_id <= 0:
        print("Invalid booking Id")
        return
    cursor.execute("""SELECT booking_id, mobile_no, room_no, check_in, check_out, no_of_guests, status, total_amount, breakfast_choice
    FROM Booking WHERE booking_id = ?""", (db_booking_id,))
    booking = cursor.fetchone()
    
    if booking is None:
        raise BookingNotFoundError("Booking ID does not exist")
    if booking[6] != "CONFIRMED":
        raise InvalidStatusChangeError("Booking status is not confirmed yet")
    today = date.today().strftime("%Y-%m-%d")
    if booking[3] != today:
        raise InvalidDateError("Invalid check-in date, Check-in is allowed only on the booking check-in date")
    
    cursor.execute("update booking set status = ? where booking_id = ?", ("CHECKED_IN", db_booking_id))
    conn.commit()
    
    print("Check-in successfully")
    print("Booking ID:", booking_id)
    print("Room Number:", booking[2])      
     
def check_out():
    booking_id = input("Enter booking ID: ").strip()
    if not booking_id.startswith("BK") or not booking_id[2:].isdigit():
        print("Invalid booking ID format")
        return
    db_booking_id = int(booking_id[2:]) - 999
    if db_booking_id <= 0:
        print("Invalid booking ID")
        return
    cursor.execute("SELECT * FROM Booking WHERE booking_id = ?", (db_booking_id,))
    booking = cursor.fetchone()
    if booking is None:
        raise BookingNotFoundError("Booking ID does not exist")
    if booking[6] != "CHECKED_IN":
        raise InvalidStatusChangeError("Only checked-in bookings can be checked out")
    today = date.today().strftime("%Y-%m-%d")
    if booking[4] != today:
        raise InvalidDateError("Check-out is allowed on the scheduled check-out day")
    cursor.execute("UPDATE Booking SET status = ? WHERE booking_id = ?", ("CHECKED_OUT", db_booking_id))
    conn.commit()
    print("\nCheck-out successful!")
    print("Booking ID:", booking_id)
    print("Room Number:", booking[2])

    generate_invoice(booking)
    
    
def generate_invoice(booking):
    booking_id = booking[0]
    mobile_no = booking[1]
    room_no = booking[2]
    check_in = datetime.strptime(booking[3], "%Y-%m-%d").date()
    check_out = datetime.strptime(booking[4], "%Y-%m-%d").date()
    no_of_guests = booking[5]
    total_amount = booking[7]
    breakfast_choice = booking[8]

    cursor.execute("SELECT name, email FROM Guests WHERE mobile_no = ?",(mobile_no,))
    guest = cursor.fetchone()
    if guest is None:
        print("Guest details not found")
        return

    room = None
    for rooms in rooms_objects:
        if rooms.room_no == room_no:
            room = rooms
            break
    if room is None:
        print("Room details not found")
        return

    no_of_nights = (check_out - check_in).days
    invoice = f"""Stayeasy Hotel Invoice
    Booking Id : BK{booking_id+999}
    Guest Name : {guest[0]}
    Mobile Number : {mobile_no}
    Email : {guest[1]}
    
    Room Number: {room_no}
    Room Type : {room.room_type}
    Number of Guests: {no_of_guests}
    
    Check-in : {check_in}
    Check-out : {check_out}
    Number of Nights : {no_of_nights}
    
    breakfast : {breakfast_choice}
    
    -----------------------------------
    Total Amount Paid : {total_amount:.2f}
    Payment Status : PAID
    Booking Status : CHECKED_OUT
    -----------------------------------
    
    ThankYou visit again........
    """

    file_name = f"invoices/BK{booking_id+999}.txt"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(invoice)
    print("Invoice generated successfully!")
    print("Invoice saved as:", file_name)
    
    
def cancel_booking():
    booking_id = input("Enter booking Id: ").strip()
    if not booking_id.startswith("BK") or not booking_id[2:].isdigit():
        print("Invalid booking ID format")
        return
    db_booking_id = int(booking_id[2:]) - 999
    if db_booking_id <= 0:
        print("Invalid booking ID")
        return
    cursor.execute("SELECT * FROM Booking WHERE booking_id = ?", (db_booking_id,))
    booking = cursor.fetchone()
    if booking is None:
        raise BookingNotFoundError("Booking ID does not exist")
    if booking[7] != "CONFIRMED":
        raise InvalidStatusChangeError("Can't cancel the room now")
    today = date.today()
    check_in_date = datetime.strptime(booking[3], "%Y-%m-%d").date()
    canel_date = (check_in_date - today).days
    if canel_date >= 7:
        refund_amt = booking[8]
    elif canel_date >= 2:
        refund_amt = booking[8] * 0.50
    else:
        refund_amt = 0
    cancellation_amount = round(booking[8] - refund_amt, 2)
    cursor.execute("update Booking set status = ?, cancellation_amount_kept = ? where booking_id = ?", ("CANCELLED", cancellation_amount, db_booking_id))
    conn.commit()
    
    print("Booking cancelled successfully")
    print("Refund Amount is: ", refund_amt)
    print("Cancellation Amount :", cancellation_amount)
    
def view_booking_details():
    booking_id = input("Enter booking Id: ").strip()
    if not booking_id.startswith("BK") or not booking_id[2:].isdigit():
        print("Invalid booking ID format")
        return
    db_booking_id = int(booking_id[2:]) - 999
    if db_booking_id <= 0:
        print("Invalid booking ID")
        return
    cursor.execute("SELECT * FROM Booking WHERE booking_id = ?", (db_booking_id,))
    booking = cursor.fetchone()
    if booking is None:
        raise BookingNotFoundError("Booking ID does not exist")
    print("......Guest details.......")
    cursor.execute("select name, email from Guests where mobile_no = ?", (booking[1],))
    guest = cursor.fetchone()
    if guest is None:
        print("Guest not found")
        return
    
    print("Booking Id: ", f"BK{booking[0] + 999}")
    print("Guest Name:", guest[0])
    print("Mobile Number:", booking[1])
    print("Email:", guest[1])
    print("Room Number:", booking[2])
    print("Check-in:", booking[3])
    print("Check-out:", booking[4])
    print("Number of Guests:", booking[5])
    print("Breakfast:", booking[6])
    print("Total Amount:", booking[8])
    print("Booking Status:", booking[7])
    
    
def guest_stay_history():
    mobile_no = input("ENter mobile number: ")
    cursor.execute("select name, email from Guests where mobile_no = ?", (mobile_no,))
    guest = cursor.fetchone()
    if guest is None:
        print("No guest found")
        return
    cursor.execute("select * from Booking where mobile_no = ?",(mobile_no,))
    bookings = cursor.fetchall()
    if len(bookings) == 0:
        print("No bookings found")
        return
    print("\nGuest Stay History")
    print("Guest Name:", guest[0])
    print("Mobile Number:", mobile_no)
    print("Email:", guest[1])
    
    for booking in bookings:
        print("Booking Id: ", f"BK{booking[0]+999}")
        print("Room Number:", booking[2])
        print("Check-in date: ", booking[3])
        print("Check-out date: ", booking[4])
        print("Total Amount: ", booking[8])
        print("Status: ", booking[7])
    print("\nTotal Number of Bookings:", len(bookings))
    
    
    
