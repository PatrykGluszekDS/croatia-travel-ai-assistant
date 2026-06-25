from database import initialize_database, get_packages_by_destination, search_travel_packages


def test_get_packages_by_destination_returns_split_package():
    initialize_database()

    result = get_packages_by_destination("Split")

    assert "Split" in result
    assert "Estimated price" in result


def test_search_travel_packages_by_style():
    initialize_database()

    result = search_travel_packages(travel_style="romantic")

    assert "Dubrovnik" in result
    assert "romantic" in result.lower()


def test_search_travel_packages_by_max_price():
    initialize_database()

    result = search_travel_packages(max_price_eur=500)

    assert "Estimated price" in result
    assert "Split" in result or "Zadar" in result or "Krk" in result