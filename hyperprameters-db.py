from sqlalchemy import create_engine, Column, Integer, String, Float, Table, MetaData
from sqlalchemy.orm import declarative_base
from config import DATABASE_URI

Base = declarative_base()

class Hyperparameters(Base):
    __tablename__ = "hyperparameters"
    id = Column(Integer, primary_key=True)
    model_version = Column(String)
    learning_rate = Column(Float)
    batch_size = Column(Integer)
    epochs = Column(Integer)

engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)

def save_hyperparameters(model_version, learning_rate, batch_size, epochs):
    with engine.begin() as connection:
        connection.execute(
            Hyperparameters.__table__.insert(),
            [
                {
                    "model_version": model_version,
                    "learning_rate": learning_rate,
                    "batch_size": batch_size,
                    "epochs": epochs,
                }
            ],
        )
