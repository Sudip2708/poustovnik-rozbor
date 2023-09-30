#######################################################################################################################
# USERS-02 #
# SOUBOR PRO VYTVÁŘENÍ STRÁNEK - PODSEKCE USERS #
# tento soubor slouží pro definici a vytváření stránek programu  #

# USERS-02-1: import externích rozšíření programu
# USERS-02-2: import vlastních rozšíření programu
# USERS-02-3: vytvoření instance pro provázání tohoto souboru se souborem __init__.py v kořenové složce programu
# USERS-02-4-A: definice stránky pro registraci
# USERS-02-4-B: definice stránky pro přihlášení
# USERS-02-4-C: definice stránky pro odhlášení
# USERS-02-4-D: definice stránky pro správu uživatelského účtu
# USERS-02-4-E: definice stránky pro zobrazení všech příspěvků od jednoho uživatele
# USERS-02-4-F: definice stránky pro odeslání tokenu pro změnu hesla
# USERS-02-4-G: definice stránky pro změnu hesla za použití tokenu


#######################################################################################################################
# USERS-02-1 #
# import externích rozšíření programu:

from flask import render_template, url_for, flash, redirect, request, Blueprint
# flask: je webový microframework pro tvorbu webu v programovacím jazyku Python
# render_template: metoda na vykreslování html šablony
# url_for: metoda pro vygenerování url adresy k souborům projektu
# flash: metoda pro zobrazení informativní zprávy
# redirect: metoda k přesměrování na jiný koncový bod
# request: metoda pro obsluhu dat odeslaných z klienta na server
# Blueprint: třída pro zpřehlednění a uspořádání aplikace
# https://flask.palletsprojects.com/en/2.3.x/quickstart/

from flask_login import login_user, current_user, logout_user, login_required
# flask_login: poskytuje správu uživatelských relací pro Flask
# login_user: metoda pro přihlášení uživatele
# current_user: proxy pro aktuálního uživatele
# logout_user: metoda pro odhlášení uživatele
# login_required: metoda pro ověření přihlášení uživatele (vhodné pro následné rozšíření možností)

from flask_babel import lazy_gettext
# flask_babel: rozšíření pro lokalizaci stránek
# lazy_gettext: metoda pro označení textu, který bude překládán až ve chvíli volání


#######################################################################################################################
# USERS-02-2 #
# import vlastních rozšíření programu:

# import souboru sloužící pro změny jazyka stránky
import flaskblog.locale as fl
# flaskblog.locale: soubor locale.py v kořenovém adresáři aplikace (flaskblok) sloužící pro změny jazyka stránky
# fl: skratka pro použití odkazu v programu

# import sqlalchemy a šifrování a jazyka stránky:
from flaskblog import db, bcrypt
# flaskblog: cesta k souboru (__init__.py v kořenovém adresáři programu)
# db: instance třídy SQLAlchemy pro databáze
# bcrypt: instance třídy Bcrypt pro šifrování
# current_lang: odkaz na proměnnou s aktuálním jazykem stránky

# import databáze pro uživatele a příspěvky:
from flaskblog.models import User, Post
# flaskblog.models: cesta k souboru (flaskblog=kořenový adresář, models=název souboru)
# User: název databázové třídy pro tabulku na uživatele
# Post: název databázové třídy pro tabulku na příspěvky

# import pro formuláře stránek uživatele:
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
# flaskblog.users.forms:  cesta k souboru (flaskblog=kořenový adresář, users=název složky, forms=název souboru)
# RegistrationForm: formulář na data pro stránku registrace nového uživatele
# LoginForm: formulář na data pro přihlašovací stránku
# UpdateAccountForm: formulář na data pro stránku pro správu uživatelského účtu
# RequestResetForm: formulář na data pro stránku pro žádost o zaslání tokenu pro změnu hesla
# ResetPasswordForm: formulář na data pro stránku na změnu hesla

# import funkcí pro práci s daty uživatele:
from flaskblog.users.utils import save_picture, send_reset_email
# flaskblog.users.utils:  cesta k souboru (flaskblog=kořenový adresář, users=název složky, utils=název souboru)
# save_picture: funkce na ukládání profilových obrázků
# send_reset_email: funkce na odeslání tokenu mailem pro změnu hesla


#######################################################################################################################
# USERS-02-3 #
# vytvoření instance pro provázání tohoto souboru se souborem __init__.py v kořenové složce programu:

users = Blueprint('users', __name__)
# posts: název vytvářené instance
# Blueprint: třída pro zpřehlednění a uspořádání aplikace
# ('users': název složky balíčku
# __name__: je vestavěná speciální proměnná, která vyhodnocuje název aktuálního modulu. Pokud je zdrojový soubor spuštěn jako hlavní program, interpret nastaví proměnnou __name__ na hodnotu „__main__“. Pokud je tento soubor importován z jiného modulu, __name__ bude nastaveno na název modulu.


#######################################################################################################################
# USERS-02-4-A #
# definice stránky pro registraci:

@users.route("/register", methods=['GET', 'POST'])
# @users.route(): je dekorátor pro cestu k stránkám aplikace
# "/nazevstranky": relativní cesta ke stránce
# methods=['GET', 'POST']: definice metod k načítání, nebo odesílání dat na server


def register():
    # register: název vytvářené stránky

    # podmínka ověřující, zda je uživatel již autentizován, pokud ano, přesměruje nás na hlavní stránku:
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # current_user.is_authenticated: je-li aktuální uživatel (current_user) přihlášen (is_authenticated)
    # return: návratová hodnota
    # redirect(url_for('main.home')): přesměrování (redirect) na domovskou stránku (url_for('main.home'))

    # vytvoření instance pro registrační formulář:
    form = RegistrationForm()
    # form: instance třídy registračního formuláře
    # RegistrationForm(): třída registračního formuláře

    # podmínka ověřující, zda byly vloženy o validní údaje:
    if form.validate_on_submit():
        # form: instance třídy registračního formuláře
        # validate_on_submit(): metoda pro kontrolu, zda byly vložené údaje odpovídají nastavení formuláře

        # vytvoření proměnné pro generované heslo:
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # hashed_password: proměnná pro vygenerované heslo
        # bcrypt: instance třídy Bcrypt pro šifrování
        # generate_password_hash(): metoda na generování hesla
        # (form.password.data) načtení hesla z instance
        # .decode('utf-8'): dekódování do utf-8 (v Pythonu 3 < musí být toto uvedeno)

        # vytvoření instance třídy User s daty uživatele a vložení do databáze:
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # user: instance třídy User s daty uživatele a vložení do databáze
        # User: třída pro databázi uživatelů
        # username=form.username.data: přiřazení uživatelského jména z patřičného pole formuláře
        # email=form.email.data: přiřazení uživatelského emailu z patřičného pole formuláře
        # password=hashed_password: přiřazení uživatelského hesla z patřičného pole formuláře

        # vložení dat do databáze:
        db.session.add(user)
        db.session.commit()
        # db: instance třídy SQLAlchemy pro databázi
        # .session.add(user): vlož do databáze údaje o uživateli
        # .session.commit(): ulož změny v databázi

        # zobrazení informativní zprávy o úspěšném vytvoření účtu:
        flash(lazy_gettext("Your account has been created! You are now able to log in"), 'success')
        # flash: metoda pro zobrazení informativní zprávy
        # gettext("...'): označení textu pro překlad [babel]
        # 'success': specifikace typu oznamu

        # přesměrování na stránku pro přihlášení:
        return redirect(url_for('users.login'))
        # return: návratová hodnota
        # redirect(url_for('users.login')): přesměrování (redirect) na stránku pro přihlášení (url_for('users.login'))

    # pokud vložená data jsou nekorektní, znovunačtení stránky s oznamem chyb:
    return render_template('register.html', title='Register', form=form, lflag=fl.current_lang)
    # return: návratová hodnota
    # render_template: metoda na vykreslování html šablony
    # ('register.html': název html souboru
    # title='Register': nadpis
    # form=form: instance pro třídu zobrazovaného formuláře
    # lflag=current_lang): odkaz na zkratku jazyka stránky (cs/en)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# USERS -02-4-B #
# definice stránky pro přihlášení

@users.route("/login", methods=['GET', 'POST'])
# @users.route(): je dekorátor pro cestu k stránkám aplikace
# "/nazevstranky": relativní cesta ke stránce
# methods=['GET', 'POST']: definice metod k načítání, nebo odesílání dat na server

def login():
    # login: název vytvářené stránky

    # podmínka ověřující, zda je uživatel již autentizován, pokud ano, přesměruje nás na hlavní stránku:
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # current_user.is_authenticated: je-li aktuální uživatel (current_user) přihlášen (is_authenticated)
    # return: návratová hodnota
    # redirect(url_for('main.home')): přesměrování (redirect) na domovskou stránku (url_for('main.home'))

    # vytvoření instance pro přihlašovací formulář:
    form = LoginForm()
    # form: instance třídy přihlašovacího formuláře
    # LoginForm(): třída přihlašovacího formuláře

    # podmínka ověřující, zda byly vloženy o validní údaje:
    if form.validate_on_submit():
        # form: instance třídy registračního formuláře
        # validate_on_submit(): metoda pro kontrolu, zda byly vložené údaje odpovídají nastavení formuláře

        # vytvoření databázového dotazu pro ověření zda se v databázi vyskytuje zadaný email:
        user = User.query.filter_by(email=form.email.data).first()
        # user: proměnná pro výsledek databázového dotazu
        # User.query: dotaz načítající (dle parametrů) data z databáze
        # filter_by(): definice filtru hledání
        # (email=form.email.data): v tabulce databáze v sloupci email hledej data z pole formuláře pro email
        # .first(): vrať první výsledek

        # podmínka ověřující přihlašovací email a heslo:
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # user: proměnná pro dotaz, ověřující zda se v databázi vyskytuje zadaný email
            # bcrypt: instance třídy Bcrypt pro šifrování
            # .check_password_hash(): metoda vrátí hodnotu True, pokud se heslo shoduje s heslem hash
            # (user.password, form.password.data): heslo z instance uživatele, heslo z formuláře stránky

            # přihlášení uživatele:
            login_user(user, remember=form.remember.data)
            # login_user(): metoda pro přihlášení uživatele
            # user: uživatel
            # remember=form.remember.data: implemetace funkce na zapamatování přihlášení uživatele (bere hodnotu ze zaškrtávacího pole formuláře)

            # vytvoření proměnné pro případnou další stránku kam po loginu přesměrovat:
            next_page = request.args.get('next')
            # next_page: proměnná pro případnou další stránku kam po loginu přesměrovat
            # request.args.get('next'): zpřístupňuje další stránku (je-li definovaná)

            # přesměrování na další stránku (je-li) nebo na domovskou stránku:
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
            # return: návratová hodnota
            # podmínka: pokud next_page je uvedena (if next_page)
            # redirect(next_page): přesměrování na další stránku (next_page)
            # podmínka: ve všech ostatních případech
            # redirect(): přesměrování
            # url_for('main.home'): na domovskou stránku

        # podmínka pro případ, když přihlašovací jméno, nebo heslo nejsou validní:
        else:

            # zobrazení informativní zprávy o neúspěšném přihlášení:
            flash(lazy_gettext("Login Unsuccessful. Please check email and password"), 'danger')
            # flash: metoda pro zobrazení informativní zprávy
            # gettext("...'): označení textu pro překlad [babel]
            # 'danger': specifikace typu oznamu

    # pokud vložená data jsou nekorektní, znovunačtení stránky s oznamem chyb:
    return render_template('login.html', title='Login', form=form, lflag=fl.current_lang)
    # return: návratová hodnota
    # render_template: metoda na vykreslování html šablony
    # ('login.html': název html souboru
    # title='Login': nadpis
    # form=form: instance pro třídu zobrazovaného formuláře
    # lflag=current_lang): odkaz na zkratku jazyka stránky (cs/en)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# USERS -02-4-C #
# definice stránky pro odhlášení:

@users.route("/logout")
# @users.route(): je dekorátor pro cestu k stránkám aplikace
# "/nazevstranky": relativní cesta ke stránce

def logout():
    # logout: název vytvářené stránky

    # odhlášení uživatele pomocí funkce z modulu flask_login:
    logout_user()
    # logout_user(): metoda modulu flask_login pro odhlášení uživatele

    # přesměrování na domovskou stránku:
    return redirect(url_for('main.home'))
    # return: návratová hodnota
    # redirect(): přesměrování
    # url_for('main.home'): na domovskou stránku


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# USERS -02-4-D #
# definice stránky pro správu uživatelského účtu:

@users.route("/account", methods=['GET', 'POST'])
# @users.route(): je dekorátor pro směrování k stránkám aplikace
# "/nazevstranky": relativní cesta ke stránce
# methods=['GET', 'POST']: definice metod k načítání, nebo odesílání dat na server

@login_required
# @login_required: dekorátor vyžadující přihlášení uživatele k zobrazení pohledu

def account():
    # account: název vytvářené stránky

    # vytvoření instance pro formulář pro aktualizaci údajů o uživateli:
    form = UpdateAccountForm()
    # form: instance třídy pro formulář pro aktualizaci údajů o uživateli
    # UpdateAccountForm(): třída formuláře pro aktualizaci údajů o uživateli

    # podmínka ověřující, zda byly vloženy o validní údaje:
    if form.validate_on_submit():
        # form: instance třídy pro formulář pro aktualizaci údajů o uživateli
        # validate_on_submit(): metoda pro kontrolu, zda byly vložené údaje odpovídají nastavení formuláře

        # podmínka ověřující, zda má uživatel nahrán vlastní obrázek:
        if form.picture.data:
            # form: instance třídy pro formulář pro aktualizaci údajů o uživateli
            # picture.data: data nahraného obrázku

            # proměnná pro nahraný obrázek:
            picture_file = save_picture(form.picture.data)
            # picture_file: proměnná pro nahraný obrázek
            # save_picture(): volání námi definované funkce na uložení obrázku
            # (form.picture.data): obrázek nahraný uživatelem

            # přidání obrázku k uživatelskému účtu:
            current_user.image_file = picture_file
            # current_user: aktuálně přihlášený uživatel
            # .image_file: prostor pro uložení obrázku
            # picture_file: proměnná pro nahraný obrázek

        # uložení uživatelského jména:
        current_user.username = form.username.data
        # current_user: aktuálně přihlášený uživatel
        # .username: prostor pro uložení jména uživatele
        # form.username.data: jméno uživatele z formuláře webové stránky

        # uložení uživatelského emailu:
        current_user.email = form.email.data
        # current_user: aktuálně přihlášený uživatel
        # .email: prostor pro uložení emailu uživatele
        # form.email.data: email uživatele z formuláře webové stránky

        # vložení dat do databáze:
        db.session.commit()
        # db: instance třídy SQLAlchemy pro databázi
        # .session.commit(): ulož změny v databázi

        # zobrazení informativní zprávy o provedeném úkonu:
        flash(lazy_gettext("Your account has been updated!"), 'success')
        # flash: metoda pro zobrazení informativní zprávy
        # gettext("...'): označení textu pro překlad [babel]
        # 'success': specifikace typu oznamu

        # navrácení na stejnou stránku (abychom se vyhnuli hlášce o opuštění stránky):
        return redirect(url_for('users.account'))
        # flash: metoda pro zobrazení informativní zprávy

    # podmínka, pro načítání stránky:
    elif request.method == 'GET':
        # request.method == 'GET': volání metody pro načtení stránky

        # předvyplnění údajů ve formuláři na stránce:
        form.username.data = current_user.username
        # form.username.data: pole formuláře stránky pro jméno
        # current_user.username: jméno uložené v instanci přihlášeného uživatele
        form.email.data = current_user.email
        # form.email.data: pole formuláře stránky pro email
        # current_user.email: email uložený v instanci přihlášeného uživatele

    # vytvoření proměnné pro cestu k obrázku uživatele:
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    # image_file: proměnná pro cestu k obrázku uživatele
    # url_for: metoda pro vygenerování url adresy k souborům projektu
    # ('static': složka kde je obrázek
    # filename='profile_pics/' + current_user.image_file): cesta k obrázku


    # navrácení na stránku:
    return render_template('account.html', title='Account', image_file=image_file, form=form, lflag=fl.current_lang)
    # return: návratová hodnota
    # render_template: metoda na vykreslování html šablony
    # ('account.html': název html souboru
    # title='Account': nadpis
    # image_file=image_file: cesta k obrázku
    # form=form: instance pro třídu zobrazovaného formuláře
    # lflag=current_lang): odkaz na zkratku jazyka stránky (cs/en)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# USERS -02-4-E #
# definice stránky pro zobrazení všech příspěvků od jednoho uživatele:

@users.route("/user/<string:username>")
# @users.route(): je dekorátor pro cestu k stránkám aplikace
# "/user/<string:username>": relativní cesta ke stránce dle jména uživatele

def user_posts(username):
    # user_posts: název vytvářené stránky
    # username: jméno uživatele

    # vytvoření proměnné s číslem stránky k zobrazení:
    page = request.args.get('page', 1, type=int)
    # page: proměnná pro číslo požadované stránky
    # request.args.get(): žádost pro přístup k parametrům URL (tyto parametry jsou připojeny na konec adresy URL ve tvaru klíč=hodnota)
    # ('page', 1, type=int): 1.par==stránka, 2.par==defaultní hodnota, 3.par==deklarace typu

    # vytvoření databázového dotazu, zda zadaný uživatel existuje v databázi:
    user = User.query.filter_by(username=username).first_or_404()
    # user: proměnná pro výsledek databázového dotazu
    # User.query: dotaz načítající (dle parametrů) data z databáze
    # filter_by(): definice filtru hledání
    # (username=username): v tabulce databáze v sloupci username hledej shodu s username přispěvatele
    # first_or_404(): vrať první výsledek, nebo vyvolej chybu 404 (nenalezení záznamu)

    # vytvoření proměnné s dotazem do databáze:
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # posts: proměnná pro data z databáze
    # Post.query: dotaz načítající (dle parametrů) data z databáze
    # filter_by(): definice filtru hledání
    # (author=user): v tabulce databáze v sloupci author hledej shodu s user (autor příspěvku)
    # order_by(): požadavek na seřazení výsledků
    # (Post.date_posted.desc()): řadit podle data a sestupně (desc)
    # paginate(): metoda stránkování počítá celkový počet záznamů z databáze
    # (page=page, per_page=5): 1.par==číslo stránky, 2.par==specifikace kolik výpisů z databáze se má zobrazit na jedné stránce

    # navrácení vygenerované stránky:
    return render_template('user_posts.html', posts=posts, user=user, lflag=fl.current_lang)
    # return: návratová hodnota
    # render_template(): metoda na vykreslování html šablony
    # ('user_posts.html': název html souboru
    # posts=posts: výsledek databázového dotazu
    # user=user: autor příspěvků
    # lflag=current_lang): odkaz na zkratku jazyka stránky (cs/en)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# USERS -02-4-F #
# definice stránky pro odeslání tokenu pro změnu hesla:

@users.route("/reset_password", methods=['GET', 'POST'])
# @app.route(): je dekorátor pro směrování k stránkám aplikace
# "/nazevstranky": relativní cesta ke stránce
# methods=['GET', 'POST']: definice metod k načítání, nebo odesílání dat na server

def reset_request():
    # reset_request: název vytvářené stránky

    # podmínka ověřující, zda je uživatel již autentizován, pokud ano, přesměruje nás na hlavní stránku:
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # current_user.is_authenticated: je-li aktuální uživatel (current_user) přihlášen (is_authenticated)
    # return: návratová hodnota
    # redirect(url_for('home')): přesměrování (redirect) na domovskou stránku (url_for('home'))

    # vytvoření instance pro formulář na odesílání tokenu pro změnu hesla:
    form = RequestResetForm()
    # form: instance třídy registračního formuláře
    # RequestResetForm(): třída formuláře na odesílání tokenu pro změnu hesla

    # podmínka ověřující, zda byly vloženy o validní údaje:
    if form.validate_on_submit():
        # form: instance třídy registračního formuláře
        # validate_on_submit(): metoda pro kontrolu, zda byly vložené údaje odpovídají nastavení formuláře

        # vytvoření databázového dotazu pro ověření zda se v databázi vyskytuje zadaný email:
        user = User.query.filter_by(email=form.email.data).first()
        # user: proměnná pro výsledek databázového dotazu
        # User.query: dotaz načítající (dle parametrů) data z databáze
        # filter_by(): definice filtru hledání
        # (email=form.email.data): v tabulce databáze v sloupci email hledej data z pole formuláře pro email
        # .first(): vrať první výsledek

        # volání funkce na odesílání tokenu pro změnu hesla:
        send_reset_email(user)
        # send_reset_email(): funkce na odesílání tokenu pro změnu hesla
        # (user): uživatel (proměnná pro výsledek databázového dotazu dle jeho emailu)

        # zobrazení informativní zprávy o neúspěšném přihlášení:
        flash(lazy_gettext("An email has been sent with instructions to reset your password."), 'info')
        # flash: metoda pro zobrazení informativní zprávy
        # gettext("...'): označení textu pro překlad [babel]
        # 'info': specifikace typu oznamu

        # přesměrování na stránku pro přihlášení:
        return redirect(url_for('users.login'))
        # return: návratová hodnota
        # redirect(url_for('login')): přesměrování (redirect) na stránku pro přihlášení (url_for('login'))

    # pokud vložená data jsou nekorektní, znovunačtení stránky s oznamem chyb:
    return render_template('reset_request.html', title='Reset Password', form=form, lflag=fl.current_lang)
    # return: návratová hodnota
    # render_template: metoda na vykreslování html šablony
    # ('reset_request.html': název html souboru
    # title='Reset Password': nadpis
    # form=form: instance pro třídu zobrazovaného formuláře
    # lflag=current_lang): odkaz na zkratku jazyka stránky (cs/en)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# USERS -02-4-G #
# definice stránky pro změnu hesla za použití tokenu:

# vytvoření stránky pro změnu hesla za použití tokenu
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
# @app.route(): je dekorátor pro cestu k stránkám aplikace
# "/nazevstranky": relativní cesta ke stránce
# methods=['GET', 'POST']: definice metod k načítání, nebo odesílání dat na server

def reset_token(token):
    # reset_token: název vytvářené stránky
    # (token): token pro změnu hesla (přichází z odkazu v mailu)

    # podmínka ověřující, zda je uživatel již autentizován, pokud ano, přesměruje nás na hlavní stránku:
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # current_user.is_authenticated: je-li aktuální uživatel (current_user) přihlášen (is_authenticated)
    # return: návratová hodnota
    # redirect(url_for('home')): přesměrování (redirect) na domovskou stránku (url_for('home'))

    # vytvoření proměnné pro ověření tokenu:
    user = User.verify_reset_token(token)
    # user: proměnná pro ověření tokenu
    # User: Třída uživatele
    # .verify_reset_token(token): metody třídy uživatele pro ověření tokenu (vrátí ID uživatele, nebo None)

    # podmínka pro případ neověření tokenu:
    if user is None:
        # if user is None: pokud proměnná user neobsahuje ID uživatele

        # zobrazení informativní zprávy o neúspěšném přihlášení:
        flash(lazy_gettext("That is an invalid or expired token"), 'warning')
        # flash: metoda pro zobrazení informativní zprávy
        # gettext("...'): označení textu pro překlad [babel]
        # 'warning': specifikace typu oznamu

        # přesměrování na stránku pro reset hesla:
        return redirect(url_for('users.reset_request'))
        # return: návratová hodnota
        # redirect(url_for('users.reset_request')): přesměrování (redirect) na stránku pro reset hesla

    # vytvoření instance pro formulář na změnu hesla:
    form = ResetPasswordForm()
    # form: instance třídy registračního formuláře
    # ResetPasswordForm(): třída formuláře na změnu hesla

    # podmínka ověřující, zda byly vloženy o validní údaje:
    if form.validate_on_submit():
        # form: instance třídy registračního formuláře
        # validate_on_submit(): metoda pro kontrolu, zda byly vložené údaje odpovídají nastavení formuláře

        # proměnná pro zašifrování vkládaného hesla:
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #hashed_password:
        # bcrypt: instance třídy Bcrypt pro šifrování
        # .generate_password_hash(): metoda třídy Bcrypt pro šifrování hesla
        # (form.password.data): heslo zadané do formuláře stránky
        # .decode('utf-8'): dekódování hesla do utf-8

        # vložení nového hesla:
        user.password = hashed_password
        # user.password: pole pro heslo uživatele
        # hashed_password: proměnná pro zašifrované heslo

        # uložení dat do databáze:
        db.session.commit()
        # db: instance třídy SQLAlchemy pro databázi
        # .session.commit(): ulož změny v databázi

        # zobrazení informativní zprávy o neúspěšném přihlášení:
        flash(lazy_gettext("Your password has been updated! You are now able to log in"), 'success')
        # flash: metoda pro zobrazení informativní zprávy
        # gettext("...'): označení textu pro překlad [babel]
        # 'success': specifikace typu oznamu

        # přesměrování na stránku pro přihlášení:
        return redirect(url_for('users.login'))
        # return: návratová hodnota
        # redirect(url_for('login')): přesměrování (redirect) na stránku pro přihlášení (url_for('login'))

    # pokud vložená data jsou nekorektní, znovunačtení stránky s oznamem chyb:
    return render_template('reset_token.html', title='Reset Password', form=form, lflag=fl.current_lang)
    # return: návratová hodnota
    # render_template: metoda na vykreslování html šablony
    # ('reset_token.html': název html souboru
    # title='Reset Password': nadpis
    # form=form: instance pro třídu zobrazovaného formuláře
    # lflag=current_lang): odkaz na zkratku jazyka stránky (cs/en)


#######################################################################################################################
