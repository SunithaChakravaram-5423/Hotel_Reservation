from abc import ABC, abstractmethod
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