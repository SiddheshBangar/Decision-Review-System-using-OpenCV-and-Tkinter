import tkinter
import cv2  # pip install opencv-python
import PIL.Image
import PIL.ImageTk   # pip install pillow
import threading
import time
from functools import partial

stream = cv2.VideoCapture("main.avi")

flag = True


def play(speed):
    global flag
    print(f"You clicked on play. Speed is {speed}")

    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read()
    if not grabbed:
        exit()

    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

    if flag:
        canvas.create_text(134, 26, fill="RED",font="Times 26 bold", text="Decision Pending")
    flag = not flag


def pending(decision):
    # 1. Display decision pending image
    frame = cv2.cvtColor(cv2.imread("decision.jpg"), cv2.COLOR_BGR2RGB)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

    # 2. Wait for 2 seconds
    time.sleep(1)

    # 3. Display Sponser Image
    frame = cv2.cvtColor(cv2.imread("sponser.jpg"), cv2.COLOR_BGR2RGB)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

    # 4. Wait for 2 seconds
    time.sleep(2)

    # 5. Display out or not out
    if decision == 'out':
        decisionimg = "out.jpg"
    else:
        decisionimg = "notout.jpg"
    frame = cv2.cvtColor(cv2.imread(decisionimg), cv2.COLOR_BGR2RGB)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    pass


def out():
    thread = threading.Thread(target=pending, args=("out", ))
    thread.daemon = 1
    thread.start()
    print("Player is out")


def notout():
    thread = threading.Thread(target=pending, args=("not out", ))
    thread.daemon = 1
    thread.start()
    print("Player is not out")


# Width Height of main screen
SET_WIDTH = 650
SET_HEIGHT = 368

# tkinter gui starts here
window = tkinter.Tk()
window.title("Third Umpire: Decision Review System")
cv_img = cv2.cvtColor(cv2.imread("welcome.jpg"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, anchor=tkinter.NW, image=photo)
canvas.pack()

# Buttons to control playback
btn = tkinter.Button(window, text="<< Backward (Fast)",
                     width=50, command=partial(play, -25))
btn.pack()
btn = tkinter.Button(window, text=">> Forward (Fast)",
                     width=50, command=partial(play, 25))
btn.pack()
btn = tkinter.Button(window, text="<< Backward (Slow)",
                     width=50, command=partial(play, -2))
btn.pack()
btn = tkinter.Button(window, text=">> Forward (Slow)",
                     width=50, command=partial(play, 2))
btn.pack()
btn = tkinter.Button(window, text="Give Out", width=50, command=out)
btn.pack()
btn = tkinter.Button(window, text="Give Not Out", width=50, command=notout)
btn.pack()


window.mainloop()
