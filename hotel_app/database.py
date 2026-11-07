
import sqlite3
conn = sqlite3.connect(r"C:\Users\sunitha.chakravaram\OneDrive - Acuvate Software Private Limited\Desktop\hotel_reservation\bookings.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")
cursor.execute("""create table if not exists Guests(
    mobile_no text primary key,
    name text not null,
    email text not null)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Booking(
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mobile_no TEXT NOT NULL,
    room_no INTEGER NOT NULL,
    check_in TEXT NOT NULL,
    check_out TEXT NOT NULL,
    no_of_guests INTEGER NOT NULL,
    breakfast_choice TEXT NOT NULL DEFAULT 'no',
    status TEXT NOT NULL,
    total_amount REAL NOT NULL,
    room_charges REAL DEFAULT 0,
    gst_amount REAL DEFAULT 0,
    cancellation_amount_kept REAL DEFAULT 0,
    FOREIGN KEY(mobile_no) REFERENCES Guests(mobile_no))
""")

conn.commit()
print("Tables created successfully")

def guest_registration():
    try:
        mobile_no = input("Enter mobile number: ").strip()
        while (len(mobile_no) != 10 or not mobile_no.isdigit() or mobile_no[0] not in "6789"):
            print("Invalid mobile number. Please enter a valid 10-digit number.")
            mobile_no = input("Enter mobile number: ").strip()
        cursor.execute("SELECT * FROM Guests WHERE mobile_no = ?",(mobile_no,))
        guest = cursor.fetchone()
        if guest:
            print("\nAlready registered Guest")
            print("Guest Name:", guest[1])
            print("Mobile Number:", guest[0])
            print("Email:", guest[2])
        else:
            print("\nNew Guest")
            name = input("Enter name: ").strip()
            while name == "":
                print("Name cannot be empty")
                name = input("Enter name: ").strip()
            email = input("Enter email: ").strip()
            while "@" not in email or "." not in email:
                print("Invalid email address")
                email = input("Enter email: ").strip()
            cursor.execute("""
                INSERT INTO Guests(mobile_no, name, email)
                VALUES (?, ?, ?)""", (mobile_no, name, email))
            conn.commit()
            print("Guest registered successfully!")
        return mobile_no
    except ValueError as e:
        print("Invalid guest details:", e)
        return None
