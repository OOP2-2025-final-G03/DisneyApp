from datetime import datetime
import random

from models.db import db
from models.user import User
from models.attraction import Attraction
from models.history import History

def insert_history():
    months = [
        "2025-01","2025-02","2025-03","2025-04",
        "2025-05","2025-06","2025-07","2025-08",
        "2025-09","2025-10","2025-11","2025-12"
    ]

    high_months = ["2025-02","2025-03","2025-07","2025-08"]

    users = list(User.select())
    attractions = list(Attraction.select())

    for m in months:
        y, mo = m.split("-")
        count = random.randint(20, 50) if m in high_months else random.randint(5, 20)

        for _ in range(count):
            dt = datetime(
                int(y),
                int(mo),
                random.randint(1, 28),
                random.randint(9, 21),
                random.randint(0, 59)
            )

            History.create(
                user=random.choice(users),
                attraction=random.choice(attractions),
                history_date=dt
            )

        print(f"{m}: {count} 件追加")

if __name__ == "__main__":
    db.connect(reuse_if_open=True)
    insert_history()
    db.close()
    print("=== 12ヶ月分の履歴作成完了 ===")
