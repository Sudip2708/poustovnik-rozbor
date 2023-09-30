#######################################################################################################################
# MAIN-03 #
# SOUBOR PRO VYTVÁŘENÍ STRÁNEK - PODSEKCE MAIN #
# tento soubor slouží pro definici a vytváření stránek programu  #

# MAIN-03-1: import externích rozšíření programu
# MAIN-03-2: import vlastních rozšíření programu
# MAIN-03-3: vytvoření instance pro provázání tohoto souboru se souborem __init__.py v kořenové složce programu
# MAIN-03-4-A: definice hlavní stránky (s výpisem příspěvků)
# MAIN-03-4-B: definice stránky about (o nás)


#######################################################################################################################
# MAIN-03-1 #
# import externích rozšíření programu:

from flask import render_template, request, Blueprint, redirect, url_for
# flask: je webový microframework pro tvorbu webu v programovacím jazyku Python
# render_template: metoda na vykreslování html šablony
# request: metoda pro obsluhu dat odeslaných z klienta na server
# Blueprint: třída pro zpřehlednění a uspořádání aplikace
# redirect: metoda k přesměrování na jiný koncový bod

from googletrans import Translator
# googletrans: knihovna pro práci s Google Translate API
# Translator: předefinovaná třída pro získání překladu
# před importem je potřeba rozšíření doinstalovat > pip install googletrans==3.1.0a0
# https://pypi.org/project/googletrans/3.1.0a0/


#######################################################################################################################
# MAIN-03-2 #
# import vlastních rozšíření programu:

# import souboru sloužící pro změny jazyka stránky
import flaskblog.locale as fl
# flaskblog.locale: soubor locale.py v kořenovém adresáři aplikace (flaskblok) sloužící pro změny jazyka stránky
# fl: skratka pro použití odkazu v programu

# import databáze pro příspěvky:
from flaskblog.models import User, Post
# flaskblog.models: cesta k souboru (flaskblog=kořenový adresář, models=název souboru)
# Post: název třídy pro databázovou tabulku na příspěvky

# import textů pro stránku about
from flaskblog.main.about_texts import texts, links
# flaskblog.main.about_texts: cesta k souboru (flaskblog=kořenový adresář, main=složka, about_texts=název souboru)
# text: seznam s texty pro stránku about
# links: seznam s odkazy pro stránku about

#######################################################################################################################
# MAIN-03-3 #
# vytvoření instance pro provázání tohoto souboru se souborem __init__.py v kořenové složce programu:

main = Blueprint('main', __name__)
# main: název vytvářené instance
# Blueprint: třída pro zpřehlednění a uspořádání aplikace
# ('main': název složky balíčku
# __name__: je vestavěná speciální proměnná, která vyhodnocuje název aktuálního modulu. Pokud je zdrojový soubor spuštěn jako hlavní program, interpret nastaví proměnnou __name__ na hodnotu „__main__“. Pokud je tento soubor importován z jiného modulu, __name__ bude nastaveno na název modulu.


#######################################################################################################################
# MAIN-03-4-A #
# definice hlavní stránky (s výpisem příspěvků):

@main.route("/")
@main.route("/home")
# @main.route(): je dekorátor pro cestu k stránkám aplikace
# "/nazevstranky": relativní cesta ke stránce

def home():
    # home: název vytvářené stránky

    # vytvoření proměnné s číslem stránky k zobrazení:
    page = request.args.get('page', 1, type=int)
    # page: proměnná pro číslo požadované stránky
    # request.args.get(): žádost pro přístup k parametrům URL (tyto parametry jsou připojeny na konec adresy URL ve tvaru klíč=hodnota)
    # ('page', 1, type=int): 1.par==stránka, 2.par==defaultní hodnota, 3.par==deklarace typu

    # vytvoření proměnné s dotazem do databáze:
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # posts: proměnná pro data z databáze (instance třídy Post)
    # Post.query: dotaz načítající (dle parametrů) data z databáze
    # order_by(): požadavek na seřazení výsledků
    # (Post.date_posted.desc()): řadit podle data a sestupně (desc)
    # paginate(): metoda stránkování počítá celkový počet záznamů z databáze
    # (page=page, per_page=5): 1.par==číslo stránky, 2.par==specifikace kolik výpisů z databáze se má zobrazit na jedné stránce

    # vytvoření proměnné pro obsah překladu:
    translate = fl.post_to_translate[:]
    # translate: proměnná pro předání případného obsahu překladu příspěvku
    # fl.post_to_translate[:]: proměnná pro získaný překladu příspěvku

    # vymazání obsahu post_to_translate
    fl.post_to_translate = [None]
    # fl.post_to_translate = [None]: smazání obsahu proměnné pro získaný překladu příspěvku

    # navrácení vygenerované stránky:
    return render_template('home.html', posts=posts, lflag=fl.current_lang, translate=translate)
    # return: návratová hodnota
    # render_template(): metoda na vykreslování html šablony
    # ('home.html': název html souboru
    # posts=posts: výsledek databázového dotazu
    # lflag=current_lang: odkaz na zkratku jazyka stránky (cs/en)
    # translate=translate):  proměnná pro předání případného obsahu překladu příspěvku


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# MAIN-03-4-B #
# definice stránky about (o nás):

@main.route("/about")
# @main.route(): je dekorátor pro cestu k stránkám aplikace
# "/nazevstranky": relativní cesta ke stránce

def about(username="Sudip2708"):
    # about: název vytvářené stránky
    # username: jméno uživatele

    # vytvoření databázového dotazu, zda zadaný uživatel existuje v databázi:
    user = User.query.filter_by(username=username).first_or_404()
    # user: proměnná pro výsledek databázového dotazu
    # User.query: dotaz načítající (dle parametrů) data z databáze
    # filter_by(): definice filtru hledání
    # (username=username): v tabulce databáze v sloupci username hledej shodu s username přispěvatele
    # first_or_404(): vrať první výsledek, nebo vyvolej chybu 404 (nenalezení záznamu)


    # navrácení vygenerované stránky:
    return render_template('about.html', user=user, lflag=fl.current_lang, links=links, text=texts)
    # return: návratová hodnota
    # render_template(): metoda na vykreslování html šablony
    # ('user_posts.html': název html souboru
    # user=user: autor příspěvků
    # lflag=current_lang: odkaz na zkratku jazyka stránky (cs/en)
    # links=links: odkaz na linky stánek, které zde chci zobrazit (importováno ze souboru about_texts.py)
    # text=text): odkaz na texty, které zde chci zobrazit (importováno ze souboru about_texts.py)


#######################################################################################################################

@main.route("/lang")
# @main.route(): je dekorátor pro cestu k stránkám aplikace
# "/lang": relativní cesta ke stránce

def langh():
    # langh: název vytvářené stránky

    # změna jazyka v proměnné current_lang
    fl.current_lang = "cs" if fl.current_lang == "en" else "en"
    # flaskblog: cesta k funkci (__init__.py v kořenovém adresáři programu)
    # .current_lang = "cs": nastavení proměnné pro výběr jazyka na češtinu (sc)
    # if flaskblog.current_lang == "en": podmínka: pokud proměnná pro výběr jazyka obsahuje zkratku pro angličtinu (en)
    # else "en": podmínka: pokud proměnná pro výběr jazyka obsahuje zkratku pro češtinu (cs) nastav angličtinu (en)

    # změna jazyka stránky
    fl.get_locale()
    # flaskblog: cesta k funkci (__init__.py v kořenovém adresáři programu)
    # .get_locale(): funkce pro zadání jazyka stránky (používá proměnnou current_lang)

    # navrácení na předchozí stránku
    return redirect(request.headers.get("Referer"))
    # return: návratová hodnota
    # redirect(request.headers.get("Referer")): přesměrování (redirect) na předchozí stránku (request.headers.get("Referer"))


#######################################################################################################################

@main.route("/translate/<int:post_id>")
# @main.route(): je dekorátor pro cestu k stránkám aplikace
# "/lang": relativní cesta ke stránce

def translate(post_id):
    # translate: název vytvářené stránky
    # post_id: databázové ID číslo příspěvku

    # vytvoření instance pro data daného příspěvku:
    post = Post.query.get_or_404(post_id)
    # post: proměnná pro vybraný příspěvek (z databáze)
    # Post.query: dotaz načítající (dle parametrů) data z databáze
    # .get_or_404(): metoda vrací buď nalezený výsledek nebo chybu 404
    # (post_id): databázové ID číslo příspěvku

    # vytvoření instance pro překlad příspěvků (za pomoci google translate)
    translator = Translator()
    # translator: instance třídy Translator pro překlad předaného obsahu pomoci google translator
    # Translator(): třída pro vytvoření instance

    # dotaz na překlad nadpisu a obsahu příspěvku
    transl_title = translator.translate(post.title, dest=fl.current_lang).text
    transl_content = translator.translate(post.content, dest=fl.current_lang).text
    # transl_title: proměnná pro výsledný překlad
    # translator.translate(): instance (translator) a modul (translate) pro získání překladu
    # (post.title, dest=fl.current_lang): obsah pro překlad (post.title) a cílový jazyk (dest=fl.current_lang)
    # .text: specifikace textové oblasti překladu

    # přidání id příspěvku a překladu do proměnné fl.post_to_translate (locale.py)
    fl.post_to_translate = [post_id, transl_title, transl_content]
    # fl.: je skratka pro obsah souboru locale.py
    # post_to_translate: proměnná pro případný překlad
    # [post_id, transl_title, transl_content]: seznam překladu (id příspěvku, nadpis, obsah)

    # přesměrování na stránku příspěvku:
    return redirect(url_for('posts.post', post_id=post.id))
    # return: návratová hodnota
    # redirect(): přesměrování
    # url_for('posts.post', post_id=post.id): na stránku příspěvku


#######################################################################################################################


