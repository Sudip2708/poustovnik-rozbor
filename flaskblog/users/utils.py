#######################################################################################################################
# USERS-04 #
# SOUBOR PRO FUNKCE SPOJENÉ S DATY UŽIVATELE USERS #
# tento soubor slouží pro definici funkcí pro práci s daty uživatele   #

# USERS-04-1: import externích rozšíření programu
# USERS-04-2: import vlastních rozšíření programu
# USERS-04-3: definice funkce na ukládání obrázků
# USERS-04-4: funkce na odesílání tokenu pro změnu hesla


#######################################################################################################################
# USERS-04-1 #
# import externích rozšíření programu:

# import modulu pro práci s daty v rámci os
import os
# os: je modul pro funkce závislých na operačním systému
# https://docs.python.org/3/library/os.html

# import modulu pro generování náhodných čísel
import secrets
# secrets: se používá pro generování kryptograficky silných náhodných čísel vhodných pro správu dat, jako jsou hesla, autentizace účtů, bezpečnostní tokeny a související tajemství
# https://docs.python.org/3/library/secrets.html

# import modulu pro úpravu obrázku (např. velikosti)
from PIL import Image
# PIL: je knihovna Python pro úpravu obrázků
# Image: třída pro vytvoření instance pro upravovaný obrázek
# před importem je potřeba rozšíření doinstalovat > python3 -m pip install --upgrade pip
# před importem je potřeba rozšíření doinstalovat > python3 -m pip install --upgrade Pillow.
# https://pillow.readthedocs.io/en/stable/

# import Flask modulů
from flask import url_for, current_app
# flask: je webový microframework pro tvorbu webu v programovacím jazyku Python
# url_for: metoda pro vygenerování url adresy k souborům projektu
# current_app: metoda pro navracení aktuální aplikace
# https://flask.palletsprojects.com/en/2.3.x/quickstart/

# import třídy pro odesílání mailů
from flask_mail import Message
# flask_mail: poskytuje jednoduché rozhraní pro nastavení SMTP a pro odesílání zpráv z vašich pohledů a skriptů
# Message: třída pro zapouzdření a odeslání emailu

from flask_babel import lazy_gettext
# flask_babel: rozšíření pro lokalizaci stránek
# lazy_gettext: metoda pro označení textu, který bude překládán až ve chvíli volání


#######################################################################################################################
# USERS-04-2 #
# import vlastních rozšíření programu:

# import vytvořené instance pro odesílání mailů
from flaskblog import mail
# flaskblog: cesta k souboru (__init__.py v kořenovém adresáři programu)
# mail: instance třídy Mail pro odesílání mailů


#######################################################################################################################
# USERS-04-3 #
# definice funkce na ukládání obrázků:

def save_picture(form_picture):
    # save_picture: název vytvářené funkce
    # form_picture: obrázek vložený uživatelem skrze formulář stránky

    # vytvoření proměnné pro náhodné 8 bitové číslo:
    random_hex = secrets.token_hex(8)
    # random_hex: proměnná pro token
    # secrets: se používá pro generování kryptograficky silných náhodných čísel vhodných pro správu dat, jako jsou hesla, autentizace účtů, bezpečnostní tokeny a související tajemství
    # .token_hex(8): vygenerování hexadecimálního čísla s daným počtem náhodných bajtů

    # vytvoření proměnné pro koncovku za názvem souboru (typ souboru):
    _, f_ext = os.path.splitext(form_picture.filename)
    # _, f_ext: proměnné  s cestou k souboru (podtržítko je pro nepotřebnou proměnou f_name) a zbytkem za tečkou
    # os: je modul pro funkce závislých na operačním systému
    # .path.splitext(): rozdělí cestu k souboru do cesty a obsahem za tečkou
    # (form_picture.filename): název vkládaného obrázku

    # vytvoření nového názvu souboru (z náhodného čísla a koncovky souboru):
    picture_fn = random_hex + f_ext
    # picture_fn: proměnná pro nový název obrázku
    # random_hex: proměnná pro token
    # f_ext: proměnná s koncovkou souboru (obsah za tečkou)

    # vytvoření  pro uložení souboru:
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    # picture_path: proměnná pro cestu k uložení obrázku (spojení cesty, složky a obrázku)
    # os: je modul pro funkce závislých na operačním systému
    # .path.join(): spojí cestu k souboru s jeho názvem
    # current_app.root_path: cesta ke složce programu
    # 'static/profile_pics': název složky, kde je má být uložen
    # picture_fn: proměnná pro nový název obrázku

    # vytvoření proměnné pro rozměr obrázku:
    output_size = (125, 125)
    # output_size: proměnná pro hodnoty velikosti profilového obrázku
    # (125, 125): x=125px, y=125px

    # vytvoření instance třídy Image pro úpravu obrázku:
    image_to_resize = Image.open(form_picture)
    # image_to_resize: instance třídy Image (pro úpravu obrázku)
    # Image: třída pro vytvoření instance pro upravovaný obrázek
    # .open(form_picture): otevření obrázku

    # změna velikosti obrázku:
    image_to_resize.thumbnail(output_size)
    # image_to_resize: instance třídy Image (pro úpravu obrázku)
    # .thumbnail(): metoda upraví obrázek tak, aby obsahoval jeho miniaturní verzi, která není větší než daná velikost
    # output_size: proměnná pro hodnoty maximální velikosti profilového obrázku

    # uložení nového obrázku se změněnou velikostí:
    image_to_resize.save(picture_path)
    # image_to_resize: instance třídy Image (pro úpravu obrázku)
    # .save(): metoda pro uložení obrázku
    # (picture_path): proměnná s cestou pro uložení obrázku

    # vrácení názvu obrázku (s koncovkou typu):
    return picture_fn
    # return: návratová hodnota
    # picture_fn: proměnná pro nový název obrázku



#######################################################################################################################
# USERS-04-4 #
# funkce na odesílání tokenu pro změnu hesla:

def send_reset_email(user):
    # send_reset_email: název vytvářené funkce
    # user: uživatel kterému se bude email s tokenem odesílat

    # vytvoření proměnné pro časový token:
    token = user.get_reset_token()
    # token: proměnná pro časový token
    # user.get_reset_token(): volání metody pro vytvoření časového tokenu

    # vytvoření instance pro odeslání emailové zprávy:
    msg = Message(lazy_gettext("Password Reset Request"), recipients=[user.email])
    # msg: instance pro odeslání emailové zprávy
    # Message: třída pro zapouzdření a odeslání emailu
    # (# gettext("...'): označení textu pro překlad [babel]
    # 'Password Reset Request': název emailu
    # sender='noreply@demo.com': odesílatel (měl by odpovídat platnému mailu)
    # recipients=[user.email]): příjemce (vytaženo z databáze uživatele)

    # vytvoření těla zprávy:
    intro = lazy_gettext("To reset your password, visit the following link:")
    url = url_for('users.reset_token', token=token, _external=True)
    footer = lazy_gettext("If you did not make this request then simply ignore this email and no changes will be made.")
    msg.body = intro+"\n"+url+"\n\n"+footer
    # intro: úvod
    # url: link na resetování vesla
    # {url_for('users.reset_token', token=token, _external=True)} odkaz na stránku validace tokenu
    # footer: patička zprávy
    # gettext("...'): označení textu pro překlad [babel]
    # msg.body: proměnná pro tělo zprávy
    # intro+"\n"+url+"\n\n"+footer: text zprávy
    # (pro delší zprávy je lepší použít jinja2 tamplate)

    # odeslání mailu:
    mail.send(msg)
    # mail: instance třídy Mail pro odesílání mailů
    # .send(): metoda třídy Mail pro odesílání mailů
    # (msg): instance třídy Mesage s vytvořeným emailem


#######################################################################################################################