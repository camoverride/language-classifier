"""
The top 14 languages with the greatest number of articles (with the exception of Waray) were
selected from here: https://en.wikipedia.org/wiki/List_of_Wikipedias

See also: https://www.quora.com/Why-are-there-so-many-articles-in-the-Cebuano-language-on-Wikipedia
"""

LANGUAGE_STATS = [ \
    # Language, code, articles, users
    ("English", "en", 6251473, 40971086),
    ("Cebuano", "ceb", 5525120, 75812),
    ("Swedish", "sv", 3417156, 762664),
    ("German", "de", 2538143, 3642783),
    ("French", "fr", 2300250, 4018582),
    ("Dutch", "nl", 2045761, 1123270),
    ("Russian", "ru", 1699933, 2924014),
    ("Italian", "it", 1674804, 2083500),
    ("Spanish", "es", 1661352, 6122869),
    ("Polish", "pl", 1457390, 1084637),
    ("Vietnamese", "vi", 1261526, 787725),
    ("Japanese", "ja", 1254240, 1751078),
    ("Egyptian Arabic", "arz", 1202137, 146896),
    ("Chinese", "zh", 1177896, 3051388)
    ]

LANGUAGES = [language for (language, _, _, _) in LANGUAGE_STATS]

# Map the language code to the name i.e. {"en": "English", ...}
mapping = {k: v for v, k, _, _ in LANGUAGE_STATS}
