from pygame import init, mixer
from tkinter import Tk, Button, Scale, HORIZONTAL, Label, PhotoImage, filedialog, Canvas, messagebox
from mutagen.mp3 import MP3


def clicked():
    global duration
    if button.cget("bg") == "red":
        mixer.music.unpause()
        button.configure(bg="green")
        button.configure(image=pause_image)
    elif button.cget("bg") == "green":
        mixer.music.pause()
        button.configure(bg="red")
        button.configure(image=play_image)
    else:
        if len(file_paths_list) != 0:
            mixer.music.load(filename=file_paths_list[position])
            audio = MP3(file_paths_list[position])
            duration = audio.info.length
            update_bar()
            mixer.music.play()
            button.configure(bg="green")
            button.configure(image=pause_image)
        else:
            messagebox.showwarning("Warning", "Please select .mp3 file(s) before playing.")


def value(x):
    mixer.music.set_volume(int(x)/100)
    print(mixer.music.get_pos() / 1000)


def current_position_update():
    time_label.configure(text=f"{round(mixer.music.get_pos() / 1000)} / {round(duration)}")
    window.after(1000, current_position_update)


def jump(x):
    mixer.music.set_pos(int(x))
    print(mixer.music.get_pos())


def open_file_dialog():
    global is_on
    global file_paths_list, file_name_labels, position
    file_paths_list = []
    for i in file_name_labels:
        i.destroy()
    file_name_labels = []
    position = 0

    reset()
    filetypes = (("Text files", "*.mp3"), ("All files", "*.*"))
    file_paths = filedialog.askopenfilenames(title="Select file(s)", filetypes=filetypes)
    for file_path in file_paths:
        file_paths_list.append(file_path)

    for i in file_paths_list:
        file_name = i.split("/")[-1]
        label = Label(window, text=file_name)
        label.pack()
        file_name_labels.append(label)

    update_music_color()


def reset():
    mixer.music.stop()
    mixer.music.unload()

    button.configure(bg="SystemButtonFace")
    button.configure(image=play_image)


def forward():
    global position
    if position < len(file_paths_list) - 1:
        position = position + 1
        reset()
        clicked()
    print(position)
    update_music_color()

    return position


def backward():
    global position
    if position > 0:
        position = position - 1
        reset()
        clicked()
    update_music_color()
    print(position)
    return position


def update_music_color():
    global position
    if len(file_name_labels) != 0 and file_paths_list != 0:
        for i in file_name_labels:
            i.configure(fg="black", bg="white")
        file_name_labels[position].configure(fg="blue", bg="gray")


def update_bar():
    current_time = int(mixer.music.get_pos() / 1000)
    fill_size = (current_time / duration) * 480
    canvas.coords(filled_bar, 10, 10, 10 + fill_size, 40)
    canvas.itemconfig(filled_bar, tags=str(current_time + 1))
    if current_time < duration:
        canvas.after(100, update_bar)


init()


file_paths_list = []
file_name_labels = []
position = 0
duration = 0

is_on = True

window = Tk()
window.geometry("1080x600")
window.title("Music PLayer")
window.configure(bg="#5F9EA0")
window.resizable(width=False, height=False)

canvas = Canvas(window, width=500, height=50, bg="white")
canvas.place(x=300, y=530)

empty_bar = canvas.create_rectangle(10, 10, 490, 40, fill="gray")
filled_bar = canvas.create_rectangle(10, 10, 10, 40, fill="green")


play_image = PhotoImage(file="play.png").subsample(7)
pause_image = PhotoImage(file="pause.png").subsample(7)


time_label = Label(window, text="0", background="gray")
time_label.place(x=530, y=545)


button = Button(window, text="Click me!", image=play_image, command=clicked)
button.place(x=500, y=450)

forward_button = Button(window, text="forward!", command=forward)
forward_button.place(x=620, y=480)

backward_button = Button(window, text="backward!", command=backward)
backward_button.place(x=390, y=480)

select_file_button = Button(window, text="Select file(s)", command=open_file_dialog)
select_file_button.pack()

sound_slider = Scale(window, from_=0, to=100, orient=HORIZONTAL, command=value)
sound_slider.pack()

sound_slider_label = Label(window, text="Sound", background="gray")
sound_slider_label.place(x=444, y=40)


print(button.cget("bg"))
sound_slider.set(60)

window.after(1000, current_position_update)


window.mainloop()
