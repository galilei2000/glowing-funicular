import typing
from typing import Optional, Callable
from PIL import Image, ImageTk
import tkinter as tk
from tkinter.font import Font
from defs import *

root: Optional[tk.Tk] = None
bg_canvas: Optional[tk.Canvas] = None
label_items: typing.List[tk.Label] = []
image_ref: Optional[tk.Image] = None
running: Optional[Callable[[], None]] = None
item_binds: typing.Dict[tk.Misc, typing.Set[str]] = dict()
# my_font = Font(family="Courier", size=13)


def __addBind(item: Optional[tk.Misc], seq: str, func: Callable[[tk.Event], None], *args, **kwargs) -> None:
    if item is None:
        return
    item.bind(seq, func)
    item_binds[item].add(seq)


def __clearBind(item: tk.Misc):
    for sequence in item_binds[item]:
        item.unbind(sequence)
    item_binds[item].clear()


def __destroy(item: Optional[tk.Misc]):
    if item is None:
        return
    if item == bg_canvas:
        label_items.clear()
    item_binds.pop(item)
    for child in item.winfo_children():
        __destroy(child)
    item.destroy()


def destroyEvent(event: tk.Event):
    global root
    if root:
        __destroy(root)
    root = None


def init() -> None:
    global root
    global bg_canvas
    global label_items

    root = tk.Tk()
    item_binds[root] = set()
    root.title("Glowing funicular dungeon")

    bg_canvas = tk.Canvas()
    item_binds[bg_canvas] = set()
    bg_canvas.pack(side='top', fill='both', expand='yes')

    for item in label_items:
        item.destroy()
    label_items = []


def setBgImage(image_name: str) -> None:
    global root
    global bg_canvas
    global image_ref

    if root is None:
        init()

    __destroy(bg_canvas)

    img = Image.open(image_name)
    img = img.resize((w, h), Image.ANTIALIAS)
    image_ref = ImageTk.PhotoImage(img)

    root.geometry("%dx%d+30+30" % (w, h))

    bg_canvas = tk.Canvas(width=w, height=h, bg='black')
    item_binds[bg_canvas] = set()
    bg_canvas.create_image(0, 0, image=image_ref, anchor='nw')
    bg_canvas.pack(side='top', fill='both', expand='yes')

    bg_canvas.update_idletasks()
    root.update_idletasks()


def deleteAllText():
    global label_items
    global bg_canvas

    for item in label_items:
        bg_canvas.delete(item)
    label_items.clear()


def addText(text: str, x: int, y: int, color="black"):
    global label_items
    label_items.append(bg_canvas.create_text(x + 2, y, text=text, fill=color, anchor='nw',
                                             font=("Courier", 13)))


def addTextCenter(text: str, line: int, color="black"):
    if line < 0:
        line -= 1
        line = lineCnt + line
    x_pos = CenterX(text) * charSize

    addText(text, x_pos, line * charSize, color=color)


def addTextShadow(text: str, x: int, y: int, color: str = "white"):
    addText(text, x + 1, y + 1, color="black")
    addText(text, x, y, color=color)


def addGameBind(sequence: str, func: Callable[[tk.Event], None], *args, **kwargs) -> None:
    global root
    __addBind(root, sequence, func, *args, **kwargs)


def gameClearBinds():
    global root
    __clearBind(root)


def setRunningFunc(to_run: Optional[Callable[[], None]] = None):
    global running
    running = to_run


def start() -> None:
    global root
    if running:
        root.after(100, running)
    if root:
        root.mainloop()
    print("Mainloop ended")


def after(delay, func, *args, **kwargs):
    global root
    if root:
        root.after(delay, func, *args, **kwargs)
