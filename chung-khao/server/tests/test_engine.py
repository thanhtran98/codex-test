import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import engine


def test_budget_math():
    catalog = engine.load_catalog()
    for pax in (1, 2, 4, 8):
        for days in (1, 2, 3):
            r = engine.generate_trip_plans(pax, days, 10_000_000, "Tổng hòa")
            assert len(r["options"]) == 3
            for opt in r["options"]:
                b = opt["budget"]["breakdown"]
                # Tổng khớp với từng khoản + dự phòng 8%.
                base = b["tickets"]["total"] + b["meals"]["total"] + b["accommodation"]["cost"] + b["transport"]["cost"]
                assert b["subtotal"] == base
                assert b["contingency"] >= round(base * 0.08 / 1000) * 1000
                assert b["total"] == b["subtotal"] + b["contingency"]
                # Đêm = ngày - 1, phòng = ceil(người/2).
                assert b["accommodation"]["nights"] == days - 1
                import math
                assert b["accommodation"]["rooms"] == math.ceil(pax / 2)


def test_budget_check():
    r = engine.generate_trip_plans(2, 1, 100_000, "Tổng hòa")
    for opt in r["options"]:
        bc = opt["budget_check"]
        assert bc["difference"] == bc["user_budget"] - bc["total_cost"]
        assert bc["status"] in ("fit", "exceeded")


def test_swap_recalculates():
    catalog = engine.load_catalog()
    r = engine.generate_trip_plans(2, 2, 5_000_000, "Tổng hòa")
    old = list(r["options"][0]["destinations"])
    new_id = "chua-khaidoan"
    swapped = engine.swap_destination_in_plan(old, old[0], new_id, 2, 2, "hotel")
    assert new_id in swapped["destinations"]
    assert old[0] not in swapped["destinations"]
    assert swapped["budget"]["breakdown"]["total"] > 0


def test_sources_present():
    sources = engine.load_sources()["sources"]
    assert len(sources) >= 3


if __name__ == "__main__":
    test_budget_math()
    test_budget_check()
    test_swap_recalculates()
    test_sources_present()
    print("ALL ENGINE TESTS PASSED")
