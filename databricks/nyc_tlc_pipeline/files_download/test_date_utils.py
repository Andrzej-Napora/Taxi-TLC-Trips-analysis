from date_utils import generate_date_range


def test_generate_date_range_includes_all_months():
    result = generate_date_range("2025-06", "2026-06")

    assert result == [
        "2025-06",
        "2025-07",
        "2025-08",
        "2025-09",
        "2025-10",
        "2025-11",
        "2025-12",
        "2026-01",
        "2026-02",
        "2026-03",
        "2026-04",
        "2026-05",
        "2026-06",
    ]