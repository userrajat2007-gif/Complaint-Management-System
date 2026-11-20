"""
COMPLAINT MANAGEMENT SYSTEM
A simple first-year B.Tech Python project.

Features:
1. Register a complaint
2. View all complaints
3. Search complaints by ID
4. Update complaint status
5. Store complaint records permanently using SQLite

Run: python complaint_management_system.py
No external Python packages are required.
"""

import sqlite3
from datetime import datetime

DB_NAME = "complaints.db"


class Complaint:
    """Represents one complaint."""

    def __init__(self, complaint_id, name, category, description,
                 status="Pending", created_at=None):
        self.complaint_id = complaint_id
        self.name = name
        self.category = category
        self.description = description
        self.status = status
        self.created_at = created_at


class ComplaintManager:
    """Handles complaint registration, storage and resolution."""

    def __init__(self, database=DB_NAME):
        self.connection = sqlite3.connect(database)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS complaints (
            complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TEXT NOT NULL
        )
        """
        self.connection.execute(query)
        self.connection.commit()

    def register_complaint(self, name, category, description):
        created_at = datetime.now().strftime("%d-%m-%Y %I:%M %p")
        query = """
        INSERT INTO complaints (name, category, description, status, created_at)
        VALUES (?, ?, ?, 'Pending', ?)
        """
        cursor = self.connection.execute(
            query, (name, category, description, created_at)
        )
        self.connection.commit()
        return cursor.lastrowid

    def get_all_complaints(self):
        cursor = self.connection.execute(
            "SELECT * FROM complaints ORDER BY complaint_id DESC"
        )
        return cursor.fetchall()

    def get_complaint(self, complaint_id):
        cursor = self.connection.execute(
            "SELECT * FROM complaints WHERE complaint_id = ?",
            (complaint_id,)
        )
        return cursor.fetchone()

    def resolve_complaint(self, complaint_id, new_status):
        allowed_statuses = ("Pending", "In Progress", "Resolved")
        if new_status not in allowed_statuses:
            return False
        cursor = self.connection.execute(
            "UPDATE complaints SET status = ? WHERE complaint_id = ?",
            (new_status, complaint_id)
        )
        self.connection.commit()
        return cursor.rowcount > 0

    def close(self):
        self.connection.close()


def print_complaint(row):
    """Display one complaint in a readable format."""
    print("-" * 55)
    print("Complaint ID :", row[0])
    print("Name         :", row[1])
    print("Category     :", row[2])
    print("Description  :", row[3])
    print("Status       :", row[4])
    print("Registered   :", row[5])


def main():
    manager = ComplaintManager()
    categories = [
        "Academic", "Hostel", "Transport", "Technical",
        "Cleanliness", "Other"
    ]

    while True:
        print("\\n========== COMPLAINT MANAGEMENT SYSTEM ==========")
        print("1. Register a complaint")
        print("2. View all complaints")
        print("3. Search complaint by ID")
        print("4. Update complaint status")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            print("\\nAvailable categories:")
            for number, category in enumerate(categories, start=1):
                print(f"{number}. {category}")

            name = input("Enter your name: ").strip()
            if not name:
                print("Name cannot be empty.")
                continue

            try:
                category_number = int(input("Choose category number: "))
                if not 1 <= category_number <= len(categories):
                    print("Invalid category number.")
                    continue
            except ValueError:
                print("Please enter a valid number.")
                continue

            description = input("Enter complaint details: ").strip()
            if not description:
                print("Complaint details cannot be empty.")
                continue

            complaint_id = manager.register_complaint(
                name, categories[category_number - 1], description
            )
            print("\\nComplaint registered successfully!")
            print("Your Complaint ID is:", complaint_id)

        elif choice == "2":
            complaints = manager.get_all_complaints()
            if not complaints:
                print("\\nNo complaints have been registered yet.")
            else:
                print("\\nALL REGISTERED COMPLAINTS")
                for row in complaints:
                    print_complaint(row)

        elif choice == "3":
            try:
                complaint_id = int(input("Enter complaint ID: "))
            except ValueError:
                print("Please enter a valid numeric ID.")
                continue

            row = manager.get_complaint(complaint_id)
            if row:
                print_complaint(row)
            else:
                print("Complaint ID not found.")

        elif choice == "4":
            try:
                complaint_id = int(input("Enter complaint ID: "))
            except ValueError:
                print("Please enter a valid numeric ID.")
                continue

            print("1. Pending")
            print("2. In Progress")
            print("3. Resolved")
            status_choice = input("Select new status: ").strip()
            status_map = {
                "1": "Pending",
                "2": "In Progress",
                "3": "Resolved"
            }

            if status_choice not in status_map:
                print("Invalid status choice.")
                continue

            updated = manager.resolve_complaint(
                complaint_id, status_map[status_choice]
            )
            if updated:
                print("Complaint status updated successfully.")
            else:
                print("Complaint ID not found.")

        elif choice == "5":
            manager.close()
            print("Thank you for using the Complaint Management System.")
            break

        else:
            print("Invalid choice. Please select from 1 to 5.")


if __name__ == "__main__":
    main()
