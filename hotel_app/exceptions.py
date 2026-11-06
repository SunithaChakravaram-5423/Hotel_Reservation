class HotelReservationError(Exception):
    pass


class RoomUnavailableError(HotelReservationError):
    pass


class InvalidDateError(HotelReservationError):
    pass


class InvalidStatusChangeError(HotelReservationError):
    pass


class BookingNotFoundError(HotelReservationError):
    pass