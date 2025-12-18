import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import math
from yaml import safe_load

# === UI-SKALIERUNG ===
UI_SCALE = 0.9  # z. B. 0.8 (kleiner), 1.0 (normal), 1.2 (größer)
IMAGE_SCALE = 0.7  # z. B. 0.6 (kleiner), 1.0 (normal), 1.2 (größer)
POPUP_FONT_SCALE = 1.5  # z. B. 1.0 (Standard), 1.2 (größer)
POPUP_IMAGE_SIZE = (int(1200*IMAGE_SCALE), int(800*IMAGE_SCALE))  # Breite x Höhe für Bilder in Popups
POPUP_WIDTH = POPUP_IMAGE_SIZE[0] + 500  # etwas Puffer links/rechts
POPUP_HEIGHT = POPUP_IMAGE_SIZE[1] + int(350 * POPUP_FONT_SCALE)  # für Text und Buttons

class GrossesPreisSpiel:
    def __init__(self, master, yaml_pfad):

        with open(yaml_pfad, "r", encoding="utf-8") as f:
            self.quiz_fragen = safe_load(f)

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
        for col, kategorie in enumerate(self.quiz_fragen.keys()):
            tk.Label(
                self.master,
                text=kategorie,
                font=("Helvetica", int(16 * UI_SCALE), "bold"),
                bg="#f5f5f5",
                fg="#444",
            ).grid(row=3, column=col, padx=int(10 * UI_SCALE), pady=int(10 * UI_SCALE))
            for i, punkte in enumerate(sorted(self.quiz_fragen[kategorie].keys()), start=4):
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
                self.quiz_fragen[kategorie][punkte]["button"] = btn

    def zeige_frage(self, kategorie, punkte):
        if (kategorie, punkte) in self.answered:
            return

        frage_daten = self.quiz_fragen[kategorie][punkte]
        self.answered.add((kategorie, punkte))
        frage_daten["button"].config(state=tk.DISABLED)

        if frage_daten.get("typ") == "kategorie":
            begriffe = frage_daten.get("begriffe")
            thema = frage_daten.get("thema")
            self.zeige_kategorie_frage(frage_daten["frage"], thema, begriffe, punkte)
        else:
            self.zeige_multiple_choice_frage(frage_daten, punkte)

    def zeige_multiple_choice_frage(self, frage_daten, punkte):
        frage = frage_daten["frage"]
        antworten = frage_daten["antworten"]
        korrekt = frage_daten["korrekt"]

        popup = tk.Toplevel(bg="#ffffff")
        popup.title("Frage")
        popup.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}")

        tk.Label(
            popup,
            text=frage,
            wraplength=int(760 * UI_SCALE),
            font=("Helvetica", int(16 * UI_SCALE * POPUP_FONT_SCALE)),
            bg="#ffffff",
            fg="#333",
        ).pack(pady=int(10 * UI_SCALE))

        frage_image = frage_daten.get("frage_image")
        if frage_image:
            try:
                image = Image.open(frage_image)
                image = image.resize(POPUP_IMAGE_SIZE)
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
                    font=("Helvetica", int(12 * UI_SCALE * POPUP_FONT_SCALE)),
                ).pack()

        team_label = tk.Label(
            popup,
            text="",
            font=("Helvetica", int(14 * UI_SCALE * POPUP_FONT_SCALE), "italic"),
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
                font=("Helvetica", int(14 * UI_SCALE * POPUP_FONT_SCALE)),
                width=int(50 * UI_SCALE),
                height=2,
                bg="#f0f0f0",
                command=lambda antw=a: auswahl(antw),
            ).pack(pady=int(5 * UI_SCALE))

        update_team_label()

    def zeige_feedback_popup(self, text, image_path=None):
        popup = tk.Toplevel(bg="#ffffff")
        popup.title("\U0001f389 Feedback")
        popup.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}")

        tk.Label(
            popup,
            text=text,
            wraplength=760,
            font=("Helvetica", int(16 * UI_SCALE * POPUP_FONT_SCALE)),
            bg="#ffffff",
        ).pack(pady=20)

        if image_path:
            try:
                image = Image.open(image_path)
                image = image.resize(POPUP_IMAGE_SIZE)
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
                    font=("Helvetica", int(12 * UI_SCALE * POPUP_FONT_SCALE)),
                ).pack()

        tk.Button(
            popup,
            text="OK",
            font=("Helvetica", int(14 * UI_SCALE * POPUP_FONT_SCALE)),
            bg="#c8e6c9",
            command=popup.destroy,
        ).pack(pady=20)

    def zeige_kategorie_frage(self, frage, thema, begriffe, punkte):
        popup = tk.Toplevel(bg="#ffffff")
        popup.title("Kategoriefrage")
        popup.geometry(f"{POPUP_WIDTH}x{int(300 * POPUP_FONT_SCALE)}")

        tk.Label(
            popup,
            text=frage,
            wraplength=int(680 * UI_SCALE),
            font=("Helvetica", int(16 * UI_SCALE * POPUP_FONT_SCALE)),
            bg="#ffffff",
        ).pack(pady=int(20 * UI_SCALE))

        tk.Label(
            popup,
            text=f"Thema: {thema.replace('_', ' ').title()}",
            fg="gray",
            bg="#ffffff",
            font=("Helvetica", int(12 * UI_SCALE * POPUP_FONT_SCALE)),
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
            font=("Helvetica", int(14 * UI_SCALE * POPUP_FONT_SCALE), "italic"),
            bg="#ffffff",
            fg="#0057a3",
        ).pack(pady=10)

        button_frame = tk.Frame(popup, bg="#ffffff")
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text=f"{aktuelles_team} bekommt {punkte} Punkte",
            font=("Helvetica", int(14 * UI_SCALE * POPUP_FONT_SCALE)),
            bg="#dcedc8",
            command=punkte_geben,
        ).pack(side=tk.LEFT, padx=20)

        tk.Button(
            button_frame,
            text="Keine Punkte",
            font=("Helvetica", int(14 * UI_SCALE * POPUP_FONT_SCALE)),
            bg="#ffcdd2",
            command=keine_punkte,
        ).pack(side=tk.LEFT, padx=20)

    def update_punktestand(self):
        self.punktestand_label.config(text=self.punktestand_text())

    def pruefe_spielende(self):
        total = sum(len(cat) for cat in self.quiz_fragen.values())
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
    app = GrossesPreisSpiel(root, "fragen.yml")
    root.mainloop()
