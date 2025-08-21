# -*- coding: utf-8 -*-

def berechne_leistung(spannung, strom):
    """Berechnet die Leistung in Watt aus Spannung (V) and Strom (A)."""
    return spannung * strom

def berechne_energieverbrauch(leistung, betriebsstunden):
    """Berechnet den Energieverbrauch in Wattstunden (Wh)."""
    return leistung * betriebsstunden

def schaetze_laufzeit(energiequelle_wh, verbrauch_w):
    """Schätzt die Laufzeit in Stunden."""
    if verbrauch_w <= 0:
        return float('inf')  # Unendliche Laufzeit, wenn kein Verbrauch
    return energiequelle_wh / verbrauch_w

def schaetze_solarenergie_gewinn(panel_leistung_wp, durchschnittliche_sonnenstunden):
    """Schätzt den täglichen Energiegewinn durch ein Solarpanel in Wh."""
    # Annahme eines durchschnittlichen Wirkungsgrades von 75% unter realen Bedingungen
    wirkungsgrad = 0.75
    return panel_leistung_wp * durchschnittliche_sonnenstunden * wirkungsgrad

def main():
    # --- GERÄTEKONFIGURATION & SCHÄTZWERTE ---

    # Hier können Sie die geschätzten Werte für Spannung (V) und Strom (A) anpassen.

    # ROBOTER Komponenten
    roboter_komponenten = {
        'Raspberry Pi': {'spannung': 5, 'strom': 1.0},  # Durchschnittlicher Verbrauch [1]
        'WiFi + 5G Router': {'spannung': 12, 'strom': 0.8}, # Geschätzt basierend auf typischen Werten [2]
        'Ethernet Switch': {'spannung': 5, 'strom': 0.5}, # Geschätzt [3]
        'ESP - RGB Camera': {'spannung': 5, 'strom': 0.4},
        'ESP - IR Camera': {'spannung': 5, 'strom': 0.4},
        'ESP - LIDAR': {'spannung': 5, 'strom': 0.5},
        'ESP - GPS Receiver': {'spannung': 5, 'strom': 0.2},
        'ESP - Flowrate & Pumps': {'spannung': 5, 'strom': 1.2} # Annahme, dass Pumpen nicht dauerhaft laufen
    }

    # DOCKINGSTATION Komponenten
    dockingstation_komponenten = {
        'Raspberry Pi': {'spannung': 5, 'strom': 0.8},
        'WiFi Router / Hotspot': {'spannung': 12, 'strom': 0.5},
        'ESP - 4x Linear Actuators': {'spannung': 12, 'strom': 2.0}, # Hoher Verbrauch bei Bewegung, hier gemittelt
        'ESP - 2x Pumps + 3x Valves': {'spannung': 12, 'strom': 1.5}, # Annahme für intermittierenden Betrieb
        'ESP - IR-LED + GPS': {'spannung': 5, 'strom': 0.3}
    }

    # ENERGIEQUELLEN
    roboter_batterie_wh = 100  # Kapazität der Roboterbatterie in Wh (z.B. 10Ah bei 10V)
    station_powerbank_wh = 200 # Kapazität der Powerbank in Wh (z.B. eine große Powerbank mit ca. 55.000 mAh bei 3.7V)

    # SOLARPANEL
    solarpanel_leistung_wp = 50  # Leistung des Solarpanels in Watt-Peak
    # Durchschnittliche tägliche Sonnenstunden in Deutschland (variiert stark nach Jahreszeit)
    durchschnittliche_sonnenstunden_deutschland = 4.7 # Durchschnittlicher Jahreswert [4]

    # --- BERECHNUNGEN ---

    # Gesamtleistung des Roboters
    roboter_gesamtleistung_w = sum(berechne_leistung(k['spannung'], k['strom']) for k in roboter_komponenten.values())

    # Gesamtleistung der Dockingstation
    dockingstation_gesamtleistung_w = sum(berechne_leistung(k['spannung'], k['strom']) for k in dockingstation_komponenten.values())

    # Laufzeitschätzungen
    roboter_laufzeit_h = schaetze_laufzeit(roboter_batterie_wh, roboter_gesamtleistung_w)
    station_laufzeit_h = schaetze_laufzeit(station_powerbank_wh, dockingstation_gesamtleistung_w)

    # Solarenergiegewinn
    taeglicher_solargewinn_wh = schaetze_solarenergie_gewinn(solarpanel_leistung_wp, durchschnittliche_sonnenstunden_deutschland)
    
    # Effektiver Verbrauch der Station mit Solarunterstützung (über 24h gemittelt)
    durchschnittliche_solar_leistung_w = taeglicher_solargewinn_wh / 24
    station_effektiver_verbrauch_w = dockingstation_gesamtleistung_w - durchschnittliche_solar_leistung_w
    
    station_laufzeit_mit_solar_h = schaetze_laufzeit(station_powerbank_wh, station_effektiver_verbrauch_w)


    # --- AUSGABE ---
    
    print("--- Energieverbrauchs- und Laufzeitschätzung ---")
    
    print("\nROBOTER:")
    print(f"  - Geschätzte Gesamtleistung: {roboter_gesamtleistung_w:.2f} W")
    print(f"  - Batteriekapazität: {roboter_batterie_wh} Wh")
    print(f"  - Geschätzte Laufzeit: {roboter_laufzeit_h:.2f} Stunden")
    
    print("\nDOCKINGSTATION:")
    print(f"  - Geschätzte Gesamtleistung: {dockingstation_gesamtleistung_w:.2f} W")
    print(f"  - Powerbank-Kapazität: {station_powerbank_wh} Wh")
    print(f"  - Geschätzte Laufzeit (ohne Solar): {station_laufzeit_h:.2f} Stunden")
    
    print("\nSOLARUNTERSTÜTZUNG (Dockingstation):")
    print(f"  - Leistung des Solarpanels: {solarpanel_leistung_wp} Wp")
    print(f"  - Durchschnittliche tägliche Sonnenstunden: {durchschnittliche_sonnenstunden_deutschland} h")
    print(f"  - Geschätzter täglicher Energiegewinn: {taeglicher_solargewinn_wh:.2f} Wh")
    print(f"  - Effektiver Verbrauch der Station mit Solar (gemittelt): {station_effektiver_verbrauch_w:.2f} W")
    if station_effektiver_verbrauch_w < 0:
        print("  - Die Station erzeugt im Durchschnitt mehr Energie als sie verbraucht (energetisch autark).")
    else:
        print(f"  - Geschätzte Laufzeit mit Solarunterstützung: {station_laufzeit_mit_solar_h:.2f} Stunden")


if __name__ == '__main__':
    main()

"""
Quellen: 
1. Stromverbrauch Raspi: https://praxistipps.chip.de/raspberry-pi-4-so-hoch-ist-der-stromverbrauch-des-geraetes_148874
2. Stromverbrauch Router: https://www.stromguide.com/ratgeber/stromverbrauch-router/
3. Stromverbrauch Switch: https://meintechblog.de/2014/08/06/gigabit-speed-im-ganzen-haushalt-5-port-switch-tp-link-tl-sg-105/
4. Durchschnittliche Sonnenstunden in Deutschland: https://www.kliwa.de/klima-klimagroessen-langzeitverhalten.htm
"""
