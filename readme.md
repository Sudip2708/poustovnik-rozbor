# Zdravím!
Toto je podrobný rozbor kódu stránek vytvořených ve Flasku podle YouTube videí od Corey Schafer: 
https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH

Tento rozbor mi sloužil pro pochopení a základní orientaci v kódu.
Vzhledem k tomu, že při vytváření jsem si hodně pomáhla hromadným přepisem, a že tato verze kódu byla zpracovávána ve chvíli, kdy jsem se s ním seznamoval a snažil pochopit, obsahuje i řadu drobných nepřesností a pravděpodobně i gramatických chyb.
Nicméně mně osobně velmi pomohlo kód si takto rozepsat. Nejen, že jsem se v kódu lépe vyznal, ale i lépe mu porozuměl a pochopil.
Konečná verze kódu, která je již psaná s ohledy na Best Practise a v angličtině, má řadu drobných (ale občas i důležitých) změn, které jsem už sem zpětně nedoplnil. A tak účel zveřejnění této verze je čistě jen pro ten případ, že by se někomu hodilo vidět, takto rozepsaný kód :-)

Konečnou verzi kódu pak můžete najít zde: https://github.com/Sudip2708/poustovnik-english.git

A stránku pak zde: https://poustovnik.fun/

### Seznam komponent:
```
/poustovnik
(hlavní složka programu)
run.py - Spouštěcí soubor programu.
readme.mp - Tento soubor, který zrovna čtete.

/poustovnik/instance
(složka pro databázy)
site.db - Databáze aplikace.

/poustovnik/flaskblog
(složka pro program)
__init__.py - Inicializační soubor programu.
config.py - Konfigurační soubor programu.
models.py - Modul s třídami pro tvorbu databázových tabulek (sqlalchemy).
locale.py - Soubor napomáhající lokalizaci stránky (v konečné verzy plně přepracováno).
babel.cfg - Konfigurační soubor Babelu pro inicializaci překladu stránek (může být smazán).
messages.pot - Výtah všech označených textů pro Babel překlad (může být smazán).

/poustovnik/flaskblog/main
(složka s blueprinty pro zobrazení hlavní a nezařazené stránky)
__init__.py - Inicializační soubor pro blueprint složku (nemusí obsahovat žádná data).
about_text.py - Soubor s textem a linky pro stránku about.
routes.py - Soubor pro vytváření stránek.

/poustovnik/flaskblog/user
(složka s blueprinty pro stránky uživatele)
__init__.py - Inicializační soubor pro blueprint složku (nemusí obsahovat žádná data).
routes.py - Soubor pro vytváření stránek.
forms.py - Soubor pro formuláře stránek.
utils.py - Soubor pro funkce.

/poustovnik/flaskblog/posts
(složka s blueprinty pro stránky na příspěvky)
__init__.py - Inicializační soubor pro blueprint složku (nemusí obsahovat žádná data).
routes.py - Soubor pro vytváření stránek.
forms.py - Soubor pro formuláře stránek.

/poustovnik/flaskblog/errors
(složka s blueprinty pro chybové stránky)
__init__.py - Inicializační soubor pro blueprint složku (nemusí obsahovat žádná data).
handlers.py - Soubor pro vytváření stránek.

/poustovnik/flaskblog/static
(složka pro statiku - obrázky, css)
main.css - CSS soubor pro dodatečnou konfiguraci vzhledu stránek (hlavní obstarává boodstrap).
favicon.ico - Obrázek pro zobrazení v záložce webu.
profile_pic - Složka na profilové obrázky uživatelů.

/poustovnik/flaskblog/templates
(složka na html podklady pro stránky)
about.html - Stránka s povídáním o této aplikaci.
account.html - Stránka pro správu uživatelského účtu.
create_post.html - Stránka pro vytvoření příspěvku.
home.html - Stránka pro výpis příspěvků (domácí stránka).
layout.html - Předloha pro všechny ostatní stránky.
login.html - Stránka pro přihlášení.
post.html - Stránka pro vytvoření příspěvku.
register.html - Stránka pro registraci uživatele.
reset_request.html - Stránka pro vygenerování a zaslání tokenu pro změnu hesla.
reset_token.html - Stránka pro změnu hesla (po obdržení tokenu).
side_panel.html - Stránka pro boční panel (rozšíření layoutu pro lepší přehladnost).
side_panel_old.html - Stránka pro původní boční panel (rozšíření bočního panelu z důvodu aby se předešlo opakování kódu).
user_posts.html - Stránka pro zobrazení příspěvků od konkrétního uživatele.

/poustovnik/flaskblog/templates/errors
(složka na stránky oznamující chybu)
403.html - Stránka pro chybu 403 (odmítnutí přístupu).
404.html - Stránka pro chybu 404 (chybný odkaz/nenalezení stránky).
500.html - Stránka pro chybu 500 (chyba serveru).

/poustovnik/flaskblog/translations/cs/LC_MESSAGES
(složka pro lokalizační překlad stránek)
messages.po - Soubor pro překlad jednotlivých textů.
messages.mo - Vygenerovaný binární soubor pro překlad stránky.
```

### Seznam pip pro virtuální prostředí
```
Instalace flasku (pro tvorbu stránek):
$ pip install flask

Instalace sqlalchemy (pro práci s databází):
$ pip install flask-sqlalchemy

Instalace bcrypt (pro šifrování):
$ pip install flask-bcrypt

Instalace login (pro správu přihlášení):
$ pip install flask-login

Instalace mail (pro nastavení a použití mailu):
$ pip install flask-mail

Instalace Babel (pro lokalizaci stránky):
$ pip install Flask-Babel

Instalace pyjwt (pro webové tokeny JWT):
$ pip install pyjwt

Instalace wtf (pro formuláře webu):
$ pip install flask_wtf

Instalace email_validator (ověření emailu):
$ pip install email_validator

Instalace Pillow (pro zpracování obrázků):
$ pip install Pillow

Instalace googletrans (pro překlad příspěvků):
$ pip install googletrans==3.1.0a0
```