from date_utils import generate_date_range


def test_generate_date_range_includes_all_months():
    result = generate_date_range("2025-06", "2025-09")

    assert result == [
        "2025-06",
        "2025-07",
        "2025-08",
        "2025-09",
    ]