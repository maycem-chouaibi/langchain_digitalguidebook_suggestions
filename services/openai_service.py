from pydantic import BaseModel, Field
from datetime import date
from supabase_service import get_reservation_data, get_reservation_by_id
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
class Reservation(BaseModel):
    id: int = Field(...)
    n_confirmation: str = Field(...)
    guest_name: str = Field(..., min_length=1)
    nb_adults: int = Field(..., gt=0)
    nb_children: int = Field(...)
    nb_babies: int = Field(...)
    listing: str = Field(..., min_length=1)
    is_new_guest: bool = Field(True)
    start_date: date = Field(...)
    end_date: date = Field(...)
    reservation_date: date = Field(...)
    contact: str = Field(...)
    
def create_reservation_string(reservation: Reservation):
    stay_duration = (reservation.end_date - reservation.start_date).days
    
    start_date_str = reservation.start_date.strftime("%Y-%m-%d")
    end_date_str = reservation.end_date.strftime("%Y-%m-%d")
    reservation_date_str = reservation.reservation_date.strftime("%Y-%m-%d")
    
    total_guests = reservation.nb_adults + reservation.nb_children + reservation.nb_babies
    
    reservation_text = f"""
    Reservation ID: {reservation.id}
    Confirmation Number: {reservation.n_confirmation}
    Guest: {reservation.guest_name} ({'new guest' if reservation.is_new_guest else 'returning guest'})
    Contact: {reservation.contact}
    Property: {reservation.listing}
    Stay Period: {start_date_str} to {end_date_str} ({stay_duration} nights)
    Booked On: {reservation_date_str}
    Guests: {total_guests} total ({reservation.nb_adults} adults, {reservation.nb_children} children, {reservation.nb_babies} babies)
    """
    
    return reservation_text.strip()

def parse_reservation(item: dict) -> Reservation:
    start_date = date.fromisoformat(item['start_date'])
    end_date = date.fromisoformat(item['end_date'])
    reservation_date = date.fromisoformat(item['reservation_date'])
    
    reservation = Reservation(
        id=item['id'],
        n_confirmation=item['n_confirmation'],
        guest_name=item['guest_name'],
        nb_adults=item['nb_adults'],
        nb_children=item['nb_children'],
        nb_babies=item['nb_babies'],
        listing=item['listing'],
        is_new_guest=item['is_new_guest'],
        start_date=start_date,
        end_date=end_date,
        reservation_date=reservation_date,
        contact=item['contact']
    )
    
    return reservation

def get_embedding(text, model="text-embedding-3-small"):
    embeddings_model = OpenAIEmbeddings(model= model, api_key=OPENAI_KEY)
    embedding = embeddings_model.embed_query(text) 

    return embedding

def create_embeddings(reservation_id: int):
    embeddings = []
    reservation = parse_reservation(get_reservation_by_id(reservation_id).data)
    content = create_reservation_string(reservation)
    embedding = get_embedding(content)
    embeddings.append(embedding)

    return embeddings

create_embeddings(123)

