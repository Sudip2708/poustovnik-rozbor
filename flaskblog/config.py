#######################################################################################################################
# 02 #
# KONFIGURAČNÍ SOUBOR PROGRAMU #
# tento soubor obsahuje třídu pro nastavení databáze, tajného klíče a mailu #

# 02-1: import externích rozšíření programu
# 02-2: vytvoření třídy pro konfiguraci aplikace
# 02-3: inicializace importovaných modulů
# 02-4: funkce pro vytvoření aplikace


#######################################################################################################################
# 02-1 #
# import externích rozšíření programu:

import os
# os: je modul pro funkce závislých na operačním systému
# https://docs.python.org/3/library/os.html


#######################################################################################################################
# 02-2 #
# vytvoření třídy pro konfiguraci aplikace:

class Config:

    # print(os.environ.get('SECRET_KEY'))
    # vytvoření tajného klíče (používá se například pro to, aby nebylo posíláno heslo ale jeho hash):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # SECRET_KEY: definování tajného klíče, který Tajný klíč, který bude použit pro bezpečné podepsání souboru cookie relace a může být použit pro jakékoli další potřeby související se zabezpečením rozšířeními nebo vaší aplikací.
    # os.environ.get('SECRET_KEY'): tajný klíč uložený s systému (je potřeba vytvořit proměnou prostředí ve win a mít import os)

    # print(os.environ.get('SQLALCHEMY_DATABASE_URI'))
    # definice cesty k databázi:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    # SQLALCHEMY_DATABASE_URI: identifikátor URI databáze, který je použit pro připojení k databázi
    # 'sqlite:///site.db': databáze sqlite se nachází v kořenovém adresáři aplikace (///: relativní cesta)

    # mail - nastavení serveru (nastavení pro gmail: https://mailmeteor.com/blog/gmail-smtp-settings)
    MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_SERVER: definice mail serveru
    # 'smtp.gmail.com': odkaz na google

    # mail - nastavení portu
    MAIL_PORT = 587
    # MAIL_PORT: definice mail portu
    # 587: definice hodnoty (pro STARTTLS, použijte 587, pro SSL/TLS použijte 465)

    # mail - definice typu zabezpečení
    MAIL_USE_TLS = True
    # MAIL_USE_TLS: definice typu zabezpečení STARTTLS
    # True: definice hodnoty (povolte buď STARTTLS nebo SSL/TLS, ne obojí)

    # mail - definice přihlašovacího jména (přes proměnou uloženou v systému)
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    # MAIL_USERNAME: definice přihlašovacího emailu
    # os.environ.get('EMAIL_USER'): přihlašovací email uložený s systému (je potřeba vytvořit proměnou prostředí ve win a mít import os)

    # mail - definice přihlašovacího hesla (přes proměnou uloženou v systému)
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    # MAIL_PASSWORD: definice přihlašovacího hesla
    # os.environ.get('EMAIL_PASS'): přihlašovací heslo uložené s systému (je potřeba vytvořit proměnou prostředí ve win a mít import os)

    # mail - definice odesílacího mailu (je-li definován, nemusí se vyplňovat při odesílání mailu sender) (přes proměnou uloženou v systému)
    MAIL_DEFAULT_SENDER = os.environ.get('EMAIL_USER')
    # MAIL_USERNAME: definice přihlašovacího emailu
    # os.environ.get('MAIL_DEFAULT_SENDER '): email uložený s systému který bude uveden jako email odkud zpráva přišla (je potřeba vytvořit proměnou prostředí ve win a mít import os)


#######################################################################################################################