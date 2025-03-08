class RBUser:
    def __init__(self, user_id: int | None = None,
                 first_name: str | None = None,
                 phone_number: str | None = None,
                 email: str | None = None):
        self.id = user_id
        self.first_name = first_name
        self.phone_number = phone_number
        self.email = email


    def to_dict(self) -> dict:
        data = {'id': self.id, 'first_name': self.first_name, 'phone_number': self.phone_number, 
                'email': self.email}
        filt_data = {k: v for k, v in data.items() if v is not None}
        return filt_data
        
