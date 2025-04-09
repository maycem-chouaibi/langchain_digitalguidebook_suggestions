import os
import supabase
from dotenv import load_dotenv

load_dotenv()

url: str = os.getenv("SUPABASE_PROJECT_URL")
key: str = os.getenv("SUPABASE_API_KEY")

def init_client():
    supabaseClient: supabase.Client = supabase.create_client(url, key)
    return supabaseClient

def get_reservation_data():
    client = init_client()
    response = (
        client.table("reservations")
        .select("*")
        .execute()
    )

    return response

def get_reservation_by_id(id: int):
    client = init_client()
    response = (client.table("reservation")
                .select("*")
                .filter(id, "=", id)
                .execute()
                )
    return response
    


