#######################################################################################################################
# POSTS-02 #
# SOUBOR PRO VYTVÁŘENÍ STRÁNEK - PODSEKCE POSTS #
# tento soubor slouží pro definici a vytváření stránek programu  #

# POSTS-02-1: import externích rozšíření programu
# POSTS-02-2: import vlastních rozšíření programu
# POSTS-02-3: vytvoření instance pro provázání tohoto souboru se souborem __init__.py v kořenové složce programu
# POSTS-02-4-A: definice stránky pro přidání nového příspěvku
# POSTS-02-4-B: definice stránky pro zobrazení vybraného příspěvku
# POSTS-02-4-C: definice stránky pro úpravu vybraného příspěvku
# POSTS-02-4-D: definice stránky pro smazání vybraného příspěvku


#######################################################################################################################
# POSTS-02-1 #
# import externích rozšíření programu:

from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
# flask: je webový microframework pro tvorbu webu v programovacím jazyku Python
# render_template: metoda na vykreslování html šablony
# url_for: metoda pro vygenerování url adresy k souborům projektu
# flash: metoda pro zobrazení informativní zprávy
# redirect: metoda k přesměrování na jiný koncový bod
# request: metoda pro obsluhu dat odeslaných z klienta na server
# abort: metoda pro předčasné zrušení požadavku s chybovým kódem
# Blueprint: třída pro zpřehlednění a uspořádání aplikace
# https://flask.palletsprojects.com/en/2.3.x/quickstart/

from flask_login import current_user, login_required
# flask_login: poskytuje správu uživatelských relací pro Flask
# current_user: proxy pro aktuálního uživatele
# login_required: metoda pro ověření přihlášení uživatele (vhodné pro následné rozšíření možností)
# https://flask-login.readthedocs.io/en/latest/

from flask_babel import lazy_gettext
# flask_babel: rozšíření pro lokalizaci stránek
# lazy_gettext: metoda pro označení textu, který bude překládán až ve chvíli volání


#######################################################################################################################
# POSTS-02-2 #
# import vlastních rozšíření programu:

# import souboru sloužící pro změny jazyka stránky
import flaskblog.locale as fl
# flaskblog.locale: soubor locale.py v kořenovém adresáři aplikace (flaskblok) sloužící pro změny jazyka stránky
# fl: skratka pro použití odkazu v programu

# import sqlalchemy:
from flaskblog import db
# flaskblog: cesta k souboru (__init__.py v kořenovém adresáři programu)
# db: instance třídy SQLAlchemy pro databáze

# import databáze pro příspěvky:
from flaskblog.models import Post
# flaskblog.models: cesta k souboru (flaskblog=kořenový adresář, models=název souboru)
# Post: název databázové třídy pro tabulku na příspěvky

# import formuláře pro stránku pro přidání nového příspěvku:
from flaskblog.posts.forms import PostForm
# flaskblog.posts.forms:  cesta k souboru (flaskblog=kořenový adresář, posts=název složky, forms=název souboru)
# PostForm: formulář na data pro stránku pro přidání nového příspěvku


#######################################################################################################################
# POSTS-02-3 #
# vytvoření instance pro provázání tohoto souboru se souborem __init__.py v kořenové složce programu:

posts = Blueprint('posts', __name__)
# posts: název vytvářené instance
# Blueprint: třída pro zpřehlednění a uspořádání aplikace
# ('users': název složky balíčku
# __name__: je vestavěná speciální proměnná, která vyhodnocuje název aktuálního modulu. Pokud je zdrojový soubor spuštěn jako hlavní program, interpret nastaví proměnnou __name__ na hodnotu „__main__“. Pokud je tento soubor importován z jiného modulu, __name__ bude nastaveno na název modulu.


#######################################################################################################################
# POSTS-02-4-A #
# definice stránky pro přidání nového příspěvku:

@posts.route("/post/new", methods=['GET', 'POST'])
# @posts.route(): je dekorátor pro cestu k stránkám aplikace
# "/nazevstranky": relativní cesta ke stránce
# methods=['GET', 'POST']: definice metod k načítání, nebo odesílání dat na server

@login_required
# @login_required: dekorátor vyžadující přihlášení uživatele k zobrazení pohledu

def new_post():
    # new_post: název vytvářené stránky

    # vytvoření instance pro formulář na vytvoření nového příspěvku:
    form = PostForm()
    # form: instance třídy pro formulář pro vytvoření nového příspěvku
    # PostForm(): třída formuláře pro vytvoření nového příspěvku

    # podmínka ověřující, zda byly vloženy o validní údaje:
    if form.validate_on_submit():
        # form: instance třídy pro formulář pro aktualizaci údajů o uživateli
        # validate_on_submit(): metoda pro kontrolu, zda byly vložené údaje odpovídají nastavení formuláře

        # vytvoření instance pro vložení dat do databáze:
        post = Post(title=form.title.data, content=form.content.data, author=current_user, lang=fl.current_lang)
        # post: proměnná pro data z databáze (instance třídy Post fro formulář stránky)
        # Post(): třída pro databázovou tabulku na příspěvky
        # (title=form.title.data: proměnná pro titulek příspěvku z formuláře stránky
        # content=form.content.data: proměnná pro obsah příspěvku z formuláře stránky
        # author=current_user): proměnná pro autora příspěvku z formuláře stránky

        # vložení dat do databáze:
        db.session.add(post)
        db.session.commit()
        # db: instance třídy SQLAlchemy pro databázi
        # .session.add(post): vlož do databáze nový příspěvek
        # .session.commit(): ulož změny v databázi

        # zobrazení informativní zprávy o úspěšném vytvoření účtu:
        flash(lazy_gettext("Your post has been created!"), 'success')
        # flash: metoda pro zobrazení informativní zprávy
        # gettext("...'): označení textu pro překlad [babel]
        # 'success': specifikace typu oznamu

        # přesměrování na domovskou stránku:
        return redirect(url_for('main.home'))
        # return: návratová hodnota
        # redirect(): přesměrování
        # url_for('main.home'): na domovskou stránku

    # pokud vložená data jsou nekorektní, znovunačtení stránky s oznamem chyb:
    return render_template('create_post.html', title='New Post', form=form, legend=lazy_gettext('New Post'), lflag=fl.current_lang)
    # return: návratová hodnota
    # render_template: metoda na vykreslování html šablony
    # ('create_post.html': název html souboru
    # title='create_post': nadpis
    # form=form: instance pro třídu zobrazovaného formuláře
    # legend='New Post': popisek
    # lflag=current_lang): odkaz na zkratku jazyka stránky (cs/en)




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# POSTS -02-4-B #
# definice stránky pro zobrazení vybraného příspěvku:

@posts.route("/post/<int:post_id>")
# @posts.route(): je dekorátor pro směrování k stránkám aplikace
# "/post/<int:post_id>": je ID číslo (z databáze) vybraného příspěvku

def post(post_id):
    # post_id: databázové ID číslo příspěvku

    # vytvoření instance pro formulář pro zobrazení příspěvku:
    post = Post.query.get_or_404(post_id)
    # post: proměnná pro vybraný příspěvek (z databáze)
    # Post.query: dotaz načítající (dle parametrů) data z databáze
    # .get_or_404(): metoda vrací buď nalezený výsledek nebo chybu 404
    # (post_id): databázové ID číslo příspěvku

    # vytvoření proměnné pro obsah překladu:
    translate = fl.post_to_translate[:]
    # translate: proměnná pro předání případného obsahu překladu příspěvku
    # fl.post_to_translate[:]: proměnná pro získaný překladu příspěvku

    # vymazání obsahu post_to_translate
    fl.post_to_translate = [None]
    # fl.post_to_translate = [None]: smazání obsahu proměnné pro získaný překladu příspěvku

    # (post_id): databázové ID číslo příspěvku:
    return render_template('post.html', title=post.title, post=post, lflag=fl.current_lang, translate=translate)
    # return: návratová hodnota
    # render_template(): metoda na vykreslování html šablony
    # ('post.html': název html souboru
    # title=post.title: nadpis
    # post=post: vybraný příspěvek (z databáze)
    # lflag=current_lang: odkaz na zkratku jazyka stránky (cs/en)
    # translate=translate):  proměnná pro předání případného obsahu překladu příspěvku


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# POSTS -02-4-C #
# definice stránky pro úpravu vybraného příspěvku:

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
# @posts.route(): je dekorátor pro cestu k stránkám aplikace
# "/post/<int:post_id>/update": cesta ke stránce (<int:post_id> je ID číslo vybraného příspěvku)
# methods=['GET', 'POST']: definice metod k načítání, nebo odesílání dat na server

@login_required
# @login_required: dekorátor vyžadující přihlášení uživatele k zobrazení pohledu

def update_post(post_id):
    # post_id: databázové ID číslo příspěvku

    # vytvoření instance pro formulář pro zobrazení příspěvku:
    post = Post.query.get_or_404(post_id)
    # post: proměnná pro vybraný příspěvek (z databáze)
    # Post.query: dotaz načítající (dle parametrů) data z databáze
    # .get_or_404(): metoda vrací buď nalezený výsledek nebo chybu 404
    # (post_id): databázové ID číslo příspěvku

    # kontrola zda se jedná o příspěvek uživatele:
    if post.author != current_user:
        abort(403)
        # post.author: autor příspěvku
        # current_user: přihlášený uživatel
        # abort(403): přerušení operace a vyvolání chyby 403

    # vytvoření instance pro formulář pro vytvoření nového příspěvku a jeho úpravu:
    form = PostForm()
    # form: instance třídy pro formulář pro vytvoření nového příspěvku a jeho úpravu
    # PostForm(): třída formuláře pro vytvoření nového příspěvku a jeho úpravu

    # podmínka ověřující, zda byly vloženy o validní údaje:
    if form.validate_on_submit():
        # form: instance třídy pro formulář pro vytvoření nového příspěvku a jeho úpravu
        # validate_on_submit(): metoda pro kontrolu, zda byly vložené údaje odpovídají nastavení formuláře

        # proměnné pro obsah příspěvku:
        post.title = form.title.data
        # post.title: název příspěvku v instanci příspěvku
        # form.title.data: název příspěvku z formuláře na webu
        post.content = form.content.data
        # post.content: obsah příspěvku v instanci příspěvku
        # form.content.data: obsah příspěvku z formuláře na webu

        # vložení dat do databáze:
        db.session.commit()
        # db: instance třídy SQLAlchemy pro databázi
        # .session.commit(): ulož změny v databázi

        # zobrazení informativní zprávy o úspěšném vytvoření účtu:
        flash(lazy_gettext("Your post has been updated!"), 'success')
        # flash: metoda pro zobrazení informativní zprávy
        # gettext("...'): označení textu pro překlad [babel]
        # 'success': specifikace typu oznamu

        # přesměrování na stránku příspěvku:
        return redirect(url_for('posts.post', post_id=post.id))
        # return: návratová hodnota
        # redirect(): přesměrování
        # url_for('posts.post', post_id=post.id): na stránku příspěvku

    # podmínka, pro načítání stránky:
    elif request.method == 'GET':
        # request.method == 'GET': volání metody pro načtení stránky

        # předvyplnění údajů ve formuláři na stránce:
        form.title.data = post.title
        # form.title.data: pole formuláře stránky pro nadpis příspěvku
        # post.title: název příspěvku z instance příspěvku
        form.content.data = post.content
        # form.content.data: pole formuláře stránky pro obsah příspěvku
        # post.content: obsah příspěvku z instance příspěvku

    # pokud vložená data jsou nekorektní, znovunačtení stránky s oznamem chyb:
    return render_template('create_post.html', title=lazy_gettext('Update Post'), form=form, legend=lazy_gettext('Update Post'), lflag=fl.current_lang)
    # return: návratová hodnota
    # render_template: metoda na vykreslování html šablony
    # ('create_post.html': název html souboru
    # title='Update Post': nadpis
    # form=form: instance pro třídu zobrazovaného formuláře
    # legend='Update Post': popis
    # lflag=current_lang): odkaz na zkratku jazyka stránky (cs/en)



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# POSTS -02-4-D #
# definice stránky pro smazání vybraného příspěvku:

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
# @posts.route(): je dekorátor pro cestu k stránkám aplikace
# "/post/<int:post_id>/delete": cesta ke stránce (<int:post_id> je ID číslo vybraného příspěvku)
# methods=['POST']: definice metod k odesílání dat na server

@login_required
# @login_required: dekorátor vyžadující přihlášení uživatele k zobrazení pohledu

def delete_post(post_id):
    # post_id: databázové ID číslo příspěvku

    # vytvoření instance pro formulář pro zobrazení příspěvku:
    post = Post.query.get_or_404(post_id)
    # post: proměnná pro vybraný příspěvek (z databáze)
    # Post.query: dotaz načítající (dle parametrů) data z databáze
    # .get_or_404(): metoda vrací buď nalezený výsledek nebo chybu 404
    # (post_id): databázové ID číslo příspěvku

    # kontrola zda se jedná o příspěvek uživatele:
    if post.author != current_user:
        abort(403)
        # post.author: autor příspěvku
        # current_user: přihlášený uživatel
        # abort(403): přerušení operace a vyvolání chyby 403

    # smazání příspěvku z databáze:
    db.session.delete(post)
    db.session.commit()
    # db: instance třídy SQLAlchemy pro databázi
    # .session.delete(post): smaž příspěvek z databáze
    # .session.commit(): ulož změny v databázi

    # zobrazení informativní zprávy o úspěšném vytvoření účtu:
    flash(lazy_gettext("Your post has been deleted!"), 'success')
    # flash: metoda pro zobrazení informativní zprávy
    # gettext("...'): označení textu pro překlad [babel]
    # 'success': specifikace typu oznamu

    # přesměrování na domovskou stránku:
    return redirect(url_for('main.home'))
    # return: návratová hodnota
    # redirect(): přesměrování
    # url_for('main.home'): na domovskou stránku


#######################################################################################################################