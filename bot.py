import asyncio
import unicodedata
import customtkinter as ctk
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent
from gtts import gTTS
from playsound import playsound
import os
import json
import threading

USERNAME = "songzz.vfr"
user_points = {}

ctk.set_appearance_mode("dark")  # Modes: "light", "dark", "system"
ctk.set_default_color_theme("green")

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
    global current_question_index, waiting_for_answer, current_expected_answer, already_answered, winner_of_the_question, questions_and_answers

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
            speak_text(message)

        current_question_index += 1
        await asyncio.sleep(2)

        questions_and_answers = load_questions()
        display_scores()

    update_question_display("✅ Le quiz est terminé ! Voici le classement final :")
    display_scores()
    speak_text("Le quiz est terminé ! Voici le classement final.")

def display_scores():
    classement_text.configure(state='normal')
    classement_text.delete("1.0", "end")
    
    if not user_points:
        classement_text.insert("end", "Aucun point marqué !")
    else:
        classement = sorted(user_points.items(), key=lambda x: x[1], reverse=True)
        classement_text.insert("end", "🏆 Classement en direct :\n\n")
        for user, points in classement:
            classement_text.insert("end", f"{user} : {points} point(s)\n")
    
    classement_text.configure(state='disabled')

def update_question_display(message):
    question_label.configure(text=message)

@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    global waiting_for_answer, already_answered, winner_of_the_question
    user = event.user.nickname
    comment = normalize_text(event.comment)

    print(f"{user} a répondu : {event.comment}")

    if waiting_for_answer and comment == current_expected_answer:
        if not already_answered:
            user_points[user] = user_points.get(user, 0) + 1
            already_answered = True
            winner_of_the_question = user

            message = f"🎉 Bravo {user} + 1 point ! Total : {user_points[user]}"
            print(message)
            update_question_display(message)
            speak_text(f"Bravo {user}, bonne réponse ! Tu gagnes 1 point.")

            display_scores()


# Initialisation
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("Quiz Time TikTok")
root.geometry("1080x1920")
root.configure(bg="#333333")  # Fond sombre pour contraster le carré vert

# === Carré vert géant de 500x500 ===
green_square = ctk.CTkFrame(
    root,
    width=500,
    height=500,
    fg_color="#00FF00",  # Vert vif
    border_width=0       # Pas de bordure
)
green_square.pack(pady=100)
green_square.pack_propagate(False)

# === Zone de question (texte blanc) ===
question_label = ctk.CTkLabel(
    green_square,
    text="En attente de la prochaine question...",
    font=("Arial Rounded MT Bold", 18, "bold"),
    fg_color="transparent",
    text_color="white",
    wraplength=400
)
question_label.pack(pady=10, padx=10, fill="x")

# === Zone de classement (fond vert, texte blanc) ===
classement_text = ctk.CTkTextbox(
    green_square,
    font=("Arial Rounded MT Bold", 16),
    fg_color="#00FF00",     # Même vert que le carré
    text_color="white",
    wrap="word",
    width=400,
    height=200
)
classement_text.pack(pady=10)
classement_text.configure(state='disabled')



# Lancement de l'interface
root.mainloop()


if __name__ == "__main__":
    def start_asyncio():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.ensure_future(client.start())
        loop.run_until_complete(game_loop())

    tiktok_thread = threading.Thread(target=start_asyncio, daemon=True)
    tiktok_thread.start()
    root.mainloop()
