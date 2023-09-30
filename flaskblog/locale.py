# vytvoření proměnné pro výběr jazyka:
current_lang = "cs"
# current_lang: proměnná pro výběr jazyka
# "cs": prvotní hodnota (nastavená na češtinu)


# funkce pro nastavení jazyka stránky
def get_locale():
    # def get_locale(): nastavení jazyka stránky (pro Babel)
    return current_lang
    # return: návratová hodnota
    # current_lang: proměnná pro výběr jazyka


# proměnná pro seznam s překladem příspěvku
post_to_translate = [None,]
# post_to_translate: název proměnné
# [None,]: seznam na výsledek překladu (id příspěvku, název, obsah)

