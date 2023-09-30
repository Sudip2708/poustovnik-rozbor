#######################################################################################################################
# 00 #
# SPOUŠTĚCÍ SOUBOR PROGRAMU #
# tento soubor slouží k spuštění programu #

# 00-1: import vytvořené instance flasku
# 00-2: vytvoření instance aplikace
# 00-3: zpuštění aplikace (aktivace/deaktivace debug modu)


#######################################################################################################################
# 00-1 #
# import vytvořené instance flasku:

from flaskblog import create_app
# flaskblog: název aplikace (__init__.py v kořenové složce aplikace)
# current_app: funkce pro základní konfiguraci aplikace


#######################################################################################################################
# 00-2 #
# vytvoření instance aplikace:

app = create_app()
# app: proměnná pro vytvářenou aplikaci
# current_app: funkce pro základní konfiguraci aplikace


#######################################################################################################################
# 00-3 #
# zpuštění aplikace (aktivace/deaktivace debug modu):

debug = True
# debug: proměnná pro hodnotu debug módu (True/False)
# True/Fales: pravda/nepravda

if debug:
    # if: podmínka
    # debug: je-li hodnota proměnné debug True

    if __name__ == '__main__':
        # if: podmínka
        # __name__ == '__main__': je-li program souštěn z tohoto souboru

        app.run(debug=True)
        # app: proměnná pro aplikaci
        # .run(): příkaz pro zpuštění aplikace [flask]
        # (debug=True): příkaz pro zpuštění aplikace v ladícím režimu (debug mod) [flask]

else:
    # else: není-li předchozí podmínka splněna

    if __name__ == '__main__':
        # if: podmínka
        # __name__ == '__main__': je-li program souštěn z tohoto souboru

        app.run()
        # app: proměnná pro aplikaci
        # .run(): příkaz pro zpuštění aplikace [flask]


#######################################################################################################################