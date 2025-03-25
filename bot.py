import asyncio
import unicodedata
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from gtts import gTTS
from playsound import playsound
import os
import json

USERNAME = "songzz.vfr"

user_points = {}

def load_questions():
    try:
        with open("questions.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

questions_and_answers = load_questions()

current_question_index = 0
waiting_for_answer = False
current_expected_answer = ""
already_answered = False
winner_of_the_question = None

def normalize_text(text):
    text = text.strip().lower()
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    return text

client = TikTokLiveClient(unique_id=USERNAME)

def speak_text(text):
    try:
        tts = gTTS(text=text, lang='fr')
        temp_file = "temp.mp3"
        tts.save(temp_file)
        playsound(temp_file)
        os.remove(temp_file)
    except Exception as e:
        print("Erreur lors de la lecture audio :", e)

async def game_loop():
    global current_question_index, waiting_for_answer, current_expected_answer, already_answered, questions_and_answers, winner_of_the_question

    while current_question_index < len(questions_and_answers):
        question = questions_and_answers[current_question_index]["question"]
        expected_answer = questions_and_answers[current_question_index]["answer"]
        current_expected_answer = normalize_text(expected_answer)
        waiting_for_answer = True
        already_answered = False
        winner_of_the_question = None

        question_text = f"❓ Question {current_question_index + 1} : {question}"
        update_question_display(question_text)
        print(f"\n{question_text}")

        speak_text(f"Question {current_question_index + 1}. {question}")
        await asyncio.sleep(20)

        if not already_answered:
            message = f"La réponse est : {expected_answer}. Personne n'a trouvé la bonne réponse."
            update_question_display(message)
            print(message)
            speak_text(f"La réponse est : {expected_answer}. Personne n'a trouvé la bonne réponse.")


        current_question_index += 1
        await asyncio.sleep(2)

        questions_and_answers = load_questions()
        display_scores()

    update_question_display("✅ Le quiz est terminé ! Voici le classement final :")
    display_scores()
    speak_text("Le quiz est terminé ! Voici le classement final.")

def display_scores():
    if not user_points:
        classement_text.config(state='normal')
        classement_text.delete(1.0, tk.END)
        classement_text.insert(tk.END, "Aucun point marqué !")
        classement_text.config(state='disabled')
    else:
        classement = sorted(user_points.items(), key=lambda x: x[1], reverse=True)
        classement_text.config(state='normal')
        classement_text.delete(1.0, tk.END)
        classement_text.insert(tk.END, "🏆 Classement en direct :\n\n")
        for user, points in classement:
            classement_text.insert(tk.END, f"{user} : {points} point(s)\n")
        classement_text.config(state='disabled')

def update_question_display(message):
    question_label.config(text=message)

@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    global waiting_for_answer, already_answered, winner_of_the_question

    user = event.user.nickname
    comment = normalize_text(event.comment)

    print(f"{user} a répondu : {event.comment}")

    if waiting_for_answer:
        if comment == current_expected_answer:
            if not already_answered:
                user_points[user] = user_points.get(user, 0) + 1
                already_answered = True
                winner_of_the_question = user

                message = f"🎉 Bravo {user} + 1 point ! Total : {user_points[user]}"
                print(message)
                update_question_display(message)
                speak_text(f"Bravo {user}, bonne réponse ! Tu gagnes 1 point.")

                display_scores()
            else:
                print(f"{user} a aussi trouvé la bonne réponse, mais trop tard !")
        else:
            print(f"{user} a donné une mauvaise réponse.")

# === Initialisation de Tkinter ===
root = tk.Tk()
root.title("Quiz Time TikTok")
root.geometry("1080x1920")
root.configure(bg="#008000")

# === Nouveau fond ===
# === Pas besoin de charger une image ===
canvas = tk.Canvas(root, width=1080, height=1920, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# === Crée un fond en dégradé simulé (simple avec une couleur unie par exemple) ===
canvas.create_rectangle(0, 0, 1080, 1920, fill="#008000", outline="")

# Tu peux jouer avec la couleur, voici d'autres couleurs stylées :
# Bleu nuit : "#0f172a"
# Violet néon : "#7c3aed"
# Rose flashy : "#ec4899"


# === Styles ===
font_title = ("Helvetica", 36, "bold")
font_text = ("Helvetica", 28)
text_color = "#ffffff"

# === Zone de question ===
question_frame = tk.Frame(root, bg="#008000", bd=5, relief="ridge")
question_frame.place(relx=0.5, y=150, anchor="center", width=900, height=160)

question_label = tk.Label(
    question_frame,
    text="En attente de la prochaine question...",
    font=font_title,
    fg=text_color,
    bg="#008000",
    wraplength=850,
    justify="center"
)
question_label.pack(expand=True, fill="both", padx=10, pady=10)

# === Zone de classement ===
classement_frame = tk.Frame(root, bg="#008000", bd=5, relief="ridge")
classement_frame.place(relx=0.5, rely=0.7, anchor="center", width=800, height=500)

classement_label = tk.Label(
    classement_frame,
    text="🏆 Classement",
    font=font_title,
    fg=text_color,
    bg="#008000"
)
classement_label.pack(pady=10)

classement_text = tk.Text(
    classement_frame,
    font=font_text,
    fg=text_color,
    bg="#008000",
    bd=0,
    height=15,
    width=40
)
classement_text.pack(expand=True, fill="both", padx=10, pady=10)
classement_text.config(state='disabled')

# === Bouton Quitter ===
btn_quit = tk.Button(
    root,
    text="Fermer",
    font=("Helvetica", 24, "bold"),
    bg="#008000",
    fg="white",
    command=root.destroy
)
btn_quit.place(relx=0.5, rely=0.95, anchor="center", width=400, height=80)

if __name__ == "__main__":
    import threading

    def start_asyncio():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.ensure_future(client.start())
        loop.run_until_complete(game_loop())

    tiktok_thread = threading.Thread(target=start_asyncio)
    tiktok_thread.daemon = True
    tiktok_thread.start()

    root.mainloop()
