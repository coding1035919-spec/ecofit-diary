"""
EcoFit Diary - Console App
Demonstrates sequence, selection, iteration, and functions.
"""

from datetime import datetime
from ecofit_diary import Diary, DiaryEntry

diary = Diary()

def parse_date(text):
    return datetime.strptime(text, "%Y-%m-%d").date()

def get_int(prompt):
    while True:
        val = input(prompt)
        if val.isdigit():
            return int(val)
        print("Enter a positive number only.")

def get_mood():
    while True:
        mood = input("Mood [low/ok/great]: ").strip().lower()
        if mood in ["low", "ok", "great"]:
            return mood
        print("Invalid mood! Try again.")

def add_entry():
    print("\nAdd New Entry")
    d = parse_date(input("Date (YYYY-MM-DD): "))
    steps = get_int("Steps: ")
    cal = get_int("Calories: ")
    water = get_int("Water (ml): ")
    mood = get_mood()
    entry = DiaryEntry(day=d, steps=steps, calories=cal, water_ml=water, mood=mood)
    try:
        diary.add_entry(entry)
        print("✅ Entry added.")
    except ValueError as e:
        print("Error:", e)

def view_summary():
    print("\nSummary:")
    s = diary.summary()
    print(s)

def view_best_days():
    print("\nTop Days:")
    n = get_int("How many top days? ")
    for i, e in enumerate(diary.best_days(n), start=1):
        print(f"{i}. {e.day} | Score {e.score(diary.goals)} | Mood: {e.mood}")

def change_goal():
    print("\nCurrent Goals:", diary.goals)
    g = input("Goal to change [steps/water_ml/calories]: ").strip()
    v = get_int("New value: ")
    try:
        diary.set_goal(g, v)
        print("Goal updated.")
    except ValueError as e:
        print("Error:", e)

def compare_days():
    print("\nCompare Two Days")
    d1 = parse_date(input("First date (YYYY-MM-DD): "))
    d2 = parse_date(input("Second date (YYYY-MM-DD): "))
    try:
        r = diary.compare(d1, d2)
        if r["result"] == 1:
            print("Day 1 is better!")
        elif r["result"] == -1:
            print("Day 2 is better!")
        else:
            print("Both days are equal.")
    except ValueError as e:
        print("Error:", e)

def main():
    while True:
        print("\n--- EcoFit Diary ---")
        print("1. Add Entry")
        print("2. Summary")
        print("3. Best Days")
        print("4. Change Goal")
        print("5. Compare Days")
        print("6. Exit")

        choice = input("Select option: ").strip()
        if choice == "1":
            add_entry()
        elif choice == "2":
            view_summary()
        elif choice == "3":
            view_best_days()
        elif choice == "4":
            change_goal()
        elif choice == "5":
            compare_days()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
