
from datetime import timedelta
from .database import cursor
def calculate_price(lowest_room, check_in_date, check_out_date, no_of_guests, mobile_no, breakfast_choice):
    no_of_nights = (check_out_date - check_in_date).days
    base_rate = lowest_room.base_rate()
    room_charges = 0
    gst = 0
    today_date = check_in_date
    while today_date < check_out_date:
        daily_rate = base_rate
        extra_guest_charge = lowest_room.extra_guest_charge(no_of_guests)
        daily_rate += extra_guest_charge
        breakfast_charge = lowest_room.breakfast(no_of_guests, breakfast_choice)
        daily_rate += breakfast_charge
        if today_date.weekday() in (4, 5):
            extra_charge = base_rate * 0.20
            daily_rate += extra_charge
        room_charges += daily_rate
        today_date += timedelta(days=1)
    if no_of_nights >= 7:
        discount = room_charges * 0.10
        room_charges -= discount
    cursor.execute("""SELECT COUNT(*) FROM Booking WHERE status = 'CHECKED_OUT' AND mobile_no = ?""", (mobile_no,))
    cnt = cursor.fetchone()[0]
    if cnt >= 3:
        loyalty_discount = room_charges * 0.05
        room_charges -= loyalty_discount
    gst = 0
    today_date = check_in_date
    while today_date < check_out_date:
        daily_rate = base_rate
        extra_guest_charge = lowest_room.extra_guest_charge(no_of_guests)
        daily_rate += extra_guest_charge
        breakfast_charge = lowest_room.breakfast(no_of_guests, breakfast_choice)
        daily_rate += breakfast_charge
        if today_date.weekday() in (4, 5):
            daily_rate += base_rate * 0.20
        if daily_rate <= 7500:
            gst_rate = 0.12
        else:
            gst_rate = 0.18
        if no_of_nights >= 7:
            daily_rate -= daily_rate * 0.10
        if cnt >= 3:
            daily_rate -= daily_rate * 0.05
        gst += daily_rate * gst_rate
        today_date += timedelta(days=1)
    room_charges = round(room_charges, 2)
    gst = round(gst, 2)
    total_amount = round(room_charges + gst, 2)

    return room_charges, gst, total_amount