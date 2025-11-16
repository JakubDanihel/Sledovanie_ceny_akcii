# --- Importovanie potrebnych kniznic ---
import yfinance as yf
import requests
import smtplib
import email.message

# --- Nastavenia ---
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
NEWS_API_KEY = "8ba86b46fafa4b348da6688c70899117"

# --- Nastavenia pre E-mail ---
# UPOZORNENIE: Heslo aplikacie nie je to iste ako heslo k vasmu Gmail uctu!
# Pre Gmail je potrebne vygenerovat "App Password".
SEND_EMAIL = True
EMAIL_SENDER = "testprogramko@gmail.com"
EMAIL_APP_PASSWORD = "fxsb awdp seti tlso"
EMAIL_RECEIVER = "testprogramko@gmail.com"


def send_email(subject, body):
    """Pripoji sa k SMTP serveru Gmail a odosle e-mail."""
    print(f"\nPripravujem a posielam e-mail na {EMAIL_RECEIVER}...")

    msg = email.message.EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_SENDER, EMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("E-mail bol uspesne odoslany!")
    except smtplib.SMTPAuthenticationError:
        print("CHYBA: Overenie zlyhalo. Skontrolujte spravnost e-mailu a hesla pre aplikaciu.")
    except Exception as e:
        print(f"CHYBA: Nepodarilo sa odoslat e-mail. Dovod: {e}")


# --- Priprava obsahu pre vypis a e-mail ---
email_lines = []
znamenko = ""
percentualna_zmena = 0.0

# --- 1. Ziskanie dat o akciach ---
stock = yf.Ticker(STOCK_NAME)
hist = stock.history(period="5d")

# --- 2. Spracovanie cien akcii ---
if len(hist) >= 2:
    predvcerajsia_cena_close = hist['Close'].iloc[-2]
    vcerajsia_cena_close = hist['Close'].iloc[-1]
    rozdiel = vcerajsia_cena_close - predvcerajsia_cena_close
    percentualna_zmena = (rozdiel / predvcerajsia_cena_close) * 100 if predvcerajsia_cena_close != 0 else 0
    znamenko = "🔺" if rozdiel > 0 else "🔻"

    email_lines.append(f"Informacie pre {COMPANY_NAME} ({STOCK_NAME}):")
    email_lines.append(f"Vcerajsia uzatvaracia cena: {vcerajsia_cena_close:.2f} USD")
    email_lines.append(f"Predvcerajsia uzatvaracia cena: {predvcerajsia_cena_close:.2f} USD")
    email_lines.append(f"Rozdiel: {znamenko} {rozdiel:.2f} USD ({percentualna_zmena:.2f}%)")
    email_lines.append("-" * 40)
else:
    print(f"Nepodarilo sa ziskat dostatok historickych dat pre {STOCK_NAME}.")
    exit()

# --- 3. Ziskanie sprav ---
email_lines.append("Najnovsie spravy:\n")
news_params = {
    "qInTitle": COMPANY_NAME,
    "apiKey": NEWS_API_KEY,
    "language": "en",
    "sortBy": "publishedAt",
}
news_response = requests.get("https://newsapi.org/v2/everything", params=news_params)

if news_response.status_code == 200:
    articles = news_response.json().get("articles", [])
    if not articles:
        email_lines.append(f"Nenasli sa ziadne relevantne spravy pre '{COMPANY_NAME}'.")
    else:
        for article in articles[:3]:
            email_lines.append(f"Nadpis: {article['title']}")
            email_lines.append(f"   Zdroj: {article['source']['name']}")
            email_lines.append(f"   URL: {article['url']}\n")
else:
    email_lines.append(f"Chyba pri ziskavani sprav: {news_response.status_code} - {news_response.text}")

# --- Finalny vystup ---
email_body = "\n".join(email_lines)
print(email_body)

# --- 4. Odoslanie e-mailu ---
if SEND_EMAIL:
    email_subject = f"Stock Alert pre {STOCK_NAME}: {znamenko} {percentualna_zmena:.2f}%"
    send_email(email_subject, email_body)
