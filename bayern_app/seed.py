import datetime
from src.db.database import SessionLocal
from src.db import models

def seed_database():
    db = SessionLocal()
    
    # 1. Проверяем, есть ли уже матчи (чтобы не дублировать при повторном запуске)
    match = db.query(models.Match).first()
    
    if not match:
        print("Создаем тестовый матч...")
        match = models.Match(
            opponent="Borussia Dortmund",
            is_home=True,
            date_match=datetime.date(2024, 11, 10) # Вымышленная дата
        )
        db.add(match)
        db.commit()
        db.refresh(match)
        print(f"Матч создан! ID: {match.id}")
    else:
        print(f"Матч уже существует (ID: {match.id}). Пропускаем создание.")

    # 2. Проверяем, есть ли уже места для этого матча
    existing_seats = db.query(models.Seat).filter(models.Seat.match_id == match.id).count()
    
    if existing_seats == 0:
        print("Генерируем 50 мест на стадионе...")
        seats_to_add = []
        
        # Сектор A (VIP) - 1 ряд, 10 мест, цена 200 EUR
        for num in range(1, 11):
            seats_to_add.append(models.Seat(match_id=match.id, sector="A", row=1, number=num, price=200.0))
            
        # Сектор B (Обычные) - 4 ряда по 10 мест, цена 50 EUR
        for r in range(1, 5):
            for num in range(1, 11):
                seats_to_add.append(models.Seat(match_id=match.id, sector="B", row=r, number=num, price=50.0))
                
        # db.add_all позволяет добавить сразу весь список (быстрее, чем по одному)
        db.add_all(seats_to_add)
        db.commit()
        print("50 мест успешно созданы!")
    else:
        print(f"Места уже существуют ({existing_seats} шт). Пропускаем.")
        
    db.close()

if __name__ == "__main__":
    seed_database()