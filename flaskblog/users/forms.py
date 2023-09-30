#######################################################################################################################
# USERS-03 #
# SOUBOR PRO VYTVÁŘENÍ FORMULÁŘŮ PRO STRÁNKY S DATY - PODSEKCE USERS #
# tento soubor slouží pro definici polí formulářů stránek s daty   #

# USERS-03-1: import externích rozšíření programu
# USERS-03-2: import vlastních rozšíření programu
# USERS-03-3-A: definice třídy formuláře pro registrace
# USERS-03-3-B: definice třídy formuláře pro přihlášení
# USERS-03-3-C: definice třídy formuláře pro správu uživatelského účtu
# USERS-03-3-D: definice třídy formuláře pro vyžádání nového hesla
# USERS-03-3-E: definice třídy formuláře pro resetování hesla


#######################################################################################################################
# USERS-03-1 #
# import externích rozšíření programu:

# import modulu FlaskForm (třída na formuláře)
from flask_wtf import FlaskForm
# flask_wtf: je balíček pro integraci Flask a WTForms , včetně CSRF, nahrávání souborů a reCAPTCHA.
# FlaskForm: třída usnadňující definování a zpracování formulářů

# import knihovny pro ověřování polí formulářů
from flask_wtf.file import FileField, FileAllowed
# FileField: třída pro ověření typu pole (zkontroluje, zda je soubor neprázdnou instancí FileStorage, jinak None)
# FileAllowed: třída pro ověření platnosti typu souboru (ověřuje nahrávání souborů pomocí FileRequireda)

# import knihovny pro ověřování a vykreslování formulářů pro vývoj webu v Pythonu
from wtforms import StringField, PasswordField, SubmitField, BooleanField
# wtforms: knihovna pro ověřování a vykreslování formulářů pro vývoj webu v Pythonu
# StringField: třída pro základní pole na zadávání textu
# PasswordField: třída pro pole na zadávání hesla
# SubmitField: třída pro tlačítko na odeslání dat
# BooleanField: třída pro zaškrtávací pole (True/False)

# import rozšíření wtforms pro ověření (validaci) zadávaných údajů
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
# wtforms.validators: modulu s třídami pro ověření (validaci) zadávaných údajů
# DataRequired: ověřuje zda je pole vyplněno
# Length: ověřuje délku řetězce (dle definovaných parametrů)
# Email: ověřuje zda se jedná o emailovou adresu
# EqualTo: porovnává hodnoty dvou polí
# ValidationError: výjimka volaná v případě, že se zadávaná data nejsou validní

# import metod z modulu flask_login (pro administraci přihlášení)
from flask_login import current_user
# flask_login: poskytuje správu uživatelských relací pro Flask
# current_user: proxy pro aktuálního uživatele

from flask_babel import lazy_gettext
# flask_babel: rozšíření pro lokalizaci stránek
# lazy_gettext: metoda pro označení textu, který bude překládán až ve chvíli volání


#######################################################################################################################
# USERS-03-2 #
# import vlastních rozšíření programu:

# import tříd ze souboru models.py (databáze)
from flaskblog.models import User
# flaskblog.models: soubor models.py (umístěný v kořenovém adresáři)
# User: třída pro databázi uživatelů


#######################################################################################################################
# USERS-03-3-A #
# definice třídy formuláře pro registrace:

class RegistrationForm(FlaskForm):
    # RegistrationForm: název vytvářené třídy
    # FlaskForm: třída usnadňující definování a zpracování formulářů

    # vytvoření atributu pro pole pro uživatelské jméno:
    username = StringField(lazy_gettext("Username"), validators=[DataRequired(), Length(min=2, max=20)])
    # username: instance pro pole pro uživatelské jméno
    # StringField: třída pro základní pole na zadávání textu
    # (lazy_gettext("...'): označení textu pro překlad [babel]
    # 'Username': název pole
    # validators: modulu s třídami pro ověření (validaci) zadávaných údajů
    # [DataRequired(): ověřuje zda je pole vyplněno
    # Length(min=2, max=20)]): ověřuje délku řetězce (dle definovaných parametrů)

    # vytvoření atributu pro pole pro email:
    email = StringField(lazy_gettext("Email"), validators=[DataRequired(), Email()])
    # email: instance pro pole pro email
    # StringField: třída pro základní pole na zadávání textu
    # (lazy_gettext("...'): označení textu pro překlad [babel]
    # 'Email': název pole
    # validators: modulu s třídami pro ověření (validaci) zadávaných údajů
    # [DataRequired(): ověřuje zda je pole vyplněno
    # Email()]: ověřuje zda se jedná o emailovou adresu

    # vytvoření atributu pro pole pro zadání hesla:
    password = PasswordField(lazy_gettext("Password"), validators=[DataRequired()])
    # password: instance pro pole pro zadání hesla
    # PasswordField: třída pro pole na zadávání hesla
    # (lazy_gettext("...'): označení textu pro překlad [babel]
    # 'Password': název pole
    # validators: modulu s třídami pro ověření (validaci) zadávaných údajů
    # [DataRequired()]): ověřuje zda je pole vyplněno

    # vytvoření atributu pro pole pro potvrzení hesla:
    confirm_password = PasswordField(lazy_gettext("Confirm Password"), validators=[DataRequired(), EqualTo('password')])
    # confirm_password: instance pro pole pro potvrzení hesla
    # PasswordField: třída pro pole na zadávání hesla
    # (lazy_gettext("...'): označení textu pro překlad [babel]
    # 'Confirm Password': název pole
    # validators: modulu s třídami pro ověření (validaci) zadávaných údajů
    # [DataRequired(): ověřuje zda je pole vyplněno
    # EqualTo('password')]): porovnává hodnoty dvou polí (tady Password a Confirm Password)

    # vytvoření atributu pro pole s odesílacím tlačítkem:
    submit = SubmitField(lazy_gettext("Sign Up"))
    # submit: instance pro pole s odesílacím tlačítkem
    # SubmitField: třída pro tlačítko na odeslání dat
    # lazy_gettext("...'): označení textu pro překlad [babel]
    # 'Sign Up': název tlačítka

    # metoda pro ověření, zda uživatelské jméno už není v databázi:
    def validate_username(self, username):
        # username: uživatelské jméno zadané ve formuláři

        # vytvoření databázového dotazu pro ověření zda zadané uživatelské jméno se vyskytuje v databázi:
        user = User.query.filter_by(username=username.data).first()
        # user: proměnná pro výsledek databázového dotazu
        # User.query: dotaz načítající (dle parametrů) data z databáze
        # filter_by(): definice filtru hledání
        # (username=username.data): v tabulce databáze v sloupci username hledej data z pole formuláře pro username
        # .first(): vrať první výsledek

        # podmínka pro případ nalezení zadaného uživatelského jména:
        if user:
            # user: proměnná pro výsledek databázového dotazu
            raise ValidationError(lazy_gettext("That username is taken. Please choose a different one."))
            # raise: metoda sloužící k vyvolání výjimky (chyby)
            # ValidationError(): výjimka pro chybu ověření
            # lazy_gettext("...'): označení textu pro překlad [babel]
            # 'That username is taken. Please choose a different one.': oznam pro vyvolání výjimky

    # metoda pro ověření, zda zadaný email už není v databázi:
    def validate_email(self, email):
        # email: email zadaný ve formuláři

        # vytvoření databázového dotazu pro ověření zda zadaný email se vyskytuje v databázi:
        user = User.query.filter_by(email=email.data).first()
        # user: proměnná pro výsledek databázového dotazu
        # User.query: dotaz načítající (dle parametrů) data z databáze
        # filter_by(): definice filtru hledání
        # (email=email.data): v tabulce databáze v sloupci email hledej data z pole formuláře pro email
        # .first(): vrať první výsledek

        # podmínka pro případ nalezení zadaného uživatelského jména:
        if user:
            # user: proměnná pro výsledek databázového dotazu
            raise ValidationError(lazy_gettext("That email is taken. Please choose a different one."))
            # raise: metoda sloužící k vyvolání výjimky (chyby)
            # ValidationError(): výjimka pro chybu ověření
            # lazy_gettext("...'): označení textu pro překlad [babel]
            # 'That email is taken. Please choose a different one.': oznam pro vyvolání výjimky


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# USERS-03-3-B #
# definice třídy formuláře pro přihlášení:

class LoginForm(FlaskForm):
    # LoginForm: název vytvářené třídy
    # FlaskForm: třída usnadňující definování a zpracování formulářů

    # vytvoření atributu pro pole pro email:
    email = StringField(lazy_gettext("Email"), validators=[DataRequired(), Email()])
    # email: instance pro pole pro email
    # StringField: třída pro základní pole na zadávání textu
    # (lazy_gettext("...'): označení textu pro překlad [babel]
    # 'Email': název pole
    # validators: modulu s třídami pro ověření (validaci) zadávaných údajů
    # [DataRequired(): ověřuje zda je pole vyplněno
    # Email()]: ověřuje zda se jedná o emailovou adresu

    # vytvoření atributu pro pole pro zadání hesla:
    password = PasswordField(lazy_gettext("Password"), validators=[DataRequired()])
    # password: instance pro pole pro zadání hesla
    # PasswordField: třída pro pole na zadávání hesla
    # (lazy_gettext("...'): označení textu pro překlad [babel]
    # 'Password': název pole
    # validators: modulu s třídami pro ověření (validaci) zadávaných údajů
    # [DataRequired()]): ověřuje zda je pole vyplněno

    # vytvoření atributu pro zaškrtávací pole pro zapamatování přihlašovacích údajů:
    remember = BooleanField(lazy_gettext("Remember Me"))
    # remember: instance pro zaškrtávací pole
    # BooleanField(): třída pro zaškrtávací pole
    # lazy_gettext("...'): označení textu pro překlad [babel]
    # 'Remember Me': název zaškrtávacího pole

    # vytvoření atributu pro pole s odesílacím tlačítkem:
    submit = SubmitField(lazy_gettext("Login"))
    # submit: instance pro pole s odesílacím tlačítkem
    # SubmitField: třída pro tlačítko na odeslání dat
    # lazy_gettext("...'): označení textu pro překlad [babel]
    # 'Login': název tlačítka


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# USERS-03-3-C #
# definice třídy formuláře pro správu uživatelského účtu:

class UpdateAccountForm(FlaskForm):
    # UpdateAccountForm: název vytvářené třídy
    # FlaskForm: třída usnadňující definování a zpracování formulářů

    # vytvoření atributu pro pole pro uživatelské jméno:
    username = StringField(lazy_gettext("Username"), validators=[DataRequired(), Length(min=2, max=20)])
    # username: instance pro pole pro uživatelské jméno
    # StringField: třída pro základní pole na zadávání textu
    # (lazy_gettext("...'): označení textu pro překlad [babel]
    # 'Username': název pole
    # validators: modulu s třídami pro ověření (validaci) zadávaných údajů
    # [DataRequired(): ověřuje zda je pole vyplněno
    # Length(min=2, max=20)]): ověřuje délku řetězce (dle definovaných parametrů)

    # vytvoření atributu pro pole pro email:
    email = StringField(lazy_gettext("Email"), validators=[DataRequired(), Email()])
    # email: instance pro pole pro email
    # StringField: třída pro základní pole na zadávání textu
    # (lazy_gettext("...'): označení textu pro překlad [babel]
    # 'Email': název pole
    # validators: modulu s třídami pro ověření (validaci) zadávaných údajů
    # [DataRequired(): ověřuje zda je pole vyplněno
    # Email()]: ověřuje zda se jedná o emailovou adresu

    # soubor obrázku s omezovačem na typ souboru (jpg, png):
    picture = FileField(lazy_gettext("Update Profile Picture"), validators=[FileAllowed(['jpg', 'png'])])
    # picture: instance pro třídu pro ověření typu pole (zde pro typ souboru jpg a png)
    # FileField(): třída pro ověření typu pole (zkontroluje, zda je soubor neprázdnou instancí FileStorage, jinak None)
    # (lazy_gettext("...'): označení textu pro překlad [babel]
    # 'Update Profile Picture': název pole
    # validators: modulu s třídami pro ověření (validaci) zadávaných údajů
    # [FileAllowed: třída pro ověření platnosti typu souboru (ověřuje nahrávání souborů pomocí FileRequireda)
    # (['jpg', 'png'])]): hodnoty pro ověření vstupního souboru (zde pro typ souboru jpg a png)

    # vytvoření atributu pro pole s odesílacím tlačítkem:
    submit = SubmitField(lazy_gettext("Update"))
    # submit: instance pro pole s odesílacím tlačítkem
    # SubmitField: třída pro tlačítko na odeslání dat
    # lazy_gettext("...'): označení textu pro překlad [babel]
    # 'Update': název tlačítka

    # metoda pro ověření, zda uživatelské jméno už není v databázi:
    def validate_username(self, username):
        # username: uživatelské jméno zadané ve formuláři

        # podmínka pro případ, že se jméno neshoduje s jménem aktuálního uživatele (bylo změněno):
        if username.data != current_user.username:
            # username.data: uživatelské jméno z formuláře
            # current_user.username: uživatelské jméno z instance aktuálního uživatele

            # vytvoření databázového dotazu pro ověření zda zadané uživatelské jméno se vyskytuje v databázi:
            user = User.query.filter_by(username=username.data).first()
            # user: proměnná pro výsledek databázového dotazu
            # User.query: dotaz načítající (dle parametrů) data z databáze
            # filter_by(): definice filtru hledání
            # (username=username.data): v tabulce databáze v sloupci username hledej data z pole formuláře pro username
            # .first(): vrať první výsledek

            # podmínka pro případ nalezení zadaného uživatelského jména:
            if user:
                # user: proměnná pro výsledek databázového dotazu
                raise ValidationError(lazy_gettext("That username is taken. Please choose a different one."))
                # raise: metoda sloužící k vyvolání výjimky (chyby)
                # ValidationError(): výjimka pro chybu ověření
                # lazy_gettext("...'): označení textu pro překlad [babel]
                # 'That username is taken. Please choose a different one.': oznam pro vyvolání výjimky

    # metoda pro ověření, zda zadaný email už není v databázi:
    def validate_email(self, email):
        # email: email zadaný ve formuláři

        # podmínka pro případ, že se email neshoduje s emailem aktuálního uživatele (byl změněno):
        if email.data != current_user.email:
            # email.data: email z formuláře
            # current_user.email: email z instance aktuálního uživatele

            # vytvoření databázového dotazu pro ověření zda zadaný email se vyskytuje v databázi:
            user = User.query.filter_by(email=email.data).first()
            # user: proměnná pro výsledek databázového dotazu
            # User.query: dotaz načítající (dle parametrů) data z databáze
            # filter_by(): definice filtru hledání
            # (email=email.data): v tabulce databáze v sloupci email hledej data z pole formuláře pro email
            # .first(): vrať první výsledek

            # podmínka pro případ nalezení zadaného uživatelského jména:
            if user:
                # user: proměnná pro výsledek databázového dotazu
                raise ValidationError(lazy_gettext("That email is taken. Please choose a different one."))
                # raise: metoda sloužící k vyvolání výjimky (chyby)
                # ValidationError(): výjimka pro chybu ověření
                # lazy_gettext("...'): označení textu pro překlad [babel]
                # 'That email is taken. Please choose a different one.': oznam pro vyvolání výjimky


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# USERS-03-3-D #
# definice třídy formuláře pro vyžádání nového hesla:

class RequestResetForm(FlaskForm):
    # RequestResetForm: název vytvářené třídy
    # FlaskForm: třída usnadňující definování a zpracování formulářů

    # vytvoření atributu pro pole pro email:
    email = StringField(lazy_gettext("Email"), validators=[DataRequired(), Email()])
    # email: instance pro pole pro email
    # StringField: třída pro základní pole na zadávání textu
    # (lazy_gettext("...'): označení textu pro překlad [babel]
    # 'Email': název pole
    # validators: modulu s třídami pro ověření (validaci) zadávaných údajů
    # [DataRequired(): ověřuje zda je pole vyplněno
    # Email()]: ověřuje zda se jedná o emailovou adresu

    # vytvoření atributu pro pole s odesílacím tlačítkem:
    submit = SubmitField(lazy_gettext("Request Password Reset"))
    # submit: instance pro pole s odesílacím tlačítkem
    # SubmitField: třída pro tlačítko na odeslání dat
    # lazy_gettext("...'): označení textu pro překlad [babel]
    # 'Request Password Reset': název tlačítka

    # metoda pro ověření, zda se jedná o platný email:
    def validate_email(self, email):
        # email: email zadaný ve formuláři

        # vytvoření databázového dotazu pro ověření zda zadaný email se vyskytuje v databázi:
        user = User.query.filter_by(email=email.data).first()
        # user: proměnná pro výsledek databázového dotazu
        # User.query: dotaz načítající (dle parametrů) data z databáze
        # filter_by(): definice filtru hledání
        # (email=email.data): v tabulce databáze v sloupci email hledej data z pole formuláře pro email
        # .first(): vrať první výsledek

        # podmínka pro případ, nebude-li email nalezen:
        if user is None:
            # user: proměnná pro výsledek databázového dotazu
            raise ValidationError(lazy_gettext("There is no account with that email. You must register first."))
            # raise: metoda sloužící k vyvolání výjimky (chyby)
            # ValidationError(): výjimka pro chybu ověření
            # lazy_gettext("...'): označení textu pro překlad [babel]
            # 'There is no account with that email. You must register first.': oznam pro vyvolání výjimky


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# USERS-03-3-E #
# definice třídy formuláře pro resetování hesla:

class ResetPasswordForm(FlaskForm):
    # ResetPasswordForm: název vytvářené třídy
    # FlaskForm: třída usnadňující definování a zpracování formulářů

    # vytvoření atributu pro pole pro zadání hesla:
    password = PasswordField(lazy_gettext("Password"), validators=[DataRequired()])
    # password: instance pro pole pro zadání hesla
    # PasswordField: třída pro pole na zadávání hesla
    # (lazy_gettext("...'): označení textu pro překlad [babel]
    # 'Password': název pole
    # validators: modulu s třídami pro ověření (validaci) zadávaných údajů
    # [DataRequired()]): ověřuje zda je pole vyplněno

    # vytvoření atributu pro pole pro potvrzení hesla:
    confirm_password = PasswordField(lazy_gettext("Confirm Password"), validators=[DataRequired(), EqualTo('password')])
    # confirm_password: instance pro pole pro potvrzení hesla
    # PasswordField: třída pro pole na zadávání hesla
    # (lazy_gettext("...'): označení textu pro překlad [babel]
    # 'Confirm Password': název pole
    # validators: modulu s třídami pro ověření (validaci) zadávaných údajů
    # [DataRequired(): ověřuje zda je pole vyplněno
    # EqualTo('password')]): porovnává hodnoty dvou polí (tady Password a Confirm Password)

    # vytvoření atributu pro pole s odesílacím tlačítkem:
    submit = SubmitField(lazy_gettext("Reset Password"))
    # submit: instance pro pole s odesílacím tlačítkem
    # SubmitField: třída pro tlačítko na odeslání dat
    # lazy_gettext("...'): označení textu pro překlad [babel]
    # 'Reset Password': název tlačítka


#######################################################################################################################