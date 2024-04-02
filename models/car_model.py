from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import db

class CarModel(db.Model):

    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    model = Column(String, nullable=False)
    make = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    sales = relationship("SaleReceiptModel", back_populates="car_sold", lazy='dynamic')


    def save_car(self):
        db.session.add(self)
        db.session.commit()


    def del_car(self):
        db.session.delete(self)
        db.session.commit()

    
    def from_dict(self, car_dict):
        for k, v in car_dict.items():
            if k != 'password':
                setattr(self, k, v)
            else:
                setattr(self, 'password_hash', generate_password_hash(v))


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)