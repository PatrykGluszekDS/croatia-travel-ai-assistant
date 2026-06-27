from database import (
    initialize_database,
    get_packages_by_destination,
    search_travel_packages,
    get_destination_overview,
    get_activities_for_destination,
    get_transport_options,
)


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


def test_get_destination_overview():
    initialize_database()

    result = get_destination_overview("Krk")

    assert "Krk" in result
    assert "Kvarner" in result
    assert "Best season" in result


def test_get_activities_for_destination():
    initialize_database()

    result = get_activities_for_destination("Istria")

    assert "Istria" in result
    assert "Activity" in result


def test_get_transport_options():
    initialize_database()

    result = get_transport_options("Split")

    assert "Split" in result
    assert "Transport type" in result