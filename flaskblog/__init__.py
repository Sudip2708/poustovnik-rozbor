#######################################################################################################################
# 01 #
# INICIALIZAČNÍ SOUBOR PROGRAMU #
# tento soubor slouží k základní konfiguraci a vytvoření aplikace #

# 01-1: import externích rozšíření programu
# 01-2: import vlastních rozšíření programu
# 01-3: inicializace importovaných modulů
# 01-4: funkce pro vytvoření aplikace


#######################################################################################################################
# 01-1 #
# import externích rozšíření programu:

from flask import Flask
# flask: je webový microframework pro tvorbu webu v programovacím jazyku Python
# Flask: třida pro vytvoření instance webové aplikace
# před importem je potřeba rozšíření doinstalovat > pip install flask
# https://flask.palletsprojects.com/en/2.3.x/

from flask_sqlalchemy import SQLAlchemy
# flask_sqlalchemy: je rozšíření pro Flask, které přidává podporu pro SQLAlchemy
# SQLAlchemy: třída pro vytvoření instance pro databázi
# před importem je potřeba rozšíření doinstalovat > pip install flask-sqlalchemy
# https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/

from flask_bcrypt import Bcrypt
# flask_bcrypt: je rozšíření Flask, které poskytuje nástroje pro hašování bcrypt
# Bcrypt: třída pro vytvoření instance pro šifrování
# před importem je potřeba rozšíření doinstalovat > pip install flask-bcrypt
# https://flask-bcrypt.readthedocs.io/en/1.0.1/

from flask_login import LoginManager
# flask_login: poskytuje správu uživatelských relací (přihlášení, odhlášení a zapamatování relací vašich uživatelů)
# LoginManager: třída pro vytvoření instance pro správu uživatelského rozhraní
# před importem je potřeba rozšíření doinstalovat > pip install flask-login
# https://flask-login.readthedocs.io/en/latest/

from flask_mail import Mail
# flask_mail: poskytuje jednoduché rozhraní pro nastavení SMTP a pro odesílání zpráv z vašich pohledů a skriptů
# Mail: třída pro vytvoření instance umožňující posílání emailů uživatelům
# před importem je potřeba rozšíření doinstalovat > pip install flask-mail
# https://pythonhosted.org/Flask-Mail/

from flask_babel import Babel
# flask.ext.babel: poskytuje rozhraní pro lokalizaci stránky
# Babel: třída pro vytvoření instance umožňující lokalizaci stránky
# gettext: metoda pro označení textu určeného pro překlad
# před importem je potřeba rozšíření doinstalovat > pip install Flask-Babel
# https://pythonhosted.org/Flask-Mail/


#######################################################################################################################
# 01-2 #
# import vlastních rozšíření programu:

from flaskblog.config import Config
# flaskblog.config: soubor config.py v kořenovém adresáři aplikace (flaskblok)
# Config: třída obsahující nastavení databáze, tajného klíče a posílání mailů

import flaskblog.locale as fl
# flaskblog.locale: soubor locale.py v kořenovém adresáři aplikace (flaskblok) sloužící pro změny jazyka stránky
# fl: skratka pro použití odkazu v programu


#######################################################################################################################
# 01-3 #
# inicializace importovaných modulů:

# vytvoření instance SQLAlchemy (používá se pro tvorbu databází):
db = SQLAlchemy()
# db: instance třídy SQLAlchemy pro databázi
# SQLAlchemy(): třída pro vytvoření instance

# vytvoření instance Bcrypt (používá se pro šifrování):
bcrypt = Bcrypt()
# bcrypt: instance třídy Bcrypt pro šifrování
# Bcrypt(): třída pro vytvoření instance

# vytvoření instance LoginManager (používá se pro administraci přihlášení)
login_manager = LoginManager()
# login_manager: zástupce pro instanci třídy LoginManager pro administraci přihlášení
# LoginManager(): třída pro vytvoření instance

# nastavení stránky pro přístup k přihlášení
login_manager.login_view = 'user.login'
#login_manager.login_view: nastavení přístupu k přihlášení
#'user.login': název pohledu, na který se má uživatel přesměrovat, když se potřebuje přihlásit

# nastavení pro oznam přihlášení
login_manager.login_message_category = 'info'
# login_manager.login_message_category: nastavení oznamu při přesměrování na přihlašovací stránku
# 'info': kategorie zprávy, která má blikat, když je uživatel přesměrován na přihlašovací stránku

# vytvoření instance Mail (pro odesílání mailů):
mail = Mail()
# mail: instance třídy Mail pro odesílání mailů
# Mail(): třída pro vytvoření instance


#######################################################################################################################
# 01-4 #
# vytvoření aplikace:

def create_app(config_class=Config):
    # create_app: název vytvářené funkce
    # config_class=Config: odkaz na konfigurační třídu obsahující nastavení databáze, tajného klíče a posílání mailů

    # vytvoření instance Flasku (používá se pro tvorbu webových aplikací):
    app = Flask(__name__)
    # app: instance Flasku pro vytvářenou webovou aplikaci
    # Flask(): třída pro vytvoření instance
    # __name__: je vestavěná speciální proměnná, která vyhodnocuje název aktuálního modulu. Pokud je zdrojový soubor spuštěn jako hlavní program, interpret nastaví proměnnou __name__ na hodnotu „__main__“. Pokud je tento soubor importován z jiného modulu, __name__ bude nastaveno na název modulu.

    # natažení konfigurace ze souboru config.py:
    app.config.from_object(Config)
    # app.config: metoda umožňující konfigurovat aplikaci pomocí přednastavených metod
    # .from_object(): odkaz na objekt z kterého se má konfigurace aplikace načíst
    # (Config): třída obsahující nastavení databáze, tajného klíče a posílání mailů

    # přiřazení instancí doinstalovaných modulů (samotné instance jsou definovány - dle instrukcí v návodu k flask - vně této funkce
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    # db: instance třídy SQLAlchemy pro databázi
    # bcrypt: instance třídy Bcrypt pro šifrování
    # login_manager: instanci třídy LoginManager pro administraci přihlášení
    # mail: instance třídy Mail pro odesílání mailů
    # .init_app(): příkaz pro inicializaci aplikace
    # (app): instance Flasku pro vytvářenou webovou aplikaci

    # import blueprintů na stránky aplikace
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    # flaskblog.users.routes: cesta k souboru (kořenový adresář, složka, soubor)
    # users: název blueprintu

    # registrace blueprintů (propojení na stránky aplikace):
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    # app.register_blueprint(): příkaz pro načtení cesty k datům
    # users: stránky spojené s databází uživatele
    # posts: stránky spojené s databází příspěvků
    # main: ostatní stránky
    # main: ostatní stránky

    # vytvoření instance babel pro překlad (lokalizaci) stránky
    babel = Babel(app, locale_selector=fl.get_locale)

    # předání vytvořené aplikace
    return app
    # return: návratová hodnota
    # app: instance Flasku pro vytvořenou webovou aplikaci


###########################################################################