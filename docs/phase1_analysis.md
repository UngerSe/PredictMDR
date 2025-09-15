Phase 1 - Analyseergebnis

Datenquelle: data/raw/dataset.csv
Zeilen: 7617722
Spalten: ['c_van17', 'c_serial_number', 'msg_timestamp', 'c_HWEL', 'c_SWFL_MOD', 'c_SWFL_ACT', 'c_istep', 'c_date_of_programming_local', 'c_date_of_programming_utc', 'status_75', 'mileage', 'ClSin300', 'ClSin150', 'ClSin50', 'ClCos300', 'ClCos150', 'ClCos50', 'ClSinCos300', 'ClSinCos150', 'ClSinCos50', 'OfsSin200', 'OfsSin100', 'OfsCos200', 'OfsCos100', 'InvSampTurn', 'PUIdle', 'PUGo2Idle', 'PUPrsMgr', 'VDown', 'PUPrsEql', 'PUZpd', 'VRange', 'RawRadius', 'AmpSyncCheck', 'OfsCheckDev', 'InvSampTime', 'RadV_25per', 'AmpDevStrict', 'OfsDevTight', 'RadV_50per', 'ZpdReq', 'OffsReset', 'FastOffComp', 'ErrorBandEntry', 'ErrorBandDur', 'ErrorBandPwrSupply', 'ErrorBandGnd', 'EarlyIndRadDur', 'OldFttiCheck', 'DevOffsetCorr', 'EarlyIndRadVDur', 'InvalidTimerLowSpd', 'RadiusVSpdEntry', 'LowSpdSinCos2', 'LowSpdSinCos', 'RegpRadIdleEntry', 'TransitionsMopsless', 'Mps_elec_final', 'Sum_of_all_other_failures', 'ZPDRequestInvalidSample', 'MOCControlMode', 'SnapshotBemfCrossCheck', 'ZPDRequest', 'EcuLifeT', 'DriverBraking_str', 'c_mps_bereich', 'time_to_fail']
Spaltenanzahl: 67

Wichtige Spalten
- Seriennummer: c_serial_number
- Zeitstempel: msg_timestamp
- Zielvariable (Platzhalter): time_to_fail (muss noch umkonvertiert werden)
- Weitere: tbd

Annahmen
- Timestamp konvertiert, falls vorhanden.
- Zielvariable time_to_fail wird aktuell als Binärziel durch time_to_fail > 0 abgebildet (Platzhalter).

Offene Fragen
- Welche Spalten denkst du sind am relevantesten?
- Wie würdest du die Zielvariable definieren
- 