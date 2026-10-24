# -*- coding: utf-8 -*-
"""
Calculation engine for foreign travel per diems, statutory meal deductions,
and lodging reimbursement under BMF guidelines 2026.
"""

from typing import List, Tuple
from .models import (
    DayType,
    TravelDayInput,
    TravelDayResult,
    TripResult,
    ForeignPerDiemRate,
)
from .bmf_rates_2026 import get_per_diem_rate


def calculate_day_per_diem(
    day: TravelDayInput,
    rate: ForeignPerDiemRate,
) -> TravelDayResult:
    """
    Calculates per diem and meal deductions for a single travel day.
    Legal rule (§ 9 Abs. 4a Satz 8 EStG): Meal deductions are always computed
    as percentages (20% breakfast, 40% lunch, 40% dinner) of the FULL 24-HOUR rate,
    even on arrival and departure days!
    """
    if day.day_type == DayType.FULL_DAY:
        base_rate = rate.full_day_rate_eur
    else:
        base_rate = rate.partial_day_rate_eur

    # Deductions based on full 24h rate
    full_rate = rate.full_day_rate_eur
    ded_breakfast = round(full_rate * 0.20, 2) if day.provided_breakfast else 0.0
    ded_lunch = round(full_rate * 0.40, 2) if day.provided_lunch else 0.0
    ded_dinner = round(full_rate * 0.40, 2) if day.provided_dinner else 0.0

    total_ded = round(ded_breakfast + ded_lunch + ded_dinner, 2)
    # Per diem cannot become negative
    net_per_diem = round(max(0.0, base_rate - total_ded), 2)

    # Lodging
    lodging = 0.0
    if day.actual_hotel_cost_eur is not None and day.actual_hotel_cost_eur > 0:
        lodging = round(day.actual_hotel_cost_eur, 2)
    elif day.use_lump_sum_hotel:
        lodging = round(rate.lodging_rate_eur, 2)

    total_claim = round(net_per_diem + lodging, 2)

    return TravelDayResult(
        date_str=day.date_str,
        destination_name=f"{rate.country_name} ({rate.city_or_region})",
        day_type=day.day_type,
        base_per_diem=base_rate,
        breakfast_deduction=ded_breakfast,
        lunch_deduction=ded_lunch,
        dinner_deduction=ded_dinner,
        total_meal_deduction=total_ded,
        net_per_diem=net_per_diem,
        lodging_amount=lodging,
        total_day_claim=total_claim,
    )


def calculate_trip(
    days: List[TravelDayInput],
) -> TripResult:
    """
    Calculates the complete multi-day foreign business trip itinerary.
    """
    if not days:
        return TripResult(
            destination_name="Keine Reisetage",
            total_days=0,
            full_days_count=0,
            arrival_departure_days_count=0,
            total_base_per_diems=0.0,
            total_meal_deductions=0.0,
            total_net_per_diems=0.0,
            total_lodging_claimed=0.0,
            grand_total_reimbursement=0.0,
            days=[],
        )

    results: List[TravelDayResult] = []
    full_days = 0
    partial_days = 0
    total_base = 0.0
    total_ded = 0.0
    total_net = 0.0
    total_lodging = 0.0

    primary_destination = ""

    for d in days:
        rate = get_per_diem_rate(d.destination_key)
        if not primary_destination:
            primary_destination = f"{rate.country_name} ({rate.city_or_region})"

        if d.day_type == DayType.FULL_DAY:
            full_days += 1
        else:
            partial_days += 1

        day_res = calculate_day_per_diem(d, rate)
        results.append(day_res)

        total_base += day_res.base_per_diem
        total_ded += day_res.total_meal_deduction
        total_net += day_res.net_per_diem
        total_lodging += day_res.lodging_amount

    grand_total = round(total_net + total_lodging, 2)

    return TripResult(
        destination_name=primary_destination,
        total_days=len(days),
        full_days_count=full_days,
        arrival_departure_days_count=partial_days,
        total_base_per_diems=round(total_base, 2),
        total_meal_deductions=round(total_ded, 2),
        total_net_per_diems=round(total_net, 2),
        total_lodging_claimed=round(total_lodging, 2),
        grand_total_reimbursement=grand_total,
        days=results,
    )
