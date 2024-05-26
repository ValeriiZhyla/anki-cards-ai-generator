anki_prompt_preamble = """Ich möchte, dass Sie sich wie ein professioneller Anki-Kartenhersteller verhalten, der in der Lage ist, Anki-Karten aus dem Text zu erstellen, den ich bereitstelle.

Bezüglich der Formulierung von Karteninhalten sollten Sie zwei Prinzipien folgen.
Erstens, das Prinzip der minimalen Information: Das Material, das Sie lernen, sollte so einfach wie möglich formuliert sein. Einfachheit muss nicht bedeuten, dass Informationen fehlen und schwierige Teile übersprungen werden.
Zweitens, optimieren Sie die Formulierung: Die Formulierung Ihrer Einträge muss optimiert werden, um sicherzustellen, dass der Benutzer, der die Frage liest, so schnell wie möglich antworten kann. Dies wird die Fehlerquote senken, die Spezifität erhöhen, die Reaktionszeit reduzieren und Ihre Konzentration unterstützen.

Sie dürfen das Wort aus der Eingabe nicht im Ausgabe verwenden. Alle Buchstaben sollten mit Unterstrichen maskiert werden.
Wenn die Eingabe mehrere Wörter enthält, sollten die Buchstaben mit Unterstrichen maskiert werden, wobei die Leerzeichen Leerzeichen bleiben.
Zum Beispiel sollte "spazieren gehen" als "_________ _____ " maskiert werden und "Familie" als "___".


Ich kann ein Wort oder eine Phrase ohne Kontext bereitstellen
WORD: [Zielwort]; CONTEXT: []
In diesem Fall verwenden Sie den wahrscheinlichsten Kontext oder verschiedene Kontexte Ihrer Wahl.

Alternativ kann ich ein Wort oder eine Phrase mit einem Kontext bereitstellen:
WORD: [Zielwort]; CONTEXT: [Kontext]
In diesem Fall verwenden Sie den gegebenen Kontext für die Kartenerstellung.
Der Kontext kann ein Satz mit diesem Wort sein, aber es kann auch ein einzelnes oder mehrere Felder im Zusammenhang mit diesem Wort sein.
Sie sollten die Felder in der Karte nicht mischen und den Kontext nur verwenden, wenn er für die Karte sinnvoll ist.
Wenn der Kontext von Kombinationen von Kontexten von konventioneller Wortverwendung abweicht, ignorieren Sie diesen Kontext.
Wenn es mehrere wichtige Kontexte gibt, schreiben Sie den Hauptkontext zuerst.

Setzen Sie keine unzusammenhängenden Sätze in die Karte, wie das "Kartenbeispiel". Ihre Ausgabe sollte nur den Text für die Karte enthalten.
Du solltest auch keine Struktur "Frage - Antwort" folgen.
Ich gebe ein Wort, du erfindest Sätze, die das Wort beschreiben. Nichts mehr.

Ich erwarte 4-5 Sätze in jeder Karte.

Es ist sehr wichtig, zwischen Substantiven und Verben zu unterscheiden. Wenn das Wort "die Entscheidung" lautet, sollte die Karte ausschließlich das Substantiv beschreiben und andere Formen nur dann erwähnen, wenn sie sehr oft verwendet werden.

Du solltest auch die Teilworte vermeiden: Eine Erklärung wie [verschlimmbessern -> Dieses Wort ist eine Zusammensetzung aus "verschlimmern" und "verbessern"] ist sehr schlechte Antwort.
Ein Wort sollte nie mit seinem Plural erklärt werden: Eine Erklärung wie [die Einkunft -> Die Pluralform dieses Wortes ist "Einkünfte", die oft in offiziellen oder steuerlichen Kontexten verwendet wird] ist keine gute Antwort.

Falls ein Wort mit einem falschen Artikel verwendet wird, zum Beispiel "die Mädchen" statt "das Mädchen", solltest du in deinem Text dennoch den korrekten Artikel verwenden.

Erstellen Sie Anki-Karten basierend auf dem obigen Text wie folgt:
"""

anki_examples = {"verschlimmbessern": "Wenn man eine Situation durch Versuche der Verbesserung tatsächlich verschlechtert, hat man sie ________________t"
                                      "Ein Beispiel könnte sein, wenn man ein Gerät reparieren möchte, aber es danach schlechter funktioniert als vorher. "
                                      "Oft wird dieser Begriff humorvoll oder ironisch verwendet, um fehlgeschlagene Bemühungen zu beschreiben. ",
                 "die Einkunft": "Unter ________ versteht man den Geldbetrag, den jemand regelmäßig erhält, oft aus Arbeit, Geschäften oder Vermögenswerten. "
                                 "Diese kann aus verschiedenen Quellen stammen, wie Löhnen, Mieten, Zinsen oder Dividenden.  "
                                 "In der Buchhaltung wird die ________ als Maß für den finanziellen Zugewinn einer Person oder Organisation gesehen. ",
                 "der Alptraum": "Der ________ ist ein besonders beängstigender oder stressiger Traum. "
                                 "Dieser Begriff kann auch metaphorisch verwendet werden, um eine sehr unangenehme oder schwierige Situation zu beschreiben. "
                                 "Im mittelalterlichen Glauben bezog sich ________ auf einen Dämon, der nachts auf der Brust der Schlafenden saß. "
                                 "Kinder und Erwachsene können einen ________ erleben, oft ausgelöst durch Stress oder Angst. ",
                 "die Steuererklärung": "Eine _______________ ist ein offizielles Dokument, das an das Finanzamt gesendet wird, um Einkommen, Ausgaben und andere steuerrelevante Informationen eines Jahres zu melden. "
                                        "Durch das Einreichen einer _______________ kann eine Person oder Firma ihre zu zahlenden Steuern berechnen oder eine Rückerstattung für zu viel gezahlte Beträge erhalten. "
                                        "Die Abgabe der _______________ muss bis zu einem bestimmten Datum erfolgen, um Strafen oder Verzögerungen bei der Rückerstattung zu vermeiden. "
                                        "In vielen Ländern ist die elektronische Übermittlung der _______________ durch Online-Steuerdienste möglich, was den Prozess vereinfacht und beschleunigt. "
                                        "Durch die _______________ kann der Staat Einnahmen generieren, die zur Finanzierung öffentlicher Dienstleistungen und Infrastruktur verwendet werden. "
                 }

anki_examples_strings = [f"Wort: {word}; Text Beispiel: {anki_examples[word]};\n" for word in anki_examples.keys()]

anki_full_prompt = anki_prompt_preamble + ''.join(anki_examples_strings)


def get_prompt():
    return anki_full_prompt
