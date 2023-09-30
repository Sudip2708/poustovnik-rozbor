#######################################################################################################################
# POSTS-03 #
# SOUBOR PRO VYTVÁŘENÍ FORMULÁŘŮ PRO STRÁNKY S DATY - PODSEKCE POSTS #
# tento soubor slouží pro definici polí formulářů stránek s daty   #

# POSTS-03-1: import externích rozšíření programu
# POSTS-03-2: definice třídy formuláře pro přidání nového příspěvku


#######################################################################################################################
# POSTS-03-1 #
# import externích rozšíření programu:

# import modulu FlaskForm (třída na formuláře):
from flask_wtf import FlaskForm
# flask_wtf: je balíček pro integraci Flask a WTForms , včetně CSRF, nahrávání souborů a reCAPTCHA.
# FlaskForm: třída usnadňující definování a zpracování formulářů

# import knihovny pro ověřování a vykreslování formulářů pro vývoj webu v Pythonu:
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
# wtforms: knihovna pro ověřování a vykreslování formulářů pro vývoj webu v Pythonu
# StringField: třída pro základní pole na zadávání textu
# SubmitField: třída pro tlačítko na odeslání dat
# TextAreaField: třída pro pole na víceřádkový text

# import rozšíření wtforms pro ověření (validaci) zadávaných údajů:
from wtforms.validators import DataRequired
# wtforms.validators: modulu s třídami pro ověření (validaci) zadávaných údajů
# DataRequired: ověřuje zda je pole vyplněno

# import rozšíření pro lokalizaci stránky
from flask_babel import lazy_gettext
# flask_babel: rozšíření pro lokalizaci stránek
# lazy_gettext: metoda pro označení textu, který bude překládán až ve chvíli volání


#######################################################################################################################
# POSTS-03-2 #
# definice třídy formuláře pro přidání nového příspěvku:

class PostForm(FlaskForm):
    # PostForm: název vytvářené třídy
    # FlaskForm: třída usnadňující definování a zpracování formulářů

    # vytvoření atributu pro pole pro nadpis příspěvku:
    title = StringField(lazy_gettext("Title"), validators=[DataRequired()])
    # title: instance pro pole pro nadpis příspěvku
    # StringField: třída pro základní pole na zadávání textu
    # (lazy_gettext("...'): označení textu pro překlad [babel]
    # 'Title': název pole
    # validators: modulu s třídami pro ověření (validaci) zadávaných údajů
    # [DataRequired(): ověřuje zda je pole vyplněno

    # vytvoření atributu pro pole pro obsah příspěvku:
    content = TextAreaField(lazy_gettext("Content"), validators=[DataRequired()])
    # content: instance pro pole pro obsah příspěvku
    # StringField: třída pro základní pole na zadávání textu
    # (lazy_gettext("...'): označení textu pro překlad [babel]
    # 'Content': název pole
    # validators: modulu s třídami pro ověření (validaci) zadávaných údajů
    # [DataRequired(): ověřuje zda je pole vyplněno

    # vytvoření atributu pro pole s odesílacím tlačítkem:
    submit = SubmitField(lazy_gettext("Post"))
    # submit: instance pro pole s odesílacím tlačítkem
    # SubmitField: třída pro tlačítko na odeslání dat
    # lazy_gettext("...'): označení textu pro překlad [babel]
    # 'Post': název tlačítka


#######################################################################################################################
