from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None


# --------------------------- WINDOWS POP-UP--------------------------------#
def bring_to_front():
    window.attributes("-topmost", True)  # Make the window topmost
    window.after(1000, lambda: window.attributes("-topmost", False))  # Remove topmost after a delay
    window.bell()


# ---------------------------- TIMER RESET ------------------------------- #
def timer_reset():
    window.after_cancel(timer)

    title.config(text='TIMER', fg=RED, font=(FONT_NAME, 30))
    canvas.itemconfig(time_text, text='00:00')
    tick_mark.config(text='')
    global reps
    reps = 0

    start_button.config(state='normal')


# ---------------------------- TIMER MECHANISM ------------------------------- #

def start_timer():
    global reps
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    reps += 1
    if reps % 8 == 0:
        count_down(long_break_sec)
        title.config(text='Long Break☕', fg=YELLOW, font=(FONT_NAME, 30, 'bold'))
        bring_to_front()

    elif reps % 2 == 0:
        count_down(short_break_sec)
        title.config(text='Short Break', fg=PINK)
        bring_to_front()

    else:
        count_down(work_sec)
        title.config(text='Work Hard 🧑‍💻', fg=RED)

    start_button.config(state='disabled')

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60

    unit_place = count_sec % 10
    tenth_place = (count_sec // 10) % 10

    canvas.itemconfig(time_text, text=f'{count_min}:{tenth_place}{unit_place}')
    if count > 0:

        global timer
        # in-built function for tk to do something after a particular milliseconds
        # call count_down function after 1000 milliseconds and pass count-1 into the function as argument.
        timer = window.after(1000, count_down, count - 1)
    else:
        if title["text"] == "Long Break":
            timer_reset()
            bring_to_front()
        else:
            start_timer()

            work_sessions = math.floor(reps / 2)
            marks = ''
            for _ in range(work_sessions):
                marks += '✔'

            tick_mark.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=GREEN)

canvas = Canvas(width=200, height=224, bg=GREEN, highlightthickness=0)

tomato_img = PhotoImage(file='tomato.png')
canvas.create_image(100, 112, image=tomato_img)
time_text = canvas.create_text(100, 130, text='00:00', fill='White', font=(FONT_NAME, 30, 'bold'))
canvas.grid(row=1, column=1)

title = Label(text='TIMER', bg=GREEN, fg=RED, font=(FONT_NAME, 30))
title.grid(row=0, column=1)

start_button = Button(text='Start', command=start_timer, highlightthickness=0)
start_button.grid(row=2, column=0)

reset_button = Button(text='Reset', highlightthickness=0, command=timer_reset)
reset_button.grid(row=2, column=2)

tick_mark = Label(bg=GREEN, fg=RED, font=(FONT_NAME, 15, 'bold'))
tick_mark.grid(row=3, column=1)

window.mainloop()
