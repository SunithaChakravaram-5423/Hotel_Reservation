from abc import ABC, abstractmethod
from datetime import datetime, date, timedelta
from .exceptions import InvalidDateError, InvalidStatusChangeError

class Room(ABC):
    def __init__(self, room_no, room_type, floor):
        self.room_no = room_no
        self.room_type=room_type
        self.floor =  floor
    
    def __str__(self):
        return (f"Room Number: {self.room_no}\n"
        f"Room Type: {self.room_type}\n"
        f"Floor: {self.floor}")
        
    @abstractmethod
    def base_rate(self):
        pass
    
    @abstractmethod
    def extra_guest_charge(self, no_of_guests):
        pass
    
    @abstractmethod
    def breakfast(self, no_of_guests, choice=None):
        pass
    
    @abstractmethod
    def maximum_guests(self):
        pass 
     
        
class StandardRoom(Room):
    def __init__(self, room_no, room_type, floor):
        super().__init__(room_no, room_type, floor)
    def base_rate(self):
        return 2500
    
    def extra_guest_charge(self, no_of_guests):
        return 0
    
    def breakfast(self, no_of_guests,choice=None):
        if choice is not None and choice.strip().lower() == "yes":
            return no_of_guests*350
        return 0
    
    def maximum_guests(self):
        return 2

class DeluxeRoom(Room):
    def __init__(self, room_no, room_type, floor):
        super().__init__(room_no, room_type, floor)
        
    def base_rate(self):
        return 4000
    
    def extra_guest_charge(self, no_of_guests):
        return max(0, no_of_guests - 2)*800
    
    def breakfast(self, no_of_guests,choice=None):
        return 0
    
    def maximum_guests(self):
        return 3

class SuiteRoom(Room):
    def __init__(self, room_no, room_type, floor):
        super().__init__(room_no, room_type, floor)
    def base_rate(self):
        return 7500
    
    def extra_guest_charge(self, no_of_guests):
        return max(0, no_of_guests - 2)*800
    
    def breakfast(self, no_of_guests,choice=None):
        return 0
    
    def maximum_guests(self):
        return 4
    

class Guest:
    def __init__(self, name, mobile_no, email, no_of_guests):
        self.set_name(name)
        self.set_mobile(mobile_no)
        self.set_email(email)
        self.set_guests(no_of_guests)
        
    def set_name(self, name):
        if name.strip() == "":
            raise ValueError("Name cannot be emptyy")
        self.__name = name.strip()
    def get_name(self):
        return self.__name
    def set_mobile(self, mobile_no):
        mobile_no = mobile_no.strip()
        if len(mobile_no) != 10 or not mobile_no.isdigit() or int(mobile_no[0]) not in [6,7,8,9]:
            raise ValueError("Invalid mobile number")
        self.__mobile_no = mobile_no
    def get_mobile(self):
        return self.__mobile_no
    def set_email(self, email):
        email = email.strip()
        if "@" not in email or "." not in email:
            raise ValueError("Invalid email address")
        self.__email = email
    def get_email(self):
        return self.__email
    def set_guests(self, no_of_guests):
        no_of_guests = int(no_of_guests)
        if no_of_guests < 1:
            raise ValueError("invalid guest number")
        self.__no_of_guests = no_of_guests
    def get_guests(self):
        return self.__no_of_guests
    
    def __str__(self):
        return (f"Guest Name: {self.__name}\n"
            f"Mobile Number: {self.__mobile_no}\n"
            f"Email: {self.__email}\n"
            f"Number of Guests: {self.__no_of_guests}")
        

class Booking():
    def __init__(self, booking_id, guest, room, check_in, check_out, total_amount):
        self.set_booking_id(booking_id)
        self.set_guest(guest)
        self.set_room(room)
        self.set_check_in(check_in)
        self.set_check_out(check_out)
        self.__status = "CONFIRMED"
        self.set_total_amount(total_amount)

    def set_booking_id(self, booking_id):
        if not booking_id.startswith("BK") or not booking_id[2:].isdigit():
            raise ValueError("Invalid Booking ID format")
        self.__booking_id = booking_id
    def get_booking_id(self):
        return self.__booking_id
    
    def set_guest(self, guest):
        if not isinstance(guest, Guest):
            raise ValueError("Ivalid guest object")
        self.__guest = guest
    def get_guest(self):
        return self.__guest
    
    def set_room(self, room):
        if not isinstance(room, Room):
            raise ValueError("INvalid room objects")
        self.__room = room
    def get_room(self):
        return self.__room
    
    def set_check_in(self, check_in):
        try:
            check_in = datetime.strptime(check_in,"%d-%m-%Y").date()
        except ValueError:
            raise ValueError("INvalid Check-in date fromat")
        today = date.today()
        if check_in < today or check_in > today + timedelta(days=180):
            raise InvalidDateError("Date must be today or 180 days from today")
        self.__check_in = check_in
    def get_check_in(self):
        return self.__check_in
    
    def set_check_out(self, check_out):
        try:
            check_out = datetime.strptime(check_out,"%d-%m-%Y").date()
        except ValueError:
            raise ValueError("Invalid check out date format")
        if check_out <= self.__check_in:
            raise ValueError("Check out should be after checkin")
        no_of_nights = (check_out - self.__check_in).days
        if (no_of_nights < 1 or no_of_nights > 30):
            raise InvalidDateError("Can't stay more than 30 days")
        self.__check_out = check_out
    def get_check_out(self):
        return self.__check_out
    
    def set_status(self, status):
        status = status.strip().upper()
        if status not in ("CONFIRMED", "CHECKED_IN", "CHECKED_OUT", "CANCELLED"):
            raise InvalidStatusChangeError("Invalid status")
        if self.__status == "CONFIRMED":
            if status not in("CHECKED_IN", "CANCELLED"):
                raise InvalidStatusChangeError("Only check_in or cancelled after confirmed")
        elif self.__status == "CHECKED_IN":
            if status != "CHECKED_OUT":
                raise InvalidStatusChangeError("Only has to check out after check in")
        else:
            raise InvalidStatusChangeError("Any other status change must be rejected")
        self.__status = status
    
    def get_status(self):
        return self.__status
    
    
    def set_total_amount(self, total_amount):
        if total_amount < 0:
            raise ValueError("Amount cannot be negative")

        self.__total_amount = total_amount

    def get_total_amount(self):
        return self.__total_amount
    
    def __str__(self):
        return (f"Booking Id: {self.__booking_id}\n"
                f"Guest Details: {self.__guest}\n"
                f"Room Details: {self.__room}\n"
                f"Chech-in Time: {self.__check_in}\n"
                f"Check_out time: {self.__check_out}\n"
                f"Status : {self.__status}\n"
                f"Total Amount: {self.__total_amount}")
