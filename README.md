# DACH Auslandstagegeld- & Reisekostenpauschalen-Rechner 2026 🌍✈️

[![CI](https://github.com/DACHDigitalwerk/auslands-reisekosten-tagegeld-rechner-dach/actions/workflows/ci.yml/badge.svg)](https://github.com/DACHDigitalwerk/auslands-reisekosten-tagegeld-rechner-dach/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![DACH Compliance](https://img.shields.io/badge/BMF%202026-EStG%20§%209%20Abs.%204a-success.svg)](https://dachdigitalwerk.github.io/auslandsreisekosten-tagegeld-rechner/)

> **Produktionsreife Berechnungs-Engine & CLI für BMF-Auslandstagegelder, gesetzliche Mahlzeitenkürzungen (20/40/40) und Übernachtungspauschalen 2026 für Deutschland, Österreich und die Schweiz.**

Berechnen Sie in Sekunden die steuerfreie Reisekostenvergütung für weltweite Dienstreisen. Vollständig konform mit der amtlichen **BMF-Auslandstabelle 2026** (§ 9 Abs. 4a EStG), den österreichischen Auslandssätzen nach § 26 Z 4 EStG sowie Schweizer Spesenreglementen.

🌐 **Interaktives Web-Tool:** [https://dachdigitalwerk.github.io/auslandsreisekosten-tagegeld-rechner/](https://dachdigitalwerk.github.io/auslandsreisekosten-tagegeld-rechner/)

---

## 🎯 Kernfunktionen

- **Amtliche BMF-Pauschalen 2026:** Aktuelle Verpflegungsmehraufwendungen (24h-Volltag & >8h An-/Abreisetag) sowie Übernachtungspauschalen für über 180 weltweite Destinationen (USA, Schweiz, UK, Frankreich, Japan, Singapur, VAE, u. v. m.).
- **Gesetzliche Mahlzeitenkürzung (§ 9 Abs. 4a Satz 8 EStG):**
  - **Frühstück:** -20 % des *vollen 24-Stunden-Satzes*
  - **Mittagessen:** -40 % des *vollen 24-Stunden-Satzes*
  - **Abendessen:** -40 % des *vollen 24-Stunden-Satzes*
  - *Wichtig:* Kürzungen beziehen sich nach deutschem Steuerrecht **immer auf den vollen 24-Stunden-Satz**, auch an An- und Abreisetagen!
- **Deckelung bei 0,00 €:** Ein Reisetag kann durch Mahlzeitenkürzungen steuerlich nie ins Negative fallen.
- **Mehrtägige Reisepläne (Itinerary Engine):** Nahtlose Berechnung komplexer Reisen mit gemischten Reisetagen, Verpflegungsnachweisen und Hotelabrechnungen (Pauschale vs. Einzelbeleg).
- **Export & CLI:** Strukturierte JSON-Ausgabe und lesbare ASCII-Abrechnungsberichte.

---

## 📦 Installation

```bash
git clone https://github.com/DACHDigitalwerk/auslands-reisekosten-tagegeld-rechner-dach.git
cd auslands-reisekosten-tagegeld-rechner-dach
pip install -e .
```

---

## 🚀 CLI-Nutzung

Nach der Installation steht der Konsolenbefehl `dach-ausland` zur Verfügung:

### 1. Schnelle Reisekostenberechnung (New York, 3 Tage)
```bash
dach-ausland --destination USA_NEW_YORK --days 3 --breakfasts 2 --lunches 1
```

**Ausgabe:**
```text
=================================================================
 BMF REISEKOSTENABRECHNUNG AUSLAND 2026: USA (New York City)
=================================================================
 Reisedauer gesamt:        3 Tage (1 volle Tage, 2 An-/Abreisetage)
 Summe Basispauschalen:        154.00 €
 Abzug Mahlzeiten:        -     52.80 €
 Netto-Verpflegungsmehraufwand: 101.20 €
 Übernachtungskosten:            0.00 €
-----------------------------------------------------------------
 GESAMTANSPRUCH (STEUERFREI):  101.20 €
=================================================================
```

### 2. Destinationen durchsuchen
```bash
dach-ausland --search "zürich"
```

### 3. Alle BMF-Pauschalen auflisten
```bash
dach-ausland --list-destinations
```

### 4. JSON-Export für ERP & Buchhaltung
```bash
dach-ausland --destination FRANKREICH_PARIS --days 4 --breakfasts 3 --json
```

---

## 💻 Python API Quickstart

```python
from auslandsreise_dach import (
    DayType,
    TravelDayInput,
    calculate_trip,
    get_per_diem_rate,
)

# 1. BMF-Sätze abrufen
rate = get_per_diem_rate("SCHWEIZ_ZUERICH")
print(f"Zürich: 24h = {rate.full_day_rate_eur} €, An/Ab = {rate.partial_day_rate_eur} €")

# 2. Reisetage definieren
trip_days = [
    TravelDayInput(
        date_str="2026-06-15",
        destination_key="SCHWEIZ_ZUERICH",
        day_type=DayType.ARRIVAL_DEPARTURE,
        provided_dinner=True,
        actual_hotel_cost_eur=220.0,
    ),
    TravelDayInput(
        date_str="2026-06-16",
        destination_key="SCHWEIZ_ZUERICH",
        day_type=DayType.FULL_DAY,
        provided_breakfast=True,
        provided_lunch=True,
        actual_hotel_cost_eur=220.0,
    ),
    TravelDayInput(
        date_str="2026-06-17",
        destination_key="SCHWEIZ_ZUERICH",
        day_type=DayType.ARRIVAL_DEPARTURE,
        provided_breakfast=True,
    ),
]

# 3. Abrechnung erstellen
result = calculate_trip(trip_days)
print(f"Netto-Tagegelder: {result.total_net_per_diems:.2f} €")
print(f"Steuerfreier Gesamtanspruch: {result.grand_total_reimbursement:.2f} €")
```

---

## ⚖️ Rechtlicher Hinweis & Disclaimer

> **Wichtiger Hinweis gem. BGH-Rechtsprechung (Az. I ZR 113/20 & I ZR 226/20):**  
> Diese Software, die CLI-Tools und die Berechnungsalgorithmen dienen ausschließlich der unverbindlichen Orientierung, Information und mathematischen Simulation von Reisekostenabrechnungen nach den Richtlinien des Bundesministeriums der Finanzen (BMF). Sie stellen ausdrücklich **keine** Rechts- oder Steuerberatung im Sinne des Steuerberatungsgesetzes (StBerG) oder Rechtsdienstleistungsgesetzes (RDG) dar. Für verbindliche steuerliche Reisekostenabrechnungen oder betriebliche Spesenvereinbarungen konsultieren Sie bitte einen qualifizierten Steuerberater oder Wirtschaftsprüfer.

---

## 📄 Lizenz

Dieses Projekt steht unter der **MIT-Lizenz**. Details finden Sie in der [LICENSE](LICENSE)-Datei.
