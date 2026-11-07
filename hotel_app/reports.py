from .database import cursor
from .hotel import rooms_objects
import csv
from datetime import datetime, timedelta

def occupancy_reports():
    total_rooms = len(rooms_objects)
    print("\nOccupancy Report")
    try:
        start_date = datetime.strptime(input("Enter start date (DD-MM-YYYY): ").strip(),"%d-%m-%Y").date()
        end_date = datetime.strptime(input("Enter end date (DD-MM-YYYY): ").strip(),"%d-%m-%Y").date()
    except ValueError:
        print("Invalid date format.")
        return
    if end_date <= start_date:
        print("End date must be after start date.")
        return
    if total_rooms == 0:
        print("No rooms registered.")
        return
    current_date = start_date
    total_occupancy = 0
    no_of_days = 0
    while current_date < end_date:
        date_db = current_date.strftime("%Y-%m-%d")
        cursor.execute("""SELECT DISTINCT room_no FROM Booking WHERE check_in <= ? AND check_out > ? AND status NOT IN ('CANCELLED', 'CHECKED_OUT')""", (date_db, date_db))

        occupied_rooms = cursor.fetchall()
        occupied_room_numbers = [room[0] for room in occupied_rooms]

        occ_cnt = len(occupied_room_numbers)
        available_rooms = []

        for room in rooms_objects:
            if room.room_no not in occupied_room_numbers:
                available_rooms.append(room.room_no)
        occ_percent = (occ_cnt / total_rooms) * 100

        print("\nDate:", current_date.strftime("%d-%m-%Y"))
        print("Occupied Room Numbers:", occupied_room_numbers)
        print("Number of occupied rooms:", occ_cnt)
        print("Total number of rooms:", total_rooms)
        print("Occupancy Percentage:", round(occ_percent, 2), "%")

        total_occupancy += occ_percent
        no_of_days += 1
        current_date += timedelta(days=1)
    average_occupancy = total_occupancy / no_of_days
    print("\nAverage Occupancy Percentage:",
          round(average_occupancy, 2), "%")


def revenue_report():
    room_types = ["Standard", "Deluxe", "Suite"]

    print("\nREVENUE REPORT")
    for room_type in room_types:
        room_numbers = []
        for room in rooms_objects:
            if room.room_type == room_type:
                room_numbers.append(room.room_no)
        completed_stays = 0
        room_revenue = 0
        gst_collected = 0
        cancellation_amount = 0
        if room_numbers:
            placeholders = ",".join("?" for room in room_numbers)
            cursor.execute(f"""select COUNT(*), sum(room_charges), sum(gst_amount) from Booking
                where room_no IN ({placeholders}) and status = 'CHECKED_OUT'""", room_numbers)
            result = cursor.fetchone()

            completed_stays = result[0]
            room_revenue = result[1] if result[1] is not None else 0
            gst_collected = result[2] if result[2] is not None else 0

            cursor.execute(f"""select SUM(cancellation_amount_kept) from Booking where room_no IN ({placeholders}) and status = 'CANCELLED'""", room_numbers)
            result = cursor.fetchone()
            cancellation_amount = result[0] if result[0] is not None else 0
        print("\nRoom Type:", room_type)
        print("Completed Stays:", completed_stays)
        print("Room Revenue:", round(room_revenue, 2))
        print("GST Collected:", round(gst_collected, 2))
        print("Amount Kept from Cancellations:", round(cancellation_amount, 2))


def export_bookings():
    cursor.execute("SELECT * FROM Booking")
    bookings = cursor.fetchall()
    if len(bookings) == 0:
        print("No bookings available to export")
        return
    cursor.execute("SELECT * FROM Guests")
    guests = cursor.fetchall()
    guest_details = {}
    for guest in guests:
        guest_details[guest[0]] = {
            "name": guest[1],
            "email": guest[2]
        }

    with open("bookings_export.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Booking ID", "Mobile Number", "Guest Name", "Email",
            "Room Number", "Check-in", "Check-out", "Number of Guests",
            "Breakfast", "Status", "Total Amount", "Room Charges",
            "GST", "Cancellation Amount Kept"
        ])

        for booking in bookings:
            mobile_no = booking[1]
            guest = guest_details[mobile_no]

            writer.writerow([
                f"BK{booking[0] + 999}",
                mobile_no,
                guest["name"],
                guest["email"],
                booking[2],
                booking[3],
                booking[4],
                booking[5],
                booking[6],
                booking[7],
                booking[8],
                booking[9],
                booking[10],
                booking[11]
            ])

    print("All bookings exported successfully!")
    print("File saved as: bookings_export.csv")

    