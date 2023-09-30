#######################################################################################################################
# ERRORS-02 #
# SOUBOR PRO VYTVÁŘENÍ STRÁNEK - PODSEKCE HANDLERS #
# tento soubor slouží pro definici a vytváření stránek oznamujících chyby #
# (bez tohoto by se při těchto chybách oznam objevil v prázdném okně, takto se objeví v rámci naší stránky)

# ERRORS-02-1: import externích rozšíření programu
# ERRORS-02-2: vytvoření instance pro provázání tohoto souboru se souborem __init__.py v kořenové složce programu
# ERRORS-02-3-A:
# ERRORS-02-3-D:
# ERRORS-02-3-C:


#######################################################################################################################
# ERRORS-02-1 #
# import externích rozšíření programu:

from flask import Blueprint, render_template
# flask: je webový microframework pro tvorbu webu v programovacím jazyku Python
# Blueprint: třída pro zpřehlednění a uspořádání aplikace


#######################################################################################################################
# ERRORS-02-2 #
# vytvoření instance pro provázání tohoto souboru se souborem __init__.py v kořenové složce programu:

errors = Blueprint('errors', __name__)
# main: název vytvářené instance
# Blueprint: třída pro zpřehlednění a uspořádání aplikace
# ('errors': název složky balíčku
# __name__: je vestavěná speciální proměnná, která vyhodnocuje název aktuálního modulu. Pokud je zdrojový soubor spuštěn jako hlavní program, interpret nastaví proměnnou __name__ na hodnotu „__main__“. Pokud je tento soubor importován z jiného modulu, __name__ bude nastaveno na název modulu.


#######################################################################################################################
# ERRORS-02-3-A #
# definice stránky oznamující chybu nenalezení stránky (error 404):

@errors.app_errorhandler(404)
# @errors: je dekorátor pro cestu k chybovým stránkám aplikace
# .app_errorhandler(): metoda pro ošetření chyb (rozdíl mezi errorhandler() a app_errorhandler(): první by se vztahoval pouze k tomuto blueprintu, kdežto app... se vztahuje k celé aplikaci)
# (404): číslo chyby

def error_404(error):
    # error_404: název vytvářené stránky
    # error: vyvolaná chyba

    # navrácení vygenerované stránky
    return render_template('errors/404.html'), 404
    # return: návratová hodnota
    # render_template: metoda na vykreslování html šablony
    # ('errors/404.html'): cesta (podsložka errors) a název html souboru (404.html)
    # 404: kód chyby (status code)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ERRORS-02-3-B #
# definice stránky oznamující chybu nna kterou nemá uživatel oprávnění (error 403):

@errors.app_errorhandler(403)

def error_403(error):
    # error_403: název vytvářené stránky
    # error: vyvolaná chyba

    # navrácení vygenerované stránky
    return render_template('errors/403.html'), 403
    # return: návratová hodnota
    # render_template: metoda na vykreslování html šablony
    # ('errors/403.html'): cesta (podsložka errors) a název html souboru (403.html)
    # 403:


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ERRORS-02-3-C #
# definice stránky oznamující chybu serveru (error 500):

@errors.app_errorhandler(500)

def error_500(error):
    # error_500: název vytvářené stránky
    # error: vyvolaná chyba


    # navrácení vygenerované stránky
    return render_template('errors/500.html'), 500
    # return: návratová hodnota
    # render_template: metoda na vykreslování html šablony
    # ('errors/500.html'): cesta (podsložka errors) a název html souboru (500.html)
    # 500:

#######################################################################################################################