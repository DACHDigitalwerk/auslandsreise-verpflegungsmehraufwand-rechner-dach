# -*- coding: utf-8 -*-
"""
Command-line interface for the DACH Foreign Travel Expense & Per Diem Calculator 2026.
"""

import argparse
import json
import os
import sys
from typing import List

if __package__ is None or __package__ == "":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from auslandsreise_dach.bmf_rates_2026 import BMF_FOREIGN_RATES, get_per_diem_rate
from auslandsreise_dach.calculator import calculate_trip
from auslandsreise_dach.models import DayType, TravelDayInput


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dach-ausland",
        description="BMF Auslandstagegeld- und Reisekostenpauschalen-Rechner 2026 (DACH)",
    )
    parser.add_argument(
        "--destination",
        "-d",
        type=str,
        default="USA_NEW_YORK",
        help="Destination key (e.g. USA_NEW_YORK, SCHWEIZ_ZUERICH, UK_LONDON)",
    )
    parser.add_argument(
        "--days",
        "-n",
        type=int,
        default=3,
        help="Total trip duration in days (default: 3)",
    )
    parser.add_argument(
        "--arrival-departure-days",
        "-a",
        type=int,
        default=2,
        help="Number of arrival/departure days (default: 2)",
    )
    parser.add_argument(
        "--breakfasts",
        type=int,
        default=0,
        help="Number of provided breakfasts (deduction: 20%% of full day per diem)",
    )
    parser.add_argument(
        "--lunches",
        type=int,
        default=0,
        help="Number of provided lunches (deduction: 40%% of full day per diem)",
    )
    parser.add_argument(
        "--dinners",
        type=int,
        default=0,
        help="Number of provided dinners (deduction: 40%% of full day per diem)",
    )
    parser.add_argument(
        "--hotel-lump-sum",
        action="store_true",
        help="Apply official BMF lodging lump sum per overnight stay",
    )
    parser.add_argument(
        "--hotel-actual",
        type=float,
        default=0.0,
        help="Total actual hotel/lodging costs (EUR)",
    )
    parser.add_argument(
        "--list-destinations",
        action="store_true",
        help="List all supported destinations with BMF 2026 per diem rates",
    )
    parser.add_argument(
        "--search",
        type=str,
        default="",
        help="Search destinations by country or city name",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.list_destinations:
        print("=== BMF Auslandstagegelder & Pauschalen 2026 ===")
        print(f"{'Key':<25} | {'Land & Stadt':<30} | {'24h Satz':<10} | {'An/Ab Satz':<10} | {'Hotel'}")
        print("-" * 90)
        for key, rate in sorted(BMF_FOREIGN_RATES.items()):
            dest = f"{rate.country_name} ({rate.city_or_region})"
            print(f"{key:<25} | {dest:<30} | {rate.full_day_rate_eur:>6.2f} € | {rate.partial_day_rate_eur:>7.2f} € | {rate.lodging_rate_eur:>6.2f} €")
        return 0

    if args.search:
        q = args.search.lower()
        print(f"=== Suchergebnisse für '{args.search}' ===")
        matches = [
            (k, v) for k, v in BMF_FOREIGN_RATES.items()
            if q in k.lower() or q in v.country_name.lower() or q in v.city_or_region.lower()
        ]
        if not matches:
            print("Keine Destinationen gefunden.")
            return 1
        for k, v in matches:
            print(f"- {k}: {v.country_name} ({v.city_or_region}) -> 24h: {v.full_day_rate_eur:.2f} €, An/Ab: {v.partial_day_rate_eur:.2f} €, Hotel: {v.lodging_rate_eur:.2f} €")
        return 0

    # Build itinerary
    total_days = max(1, args.days)
    partial_days_count = min(total_days, max(0, args.arrival_departure_days))
    full_days_count = total_days - partial_days_count

    b_count = args.breakfasts
    l_count = args.lunches
    d_count = args.dinners

    itinerary: List[TravelDayInput] = []
    hotel_per_night = (args.hotel_actual / max(1, total_days - 1)) if args.hotel_actual > 0 else 0.0

    for i in range(total_days):
        is_partial = (i == 0 and partial_days_count >= 1) or (i == total_days - 1 and partial_days_count >= 2)
        day_type = DayType.ARRIVAL_DEPARTURE if is_partial else DayType.FULL_DAY

        has_b = (b_count > 0)
        if has_b:
            b_count -= 1
        has_l = (l_count > 0)
        if has_l:
            l_count -= 1
        has_d = (d_count > 0)
        if has_d:
            d_count -= 1

        is_last_day = (i == total_days - 1)
        actual_hotel = 0.0 if is_last_day else hotel_per_night
        use_lump = args.hotel_lump_sum if not is_last_day else False

        itinerary.append(
            TravelDayInput(
                date_str=f"Tag {i + 1}",
                destination_key=args.destination,
                day_type=day_type,
                provided_breakfast=has_b,
                provided_lunch=has_l,
                provided_dinner=has_d,
                actual_hotel_cost_eur=actual_hotel,
                use_lump_sum_hotel=use_lump,
            )
        )

    trip_res = calculate_trip(itinerary)

    if args.json:
        out = {
            "destination": trip_res.destination_name,
            "total_days": trip_res.total_days,
            "full_days": trip_res.full_days_count,
            "arrival_departure_days": trip_res.arrival_departure_days_count,
            "total_base_per_diems": trip_res.total_base_per_diems,
            "total_meal_deductions": trip_res.total_meal_deductions,
            "total_net_per_diems": trip_res.total_net_per_diems,
            "total_lodging_claimed": trip_res.total_lodging_claimed,
            "grand_total_reimbursement": trip_res.grand_total_reimbursement,
            "days": [
                {
                    "date": d.date_str,
                    "day_type": d.day_type.value,
                    "base_per_diem": d.base_per_diem,
                    "deductions": {
                        "breakfast": d.breakfast_deduction,
                        "lunch": d.lunch_deduction,
                        "dinner": d.dinner_deduction,
                        "total": d.total_meal_deduction,
                    },
                    "net_per_diem": d.net_per_diem,
                    "lodging": d.lodging_amount,
                    "day_total": d.total_day_claim,
                }
                for d in trip_res.days
            ],
        }
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0

    print("=" * 65)
    print(f" BMF REISEKOSTENABRECHNUNG AUSLAND 2026: {trip_res.destination_name}")
    print("=" * 65)
    print(f" Reisedauer gesamt:        {trip_res.total_days} Tage ({trip_res.full_days_count} volle Tage, {trip_res.arrival_departure_days_count} An-/Abreisetage)")
    print(f" Summe Basispauschalen:    {trip_res.total_base_per_diems:>10.2f} €")
    print(f" Abzug Mahlzeiten:        -{trip_res.total_meal_deductions:>10.2f} €")
    print(f" Netto-Verpflegungsmehraufwand: {trip_res.total_net_per_diems:>6.2f} €")
    print(f" Übernachtungskosten:      {trip_res.total_lodging_claimed:>10.2f} €")
    print("-" * 65)
    print(f" GESAMTANSPRUCH (STEUERFREI): {trip_res.grand_total_reimbursement:>7.2f} €")
    print("=" * 65)
    print("\nDetails nach Reisetagen:")
    for d in trip_res.days:
        meals = []
        if d.breakfast_deduction > 0:
            meals.append(f"F(-{d.breakfast_deduction}€)")
        if d.lunch_deduction > 0:
            meals.append(f"M(-{d.lunch_deduction}€)")
        if d.dinner_deduction > 0:
            meals.append(f"A(-{d.dinner_deduction}€)")
        meals_str = ", ".join(meals) if meals else "Keine Kürzung"
        print(f"  * {d.date_str} [{d.day_type.value}]: Basis {d.base_per_diem:.2f} € | Kürzung: {meals_str} | Netto: {d.net_per_diem:.2f} € | Hotel: {d.lodging_amount:.2f} €")

    print("\nHinweis: Gesetzliche Mahlzeitenkürzungen (§ 9 Abs. 4a EStG) basieren stets")
    print("auf dem vollen 24-Stunden-Satz (20% Frühstück / 40% Mittag / 40% Abendessen).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
