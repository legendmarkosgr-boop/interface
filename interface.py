# INTERFACE LIB

import tkinter as tk
from tkinter import ttk


# =====================================================
# Base Component Wrapper
# =====================================================

class UIElement:
    """Base class for all UI elements."""
    def __init__(self, widget):
        self.widget = widget

    def setText(self, text):
        """Set the text of the UI element."""
        if hasattr(self.widget, "config"):
            self.widget.config(text=text)

    def setSize(self, width=None, height=None):
        """Set the size of the UI element."""
        if width is not None:
            self.widget.config(width=width)
        if height is not None:
            self.widget.config(height=height)

    def setBackground(self, color):
        """Set the background color of the UI element."""
        self.widget.config(bg=color)

    def setForeground(self, color):
        """Set the foreground (text) color of the UI element."""
        self.widget.config(fg=color)

    def setFont(self, family="Arial", size=10, weight="normal"):
        """Set the font of the UI element."""
        self.widget.config(font=(family, size, weight))

    def setPadding(self, padx=0, pady=0):
        """Set internal padding of the UI element."""
        if hasattr(self.widget, "config"):
            self.widget.config(padx=padx, pady=pady)

    def setBorder(self, width=1, style="flat"):
        """Set border style and width."""
        style_map = {"flat": tk.FLAT, "raised": tk.RAISED, "sunken": tk.SUNKEN, "groove": tk.GROOVE, "ridge": tk.RIDGE}
        if style not in style_map:
            raise ValueError("Style must be: flat, raised, sunken, groove, ridge")
        self.widget.config(bd=width, relief=style_map[style])

    def setCursor(self, cursor_type="arrow"):
        """Set the cursor type when hovering over the element."""
        self.widget.config(cursor=cursor_type)

    def setOpacity(self, alpha=1.0):
        """Set transparency (0.0 to 1.0). Note: Limited support in Tkinter."""
        if 0.0 <= alpha <= 1.0:
            self.widget.config(activeforeground=self.widget.cget("fg"))
        else:
            raise ValueError("Alpha must be between 0.0 and 1.0")

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
        """Get the current value of the UI element."""
        try:
            return self.widget.get()
        except:
            return None


# =====================================================
# Component Classes
# =====================================================

class Button(UIElement):
    """A clickable button."""
    def __init__(self, text=""):
        super().__init__(tk.Button(text=text))


class Label(UIElement):
    """A text label."""
    def __init__(self, text=""):
        super().__init__(tk.Label(text=text))


class TextInput(UIElement):
    """A single-line text input field."""
    def __init__(self, width=20):
        super().__init__(tk.Entry(width=width))

    def setText(self, text):
        self.widget.delete(0, tk.END)
        self.widget.insert(0, text)

    def get(self):
        return self.widget.get()


class FrameBox(UIElement):
    """A container that can hold other UI elements."""
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
    """Main interface window."""
    def __init__(self):
        self.root = tk.Tk()
        self._layout = None
        self._pack_side = tk.TOP

    # ---------------- Window ----------------

    def setTitle(self, title: str):
        """Set the window title."""
        self.root.title(title)

    def setSize(self, width: int, height: int):
        """Set the window size."""
        self.root.geometry(f"{width}x{height}")

    def setResizable(self, width: bool, height: bool):
        """Set whether the window is resizable in width and height."""
        self.root.resizable(width, height)

    def setBackground(self, color: str):
        """Set the window background color."""
        self.root.configure(bg=color)

    def setIcon(self, icon_path: str):
        """Set the window icon."""
        self.root.iconbitmap(icon_path)

    # ---------------- Layout ----------------

    def setLayout(self, layout: str):
        """Set the layout manager for the interface."""
        if layout not in ("pack", "grid", "place"):
            raise ValueError("Layout must be: pack, grid, or place")
        self._layout = layout

    def setPackSide(self, side: str):
        """Set the side for pack layout."""
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
        """Add a UI element to the interface with the specified layout."""
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
        """Display the interface window."""
        self.root.mainloop()
