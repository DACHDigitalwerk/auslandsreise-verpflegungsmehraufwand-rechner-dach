# -*- coding: utf-8 -*-
"""
Quickstart Example: BMF Auslandstagegeld- und Reisekostenpauschalen-Rechner 2026.
"""

import os
import sys

# Add parent path to allow direct execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from auslandsreise_dach import (
    BMF_FOREIGN_RATES,
    DayType,
    TravelDayInput,
    calculate_trip,
    get_per_diem_rate,
)


def main():
    print("=== Quickstart: BMF Auslandsreisekosten DACH 2026 ===")

    # 1. Look up per diems
    dest_key = "SCHWEIZ_ZUERICH"
    rate = get_per_diem_rate(dest_key)
    print(f"\nDestination: {rate.country_name} ({rate.city_or_region})")
    print(f"  * Voller Tag (24h):     {rate.full_day_rate_eur:.2f} €")
    print(f"  * An-/Abreisetag (>8h): {rate.partial_day_rate_eur:.2f} €")
    print(f"  * Übernachtungspauschale: {rate.lodging_rate_eur:.2f} €")

    # 2. Plan a 3-day business trip to Zürich
    # Day 1: Arrival, Client Dinner provided (40% of 64€ = 25.60€ deduction)
    # Day 2: Full day, Breakfast at hotel (20% of 64€ = 12.80€ deduction), Lunch with partner (40% of 64€ = 25.60€)
    # Day 3: Departure, Breakfast at hotel (20% of 64€ = 12.80€ deduction)
    # Hotel: Actual invoice 220.00 € / night (2 nights = 440.00 €)
    itinerary = [
        TravelDayInput(
            date_str="2026-06-15",
            destination_key=dest_key,
            day_type=DayType.ARRIVAL_DEPARTURE,
            provided_dinner=True,
            actual_hotel_cost_eur=220.0,
        ),
        TravelDayInput(
            date_str="2026-06-16",
            destination_key=dest_key,
            day_type=DayType.FULL_DAY,
            provided_breakfast=True,
            provided_lunch=True,
            actual_hotel_cost_eur=220.0,
        ),
        TravelDayInput(
            date_str="2026-06-17",
            destination_key=dest_key,
            day_type=DayType.ARRIVAL_DEPARTURE,
            provided_breakfast=True,
        ),
    ]

    result = calculate_trip(itinerary)

    print(f"\nErgebnis der Reisekostenabrechnung:")
    print(f"  * Gesamttage:            {result.total_days} ({result.full_days_count} volle Tage, {result.arrival_departure_days_count} An-/Abreisetage)")
    print(f"  * Basispauschalen:       {result.total_base_per_diems:.2f} €")
    print(f"  * Mahlzeitenabzüge:     -{result.total_meal_deductions:.2f} €")
    print(f"  * Netto-Tagegelder:      {result.total_net_per_diems:.2f} €")
    print(f"  * Übernachtungskosten:   {result.total_lodging_claimed:.2f} €")
    print(f"  * STEUERFREIER GESAMTANSPRUCH: {result.grand_total_reimbursement:.2f} €")

    print("\nReisetag-Aufschlüsselung:")
    for d in result.days:
        print(f"  - {d.date_str} [{d.day_type.value}]: Basis {d.base_per_diem:.2f} € | Abzug: -{d.total_meal_deduction:.2f} € | Netto: {d.net_per_diem:.2f} € | Hotel: {d.lodging_amount:.2f} € | Tag: {d.total_day_claim:.2f} €")


if __name__ == "__main__":
    main()
