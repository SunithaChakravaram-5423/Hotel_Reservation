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
