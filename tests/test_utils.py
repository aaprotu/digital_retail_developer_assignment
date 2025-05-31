from popup_pos.utils.utils import calculate_unikko_points

def test_calculate_unikko_points_eur():
    assert calculate_unikko_points(100, "EUR") == 100

def test_calculate_unikko_points_usd():
    assert calculate_unikko_points(100, "USD") == 100

def test_calculate_unikko_points_sek():
    assert calculate_unikko_points(100, "SEK") == 10