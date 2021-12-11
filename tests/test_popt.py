import popt


def test_choice():
    assert popt.choice("1234567890", {"alpha", "beta", "gamma", "delta", "epsilon"}) == "delta"
