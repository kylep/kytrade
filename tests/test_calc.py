"""Test calculations"""
from kytrade import calc

def test_compound_anual_growth_rate():
    """test the cagr logic"""
    # Assumption, 12 years at 6% doubles a value
    # verifying...
    years = 3
    start = 1000
    end = 8000
    verify_cagr = 100
    test_cagr = (verify_cagr/100+1) ** years * start  # double start 3 times, 2, 4, 8...
    assert test_cagr == end
    assert calc.compound_anual_growth_rate(start, end, years) == verify_cagr
