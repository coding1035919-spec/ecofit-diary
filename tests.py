from datetime import date
from ecofit_diary import Diary, DiaryEntry

def run_tests():
    d = Diary()
    d.add_entry(DiaryEntry(date(2025, 10, 1), 9000, 2000, 2500, "great"))
    d.add_entry(DiaryEntry(date(2025, 10, 2), 7000, 2200, 1800, "ok"))
    d.add_entry(DiaryEntry(date(2025, 10, 3), 8000, 2300, 2000, "low"))

    print("Summary:", d.summary())
    print("Best Days:", [e.day for e in d.best_days(2)])
    print("Compare:", d.compare(date(2025, 10, 1), date(2025, 10, 2)))

if __name__ == "__main__":
    run_tests()
