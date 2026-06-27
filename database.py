import sqlite3
from pathlib import Path


DB_PATH = Path("data/croatia_travel.db")


def initialize_database():
    """
    Create the SQLite database and add sample travel data
    if the database does not exist yet.
    """

    DB_PATH.parent.mkdir(exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS destinations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                region TEXT NOT NULL,
                description TEXT NOT NULL,
                best_season TEXT NOT NULL,
                crowd_level TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                duration_days INTEGER NOT NULL,
                travel_style TEXT NOT NULL,
                description TEXT NOT NULL,
                estimated_price_eur INTEGER NOT NULL,
                FOREIGN KEY (destination_id) REFERENCES destinations(id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                indoor_outdoor TEXT NOT NULL,
                FOREIGN KEY (destination_id) REFERENCES destinations(id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS transport_options (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination_id INTEGER NOT NULL,
                origin_region TEXT NOT NULL,
                transport_type TEXT NOT NULL,
                description TEXT NOT NULL,
                approximate_duration TEXT NOT NULL,
                FOREIGN KEY (destination_id) REFERENCES destinations(id)
            )
            """
        )

        cursor.execute("SELECT COUNT(*) FROM destinations")
        count = cursor.fetchone()[0]

        if count == 0:
            seed_database(cursor)

        conn.commit()


def seed_database(cursor):
    """
    Insert sample data into the database.
    """

    destinations = [
        (
            "Split",
            "Dalmatia",
            "Historic coastal city known for Diocletian's Palace, beaches, nightlife, and island connections.",
            "May to October",
            "medium to high in summer",
        ),
        (
            "Dubrovnik",
            "Dalmatia",
            "Famous walled city with sea views, old town walks, romantic restaurants, and nearby islands.",
            "April to October",
            "high in summer",
        ),
        (
            "Krk",
            "Kvarner",
            "Accessible island with beaches, small towns, local wine, and relaxed coastal atmosphere.",
            "May to September",
            "medium in summer",
        ),
        (
            "Zadar",
            "Dalmatia",
            "Coastal city known for sunsets, Sea Organ, Roman ruins, and access to islands and national parks.",
            "May to October",
            "medium in summer",
        ),
        (
            "Istria",
            "Istria",
            "Region known for Rovinj, hilltop towns, truffles, wine, cycling, and Italian-influenced coastal culture.",
            "April to October",
            "medium in summer",
        ),
    ]

    cursor.executemany(
        """
        INSERT INTO destinations (
            name,
            region,
            description,
            best_season,
            crowd_level
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        destinations,
    )

    cursor.execute("SELECT id, name FROM destinations")
    destination_ids = {name: destination_id for destination_id, name in cursor.fetchall()}

    packages = [
        (
            destination_ids["Split"],
            "Split Culture and Beaches City Break",
            3,
            "culture and beaches",
            "A short city break with Diocletian's Palace, local food, beaches, and a possible island trip.",
            450,
        ),
        (
            destination_ids["Dubrovnik"],
            "Romantic Dubrovnik Weekend",
            3,
            "romantic",
            "A romantic weekend with old town walks, sea views, restaurants, and a sunset viewpoint.",
            650,
        ),
        (
            destination_ids["Krk"],
            "Relaxed Krk Island Escape",
            4,
            "relaxed island",
            "A relaxed island stay with beaches, small towns, local wine, and easy car trips around the island.",
            500,
        ),
        (
            destination_ids["Zadar"],
            "Zadar Hidden Gems Break",
            3,
            "hidden gems",
            "A city break with Sea Organ, sunsets, nearby islands, and less crowded local experiences.",
            420,
        ),
        (
            destination_ids["Istria"],
            "Istria Food and Wine Trip",
            5,
            "food and wine",
            "A food-focused trip with Rovinj, Motovun, truffles, wine tasting, and coastal towns.",
            700,
        ),
    ]

    cursor.executemany(
        """
        INSERT INTO packages (
            destination_id,
            name,
            duration_days,
            travel_style,
            description,
            estimated_price_eur
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        packages,
    )

    activities = [
        (
            destination_ids["Split"],
            "Diocletian's Palace walk",
            "culture",
            "Explore the old Roman palace area, small streets, cafes, and historic squares.",
            "outdoor",
        ),
        (
            destination_ids["Split"],
            "Bačvice beach",
            "beach",
            "Popular city beach close to the center, useful for a short beach break.",
            "outdoor",
        ),
        (
            destination_ids["Dubrovnik"],
            "Old Town walls",
            "culture",
            "Walk along the city walls for views over the old town and the Adriatic Sea.",
            "outdoor",
        ),
        (
            destination_ids["Dubrovnik"],
            "Sunset viewpoint",
            "romantic",
            "Enjoy sunset views above the city or from a coastal viewpoint.",
            "outdoor",
        ),
        (
            destination_ids["Krk"],
            "Vrbnik wine tasting",
            "food and wine",
            "Visit Vrbnik and try local wine in a relaxed island setting.",
            "indoor/outdoor",
        ),
        (
            destination_ids["Zadar"],
            "Sea Organ and sunset",
            "hidden gems",
            "Experience Zadar's waterfront, Sea Organ, and famous sunset atmosphere.",
            "outdoor",
        ),
        (
            destination_ids["Istria"],
            "Motovun and truffle tasting",
            "food and wine",
            "Visit a hilltop town and try local truffle-based food.",
            "indoor/outdoor",
        ),
    ]

    cursor.executemany(
        """
        INSERT INTO activities (
            destination_id,
            name,
            category,
            description,
            indoor_outdoor
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        activities,
    )

    transport_options = [
        (
            destination_ids["Split"],
            "Central Europe",
            "car",
            "Driving to Split is possible from Central Europe, usually through Slovenia and Croatia. Check motorway tolls, border waiting times, and parking.",
            "long full-day drive or overnight stop",
        ),
        (
            destination_ids["Split"],
            "Europe",
            "flight",
            "Flying to Split Airport is usually the fastest option during the travel season. Check seasonal connections and transfer options to the city.",
            "usually same day",
        ),
        (
            destination_ids["Dubrovnik"],
            "Europe",
            "flight",
            "Flying is usually the most practical way to reach Dubrovnik from many European countries. Check airport transfers to the old town area.",
            "usually same day",
        ),
        (
            destination_ids["Krk"],
            "Central Europe",
            "car",
            "Krk is convenient by car because it is connected to the mainland by bridge. Good option for travelers from Poland, Austria, Slovenia, or nearby regions.",
            "long drive depending on origin",
        ),
        (
            destination_ids["Istria"],
            "Central Europe",
            "car",
            "Istria is one of the easiest Croatian regions to reach by car from Central Europe. It is suitable for road trips and flexible travel.",
            "long drive depending on origin",
        ),
        (
            destination_ids["Zadar"],
            "Europe",
            "flight",
            "Zadar Airport has seasonal European connections. It can be a practical option for shorter city breaks.",
            "usually same day",
        ),
    ]

    cursor.executemany(
        """
        INSERT INTO transport_options (
            destination_id,
            origin_region,
            transport_type,
            description,
            approximate_duration
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        transport_options,
    )


def get_packages_by_destination(destination):
    """
    Return packages matching a destination name.
    """

    initialize_database()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                d.name,
                d.region,
                p.name,
                p.duration_days,
                p.travel_style,
                p.description,
                p.estimated_price_eur
            FROM packages p
            JOIN destinations d ON p.destination_id = d.id
            WHERE LOWER(d.name) = LOWER(?)
            ORDER BY p.estimated_price_eur ASC
            """,
            (destination,),
        )

        rows = cursor.fetchall()

    if not rows:
        return f"No travel packages found for {destination}."

    results = []

    for row in rows:
        destination, region, package_name, duration_days, travel_style, description, price = row

        results.append(
            f"Package: {package_name}\n"
            f"Destination: {destination}\n"
            f"Region: {region}\n"
            f"Duration: {duration_days} days\n"
            f"Style: {travel_style}\n"
            f"Description: {description}\n"
            f"Estimated price: €{price}"
        )

    return "\n\n".join(results)


def search_travel_packages(
    destination=None,
    region=None,
    travel_style=None,
    max_price_eur=None,
    duration_days=None,
):
    """
    Search travel packages using optional filters.
    """

    initialize_database()

    query = """
        SELECT
            d.name,
            d.region,
            p.name,
            p.duration_days,
            p.travel_style,
            p.description,
            p.estimated_price_eur
        FROM packages p
        JOIN destinations d ON p.destination_id = d.id
        WHERE 1 = 1
    """

    params = []

    if destination:
        query += " AND LOWER(d.name) = LOWER(?)"
        params.append(destination)

    if region:
        query += " AND LOWER(d.region) = LOWER(?)"
        params.append(region)

    if travel_style:
        query += " AND LOWER(p.travel_style) LIKE LOWER(?)"
        params.append(f"%{travel_style}%")

    if max_price_eur:
        query += " AND p.estimated_price_eur <= ?"
        params.append(max_price_eur)

    if duration_days:
        query += " AND p.duration_days = ?"
        params.append(duration_days)

    query += " ORDER BY p.estimated_price_eur ASC"

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

    if not rows:
        return "No matching travel packages found."

    results = []

    for row in rows:
        destination, region, package_name, duration_days, travel_style, description, price = row

        results.append(
            f"Package: {package_name}\n"
            f"Destination: {destination}\n"
            f"Region: {region}\n"
            f"Duration: {duration_days} days\n"
            f"Style: {travel_style}\n"
            f"Description: {description}\n"
            f"Estimated price: €{price}"
        )

    return "\n\n".join(results)


def get_destination_overview(destination):
    """
    Return general information about a Croatian destination.
    """

    initialize_database()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT name, region, description, best_season, crowd_level
            FROM destinations
            WHERE LOWER(name) = LOWER(?)
            """,
            (destination,),
        )

        row = cursor.fetchone()

    if not row:
        return f"No destination overview found for {destination}."

    name, region, description, best_season, crowd_level = row

    return (
        f"Destination: {name}\n"
        f"Region: {region}\n"
        f"Description: {description}\n"
        f"Best season: {best_season}\n"
        f"Crowd level: {crowd_level}"
    )


def get_activities_for_destination(destination, category=None):
    """
    Return activities for a destination, optionally filtered by category.
    """

    initialize_database()

    query = """
        SELECT
            d.name,
            a.name,
            a.category,
            a.description,
            a.indoor_outdoor
        FROM activities a
        JOIN destinations d ON a.destination_id = d.id
        WHERE LOWER(d.name) = LOWER(?)
    """

    params = [destination]

    if category:
        query += " AND LOWER(a.category) LIKE LOWER(?)"
        params.append(f"%{category}%")

    query += " ORDER BY a.category, a.name"

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

    if not rows:
        if category:
            return f"No {category} activities found for {destination}."
        return f"No activities found for {destination}."

    results = []

    for row in rows:
        destination_name, activity_name, category, description, indoor_outdoor = row

        results.append(
            f"Destination: {destination_name}\n"
            f"Activity: {activity_name}\n"
            f"Category: {category}\n"
            f"Description: {description}\n"
            f"Type: {indoor_outdoor}"
        )

    return "\n\n".join(results)


def get_transport_options(destination, origin_region=None, transport_type=None):
    """
    Return transport options for reaching a Croatian destination.
    """

    initialize_database()

    query = """
        SELECT
            d.name,
            t.origin_region,
            t.transport_type,
            t.description,
            t.approximate_duration
        FROM transport_options t
        JOIN destinations d ON t.destination_id = d.id
        WHERE LOWER(d.name) = LOWER(?)
    """

    params = [destination]

    if origin_region:
        query += " AND LOWER(t.origin_region) LIKE LOWER(?)"
        params.append(f"%{origin_region}%")

    if transport_type:
        query += " AND LOWER(t.transport_type) = LOWER(?)"
        params.append(transport_type)

    query += " ORDER BY t.transport_type"

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

    if not rows:
        return f"No transport options found for {destination}."

    results = []

    for row in rows:
        destination_name, origin_region, transport_type, description, approximate_duration = row

        results.append(
            f"Destination: {destination_name}\n"
            f"Origin region: {origin_region}\n"
            f"Transport type: {transport_type}\n"
            f"Description: {description}\n"
            f"Approximate duration: {approximate_duration}"
        )

    return "\n\n".join(results)


if __name__ == "__main__":
    initialize_database()

    print("Database initialized successfully.")
    print()
    print(get_packages_by_destination("Split"))
    print()
    print("Romantic packages:")
    print(search_travel_packages(travel_style="romantic"))
    print()
    print("Destination overview:")
    print(get_destination_overview("Krk"))

    print()
    print("Activities:")
    print(get_activities_for_destination("Istria"))

    print()
    print("Transport:")
    print(get_transport_options("Split", origin_region="Europe"))