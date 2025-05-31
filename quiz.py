import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import math

# === UI-SKALIERUNG ===
UI_SCALE = 0.9  # z. B. 0.8 (kleiner), 1.0 (normal), 1.2 (größer)

# Daten einfügen
quiz_fragen = {
    "Baden-Württemberg": {
        10: {
            "frage": "Wie viel kostet ein Erwachsenenticket im Europapark?",
            "antworten": ["63", "45", "72", "52"],
            "korrekt": "52"
        },
        20: {
            "frage": "Wann wurde BW gegründet?",
            "antworten": ["1736", "1952", "1922", "1872"],
            "korrekt": "1952"
        },
        30: {
            "frage": "Wäre BW ein eigener Staat, nähme das Land unter den 27 Mitgliedstaaten der Europäischen Union der Einwohnerzahl nach den wievielten Platz ein?",
            "antworten": ["13.", "9.", "20.", "24."],
            "korrekt": "9.",
        },
        40: {
            "frage": "Mit 1,493m ist der Feldberg die höchste Erhebung BW, aber wo liegt der niedrigste Punkt?",
            "antworten": ["Karlsruhe", "Mannheim", "Kirchheim", "Kehl"],
            "korrekt": "Mannheim"
        },
        50: {
            "frage": "Wo steht dieses Denkmal?",
            "antworten": ["Lörrach", "xx", "xx", "xx"],
            "korrekt": "Lörrach",
            "frage_image": "bilder/bw50.jpeg",
        }
    },
    "Kategorie": {
        10: {
            "frage": "Nenne reihum Synonyme für Geld",
            "typ": "kategorie",
            "thema": "synonyme_geld"
        },
        20: {
            "frage": "Nenne reihum EU Länder",
            "typ": "kategorie",
            "thema": "europaeische_laender"
        },
        30: {
            "frage": "Nenne reihum deutsche Supermärkte",
            "typ": "kategorie",
            "thema": "supermärkte"
        },
        40: {
            "frage": "Nenne reihum Politiker:innen der jetzigen Regierung",
            "typ": "kategorie",
            "thema": "europaeische_laender"
        },
        50: {
            "frage": "Nenne reihum griechische Buchstaben",
            "typ": "kategorie",
            "thema": "griechische_buchstaben"
        }
    },
    "Rund um die Welt": {
        10: {
            "frage": "Italien und Eiscreme sind untrennbar miteinander verbunden. Aber wo wurde Eiscreme eigentlich erfunden?",
            "antworten": ["Irak", "Griechenland", "Italien", "China"],
            "korrekt": "China"
        },
        20: {
            "frage": "An wie viele Länder grenzt Bulgarien?",
            "antworten": ["3", "12", "8", "5"],
            "korrekt": "5"
        },
        30: {
            "frage": "Vatikanstadt, Monaco, Nauru und Tuvalu gehören zu den 5 kleinsten Ländern. Welches Land gehört auch dazu?",
            "antworten": ["Malta", "Palau", "San Marino", "Andorra"],
            "korrekt": "San Marino"
        },
        40: {
            "frage": "Ferdinand Magellan war ein Seefahrer im 16. Jahrhundert, der für die erste dokumentierte Weltumsegelung bekannt ist. Für welche Musikrichtung ist heute seine Heimat bekannt?",
            "antworten": ["Fado", "Regggae", "Flamenco", "Liscio"],
            "korrekt": "Fado"
        },
        50: {
            "frage": "Wo kann man Affen so beim entspannen vorfinden? ",
            "antworten": ["Japan", "Russland", "UK", "Vietnam"],
            "korrekt": "Japan",
            "frage_image": "bilder/welt50.jpeg",
        }
    },
     "Musik": {
        10: {
            "frage": "Wer trug den Beinamen „Walzerkönig“?",
            "antworten": ["Johann Baptist Strauss", "Frédéric Chopin", "Friedrich Merz", "Wolfgang Amadeus Mozart"],
            "korrekt": "Johann Baptist Strauss"
        },
        20: {
            "frage": "Wie heißt das letzte Album von den Beatles?",
            "antworten": ["Yellow Submarine", "Let it be", "Abby Road", "The BEATLES"],
            "korrekt": "Let it be"
        },
        30: {
            "frage": "Was ist laut popkultur.de das meistverkaufte Album in Deutschland?",
            "antworten": ["Dirty Dancing - verschiedene Interpreten", "ABBA Gold - ABBA", "Mensch - Herbert Grönemeyer", "Jazz ist anders - Die Ärzte"],
            "korrekt": "Dirty Dancing - verschiedene Interpreten"
        },
        40: {
            "frage": "Wie viele Pfeifen hat die Orgel mit den meisten Pfeifen der Welt?",
            "antworten": ["19,001", "8,093", "11,753", "33,112"],
            "korrekt": "33,112",
        },
        50: {
            "frage": "Welches dieser Instrumente ist ein Blasinstrument?",
            "antworten": ["Okarina", "Ukele", "Balalaika", "Bandoneon"],
            "korrekt": "Okarina"
        }
    },
    "Dialekte": {
        10: {
            "frage": "In welcher deutschen Stadt wird laut Forsa-Umfrage am wenigsten Dialekt gesprochen?",
            "antworten": ["Berlin", "Hannover", "Karlsruhe", "Bielefeld"],
            "korrekt": "Hannover"
        },
        20: {
            "frage": "Was bedeutet das bayrische Wort „Grattler“??",
            "antworten": ["Ein gezapftes Bier, bei dem mehr Schaum als Flüssigkeit im Glas ist", "Ein ungepflegter, arbeitsscheuer Kerl", "Ein Rechen", "Zuckerrüben"],
            "korrekt": "Ein ungepflegter, arbeitsscheuer Kerl"
        },
        30: {
            "frage": "Was bedeutet das sächsische Wort „Abfedd´n“ ?",
            "antworten": ["Sich betrinken", "Sich schlafen legen", "Geld abknöpfen", "Abhauen"],
            "korrekt": "Geld abknöpfen"
        },
        40: {
            "frage": "xxx",
            "antworten": ["19,001", "8,093", "11,753", "33,112"],
            "korrekt": "33,112"
        },
        50: {
            "frage": "xxx",
            "antworten": ["Okarina", "Ukele", "Balalaika", "Bandoneon"],
            "korrekt": "Okarina"
        }
    },
    "Wer wird Millionär": {
        10: {
            "frage": "Hab ich das Geld für eine Anschaffung nicht auf der hohen Kante, bleibt die Möglichkeit, dass ich auf ...?",
            "antworten": ["Teil zahlung", "Kredit geschäft", "Hypo thek", "Raten kauf"],
            "korrekt": "Raten kauf"
        },
        20: {
            "frage": "Was sehen ihre über 4,5 Millionen Instagram-Follower:innen sozusagen, wenn Mode- und Fitness-Influencerin Caro live beim Sport streamt?",
            "antworten": ["Daurlauf", "Wandrung", "Spazirgang", "Abstechr"],
            "korrekt": "Daurlauf"
        },
        30: {
            "frage": "Was durften Männer ihren Ehefrauen in Deutschland bis 1977 (rechtlich) verbieten??",
            "antworten": ["Autofahren", "Arbeiten", "Wählen gehen", "Rauchen"],
            "korrekt": "Arbeiten"
        },
        40: {
            "frage": "Welches war 2024 mit ca. 300.000 Einheiten das meistverkaufte Auto in Europa - davon aber nur ein winziger Bruchteil im Heimatland?",
            "antworten": ["Peugeot 208", "Hyundai Tucson", "VW golf", "Dacia Sandero"],
            "korrekt": "Dacia Sandero"
        },
        50: {
            "frage": "Rigoberta Menchú Friedensnobelpreisträgerin von 1992 kandidierte einst für das Präsidentenamt in welchem Land?",
            "antworten": ["Honduras", "Kolumbien", "Guatemala", "Mexiko"],
            "korrekt": "Guatemala"
        }
    }
}

kategorie_begriffe = {
    "europaeische_laender": [
        "deutschland", "frankreich", "italien", "spanien", "portugal", "bulgarien", "dänemark", "estland", "irland", "kroatien",
         "rumänien", "polen", "niederlande", "österreich", "belgien", "griechenland", "ungarn", "schweden", "finnland",
         "lettland", "litauen", "luxemburg", "malta", "slowakai", "slowenien" , "tschechien", "zypern"
    ],
    "politiker": [
        "merz", "klingbeil", "dobrindt", "wadephul", "pistorius", "reiche", "bär", "hubig",
        "prien", "bas", "wildberger", "schnieder", "schneider", "warken", "rainer", "alabali-radovan", "hubertz", "frei"
    ],
    "griechische_buchstaben": [
        "alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", "iota", "kappa", "lambda",
        "mu", "nu", "xi", "omicron", "pi", "rho", "sigma", "tau", "upsilon", "phi", "chi", "psi", "omega"
    ],
    "supermärkte": [
        "aldi", "familia", "combi", "hit", "diska", "edeka", "marktkauf", "nahundgut",
        "netto", "np", "globus", "tegut", "norma", "nahkauf", "penny", "rewe", "kaufland", "lidl", "spar"
    ],
    "synonyme_geld": [
        "banknoten", "münzen", "scheine", "zahoungsmittel", "bims", "flocken", "flöhe", "kies", "knete", "kohle",
        "kröten", "lappen", "marie", "mäuse", "moos", "peseten", "piepen", "pulver", "schotter", "steine", "strom", "zaster", 
        "koks", "bimbes", "mammon", "asche", "bares", "eier", "heu", "knöpfe", "moneten", "penunze", "pinke", "schluse"
        ],
}

class GrossesPreisSpiel:
    def __init__(self, master):
        self.master = master
        self.master.title("\U0001f393 Der Große Preis")

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.master.geometry(f"{int(screen_width * 0.95)}x{int(screen_height * 0.95)}")
        self.master.configure(bg="#f5f5f5")

        self.teams = self.frage_nach_teamnamen()
        self.punktestand = {team: 0 for team in self.teams}
        self.aktuelles_team_index = 0
        self.answered = set()

        tk.Label(
            master,
            text="Der Große Preis",
            font=("Helvetica", int(32 * UI_SCALE), "bold"),
            bg="#f5f5f5",
            fg="#333",
        ).grid(row=0, column=0, columnspan=10, pady=(int(20 * UI_SCALE), 0))

        self.punktestand_label = tk.Label(
            master,
            text=self.punktestand_text(),
            font=("Helvetica", int(18 * UI_SCALE)),
            bg="#f5f5f5",
            fg="#222",
        )
        self.punktestand_label.grid(
            row=1, column=0, columnspan=10, pady=(5, int(10 * UI_SCALE))
        )

        self.team_label = tk.Label(
            master,
            text=self.aktuelles_team_text(),
            font=("Helvetica", int(18 * UI_SCALE), "italic"),
            bg="#f5f5f5",
            fg="#0057a3",
        )
        self.team_label.grid(
            row=2, column=0, columnspan=10, pady=(0, int(20 * UI_SCALE))
        )

        self.create_board()

    def punktestand_text(self):
        return " | ".join(
            f"{team}: {punkte} Punkte" for team, punkte in self.punktestand.items()
        )

    def aktuelles_team_text(self):
        return f"\U0001f3af Am Zug: {self.teams[self.aktuelles_team_index]}"

    def next_team(self):
        self.aktuelles_team_index = (self.aktuelles_team_index + 1) % len(self.teams)
        self.team_label.config(text=self.aktuelles_team_text())

    def create_board(self):
        for col, kategorie in enumerate(quiz_fragen.keys()):
            tk.Label(
                self.master,
                text=kategorie,
                font=("Helvetica", int(16 * UI_SCALE), "bold"),
                bg="#f5f5f5",
                fg="#444",
            ).grid(row=3, column=col, padx=int(10 * UI_SCALE), pady=int(10 * UI_SCALE))
            for i, punkte in enumerate(sorted(quiz_fragen[kategorie].keys()), start=4):
                btn = tk.Button(
                    self.master,
                    text=f"{punkte} Punkte",
                    font=("Helvetica", int(16 * UI_SCALE), "bold"),
                    command=lambda c=kategorie, p=punkte: self.zeige_frage(c, p),
                    width=int(20 * UI_SCALE),
                    height=int(4 * UI_SCALE),
                    bg="#e0e0e0",
                    activebackground="#c8e6c9",
                )
                btn.grid(
                    row=i, column=col, padx=int(10 * UI_SCALE), pady=int(10 * UI_SCALE)
                )
                quiz_fragen[kategorie][punkte]["button"] = btn

    def zeige_frage(self, kategorie, punkte):
        if (kategorie, punkte) in self.answered:
            return

        frage_daten = quiz_fragen[kategorie][punkte]
        self.answered.add((kategorie, punkte))
        frage_daten["button"].config(state=tk.DISABLED)

        if frage_daten.get("typ") == "kategorie":
            thema = frage_daten["thema"]
            begriffe = kategorie_begriffe.get(thema, [])
            self.zeige_kategorie_frage(frage_daten["frage"], thema, begriffe, punkte)
        else:
            self.zeige_multiple_choice_frage(frage_daten, punkte)

    def zeige_multiple_choice_frage(self, frage_daten, punkte):
        frage = frage_daten["frage"]
        antworten = frage_daten["antworten"]
        korrekt = frage_daten["korrekt"]

        popup = tk.Toplevel(bg="#ffffff")
        popup.title("Frage")
        popup.geometry(f"{int(800 * UI_SCALE)}x{int(600 * UI_SCALE)}")

        tk.Label(
            popup,
            text=frage,
            wraplength=int(760 * UI_SCALE),
            font=("Helvetica", int(16 * UI_SCALE)),
            bg="#ffffff",
            fg="#333",
        ).pack(pady=int(10 * UI_SCALE))

        frage_image = frage_daten.get("frage_image")
        if frage_image:
            try:
                image = Image.open(frage_image)
                image = image.resize((400, 250))
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(popup, image=photo, bg="#ffffff")
                image_label.image = photo
                image_label.pack(pady=(0, 10))
            except Exception as e:
                tk.Label(
                    popup,
                    text=f"[Bild konnte nicht geladen werden: {e}]",
                    fg="red",
                    bg="#ffffff",
                ).pack()

        team_label = tk.Label(
            popup,
            text="",
            font=("Helvetica", int(14 * UI_SCALE), "italic"),
            bg="#ffffff",
            fg="#0057a3",
        )
        team_label.pack(pady=(0, int(10 * UI_SCALE)))

        versuchs_index = 0
        fragestart_index = self.aktuelles_team_index
        versuchsreihenfolge = [
            self.teams[(fragestart_index + i) % len(self.teams)]
            for i in range(len(self.teams))
        ]

        def update_team_label():
            team_label.config(text=f"{versuchsreihenfolge[versuchs_index]} ist dran")

        def auswahl(antwort):
            nonlocal versuchs_index
            aktuelles_team = versuchsreihenfolge[versuchs_index]

            if antwort == korrekt:
                multiplikator = 1 / (versuchs_index + 1)
                punkte_fuer_team = math.ceil(punkte * multiplikator)
                self.punktestand[aktuelles_team] += punkte_fuer_team
                self.update_punktestand()

                feedback_text = frage_daten.get(
                    "feedback_text",
                    f"{aktuelles_team} bekommt {punkte_fuer_team} Punkte!",
                )
                feedback_image = frage_daten.get("feedback_image", None)
                self.zeige_feedback_popup(feedback_text, feedback_image)

                popup.destroy()
                self.aktuelles_team_index = (fragestart_index + 1) % len(self.teams)
                self.team_label.config(text=self.aktuelles_team_text())
                self.pruefe_spielende()
            else:
                versuchs_index += 1
                if versuchs_index >= len(versuchsreihenfolge):
                    messagebox.showinfo(
                        "Kein Treffer",
                        f"Niemand hat richtig geantwortet. Lösung: {korrekt}",
                    )
                    popup.destroy()
                    self.aktuelles_team_index = (fragestart_index + 1) % len(self.teams)
                    self.team_label.config(text=self.aktuelles_team_text())
                    self.pruefe_spielende()
                else:
                    update_team_label()

        for a in antworten:
            tk.Button(
                popup,
                text=a,
                font=("Helvetica", int(14 * UI_SCALE)),
                width=int(50 * UI_SCALE),
                height=2,
                bg="#f0f0f0",
                command=lambda antw=a: auswahl(antw),
            ).pack(pady=int(5 * UI_SCALE))

        update_team_label()

    def zeige_feedback_popup(self, text, image_path=None):
        popup = tk.Toplevel(bg="#ffffff")
        popup.title("\U0001f389 Feedback")
        popup.geometry(f"{int(800 * UI_SCALE)}x{int(500 * UI_SCALE)}")

        tk.Label(
            popup,
            text=text,
            wraplength=760,
            font=("Helvetica", int(16 * UI_SCALE)),
            bg="#ffffff",
        ).pack(pady=20)

        if image_path:
            try:
                image = Image.open(image_path)
                image = image.resize((400, 300))
                photo = ImageTk.PhotoImage(image)
                label = tk.Label(popup, image=photo, bg="#ffffff")
                label.image = photo
                label.pack(pady=10)
            except Exception as e:
                tk.Label(
                    popup,
                    text=f"[Bild konnte nicht geladen werden: {e}]",
                    bg="#ffffff",
                    fg="red",
                ).pack()

        tk.Button(
            popup,
            text="OK",
            font=("Helvetica", int(14 * UI_SCALE)),
            bg="#c8e6c9",
            command=popup.destroy,
        ).pack(pady=20)

    def zeige_kategorie_frage(self, frage, thema, begriffe, punkte):
        popup = tk.Toplevel(bg="#ffffff")
        popup.title("Kategoriefrage")
        popup.geometry(f"{int(700 * UI_SCALE)}x{int(350 * UI_SCALE)}")

        tk.Label(
            popup,
            text=frage,
            wraplength=int(680 * UI_SCALE),
            font=("Helvetica", int(16 * UI_SCALE)),
            bg="#ffffff",
        ).pack(pady=int(20 * UI_SCALE))

        tk.Label(
            popup,
            text=f"Thema: {thema.replace('_', ' ').title()}",
            fg="gray",
            bg="#ffffff",
            font=("Helvetica", int(12 * UI_SCALE)),
        ).pack()

        aktuelles_team = self.teams[self.aktuelles_team_index]

        def punkte_geben():
            self.punktestand[aktuelles_team] += punkte
            self.update_punktestand()
            popup.destroy()
            self.next_team()
            self.pruefe_spielende()

        def keine_punkte():
            popup.destroy()
            self.next_team()
            self.pruefe_spielende()

        tk.Label(
            popup,
            text=f"{aktuelles_team} ist dran",
            font=("Helvetica", int(14 * UI_SCALE), "italic"),
            bg="#ffffff",
            fg="#0057a3",
        ).pack(pady=10)

        button_frame = tk.Frame(popup, bg="#ffffff")
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text=f"{aktuelles_team} bekommt {punkte} Punkte",
            font=("Helvetica", int(14 * UI_SCALE)),
            bg="#dcedc8",
            command=punkte_geben,
        ).pack(side=tk.LEFT, padx=20)

        tk.Button(
            button_frame,
            text="Keine Punkte",
            font=("Helvetica", int(14 * UI_SCALE)),
            bg="#ffcdd2",
            command=keine_punkte,
        ).pack(side=tk.LEFT, padx=20)

    def update_punktestand(self):
        self.punktestand_label.config(text=self.punktestand_text())

    def pruefe_spielende(self):
        total = sum(len(cat) for cat in quiz_fragen.values())
        if len(self.answered) == total:
            gewinner = max(self.punktestand, key=self.punktestand.get)
            messagebox.showinfo(
                "\U0001f3c1 Spiel beendet",
                f"Alle Fragen beantwortet!\n\nEndstand:\n{self.punktestand_text()}\n\n\U0001f3c6 Gewinner: {gewinner}",
            )
            self.master.quit()

    def frage_nach_teamnamen(self):
        popup = tk.Toplevel()
        popup.title("Teamnamen eingeben")
        popup.geometry("400x300")
        popup.grab_set()

        tk.Label(popup, text="Bitte gebt eure Teamnamen ein:", font=("Helvetica", 14)).pack(pady=10)

        entries = []
        for i in range(3):
            tk.Label(popup, text=f"Team {i+1}:", font=("Helvetica", 12)).pack()
            entry = tk.Entry(popup, font=("Helvetica", 12))
            entry.insert(0, f"Team {chr(65+i)}")
            entry.pack(pady=5)
            entries.append(entry)

        teamnamen = []

        def speichern():
            for e in entries:
                name = e.get().strip()
                if not name:
                    messagebox.showerror("Fehler", "Alle Teamnamen müssen ausgefüllt sein.")
                    return
                teamnamen.append(name)
            popup.destroy()

        tk.Button(popup, text="Weiter", command=speichern, font=("Helvetica", 12)).pack(pady=20)

        popup.wait_window()
        return teamnamen


if __name__ == "__main__":
    root = tk.Tk()
    app = GrossesPreisSpiel(root)
    root.mainloop()
