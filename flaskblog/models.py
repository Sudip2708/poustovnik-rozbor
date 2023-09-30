#######################################################################################################################
# 03 #
# VYTVOŘENÍ TŘÍD PRO TABULKY DATABÁZE #
# tento soubor slouží k pro třídy tabulek databáze  #

# 03-1: import externích rozšíření programu
# 03-2: import vlastních rozšíření programu
# 03-3: vytvoření funkce pro vyhledávání uživatele v databázi dle ID
# 03-4-A: vytvoření třídy pro databázovou tabulku uživatele
# 03-4-B: definice metody pro vytvoření časového tokenu
# 03-4-C: definice metody pro ověření časového tokenu
# 03-4-D: přepsání magické metody repr
# 03-4-A: vytvoření třídy pro databázovou tabulku na příspěvky
# 03-4-B: přepsání magické metody repr


#######################################################################################################################
# 03-1 #
# import externích rozšíření programu:

import jwt
# import modulu na vytváření tokenů pro ověření autenticity (např. reset hesla přes email)
# jwt: je knihovna Pythonu, která vám umožňuje kódovat a dekódovat webové tokeny JSON (JWT)
# před importem je potřeba rozšíření doinstalovat > pip install pyjwt
# https://pyjwt.readthedocs.io/en/stable/

from datetime import datetime, timedelta
# datetime: modul poskytující třídy pro manipulaci s daty a časy.
# datetime: objekt obsahující všechny informace o objektu datea timeobjektu.
# timedelta: objekt pro dobu trvání, rozdíl mezi dvěma daty, nebo časy
# https://docs.python.org/3/library/datetime.html

from flask_login import UserMixin
# flask_login: poskytuje správu uživatelských relací (přihlášení, odhlášení a zapamatování relací vašich uživatelů)
# UserMixin: třída poskytující výchozí implementace pro metody, které Flask-Login očekává, že budou mít uživatelské objekty
# https://flask-bcrypt.readthedocs.io/en/1.0.1/

from flask import current_app
# flask: je webový microframework pro tvorbu webu v programovacím jazyku Python
# current_app: metoda pro navracení aktuální aplikace
# https://flask.palletsprojects.com/en/2.3.x/


#######################################################################################################################
# 03-2 #
# import vlastních rozšíření programu:

from flaskblog import db, login_manager
# flaskblog: inicializační soubor hlavní složky programu (__init__.py v složce flaskblog)
# db: instance třídy SQLAlchemy pro databázi
# login_manager: zástupce pro instanci třídy LoginManager pro administraci přihlášení


#######################################################################################################################
# 03-3 #
# vytvoření funkce pro vyhledávání uživatele v databázi dle ID:

@login_manager.user_loader
# @login_manager: dekorátor (konfigurátor) přihlášení
# .user_loader: funkce umožňuje vyhledat a načíst uživatele dle jeho ID

def load_user(user_id):
    # load_user: název vytvářené funkce
    # user_id: ID uživatele dle kterého se bude vyhledávat

    return User.query.get(int(user_id))
    # return: návratová hodnota
    # User.query: dotaz do databáze
    # .get(): metoda pro získání dat z databáze
    # int():  metoda převádějící vstup ID na číslo
    # (user_id): ID uživatele dle kterého se bude vyhledávat


#######################################################################################################################
# 03-4-A #
# vytvoření třídy pro databázovou tabulku uživatele:
# (instance dědí tabulku z třídy Model a přihlášení z UserMixin)

class User(db.Model, UserMixin):
    # User: název vytvářené třídy
    # db: instance třídy SQLAlchemy pro databázi
    # .Model: základní třída pro všechny databázové modely
    # UserMixin: třída poskytující výchozí implementace pro metody, které Flask-Login očekává, že budou mít uživatelské objekty

    # definování sloupce pro ID příspěvku
    id = db.Column(db.Integer, primary_key=True)
    # id: instance třídy Column pro sloupec databáze
    # db.Column(): třída pro sloupec databáze
    # (db.Integer: omezení typu zadávaných dat pro celá čísla
    # primary_key=True): definice primárního klíče

    # definování sloupce pro uživatelské jméno
    username = db.Column(db.String(20), unique=True, nullable=False)
    # username: instance třídy Column pro uživatelské jméno
    # db.Column(): třída pro sloupec databáze
    # (db.String(20): omezení typu zadávaných dat pro textový řetězec omezený na 20 znaků
    # unique=True:
    # nullable=False): definice nenulové hodnoty = pole musí být vyplněno

    # definování sloupce pro email
    email = db.Column(db.String(120), unique=True, nullable=False)
    # email: instance třídy Column pro email
    # db.Column(): třída pro sloupec databáze
    # (db.String(120): omezení typu zadávaných dat pro textový řetězec omezený na 120 znaků
    # unique=True: nastavení jedinečnosti pole, hodnota nesmí být použita v rámci sloupce více než jednou
    # nullable=False): definice nenulové hodnoty = pole musí být vyplněno

    # definování sloupce pro profilový obrázek
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    # image_file instance třídy Column pro profilový obrázek
    # db.Column(): třída pro sloupec databáze
    # (db.String(20): omezení typu zadávaných dat pro textový řetězec omezený na 20 znaků
    # nullable=False: definice nenulové hodnoty = pole musí být vyplněno
    # default='default.jpg'): definice defaultního obrázku (když uživatel nenahraje svůj)

    # definování sloupce pro heslo
    password = db.Column(db.String(60), nullable=False)
    # password: instance třídy Column pro heslo
    # db.Column(): třída pro sloupec databáze
    # (db.String(60): omezení typu zadávaných dat pro textový řetězec omezený na 60 znaků
    # nullable=False): definice nenulové hodnoty = pole musí být vyplněno

    # definování sloupce pro odkaz na propojení s příspěvkem
    posts = db.relationship('Post', backref='author', lazy=True)
    # posts: odkaz na propojení s příspěvkem
    # db.relationship(): je funkce která poskytuje vztah mezi dvěma mapovanými třídami (to odpovídá vztahu rodič-dítě nebo asociativní tabulka)
    # ('Post': název třídy propojované tabulky
    # backref='author': definice sloupce propojení
    # lazy=True): nastavuje zda se mají načíst podřízené objekty při načítání nadřazeného objektu (lazy=True znamená nezatěžovat dítě)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# 03-4-B #
# definice metody pro vytvoření časového tokenu:

    def get_reset_token(self, expires_sec=1800):
        # get_reset_token: název vytvářené metody
        # self: instance třídy User
        # expires_sec=1800: čas vypršení (zde defaultně 30 min.)

        # definice parametrů tokenu
        payload = {'exp': datetime.utcnow() + timedelta(days=0, seconds=expires_sec), 'sub': self.id}
        # payload: proměnná pro specifikaci nároků tokenu
        # {'exp': doba vypršení platnosti
        # datetime.utcnow(): metoda pro získání aktuálního času
        # + timedelta(days=0, seconds=expires_sec): metoda pro přidání času
        # 'sub': self.id}: ID uživatele

        # vytvoření a předání tokenu
        return jwt.encode(payload, current_app.config.get('SECRET_KEY'), algorithm='HS256')
        # return: návratová hodnota
        # jwt.encode(): metoda pro vytvoření tokenu
        # (payload: proměnná pro specifikaci nároků tokenu
        # current_app.config.get('SECRET_KEY'): tajný klíč pro šifrování (nastaveno v __init__.py)
        # algorithm='HS256'): algoritmus šifrování (pozor! při vytváření se píše je "algorithm" a ne "algorithms" jako u čtení)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# 03-4-C #
# definice metody pro ověření časového tokenu
    @staticmethod
    # @staticmethod: dekorátor pro definici statické metody (nepracuje s instancí a nepoužívá self)

    def verify_reset_token(token):
        # verify_reset_token: název vytvářené metody
        # token: získaný token pro ověření

        try:
            # vyzkoušej: (načtení ID uživatele z tokenu)
            user_id = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms='HS256')['sub']
            # user_id: npro ID z tokenu uživatele
            # jwt.decode(): metoda pro čtení tokenu
            # (token: získaný token pro ověření
            # current_app.config.get('SECRET_KEY'): tajný klíč pro šifrování (nastaveno v __init__.py)
            # algorithms='HS256'): algoritmus šifrování (pozor! při čtení se píše je "algorithms" a ne "algorithm" jako u vytváření)
            # ['sub']: odkaz na klíč (v již dekódovaném tokenu), za kterým by mělo následovat ID uživatele

        except:
            # pokud se token nepodaří načíst
            return None
            # return: návratová hodnota
            # None: nic

        # návratová hodnota pro případ úspěšné identifikace
        return User.query.get(user_id)
        # return: návratová hodnota
        # User.query: databázový dotaz do tabulky uživatelů
        # .get(): příkaz pro vytažení hodnot
        # (user_id): definice klíče pro vytažení hodnot (zde ID uživatele)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# 03-4-D #
# přepsání magické metody repr (textové reprezentace instance)
    def __repr__(self):
        # __repr__: magická metoda pro textovou representaci instance
        # self: instance třídy
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
        # return:  návratová hodnota
        # f": řetězec reprezentující vytvořenou instanci
        # User(): název třídy pro vytvoření instance
        # ('{self.username}': přihlašovací jméno uživatele
        # '{self.email}': email uživatele
        # '{self.image_file}')": profilový obrázek uživatele


#######################################################################################################################
# 03-5-A #
# vytvoření třídy pro databázovou tabulku na příspěvky:

class Post(db.Model):
    # Post: název vytvářené třídy
    # db: instance třídy SQLAlchemy pro databázi
    # .Model: základní třída pro všechny databázové modely

    # definování sloupce pro ID příspěvku
    id = db.Column(db.Integer, primary_key=True)
    # id: instance třídy Column pro sloupec databáze
    # db.Column(): třída pro sloupec databáze
    # (db.Integer: omezení typu zadávaných dat pro celá čísla
    # primary_key=True): definice primárního klíče

    # definování sloupce pro název příspěvku
    title = db.Column(db.String(100), nullable=False)
    # title: instance třídy Column pro sloupec databáze
    # db.Column(): třída pro sloupec databáze
    # (db.String(100): omezení typu zadávaných dat pro textový řetězec omezený na 100 znaků
    # nullable=False): definice nenulové hodnoty = pole musí být vyplněno

    # definování sloupce pro datum příspěvku
    # přidání datumu příspěvku (datetime.utcnow je bez závorek, protože to předáváme jako proměnou a ne funkci)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # date_posted: instance třídy Column pro sloupec databáze
    # db.Column(): třída pro sloupec databáze
    # (db.DateTime: omezení typu zadávaných dat pro datum a čas
    # nullable=False: definice nenulové hodnoty = pole musí být vyplněno
    # default=: definice přednastavené hodnoty
    # datetime.utcnow): vrací aktuální datum a čas

    # definování sloupce pro obsah příspěvku
    content = db.Column(db.Text, nullable=False)
    # content: instance třídy Column pro sloupec databáze
    # db.Column(): třída pro sloupec databáze
    # (db.Text: omezení typu zadávaných dat pro text
    # nullable=False): definice nenulové hodnoty = pole musí být vyplněno

    # definování sloupce pro ID autora příspěvku (vytvoření cizího klíče)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # user_id: instance třídy Column pro sloupec databáze
    # db.Column(): třída pro sloupec databáze
    # (db.Integer:  omezení typu zadávaných dat pro celá čísla
    # db.ForeignKey('user.id'): nástroj na přidání existujícího klíče jiné databáze (zde pro autora)
    # nullable=False): definice nenulové hodnoty = pole musí být vyplněno

    lang = db.Column(db.Text, nullable=False)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# 03-4-D #
# přepsání magické metody repr (textové reprezentace instance)

    def __repr__(self):
        # __repr__: magická metoda pro textovou representaci instance
        # self: instance třídy
        return f"Post('{self.title}', '{self.date_posted}')"
        # return:  návratová hodnota
        # f": řetězec representující vytvořenou instanci
        # Post(): název třídy pro vytvoření instance
        # ('{self.title}': název příspěvku
        # '{self.date_posted}')": obsah příspěvku


#######################################################################################################################

