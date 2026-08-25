from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..repositories import LocalTransportRepository
from ..schemas.local_transport import LocalTransportCreate, LocalTransportBook


class LocalTransportService:
    def __init__(self, db: Session):
        self.repo = LocalTransportRepository(db)

    def get(self, transport_id: int):
        return self.repo.get_or_404(transport_id)

    def search(self, transport_type=None, departure_city=None, arrival_city=None,
               min_price=None, max_price=None, skip=0, limit=50):
        return self.repo.search(
            transport_type=transport_type, departure_city=departure_city,
            arrival_city=arrival_city, min_price=min_price, max_price=max_price,
            skip=skip, limit=limit
        )

    def create(self, payload: LocalTransportCreate):
        return self.repo.create(payload.model_dump())

    def delete(self, transport_id: int) -> None:
        self.repo.delete(transport_id)

    def book_seats(self, transport_id: int, payload: LocalTransportBook):
        transport = self.repo.get_or_404(transport_id)
        if transport.available_seats < payload.seats_to_book:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Only {transport.available_seats} seats available, cannot book {payload.seats_to_book}"
            )
        transport.available_seats -= payload.seats_to_book
        db = self.repo.db
        db.commit()
        db.refresh(transport)

        return {
            "transport_id": transport.transport_id,
            "provider_name": transport.provider_name,
            "route_name": transport.route_name,
            "transport_type": transport.transport_type,
            "seats_booked": payload.seats_to_book,
            "price_per_seat": float(transport.price_per_person),
            "total_price": round(float(transport.price_per_person) * payload.seats_to_book, 2),
            "remaining_seats": transport.available_seats,
        }
