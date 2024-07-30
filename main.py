import customtkinter as ctk
import json
import os
from tkinter import filedialog, messagebox, simpledialog
from customtkinter import CTkImage, CTkEntry, CTkButton, CTkLabel
from PIL import Image

# Initialiser customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Créer le dossier 'Build' s'il n'existe pas déjà
if not os.path.exists("Build"):
    os.makedirs("Build")

class EldenRingBuildApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Elden Ring Build Manager")
        self.geometry("800x650")
        
        absolute_path_logo = os.path.abspath("src/EldenForge.png")
        # Créez une instance de CTkImage en utilisant les chemins absolus des images
        self.my_logo = ctk.CTkImage(light_image=Image.open(absolute_path_logo), dark_image=Image.open(absolute_path_logo), size=(500, 500))
        self.button_image = ctk.CTkLabel(self, image=self.my_logo, text="")
        self.button_image.pack(pady=5)

        # Boutons pour les différentes actions
        self.create_button = ctk.CTkButton(self, text="Créer un build", command=self.create_build)
        self.create_button.pack(pady=10)
        
        self.view_button = ctk.CTkButton(self, text="Afficher les builds", command=self.view_builds)
        self.view_button.pack(pady=10)
        
        self.import_button = ctk.CTkButton(self, text="Importer un build", command=self.import_build)
        self.import_button.pack(pady=10)

    def create_build(self):
        CreateBuildWindow(self)

    def view_builds(self):
        ViewBuildsWindow(self)

    def import_build(self):
        ImportBuildWindow(self)


class CreateBuildWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Créer un build")
        self.geometry("600x1000")

        self.build_data = {
            "Class": [""],
            "Armor set": [""],
            "Talismans": ["", "", "", ""],
            "Main weapon": [""],
            "Shield": [""],
            "Spells": [""],
            "Off Hand weapon": [""],
            "Crystal tear": ["", ""],
            "Flask spread": [""],
            "Primary stats": [""],
            "Secondary stats": [""],
            "Skills": [""],
            "Great runes": [""]
        }

        # Fonction pour créer un champ
        def create_field(label_text, key, index=0):
            ctk.CTkLabel(self, text=label_text).pack()
            entry = ctk.CTkEntry(self)
            entry.pack()
            if isinstance(self.build_data[key], list):
                self.build_data[key][index] = entry
            else:
                self.build_data[key] = entry

        # Création des champs
        create_field("Class", "Class")
        create_field("Armor set", "Armor set")
        for i in range(4):
            create_field(f"Talisman {i+1}", "Talismans", i)
        create_field("Main weapon", "Main weapon")
        create_field("Shield", "Shield")
        create_field("Spells", "Spells")
        create_field("Off Hand weapon", "Off Hand weapon")
        for i in range(2):
            create_field(f"Crystal tear {i+1}", "Crystal tear", i)
        create_field("Flask spread", "Flask spread")
        create_field("Primary stats", "Primary stats")
        create_field("Secondary stats", "Secondary stats")
        create_field("Skills", "Skills")
        create_field("Great runes", "Great runes")

        ctk.CTkButton(self, text="Enregistrer", command=self.save_build).pack(pady=10)

    def save_build(self):
        build = {
            "Class": self.build_data["Class"][0].get(),
            "Armor set": self.build_data["Armor set"][0].get(),
            "Talismans": [entry.get() for entry in self.build_data["Talismans"]],
            "Main weapon": self.build_data["Main weapon"][0].get(),
            "Shield": self.build_data["Shield"][0].get(),
            "Spells": self.build_data["Spells"][0].get(),
            "Off Hand weapon": self.build_data["Off Hand weapon"][0].get(),
            "Crystal tear": [entry.get() for entry in self.build_data["Crystal tear"]],
            "Flask spread": self.build_data["Flask spread"][0].get(),
            "Primary stats": self.build_data["Primary stats"][0].get(),
            "Secondary stats": self.build_data["Secondary stats"][0].get(),
            "Skills": self.build_data["Skills"][0].get(),
            "Great runes": self.build_data["Great runes"][0].get()
        }

        build_name = simpledialog.askstring("Nom du Build", "Entrez le nom du build:")
        if build_name:
            file_path = os.path.join("Build", f"{build_name}.json")
            with open(file_path, 'w') as file:
                json.dump(build, file)
            messagebox.showinfo("Succès", f"Build enregistré sous le nom {build_name}.json")
        else:
            messagebox.showwarning("Annulé", "Le nom du build ne peut pas être vide.")

        self.destroy()


class ViewBuildsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Afficher les builds")
        self.geometry("600x400")

        # Charger et afficher les builds
        self.builds = self.load_builds()
        if self.builds:
            self.display_builds(self.builds)

    def load_builds(self):
        file = filedialog.askopenfile(mode='r', defaultextension=".json")
        if file:
            builds = json.load(file)
            if isinstance(builds, dict):  # Si le fichier ne contient qu'un seul build
                builds = [builds]
            return builds
        else:
            messagebox.showerror("Erreur", "Aucun fichier sélectionné.")
            return None

    def display_builds(self, builds):
        for build in builds:
            for key, value in build.items():
                if isinstance(value, list):
                    value = ', '.join(value)
                ctk.CTkLabel(self, text=f"{key}: {value}").pack()
            ctk.CTkLabel(self, text="").pack()  # Ajouter une ligne vide pour séparer les builds


class ImportBuildWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Importer un build")
        self.geometry("600x400")

        ctk.CTkLabel(self, text="Sélectionner un fichier JSON pour importer un build").pack(pady=10)
        ctk.CTkButton(self, text="Importer", command=self.import_build).pack(pady=10)

    def import_build(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                build = json.load(file)
                ctk.CTkLabel(self, text=str(build)).pack()


if __name__ == "__main__":
    app = EldenRingBuildApp()
    app.mainloop()
