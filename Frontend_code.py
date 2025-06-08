import tkinter as tk
import math
import random

class GuessTheNumberGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Guess The Number Game")
        self.root.geometry("1200x700")
        self.root.configure(bg='black')

        self.canvas = tk.Canvas(self.root, width=1200, height=700, bg='black', highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Background balls setup
        self.balls = [(random.randint(100, 1100), random.randint(100, 600), random.uniform(0, 2*math.pi)) for _ in range(60)]
        self.velocities = [(random.uniform(-3, 3), random.uniform(-3, 3)) for _ in range(60)]
        self.radius = 4
        self.animate_background()

        self.points = 0
        self.next_window = None

        self.setup_main_screen()

    def setup_main_screen(self):
        self.canvas.delete("all")
        self.points_text = self.canvas.create_text(1170, 30, anchor="ne", text=f"Points: {self.points}", font=("Arial", 18, "bold"), fill="white")
        self.title_text = self.canvas.create_text(600, 280, text="GUESS THE NUMBER", font=("Arial", 60, "bold"), fill="#39FF14")

        self.play_button = tk.Button(self.root, text="PLAY", font=("Arial", 20, "bold"), bg="green", fg="white", command=self.show_instructions)
        self.play_button_window = self.canvas.create_window(600, 400, window=self.play_button)

    def animate_background(self):
        self.canvas.delete("ball")
        for i, ((x, y, _), (vx, vy)) in enumerate(zip(self.balls, self.velocities)):
            new_x = x + vx
            new_y = y + vy

            if new_x < 0 or new_x > 1200:
                vx *= -1
            if new_y < 0 or new_y > 700:
                vy *= -1

            self.canvas.create_oval(new_x - self.radius, new_y - self.radius,
                                    new_x + self.radius, new_y + self.radius,
                                    fill='white', outline='', tags="ball")
            self.balls[i] = (new_x, new_y, 0)
            self.velocities[i] = (vx, vy)

        self.root.after(50, self.animate_background)

    def show_instructions(self):
        self.canvas.delete("all")
        self.play_button.destroy()

        self.canvas.create_text(600, 60, text="Welcome in the Game!", font=("Times New Roman", 50, "bold"), fill="white")
        self.canvas.create_text(600, 130, text="Instructions", font=("Times New Roman", 45, "bold"), fill="white")

        instructions = [
            "• Guess The Number Between 1 to 50",
            "• You will get 5 attempts to Guess The Number",
            "• You will get a Hint to guess",
            "• If your answer will be wrong, Then you will get TRY AGAIN",
            "• If your answer will be correct, Then will get a point 1",
            "• Click 'Play Again' to start a new Game"
        ]

        y = 200
        for line in instructions:
            self.canvas.create_text(100, y, anchor="w", text=line, font=("Times New Roman", 22), fill="white")
            y += 50

        back_button = tk.Button(self.root, text="BACK", font=("Arial", 16, "bold"), bg="red", fg="white", command=self.setup_main_screen)
        self.canvas.create_window(150, 630, window=back_button)

        next_button = tk.Button(self.root, text="NEXT", font=("Arial", 16, "bold"), bg="green", fg="white", command=self.show_next_window)
        self.canvas.create_window(1050, 630, window=next_button)

    def show_next_window(self):
        if self.next_window is not None and tk.Toplevel.winfo_exists(self.next_window):
            self.next_window.destroy()

        self.next_window = tk.Toplevel(self.root)
        self.next_window.title("Guessing Game")
        self.next_window.geometry("1200x700")
        self.next_window.configure(bg='black')

        self.guess_canvas = tk.Canvas(self.next_window, width=1200, height=700, bg='black', highlightthickness=0)
        self.guess_canvas.pack(fill="both", expand=True)

        # Background balls in guess window
        self.local_balls = [(random.randint(100, 1100), random.randint(100, 600), random.uniform(0, 2 * math.pi)) for _ in range(60)]
        self.local_velocities = [(random.uniform(-3, 3), random.uniform(-3, 3)) for _ in range(60)]
        self.radius = 4

        def animate():
            self.guess_canvas.delete("ball")
            for i, ((x, y, _), (vx, vy)) in enumerate(zip(self.local_balls, self.local_velocities)):
                new_x = x + vx
                new_y = y + vy

                if new_x < 0 or new_x > 1200:
                    vx *= -1
                if new_y < 0 or new_y > 700:
                    vy *= -1

                self.guess_canvas.create_oval(new_x - self.radius, new_y - self.radius,
                                   new_x + self.radius, new_y + self.radius,
                                   fill='white', outline='', tags="ball")
                self.local_balls[i] = (new_x, new_y, 0)
                self.local_velocities[i] = (vx, vy)

            self.next_window.after(50, animate)

        animate()

        self.points_text_guess = self.guess_canvas.create_text(1170, 30, anchor="ne", text=f"Points: {self.points}", font=("Arial", 18, "bold"), fill="white")

        self.guess_canvas.create_text(600, 80, text="Guess the Number (1 to 50)", font=("Arial", 40, "bold"), fill="white")

        self.random_number = random.randint(1, 50)
        self.attempts = 5

        hint = self.get_hint(self.random_number)
        self.hint_text_id = self.guess_canvas.create_text(600, 150, text=f"Hint: {hint}", font=("Arial", 28), fill="white")

        self.input_var = tk.StringVar()
        entry = tk.Entry(self.next_window, textvariable=self.input_var, font=("Arial", 24), justify="center", width=6)
        self.guess_canvas.create_window(600, 210, window=entry)

        self.result_label = tk.Label(self.next_window, text="", font=("Arial", 22), bg="black", fg="white")
        self.guess_canvas.create_window(600, 270, window=self.result_label)

        self.attempts_label = tk.Label(self.next_window, text=f"You have {self.attempts} Attempts!!", font=("Arial", 22), bg="black", fg="white")
        self.guess_canvas.create_window(600, 320, window=self.attempts_label)

        self.submit_button = tk.Button(self.next_window, text="SUBMIT", font=("Arial", 20, "bold"), bg="green", fg="white", command=self.check_answer)
        reset_button = tk.Button(self.next_window, text="RESET", font=("Arial", 20, "bold"), bg="red", fg="white", command=lambda: [self.next_window.destroy(), self.setup_main_screen()])
        play_again_button = tk.Button(self.next_window, text="Play Again", font=("Arial", 20, "bold"), fg="white", bg="blue", command=self.play_again_fields)

        # Place buttons in one row, spaced evenly
        self.guess_canvas.create_window(450, 400, window=reset_button)
        self.guess_canvas.create_window(600, 400, window=self.submit_button)
        self.guess_canvas.create_window(750, 400, window=play_again_button)

    def play_again_fields(self):
        self.input_var.set("")
        self.result_label.config(text="")
        self.attempts = 5
        self.attempts_label.config(text=f"You have {self.attempts} Attempts!!")
        self.submit_button.config(state="normal")
        self.random_number = random.randint(1, 50)
        hint = self.get_hint(self.random_number)
        self.guess_canvas.itemconfig(self.hint_text_id, text=f"Hint: {hint}")

    def get_hint(self, n):
        hints = {
            1: "A Unique Number", 2: "An Even & Prime Number", 3: "Smallest Odd Prime Number", 4: "Only Divisible by 2",
            5: "Its Multiple always ends with 5 or 0", 6: "Divisible by 2 and 3 Only", 7: "Only Divisible by itself in the range of 10",
            8: "Only Divisible by 2 and 4", 9: "Only Divisible by 3", 10: "Only Divisible by 2 and 5", 11: "A Prime Number with same Tens & Ones Digit",
            12: "Divisible by 2 and 3", 13: "A Prime Number ending with 3", 14: "Divisible by 2 and 7", 15: "Only Divisible by 3 and 5",
            16: "Divisible by 2 and 4", 17: "A Prime Number ending with 7", 18: "Only Divisible by 2 and 9", 19: "A Prime Number ending with 9",
            20: "Divisible by 2 and 5", 21: "Only Divisible by 3 and 7", 22: "A Number with same Tens & Ones Digit",
            23: "A Prime Number ending with 3", 24: "Divisible by 2 and 4", 25: "Only Divisible by 5", 26: "Only Divisible by 2 and 13",
            27: "Divisible by 2 and 3", 28: "Divisible by 2 and 7", 29: "A Biggest Prime Number", 30: "Divisible by 2 and 5",
            31: "A Prime Number ending with 1", 32: "Divisible by 2^n, where n ≤ 5", 33: "A Number with same Tens & Ones Digit",
            34: "Divisible by 17", 35: "Divisible by 7", 36: "Divisible by 18", 37: "A Prime Number ending with 7", 38: "Divisible by 2 and 19",
            39: "Divisible by 3 and 13", 40: "Divisible by 2 and 5", 41: "A Prime Number ending with 1", 42: "Divisible by 2 and 3",
            43: "A Prime Number ending with 3", 44: "Divisible by 4", 45: "Divisible by 3 and 5", 46: "Divisible by 2 and 23",
            47: "A Prime Number ending with 7", 48: "Divisible by 2 and 3", 49: "Only Divisible by 7", 50: "Only Divisible by 2 and 5"
        }
        return hints.get(n, "Guess a number!")

    def check_answer(self):
        try:
            guess = int(self.input_var.get())
        except ValueError:
            self.result_label.config(text="Please enter a valid number!")
            return

        if guess < 1 or guess > 50:
            self.result_label.config(text="Number must be between 1 and 50!")
            return

        self.attempts -= 1
        if guess == self.random_number:
            self.points += 1
            self.result_label.config(text="Congratulations! You guessed it right!")
            self.submit_button.config(state="disabled")
            self.update_points()
        else:
            if self.attempts > 0:
                self.result_label.config(text=f"Try Again! Attempts left: {self.attempts}")
            else:
                self.result_label.config(text=f"Game Over! The number was {self.random_number}")
                self.submit_button.config(state="disabled")

        self.attempts_label.config(text=f"You have {self.attempts} Attempts!!")

    def update_points(self):
        self.canvas.itemconfig(self.points_text, text=f"Points: {self.points}")
        if self.next_window and tk.Toplevel.winfo_exists(self.next_window):
            self.guess_canvas.itemconfig(self.points_text_guess, text=f"Points: {self.points}")

if __name__ == "__main__":
    root = tk.Tk()
    game = GuessTheNumberGame(root)
    root.mainloop()
