import tkinter as tk

# Background colors
BG_DARK = "gray15"
BG_DARKER = "gray10"
BG_LIGHTER = "gray20"
BG_BUTTON = "gray25"

# Text colors
TEXT_NORMAL = "white"
TEXT_GRAY = "gray70"

# Fonts
FONT_NORMAL = ("Arial", 11)
FONT_SMALL = ("Arial", 10)
FONT_TITLE = ("Arial", 12)
FONT_MONO = ("Arial", 12)  #TODO make this something unique

# Common styles
BUTTON_STYLE = {
    "width": 20,
    "font": FONT_NORMAL,
    "bg": BG_BUTTON,
    "fg": TEXT_NORMAL,
    "pady": 5
}

LABEL_STYLE = {
    "bg": BG_DARK,
    "fg": TEXT_NORMAL,
    "font": FONT_NORMAL
}

ENTRY_STYLE = {
    "bg": BG_BUTTON,
    "fg": TEXT_NORMAL,
    "font": FONT_NORMAL
}

LIST_STYLE = {
    "bg": BG_DARKER,
    "fg": TEXT_NORMAL,
    "font": FONT_NORMAL,
    "selectmode": tk.MULTIPLE,
}