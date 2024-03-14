from db_connection import engine, Task
from sqlalchemy.orm import Session

with Session(engine) as session:
    for i in range(1, 26):
        session.add(Task(name=f"Task {i}"))
    session.commit()