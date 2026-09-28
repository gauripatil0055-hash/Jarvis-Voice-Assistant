import tkinter as tk
import threading
import speech_recognition as sr
import main


# ---------- Functions ----------

def update_status(text):
    root.after(0, lambda: status.config(text=text))


def update_command(text):
    root.after(0, lambda: command_label.config(text=text))


def listen_to_jarvis():

    update_status("● Listening...")
    update_command("Listening for your command...")

    def listen():

        try:
            r = sr.Recognizer()

            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.4)
                audio = r.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=5
                )

            command = r.recognize_google(audio)

            update_command("You: " + command)
            update_status("● Processing...")

            main.processCommand(command)

            update_status("● Ready")

        except sr.WaitTimeoutError:
            update_command("No command detected.")
            update_status("● Ready")

        except sr.UnknownValueError:
            update_command("Sorry, I couldn't understand.")
            update_status("● Ready")

        except Exception as e:
            update_command("Error: " + str(e))
            update_status("● Ready")

    threading.Thread(target=listen, daemon=True).start()


def exit_jarvis():
    root.destroy()


# ---------- Window ----------

root = tk.Tk()

root.title("JARVIS - Voice Assistant")
root.geometry("650x600")
root.resizable(False, False)

root.configure(bg="#101010")


# ---------- Title ----------

title = tk.Label(
    root,
    text="🤖 J A R V I S",
    font=("Arial", 30, "bold"),
    bg="#101010",
    fg="white"
)
title.pack(pady=(35, 5))

# JARVIS Circle

circle = tk.Label(
    root,
    text="J",
    font=("Impact", 40, "bold"),
    bg="#1c1c1c",
    fg="white",
    width=3,
    height=1
)
circle.pack(pady=20)

subtitle = tk.Label(
    root,
    text="PERSONAL VOICE ASSISTANT",
    font=("Arial", 11),
    bg="#101010",
    fg="gray"
)
subtitle.pack()


# ---------- Status ----------

status = tk.Label(
    root,
    text="● Ready",
    font=("Arial", 15, "bold"),
    bg="#101010",
    fg="lime"
)
status.pack(pady=(40, 20))


# ---------- Command Box ----------

command_label = tk.Label(
    root,
    text="Click START LISTENING and speak your command...",
    font=("Arial", 13),
    bg="#1c1c1c",
    fg="white",
    width=55,
    height=4,
    wraplength=500
)
command_label.pack(pady=10)


# ---------- Listen Button ----------

listen_button = tk.Button(
    root,
    text="🎤  START LISTENING",
    font=("Arial", 14, "bold"),
    bg="#252525",
    fg="white",
    activebackground="#333333",
    activeforeground="white",
    padx=25,
    pady=12,
    bd=0,
    cursor="hand2",
    command=listen_to_jarvis
)
listen_button.pack(pady=25)


# ---------- Exit Button ----------

exit_button = tk.Button(
    root,
    text="EXIT",
    font=("Arial", 11),
    bg="#252525",
    fg="white",
    activebackground="#333333",
    activeforeground="white",
    padx=25,
    pady=7,
    bd=0,
    cursor="hand2",
    command=exit_jarvis
)
exit_button.pack()


# ---------- Run ----------

root.mainloop()