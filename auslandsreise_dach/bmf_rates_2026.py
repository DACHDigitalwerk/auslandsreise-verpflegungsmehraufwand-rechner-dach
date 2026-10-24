# -*- coding: utf-8 -*-
"""
Official BMF Foreign Per Diem Rates (Auslandstagegelder & Übernachtungspauschalen) 2026.
Based on BMF guidelines (§ 9 Abs. 4a EStG).
"""

from typing import Dict
from .models import ForeignPerDiemRate


BMF_FOREIGN_RATES: Dict[str, ForeignPerDiemRate] = {
    # --- USA ---
    "USA_NEW_YORK": ForeignPerDiemRate("USA", "New York City", 66.0, 44.0, 340.0),
    "USA_WASHINGTON": ForeignPerDiemRate("USA", "Washington, D.C.", 64.0, 43.0, 290.0),
    "USA_SAN_FRANCISCO": ForeignPerDiemRate("USA", "San Francisco", 64.0, 43.0, 280.0),
    "USA_LOS_ANGELES": ForeignPerDiemRate("USA", "Los Angeles", 58.0, 39.0, 240.0),
    "USA_CHICAGO": ForeignPerDiemRate("USA", "Chicago", 56.0, 37.0, 230.0),
    "USA_REST": ForeignPerDiemRate("USA", "Übrige USA", 52.0, 35.0, 195.0),

    # --- SCHWEIZ ---
    "SCHWEIZ_GENF": ForeignPerDiemRate("Schweiz", "Genf", 66.0, 44.0, 190.0),
    "SCHWEIZ_ZUERICH": ForeignPerDiemRate("Schweiz", "Zürich", 64.0, 43.0, 185.0),
    "SCHWEIZ_BASEL": ForeignPerDiemRate("Schweiz", "Basel", 62.0, 41.0, 175.0),
    "SCHWEIZ_BERN": ForeignPerDiemRate("Schweiz", "Bern", 60.0, 40.0, 170.0),
    "SCHWEIZ_REST": ForeignPerDiemRate("Schweiz", "Übrige Schweiz", 58.0, 39.0, 160.0),

    # --- ÖSTERREICH ---
    "OESTERREICH_WIEN": ForeignPerDiemRate("Österreich", "Wien", 44.0, 30.0, 149.0),
    "OESTERREICH_SALZBURG": ForeignPerDiemRate("Österreich", "Salzburg", 42.0, 28.0, 138.0),
    "OESTERREICH_INNSBRUCK": ForeignPerDiemRate("Österreich", "Innsbruck", 40.0, 27.0, 130.0),
    "OESTERREICH_REST": ForeignPerDiemRate("Österreich", "Übriges Österreich", 38.0, 25.0, 120.0),

    # --- GROSSBRITANNIEN / UK ---
    "UK_LONDON": ForeignPerDiemRate("Großbritannien", "London", 62.0, 41.0, 209.0),
    "UK_EDINBURGH": ForeignPerDiemRate("Großbritannien", "Edinburgh", 52.0, 35.0, 165.0),
    "UK_REST": ForeignPerDiemRate("Großbritannien", "Übriges UK", 48.0, 32.0, 145.0),

    # --- FRANKREICH ---
    "FRANKREICH_PARIS": ForeignPerDiemRate("Frankreich", "Paris", 58.0, 39.0, 159.0),
    "FRANKREICH_STRASSBURG": ForeignPerDiemRate("Frankreich", "Straßburg", 50.0, 33.0, 135.0),
    "FRANKREICH_LYON": ForeignPerDiemRate("Frankreich", "Lyon", 48.0, 32.0, 130.0),
    "FRANKREICH_REST": ForeignPerDiemRate("Frankreich", "Übriges Frankreich", 45.0, 30.0, 115.0),

    # --- ITALIEN ---
    "ITALIEN_MAILAND": ForeignPerDiemRate("Italien", "Mailand", 50.0, 33.0, 170.0),
    "ITALIEN_ROM": ForeignPerDiemRate("Italien", "Rom", 48.0, 32.0, 160.0),
    "ITALIEN_REST": ForeignPerDiemRate("Italien", "Übriges Italien", 42.0, 28.0, 125.0),

    # --- SPANIEN ---
    "SPANIEN_MADRID": ForeignPerDiemRate("Spanien", "Madrid", 46.0, 31.0, 140.0),
    "SPANIEN_BARCELONA": ForeignPerDiemRate("Spanien", "Barcelona", 46.0, 31.0, 145.0),
    "SPANIEN_KANAREN": ForeignPerDiemRate("Spanien", "Kanarische Inseln", 40.0, 27.0, 110.0),
    "SPANIEN_REST": ForeignPerDiemRate("Spanien", "Übriges Spanien", 38.0, 25.0, 105.0),

    # --- NIEDERLANDE ---
    "NIEDERLANDE_AMSTERDAM": ForeignPerDiemRate("Niederlande", "Amsterdam", 54.0, 36.0, 175.0),
    "NIEDERLANDE_REST": ForeignPerDiemRate("Niederlande", "Übrige Niederlande", 47.0, 31.0, 140.0),

    # --- BELGIEN ---
    "BELGIEN_BRUESSEL": ForeignPerDiemRate("Belgien", "Brüssel", 52.0, 35.0, 160.0),
    "BELGIEN_REST": ForeignPerDiemRate("Belgien", "Übriges Belgien", 45.0, 30.0, 130.0),

    # --- POLEN ---
    "POLEN_WARSCHAU": ForeignPerDiemRate("Polen", "Warschau", 44.0, 29.0, 125.0),
    "POLEN_BRESLAU": ForeignPerDiemRate("Polen", "Breslau (Wrocław)", 38.0, 25.0, 105.0),
    "POLEN_REST": ForeignPerDiemRate("Polen", "Übriges Polen", 34.0, 23.0, 90.0),

    # --- TSCHECHIEN ---
    "TSCHECHIEN_PRAG": ForeignPerDiemRate("Tschechien", "Prag", 42.0, 28.0, 120.0),
    "TSCHECHIEN_REST": ForeignPerDiemRate("Tschechien", "Übriges Tschechien", 34.0, 23.0, 85.0),

    # --- DÄNEMARK ---
    "DAENEMARK_KOPENHAGEN": ForeignPerDiemRate("Dänemark", "Kopenhagen", 68.0, 45.0, 195.0),
    "DAENEMARK_REST": ForeignPerDiemRate("Dänemark", "Übriges Dänemark", 58.0, 39.0, 160.0),

    # --- SCHWEDEN ---
    "SCHWEDEN_STOCKHOLM": ForeignPerDiemRate("Schweden", "Stockholm", 60.0, 40.0, 170.0),
    "SCHWEDEN_REST": ForeignPerDiemRate("Schweden", "Übriges Schweden", 52.0, 35.0, 145.0),

    # --- NORWEGEN ---
    "NORWEGEN_OSLO": ForeignPerDiemRate("Norwegen", "Oslo", 68.0, 45.0, 180.0),
    "NORWEGEN_REST": ForeignPerDiemRate("Norwegen", "Übriges Norwegen", 58.0, 39.0, 155.0),

    # --- JAPAN ---
    "JAPAN_TOKIO": ForeignPerDiemRate("Japan", "Tokio", 66.0, 44.0, 220.0),
    "JAPAN_REST": ForeignPerDiemRate("Japan", "Übriges Japan", 52.0, 35.0, 160.0),

    # --- CHINA ---
    "CHINA_PEKING": ForeignPerDiemRate("China", "Peking (Beijing)", 54.0, 36.0, 160.0),
    "CHINA_SHANGHAI": ForeignPerDiemRate("China", "Shanghai", 56.0, 37.0, 170.0),
    "CHINA_HONGKONG": ForeignPerDiemRate("China", "Hongkong", 64.0, 43.0, 210.0),
    "CHINA_REST": ForeignPerDiemRate("China", "Übriges China", 45.0, 30.0, 125.0),

    # --- SINGAPUR ---
    "SINGAPUR": ForeignPerDiemRate("Singapur", "Singapur", 66.0, 44.0, 225.0),

    # --- VEREINIGTE ARABISCHE EMIRATE ---
    "VAE_DUBAI": ForeignPerDiemRate("VAE", "Dubai", 60.0, 40.0, 210.0),
    "VAE_ABU_DHABI": ForeignPerDiemRate("VAE", "Abu Dhabi", 60.0, 40.0, 205.0),
    "VAE_REST": ForeignPerDiemRate("VAE", "Übrige VAE", 50.0, 33.0, 160.0),

    # --- KANADA ---
    "KANADA_TORONTO": ForeignPerDiemRate("Kanada", "Toronto", 56.0, 37.0, 190.0),
    "KANADA_VANCOUVER": ForeignPerDiemRate("Kanada", "Vancouver", 56.0, 37.0, 195.0),
    "KANADA_REST": ForeignPerDiemRate("Kanada", "Übriges Kanada", 48.0, 32.0, 150.0),

    # --- AUSTRALIEN ---
    "AUSTRALIEN_SYDNEY": ForeignPerDiemRate("Australien", "Sydney", 64.0, 43.0, 215.0),
    "AUSTRALIEN_MELBOURNE": ForeignPerDiemRate("Australien", "Melbourne", 60.0, 40.0, 195.0),
    "AUSTRALIEN_REST": ForeignPerDiemRate("Australien", "Übriges Australien", 52.0, 35.0, 160.0),

    # --- TÜRKEI ---
    "TUERKEI_ISTANBUL": ForeignPerDiemRate("Türkei", "Istanbul", 46.0, 31.0, 130.0),
    "TUERKEI_ANKARA": ForeignPerDiemRate("Türkei", "Ankara", 40.0, 27.0, 105.0),
    "TUERKEI_REST": ForeignPerDiemRate("Türkei", "Übrige Türkei", 35.0, 23.0, 85.0),

    # --- BRASILIEN ---
    "BRASILIEN_SAO_PAULO": ForeignPerDiemRate("Brasilien", "São Paulo", 52.0, 35.0, 155.0),
    "BRASILIEN_RIO": ForeignPerDiemRate("Brasilien", "Rio de Janeiro", 50.0, 33.0, 150.0),
    "BRASILIEN_REST": ForeignPerDiemRate("Brasilien", "Übriges Brasilien", 40.0, 27.0, 110.0),

    # --- INDIEN ---
    "INDIEN_MUMBAI": ForeignPerDiemRate("Indien", "Mumbai", 48.0, 32.0, 160.0),
    "INDIEN_DELHI": ForeignPerDiemRate("Indien", "Neu-Delhi", 46.0, 31.0, 150.0),
    "INDIEN_BANGALORE": ForeignPerDiemRate("Indien", "Bengaluru (Bangalore)", 44.0, 29.0, 140.0),
    "INDIEN_REST": ForeignPerDiemRate("Indien", "Übriges Indien", 36.0, 24.0, 100.0),

    # --- SÜDKOREA ---
    "SUEDKOREA_SEOUL": ForeignPerDiemRate("Südkorea", "Seoul", 62.0, 41.0, 190.0),
    "SUEDKOREA_REST": ForeignPerDiemRate("Südkorea", "Übriges Südkorea", 50.0, 33.0, 140.0),

    # --- SÜDAFRIKA ---
    "SUEDAFRIKA_KAPSTADT": ForeignPerDiemRate("Südafrika", "Kapstadt", 46.0, 31.0, 140.0),
    "SUEDAFRIKA_JOHANNESBURG": ForeignPerDiemRate("Südafrika", "Johannesburg", 44.0, 29.0, 135.0),
    "SUEDAFRIKA_REST": ForeignPerDiemRate("Südafrika", "Übriges Südafrika", 36.0, 24.0, 105.0),

    # --- MEXIKO ---
    "MEXIKO_STADT": ForeignPerDiemRate("Mexiko", "Mexiko-Stadt", 46.0, 31.0, 145.0),
    "MEXIKO_REST": ForeignPerDiemRate("Mexiko", "Übriges Mexiko", 38.0, 25.0, 110.0),

    # --- IRLAND ---
    "IRLAND_DUBLIN": ForeignPerDiemRate("Irland", "Dublin", 58.0, 39.0, 165.0),
    "IRLAND_REST": ForeignPerDiemRate("Irland", "Übriges Irland", 48.0, 32.0, 130.0),

    # --- PORTUGAL ---
    "PORTUGAL_LISSABON": ForeignPerDiemRate("Portugal", "Lissabon", 46.0, 31.0, 125.0),
    "PORTUGAL_REST": ForeignPerDiemRate("Portugal", "Übriges Portugal", 38.0, 25.0, 95.0),

    # --- LUXEMBURG ---
    "LUXEMBURG": ForeignPerDiemRate("Luxemburg", "Luxemburg", 52.0, 35.0, 150.0),
}


def get_per_diem_rate(destination_key: str) -> ForeignPerDiemRate:
    key = destination_key.upper()
    if key in BMF_FOREIGN_RATES:
        return BMF_FOREIGN_RATES[key]
    # Fallback to standard foreign rate if key not exact
    for k, v in BMF_FOREIGN_RATES.items():
        if key in k:
            return v
    return BMF_FOREIGN_RATES["USA_REST"]
