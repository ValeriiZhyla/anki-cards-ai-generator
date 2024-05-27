from generator.config import Config

anki_prompt_preamble = """Ich möchte, dass Sie sich wie ein professioneller Anki-Kartenhersteller verhalten, der in der Lage ist, Anki-Karten aus dem Text zu erstellen, den ich bereitstelle.

Während der Formulierung von Karteninhalten sollten Sie zwei Prinzipien folgen.
1. Minimale Information: Das Lernmaterial sollte einfach, aber umfassend sein, ohne komplexe Details auszulassen.
2. Optimierte Wortwahl: Die Formulierung auf den Karten sollte eine schnelle Auffassung und Reaktion ermöglichen, um die Fehlerquote zu senken und die Konzentration zu erhöhen.

Umgang mit Kontext:
- Karten können mit oder ohne Kontext bereitgestellt werden:
  - Ohne Kontext: Ist kein Kontext gegeben, verwenden Sie geeignete oder selbst erstellte Kontexte.
  - Mit Kontext: Verwenden Sie den bereitgestellten Kontext. Sollte der Kontext die konventionelle Nutzung des Wortes verzerren, ist er zu ignorieren.
- Verschiedene Kontexte sollten in der Karte nicht gemischt werden und nur verwendet werden, wenn sie für den Karteninhalt sinnvoll sind.

Eingabeformat:
- Ich kann ein Wort oder einen Satz ohne Kontext bereitstellen: 
  - WORT: [Zielwort]; KONTEXT: []
Alternativ kann ich ein Wort oder einen Satz mit Kontext bereitstellen:
  - WORT: [Zielwort]; KONTEXT: [Kontext]


Ausgabeanforderungen:
- Unbezogene Sätze ausschließen, wie das "Kartenbeispiel".
- Das Eingabewort darf in der Ausgabe nicht verwendet werden.
- Jede Karte sollte 4-5 Sätze enthalten, die ausschließlich das maskierte Wort oder den Satz erläutern.
- Ihre Ausgabe sollte nur den Text für die Karte enthalten.


Weitere Regeln:
- Es ist sehr wichtig, zwischen Substantiven und Verben zu unterscheiden. Wenn das Wort "die Entscheidung" lautet, sollte die Karte ausschließlich das Substantiv beschreiben und andere Formen nur dann erwähnen, wenn sie sehr oft verwendet werden.
- Du solltest auch die Teilworte vermeiden: Eine Erklärung wie [verschlimmbessern -> Dieses Wort ist eine Zusammensetzung aus "verschlimmern" und "verbessern"] ist sehr schlechte Antwort.
- Auch die Worte die enthalten das Zielwort sollen nicht benutzt werden. Wort "Schusswaffen" in Karte mit dem Zielwort "Waffen" ist nicht akzeptabel.
- Ein Wort sollte nie mit seinem Plural erklärt werden: Eine Erklärung wie [die Einkunft -> Die Pluralform dieses Wortes ist "Einkünfte", die oft in offiziellen oder steuerlichen Kontexten verwendet wird] ist keine gute Antwort.
- Falls ein Wort mit einem falschen Artikel verwendet wird, zum Beispiel "die Mädchen" statt "das Mädchen", solltest du in deinem Text dennoch den korrekten Artikel verwenden.


Regeln für das Maskieren:
- Das Zielwort wird mit Unterstrichen maskiert, wobei Leerzeichen zwischen Wörtern erhalten bleiben (z.B. wird "freier Wille" zu "_____ _____").
- Die Anzahl der Unterstriche sollte der Anzahl der Buchstaben entsprechen ("Erlösung" wird zu "________").
- Sie sollten nur das Wort maskieren, nicht den Kontext. Zum Beispiel, wenn das Wort 'Grafikkarte' lautet und der Kontext ein 'Rechner' ist, dann sollte die Karte nur 'Grafikkarte' erklären und maskieren, nicht 'Rechner'."


"""


def examples() -> str:
    examples_preamble = """
    Hier sind die Beispiele im Format
    WORD: [Zielwort]; CONTEXT: [Kontext (optional)]; RESULT: [was ich als Ausgabe erwarte]
    """

    anki_examples = {"verschlimmbessern": ["", "Wenn man eine Situation durch Versuche der Verbesserung tatsächlich verschlechtert, hat man sie ________________t"
                                               "Ein Beispiel könnte sein, wenn man ein Gerät reparieren möchte, aber es danach schlechter funktioniert als vorher. "
                                               "Oft wird dieser Begriff humorvoll oder ironisch verwendet, um fehlgeschlagene Bemühungen zu beschreiben. "],
                     "die Einkunft": ["", "Unter ________ versteht man den Geldbetrag, den jemand regelmäßig erhält, oft aus Arbeit, Geschäften oder Vermögenswerten. "
                                          "Diese kann aus verschiedenen Quellen stammen, wie Löhnen, Mieten, Zinsen oder Dividenden.  "
                                          "In der Buchhaltung wird die ________ als Maß für den finanziellen Zugewinn einer Person oder Organisation gesehen. "],
                     "der Alptraum": ["", "Der ________ ist ein besonders beängstigender oder stressiger Traum. "
                                          "Dieser Begriff kann auch metaphorisch verwendet werden, um eine sehr unangenehme oder schwierige Situation zu beschreiben. "
                                          "Im mittelalterlichen Glauben bezog sich ________ auf einen Dämon, der nachts auf der Brust der Schlafenden saß. "
                                          "Kinder und Erwachsene können einen ________ erleben, oft ausgelöst durch Stress oder Angst. "],
                     "die Steuererklärung": ["",
                                             "Eine _______________ ist ein offizielles Dokument, das an das Finanzamt gesendet wird, um Einkommen, Ausgaben und andere steuerrelevante Informationen eines Jahres zu melden. "
                                             "Durch das Einreichen einer _______________ kann eine Person oder Firma ihre zu zahlenden Steuern berechnen oder eine Rückerstattung für zu viel gezahlte Beträge erhalten. "
                                             "Die Abgabe der _______________ muss bis zu einem bestimmten Datum erfolgen, um Strafen oder Verzögerungen bei der Rückerstattung zu vermeiden. "
                                             "In vielen Ländern ist die elektronische Übermittlung der _______________ durch Online-Steuerdienste möglich, was den Prozess vereinfacht und beschleunigt. "
                                             "Durch die _______________ kann der Staat Einnahmen generieren, die zur Finanzierung öffentlicher Dienstleistungen und Infrastruktur verwendet werden. "],
                     "Waffen": ["", "________ sind Werkzeuge oder Geräte, die entwickelt wurden, um Schaden zu verursachen oder Gegner zu besiegen. "
                                    "Sie können in verschiedenen Formen auftreten. "
                                    "In Kriegszeiten spielt die Produktion von ________ eine entscheidende Rolle für die militärische Stärke eines Landes. "
                                    "Die Herstellung und der Handel von ________ unterliegen oft strengen gesetzlichen Kontrollen und internationalen Abkommen."]
                     }

    anki_examples_strings = [f"WORD: [{word}]; CONTEXT: [{anki_examples[word][0]}]; RESULT:[{anki_examples[word][1]}]\n" for word in anki_examples.keys()]
    return examples_preamble + ''.join(anki_examples_strings)


def rule_language_level() -> str:
    return f"""
    Sprachniveau:
    - Eine Person mit Sprachniveau [{Config.LEVEL}] sollte die Karte verstehen. 
    - Wörter und Konstruktionen, die einer Person mit diesem Niveau vertraut sein sollten.
    - Falls die Sprachniveau C1 oder C2 gesetzt wird, verwende Wörter und Konstruktionen deiner Wahl.
    """


def get_prompt() -> str:
    return anki_prompt_preamble + rule_language_level() + examples()
