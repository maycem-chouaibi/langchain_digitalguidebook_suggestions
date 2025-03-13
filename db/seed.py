from models import User
from crud import create_record, get_record_by_id, update_record, delete_record

new_user = create_record(User, first_name="Alice", last_name="Cooper", phone="123", phone_ext="+33", email="alice@example.com", dob="01/01/1999", gender="female")
# print(new_user)
# user = get_record_by_id(User, new_user.id)
# print(user)
# updated_user = update_record(User, new_user.id, first_name="James")
# print(updated_user)
# delete_status = delete_record(User, new_user.id)
# print(delete_status)