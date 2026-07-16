from sqlalchemy.exc import SQLAlchemyError

from app.database.base import Base, engine


def init_db() -> None:
    try:
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError as exc:
        print(f"Initialisation de la base de données ignorée : {exc}")
