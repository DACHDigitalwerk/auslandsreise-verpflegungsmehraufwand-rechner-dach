# -*- coding: utf-8 -*-
"""
auslandsreise_dach: BMF Auslandstagegeld- und Reisekostenpauschalen-Engine 2026 für DACH-Unternehmen.
"""

from .models import (
    CountryCode,
    DayType,
    ForeignPerDiemRate,
    TravelDayInput,
    TravelDayResult,
    TripResult,
)
from .bmf_rates_2026 import (
    BMF_FOREIGN_RATES,
    get_per_diem_rate,
)
from .calculator import (
    calculate_day_per_diem,
    calculate_trip,
)

__version__ = "1.0.0"
__all__ = [
    "CountryCode",
    "DayType",
    "ForeignPerDiemRate",
    "TravelDayInput",
    "TravelDayResult",
    "TripResult",
    "BMF_FOREIGN_RATES",
    "get_per_diem_rate",
    "calculate_day_per_diem",
    "calculate_trip",
    "__version__",
]
