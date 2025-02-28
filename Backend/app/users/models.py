from sqlalchemy.orm import Mapped
from app.database import Base, str_uniq, int_pk


class User(Base):
    id: Mapped[int_pk]
    first_name: Mapped[str]
    phone_number: Mapped[str_uniq]
    email: Mapped[str]


    def __str__(self):
        return (f'{self.__class__.__name__}(id={self.id}), '
                f"first_name={self.first_name!r}")
    
    def __repr__(self):
        return str(self)
    
    def to_dict(self):
        return{
        "id": self.id,
        "first_name": self.first_name,
        "phone_number": self.phone_number,
        "email": self.email,
        }   