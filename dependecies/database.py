from database import SessionLocal


# Instantiate database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
