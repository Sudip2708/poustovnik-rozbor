#######################################################################################################################
# MAIN-02 #
# SOUBOR S TEXTY A ODKAZY PRO STRÁNKU ABOUT #
# tento soubor slouží pro seskupení textů a odkazů pro stránku about #

# MAIN-03-1: import externích rozšíření programu
# MAIN-03-2: import vlastních rozšíření programu






from flask_babel import lazy_gettext
# flask_babel: rozšíření pro lokalizaci stránek
# lazy_gettext: metoda pro označení textu, který bude překládán až ve chvíli volání

#######################################################################################################################
# MAIN-03-1 #
# seznam odstavců pro stránku about:

texts = [

    (lazy_gettext("...and thank you Corey!"),
     lazy_gettext("This pages are based on a YouTube video tutorial by Corey Schafer. "
     "They are made in Flask and they are my first real project and also real proof of Corey great teaching skills.")),

    (lazy_gettext("About me"),
     lazy_gettext("I am quite newbie in the programming world. "
     "I've been studying Python for about a year and a half, and recently I completed a three-month course on creating web applications. "
     "So I was looking for some project to combine and practice new skills and found this. "
     "And I was perfect.")),

    (lazy_gettext("Purpose of this page"),
     lazy_gettext("The main purpose of this page is just to present my current level to a potential employer and apart the fact I learned a lot by doing them they don't have a deeper meaning.")),

    (lazy_gettext("Sharing is caring"),
     lazy_gettext("Anything here is free to use. "
     "And if you have some question about this page or you have a job offer don't hesitate to ask. "
     "My email is in linkedin profile :-)")),

    (lazy_gettext("Wish you all Wonderful Life..."),
     "9. 9. 2023"),

]

# text = []: seznam na jednotlivé odstavce
# ("Krátce o mě": nadpis odstavce
# "Tyto stránky jsou věnované mé vášni pro python"): text odstavce


#######################################################################################################################
# MAIN-03-2 #
# seznam odkazů pro stránku about:

links = [

    (lazy_gettext("Tutorial by Corey Schafer"),
     'https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH',
     '_blank',
     lazy_gettext("link to Corey Schafer youtube tutorial")),

    (lazy_gettext("Full code description (Czech)"),
     'https://github.com/Sudip2708/poustovnik-rozbor.git',
     '_blank',
     lazy_gettext("code analysis in Czech")),

    (lazy_gettext("Code in readable form (English)"),
     'https://github.com/Sudip2708/poustovnik-english.git',
     '_blank',
     lazy_gettext("code in English transcribed into readable notation")),

    (lazy_gettext("My LinkedIn"),
     'https://www.linkedin.com/in/dalibor-sova-51652b286/',
     '_blank',
     lazy_gettext("link to my LinkedIn")),
]
# links = []: seznam odkazů
# ("Flask Tutorials": popis odkazu
# 'https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH'): odkaz


#######################################################################################################################