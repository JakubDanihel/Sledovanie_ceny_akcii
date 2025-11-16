# Sledovanie_ceny_akcii

Tento Python skript automaticky monitoruje dennú zmenu ceny pre zadanú akciu, získava najnovšie správy o danej spoločnosti a posiela súhrnné upozornenie e-mailom.

## Funkcie

- **Monitorovanie cien:** Získava denné uzatváracie ceny akcií z Yahoo Finance.
- **Analýza zmeny:** Vypočíta percentuálnu a absolútnu zmenu ceny medzi poslednými dvoma obchodnými dňami.
- **Agregácia správ:** Sťahuje najnovšie relevantné správy zo služby NewsAPI.org.
- **Notifikácie:** Formátuje prehľadnú správu a odosiela ju ako e-mailové upozornenie cez zabezpečený SMTP server Gmailu.
- **Robustnosť:** Obsahuje spracovanie chýb pri odosielaní e-mailu a pri komunikácii s API.

---

## Požiadavky

Pred spustením skriptu je potrebné mať nainštalovaný Python 3 a nasledujúce knižnice:

```bash
pip install yfinance requests
```

Knižnice `smtplib` a `email.message` sú súčasťou štandardnej knižnice Pythonu a nie je potrebné ich inštalovať.

---

## Konfigurácia

Všetky nastavenia sa nachádzajú na začiatku súboru `main.py`. Pred prvým spustením je potrebné ich správne nastaviť.

### 1. Nastavenia Akcie a Správ

- `STOCK_NAME`: Symbol (ticker) akcie, ktorú chcete sledovať (napr. `"TSLA"` pre Teslu, `"AAPL"` pre Apple).
- `COMPANY_NAME`: Plný názov spoločnosti. Používa sa na presnejšie vyhľadávanie správ.
- `NEWS_API_KEY`: Váš osobný API kľúč od služby NewsAPI.org. Pre získanie kľúča je potrebná bezplatná registrácia.

### 2. Nastavenia pre E-mail

- `SEND_EMAIL`: Nastavte na `True`, ak chcete posielať e-mailové upozornenia, alebo na `False`, ak chcete iba výpis do konzoly.
- `EMAIL_SENDER`: Vaša Gmail adresa, z ktorej sa bude e-mail odosielať.
- `EMAIL_RECEIVER`: E-mailová adresa príjemcu upozornenia.
- `EMAIL_APP_PASSWORD`: **16-miestne heslo pre aplikáciu (App Password)**.
  - **DÔLEŽITÉ:** Toto **nie je** vaše bežné heslo k Gmail účtu.
  - Pre jeho získanie musíte mať na svojom Google účte zapnuté dvojfaktorové overenie (2FA).
  - Heslo vygenerujete v nastaveniach svojho Google účtu v sekcii **Zabezpečenie -> Heslá aplikácií**.

---

## Použitie

Po správnom nastavení konfiguračných premenných stačí spustiť skript z príkazového riadka:

```bash
python main.py
```

Skript vykoná všetky kroky a vypíše výslednú správu do konzoly. Ak je povolené odosielanie e-mailov, odošle ju aj na zadanú adresu.

---

## Štruktúra Kódu

- **Importy:** Načítanie potrebných knižníc (`yfinance`, `requests`, `smtplib`).
- **Konfigurácia:** Všetky používateľské nastavenia sú centralizované na začiatku súboru.
- **Funkcia `send_email()`:** Zapuzdruje logiku pre vytvorenie a odoslanie e-mailovej správy vrátane spracovania chýb.
- **Získanie dát o akciách:** Pomocou `yfinance` sa stiahnu historické dáta.
- **Spracovanie cien:** Vypočíta sa rozdiel medzi poslednými dvoma dňami.
- **Získanie správ:** Pomocou `requests` sa odošle požiadavka na NewsAPI a spracujú sa prijaté články.
- **Finálny výstup:** Zostavenie tela správy, výpis do konzoly a volanie funkcie `send_email()`.
  
