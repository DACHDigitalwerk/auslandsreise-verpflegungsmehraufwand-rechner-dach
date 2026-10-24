# -*- coding: utf-8 -*-
import pytest
from auslandsreise_dach.bmf_rates_2026 import BMF_FOREIGN_RATES, get_per_diem_rate
from auslandsreise_dach.calculator import calculate_day_per_diem, calculate_trip
from auslandsreise_dach.models import DayType, TravelDayInput, ForeignPerDiemRate


def test_bmf_rates_lookup():
    nyc = get_per_diem_rate("USA_NEW_YORK")
    assert nyc.country_name == "USA"
    assert nyc.city_or_region == "New York City"
    assert nyc.full_day_rate_eur == 66.0
    assert nyc.partial_day_rate_eur == 44.0
    assert nyc.lodging_rate_eur == 340.0

    zurich = get_per_diem_rate("schweiz_zuerich")
    assert zurich.full_day_rate_eur == 64.0
    assert zurich.partial_day_rate_eur == 43.0

    wien = get_per_diem_rate("OESTERREICH_WIEN")
    assert wien.full_day_rate_eur == 44.0
    assert wien.partial_day_rate_eur == 30.0

    fallback = get_per_diem_rate("UNKNOWN_COUNTRY_XYZ")
    assert fallback.country_name == "USA"  # fallback default


def test_full_day_no_deductions():
    rate = ForeignPerDiemRate("Schweiz", "Zürich", 64.0, 43.0, 185.0)
    day = TravelDayInput(
        date_str="2026-06-10",
        destination_key="SCHWEIZ_ZUERICH",
        day_type=DayType.FULL_DAY,
    )
    res = calculate_day_per_diem(day, rate)
    assert res.base_per_diem == 64.0
    assert res.total_meal_deduction == 0.0
    assert res.net_per_diem == 64.0
    assert res.lodging_amount == 0.0
    assert res.total_day_claim == 64.0


def test_full_day_with_breakfast_deduction():
    # 20% of 64.0 = 12.80
    rate = ForeignPerDiemRate("Schweiz", "Zürich", 64.0, 43.0, 185.0)
    day = TravelDayInput(
        date_str="2026-06-10",
        destination_key="SCHWEIZ_ZUERICH",
        day_type=DayType.FULL_DAY,
        provided_breakfast=True,
    )
    res = calculate_day_per_diem(day, rate)
    assert res.breakfast_deduction == 12.80
    assert res.net_per_diem == 51.20
    assert res.total_day_claim == 51.20


def test_full_day_with_all_meals_deduction():
    # 20% + 40% + 40% = 100% of 60.0 = 60.0
    rate = ForeignPerDiemRate("Großbritannien", "London", 62.0, 41.0, 209.0)
    day = TravelDayInput(
        date_str="2026-06-11",
        destination_key="UK_LONDON",
        day_type=DayType.FULL_DAY,
        provided_breakfast=True,
        provided_lunch=True,
        provided_dinner=True,
    )
    res = calculate_day_per_diem(day, rate)
    assert res.breakfast_deduction == round(62.0 * 0.20, 2)
    assert res.lunch_deduction == round(62.0 * 0.40, 2)
    assert res.dinner_deduction == round(62.0 * 0.40, 2)
    assert res.net_per_diem == 0.0  # Completely capped at 0


def test_arrival_departure_day_deduction_calculation():
    # BMF Rule: Deductions on arrival day are calculated on FULL 24h rate, not partial rate!
    # Full rate = 66.0, Partial rate = 44.0.
    # Provided dinner: 40% of 66.0 = 26.40.
    # Net per diem: 44.0 - 26.40 = 17.60.
    rate = ForeignPerDiemRate("USA", "New York City", 66.0, 44.0, 340.0)
    day = TravelDayInput(
        date_str="2026-06-01",
        destination_key="USA_NEW_YORK",
        day_type=DayType.ARRIVAL_DEPARTURE,
        provided_dinner=True,
    )
    res = calculate_day_per_diem(day, rate)
    assert res.base_per_diem == 44.0
    assert res.dinner_deduction == 26.40
    assert res.net_per_diem == 17.60


def test_arrival_day_cap_at_zero():
    # Full rate = 44.0, Partial rate = 30.0.
    # Provided lunch (40% of 44 = 17.60) + dinner (40% of 44 = 17.60) = 35.20.
    # Base is 30.0, deduction is 35.20 -> Net must not be negative! Max(0, 30.0 - 35.20) = 0.0.
    rate = ForeignPerDiemRate("Österreich", "Wien", 44.0, 30.0, 149.0)
    day = TravelDayInput(
        date_str="2026-06-01",
        destination_key="OESTERREICH_WIEN",
        day_type=DayType.ARRIVAL_DEPARTURE,
        provided_lunch=True,
        provided_dinner=True,
    )
    res = calculate_day_per_diem(day, rate)
    assert res.base_per_diem == 30.0
    assert res.total_meal_deduction == 35.20
    assert res.net_per_diem == 0.0


def test_hotel_lump_sum_and_actual_costs():
    rate = ForeignPerDiemRate("Frankreich", "Paris", 58.0, 39.0, 159.0)
    
    # Lump sum
    day_lump = TravelDayInput(
        date_str="2026-06-01",
        destination_key="FRANKREICH_PARIS",
        use_lump_sum_hotel=True,
    )
    res_lump = calculate_day_per_diem(day_lump, rate)
    assert res_lump.lodging_amount == 159.0
    assert res_lump.total_day_claim == 58.0 + 159.0

    # Actual receipts
    day_actual = TravelDayInput(
        date_str="2026-06-02",
        destination_key="FRANKREICH_PARIS",
        actual_hotel_cost_eur=215.50,
    )
    res_actual = calculate_day_per_diem(day_actual, rate)
    assert res_actual.lodging_amount == 215.50
    assert res_actual.total_day_claim == 58.0 + 215.50


def test_calculate_trip_aggregation():
    days = [
        TravelDayInput("2026-07-01", "USA_NEW_YORK", day_type=DayType.ARRIVAL_DEPARTURE, provided_dinner=True, actual_hotel_cost_eur=250.0),
        TravelDayInput("2026-07-02", "USA_NEW_YORK", day_type=DayType.FULL_DAY, provided_breakfast=True, actual_hotel_cost_eur=250.0),
        TravelDayInput("2026-07-03", "USA_NEW_YORK", day_type=DayType.ARRIVAL_DEPARTURE, provided_breakfast=True),
    ]
    trip = calculate_trip(days)
    assert trip.total_days == 3
    assert trip.full_days_count == 1
    assert trip.arrival_departure_days_count == 2
    # Base: 44 (day1) + 66 (day2) + 44 (day3) = 154.00
    assert trip.total_base_per_diems == 154.00
    # Day 1: 44 - 26.40 (dinner) = 17.60
    # Day 2: 66 - 13.20 (breakfast) = 52.80
    # Day 3: 44 - 13.20 (breakfast) = 30.80
    # Net per diems: 17.60 + 52.80 + 30.80 = 101.20
    assert trip.total_net_per_diems == 101.20
    assert trip.total_lodging_claimed == 500.0
    assert trip.grand_total_reimbursement == 601.20


def test_empty_trip():
    trip = calculate_trip([])
    assert trip.total_days == 0
    assert trip.grand_total_reimbursement == 0.0
