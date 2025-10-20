import os

class Config:
    MOCK_PAYMENTS_CALLBACK_SECRET: str = os.getenv("SHARED_CALLBACK_SECRET")
    MOCK_PAYMENTS_URL: str = os.getenv("MOCK_PAYMENTS_URL")
    RETRY_ATTEMPTS = 3
    MAX_WEBHOOK_AGE = 300
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("GOOGLE_AUTH_REDIRECT_URI")
    GOOGLE_AUTH_BASE_URL = "https://oauth2.googleapis.com"
    GOOGLE_ACCOUNTS_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth?"
    CODE_CHALLENGE = os.getenv("CODE_CHALLENGE", "S256")
    FRONTEND_SUCCESS_URL = "http://localhost/login/success"
    FRONTEND_ERROR_URL = "http://localhost/login/failure"
    MAX_TIMESTAMP_RETRIES = 3
    VALID_CURRENCIES = [
        "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN",
        "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BOV",
        "BRL", "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHE", "CHF",
        "CHW", "CLF", "CLP", "CNY", "COP", "COU", "CRC", "CUC", "CUP", "CVE",
        "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD",
        "FKP", "GBP", "GEL", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD",
        "HNL", "HRK", "HTG", "HUF", "IDR", "ILS", "INR", "IQD", "IRR", "ISK",
        "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW", "KWD",
        "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL",
        "MGA", "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR", "MWK", "MXN",
        "MXV", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR",
        "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD",
        "CNY", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP",
        "SLL", "SOS", "SRD", "SSP", "STN", "SVC", "SYP", "SZL", "THB", "TJS",
        "TMT", "TND", "TOP", "TRY", "TTD", "TWD", "TZS", "UAH", "UGX", "USD",
        "USN", "UYI", "UYU", "UYW", "UZS", "VED", "VES", "VND", "VUV", "WST",
        "XAF", "XAG", "XAU", "XBA", "XBB", "XBC", "XBD", "XCD", "XDR", "XOF",
        "XPD", "XPF", "XPT", "XSU", "XTS", "XUA", "XXX", "YER", "ZAR", "ZMW",
        "ZWL"
    ]

config = Config()