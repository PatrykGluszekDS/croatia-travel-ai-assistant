import sqlite3
from pathlib import Path


DB_PATH = Path("data/croatia_travel.db")


def initialize_database():
    """
    Create the SQLite database and add sample travel packages
    if the database does not exist yet.
    """

    DB_PATH.parent.mkdir(exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS travel_packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination TEXT NOT NULL,
                region TEXT NOT NULL,
                duration_days INTEGER NOT NULL,
                travel_style TEXT NOT NULL,
                description TEXT NOT NULL,
                estimated_price_eur INTEGER NOT NULL
            )
            """
        )

        cursor.execute("SELECT COUNT(*) FROM travel_packages")
        count = cursor.fetchone()[0]

        if count == 0:
            sample_packages = [
                (
                    "Split",
                    "Dalmatia",
                    3,
                    "culture and beaches",
                    "A short city break with Diocletian's Palace, local food, beaches, and a possible island trip.",
                    450,
                ),
                (
                    "Dubrovnik",
                    "Dalmatia",
                    3,
                    "romantic",
                    "A romantic weekend with old town walks, sea views, restaurants, and a sunset viewpoint.",
                    650,
                ),
                (
                    "Krk",
                    "Kvarner",
                    4,
                    "relaxed island",
                    "A relaxed island stay with beaches, small towns, local wine, and easy car trips around the island.",
                    500,
                ),
                (
                    "Zadar",
                    "Dalmatia",
                    3,
                    "hidden gems",
                    "A city break with sea organ, sunsets, nearby islands, and less crowded local experiences.",
                    420,
                ),
                (
                    "Istria",
                    "Istria",
                    5,
                    "food and wine",
                    "A food-focused trip with Rovinj, Motovun, truffles, wine tasting, and coastal towns.",
                    700,
                ),
            ]

            cursor.executemany(
                """
                INSERT INTO travel_packages (
                    destination,
                    region,
                    duration_days,
                    travel_style,
                    description,
                    estimated_price_eur
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                sample_packages,
            )

        conn.commit()


def get_packages_by_destination(destination):
    """
    Return packages matching a destination name.
    """

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT destination, region, duration_days, travel_style, description, estimated_price_eur
            FROM travel_packages
            WHERE LOWER(destination) = LOWER(?)
            """,
            (destination,),
        )

        rows = cursor.fetchall()

    if not rows:
        return f"No travel packages found for {destination}."

    results = []

    for row in rows:
        destination, region, duration_days, travel_style, description, price = row

        results.append(
            f"Destination: {destination}\n"
            f"Region: {region}\n"
            f"Duration: {duration_days} days\n"
            f"Style: {travel_style}\n"
            f"Description: {description}\n"
            f"Estimated price: €{price}"
        )

    return "\n\n".join(results)


if __name__ == "__main__":
    initialize_database()

    print("Database initialized successfully.")
    print()
    print(get_packages_by_destination("Split"))