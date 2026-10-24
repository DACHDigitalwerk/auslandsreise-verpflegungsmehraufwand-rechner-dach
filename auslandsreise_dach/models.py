# -*- coding: utf-8 -*-
"""
Data models for international travel expenses, per diems, and meal deductions.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class CountryCode(str, Enum):
    DE = "DE"
    AT = "AT"
    CH = "CH"


class DayType(str, Enum):
    FULL_DAY = "FULL_DAY"           # 24 hours absence
    ARRIVAL_DEPARTURE = "ARRIVAL"  # An- oder Abreisetag (> 0 hours with overnight or > 8 hours)


@dataclass
class ForeignPerDiemRate:
    country_name: str
    city_or_region: str
    full_day_rate_eur: float       # 24h Pauschale
    partial_day_rate_eur: float    # An-/Abreisetag & > 8h
    lodging_rate_eur: float        # Amtliche Übernachtungspauschale
    currency: str = "EUR"


@dataclass
class TravelDayInput:
    date_str: str                  # e.g. "2026-06-15"
    destination_key: str           # e.g. "USA_NEW_YORK" or "FRANCE_PARIS"
    day_type: DayType = DayType.FULL_DAY
    provided_breakfast: bool = False
    provided_lunch: bool = False
    provided_dinner: bool = False
    actual_hotel_cost_eur: Optional[float] = None
    use_lump_sum_hotel: bool = False


@dataclass
class TravelDayResult:
    date_str: str
    destination_name: str
    day_type: DayType
    base_per_diem: float
    breakfast_deduction: float
    lunch_deduction: float
    dinner_deduction: float
    total_meal_deduction: float
    net_per_diem: float
    lodging_amount: float
    total_day_claim: float


@dataclass
class TripResult:
    destination_name: str
    total_days: int
    full_days_count: int
    arrival_departure_days_count: int
    total_base_per_diems: float
    total_meal_deductions: float
    total_net_per_diems: float
    total_lodging_claimed: float
    grand_total_reimbursement: float
    days: List[TravelDayResult] = field(default_factory=list)
