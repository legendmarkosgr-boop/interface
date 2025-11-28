# INTERFACE LIB

import tkinter as tk
from tkinter import ttk


# =====================================================
# Base Component Wrapper
# =====================================================

class UIElement:
    def __init__(self, widget):
        self.widget = widget

    def setText(self, text):
        if hasattr(self.widget, "config"):
            self.widget.config(text=text)

    def setSize(self, width=None, height=None):
        if width is not None:
            self.widget.config(width=width)
        if height is not None:
            self.widget.config(height=height)

    def setBackground(self, color):
        self.widget.config(bg=color)

    def setForeground(self, color):
        self.widget.config(fg=color)

    def event(self, *functions):
        """
        Attach multiple functions to the component.
        Each function is executed in order when the event fires.
        """
        def combined():
            for fn in functions:
                fn()
        self.widget.config(command=combined)

    def get(self):
        try:
            return self.widget.get()
        except:
            return None


# =====================================================
# Component Classes
# =====================================================

class Button(UIElement):
    def __init__(self, text=""):
        super().__init__(tk.Button(text=text))


class Label(UIElement):
    def __init__(self, text=""):
        super().__init__(tk.Label(text=text))


class TextInput(UIElement):
    def __init__(self, width=20):
        super().__init__(tk.Entry(width=width))

    def setText(self, text):
        self.widget.delete(0, tk.END)
        self.widget.insert(0, text)

    def get(self):
        return self.widget.get()


class FrameBox(UIElement):
    def __init__(self):
        self.frame = tk.Frame()
        super().__init__(self.frame)

    def add(self, element, **opts):
        # default pack
        element.widget.pack()
        

# =====================================================
# Main Window
# =====================================================

class Interface:
    def __init__(self):
        self.root = tk.Tk()
        self._layout = None
        self._pack_side = tk.TOP

    # ---------------- Window ----------------

    def setTitle(self, title: str):
        self.root.title(title)

    def setSize(self, width: int, height: int):
        self.root.geometry(f"{width}x{height}")

    def setResizable(self, width: bool, height: bool):
        self.root.resizable(width, height)

    def setBackground(self, color: str):
        self.root.configure(bg=color)

    # ---------------- Layout ----------------

    def setLayout(self, layout: str):
        if layout not in ("pack", "grid", "place"):
            raise ValueError("Layout must be: pack, grid, or place")
        self._layout = layout

    def setPackSide(self, side: str):
        side_map = {
            "top": tk.TOP,
            "bottom": tk.BOTTOM,
            "left": tk.LEFT,
            "right": tk.RIGHT
        }
        if side not in side_map:
            raise ValueError("Side must be: top, bottom, left, right")

        self._pack_side = side_map[side]

    # ---------------- Add Widgets ----------------

    def add(self, element: UIElement, **options):
        widget = element.widget

        if self._layout == "pack":
            widget.pack(side=self._pack_side)
        elif self._layout == "grid":
            widget.grid(row=options.get("row", 0), column=options.get("column", 0))
        elif self._layout == "place":
            widget.place(x=options.get("x", 0), y=options.get("y", 0))
        else:
            raise RuntimeError("Layout not set! Use setLayout().")

    # ---------------- Show Window ----------------

    def show(self):
        self.root.mainloop()
