from .operations import (Booking,check_in,check_out,cancel_booking,view_booking_details,guest_stay_history, search_availability)

from .reports import (occupancy_reports, revenue_report, export_bookings)

from .exceptions import HotelReservationError

def main_menu():
    while True:
        print("\n========== STAYEASY HOTEL ==========")
        print("1. Search Room Availability")
        print("2. Create Booking")
        print("3. Check-in")
        print("4. Check-out")
        print("5. Cancel Booking")
        print("6. View Booking Details")
        print("7. Guest Stay History")
        print("8. Occupancy Report")
        print("9. Revenue Report")
        print("10. Export All Bookings to CSV")
        print("11. Exit")

        choice = input("\nEnter your choice: ").strip()

        try:
            if choice == "1":
                search_availability()

            elif choice == "2":
                Booking()

            elif choice == "3":
                check_in()

            elif choice == "4":
                check_out()

            elif choice == "5":
                cancel_booking()

            elif choice == "6":
                view_booking_details()

            elif choice == "7":
                guest_stay_history()

            elif choice == "8":
                occupancy_reports()

            elif choice == "9":
                revenue_report()

            elif choice == "10":
                export_bookings()

            elif choice == "11":
                print("Thank you for using StayEasy Hotel!")
                break

            else:
                print("Invalid choice. Please select between 1 and 11.")

        except HotelReservationError as e:
            print("Error:", e)

        except ValueError as e:
            print("Invalid input:", e)
