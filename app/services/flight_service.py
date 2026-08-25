from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..repositories import FlightRepository
from ..schemas.flight import FlightCreate, FlightUpdate, FlightBookSeat


class FlightService:
    def __init__(self, db: Session):
        self.repo = FlightRepository(db)

    def get(self, flight_id: int):
        return self.repo.get_or_404(flight_id)

    def search(self, departure_city=None, arrival_city=None, min_price=None, max_price=None,
               skip=0, limit=50):
        return self.repo.search(departure_city=departure_city, arrival_city=arrival_city,
                                min_price=min_price, max_price=max_price, skip=skip, limit=limit)

    def create(self, payload: FlightCreate):
        return self.repo.create(payload.model_dump())

    def update(self, flight_id: int, payload: FlightUpdate):
        return self.repo.update(flight_id, payload.model_dump(exclude_unset=True))

    def delete(self, flight_id: int) -> None:
        self.repo.delete(flight_id)

    def book_seats(self, flight_id: int, payload: FlightBookSeat):
        flight = self.repo.get_or_404(flight_id)
        if flight.available_seats < payload.seats_to_book:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Only {flight.available_seats} seats available, cannot book {payload.seats_to_book}"
            )
        flight.available_seats -= payload.seats_to_book
        self.db = self.repo.db
        self.db.commit()
        self.db.refresh(flight)

        if payload.cabin_class == "First":
            unit_price = float(flight.price_first_class or flight.price_business or flight.price_economy * 2.5)
        elif payload.cabin_class == "Business":
            unit_price = float(flight.price_business or flight.price_economy * 1.8)
        else:
            unit_price = float(flight.price_economy)

        return {
            "flight_id": flight.flight_id,
            "flight_number": flight.flight_number,
            "airline": flight.airline,
            "seats_booked": payload.seats_to_book,
            "cabin_class": payload.cabin_class,
            "price_per_seat": unit_price,
            "total_price": round(unit_price * payload.seats_to_book, 2),
            "remaining_seats": flight.available_seats,
        }
