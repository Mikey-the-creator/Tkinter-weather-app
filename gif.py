import tkinter as tk
from PIL import Image, ImageTk
from itertools import count, cycle

class AnimatedGIF(tk.Label):
    """
    A Label widget that can display animated GIFs by cycling through frames.
    It handles loading, resizing, and animating the GIF.
    """
    def __init__(self, master, path, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.path = path
        self.frames = []
        self.delay = 100  # Default delay between frames
        self.frame_iter = None
        self.is_running = False
        self.load()

    def load(self):
        """Loads, resizes, and prepares all frames from the GIF file."""
        try:
            with Image.open(self.path) as img:
                self.frames = []
                for i in count(1):
                    # Resize each frame consistently
                    frame_photo = ImageTk.PhotoImage(img.copy().resize((250, 200), Image.Resampling.LANCZOS))
                    duration = img.info.get('duration', 100)
                    self.frames.append((frame_photo, duration))
                    try:
                        img.seek(i)  # Move to the next frame
                    except EOFError:
                        break  # End of frames
                self.frame_iter = cycle(self.frames)
                self.is_running = True
        except FileNotFoundError:
            print(f"Error: GIF file not found at {self.path}")
            self.is_running = False
        except Exception as e:
            print(f"Error loading {self.path}: {e}")
            self.is_running = False

    def start_animation(self):
        """Starts the animation loop if the GIF was loaded successfully."""
        if self.is_running:
            self.animate()

    def animate(self):
        """Cycles through frames to create the animation effect."""
        if self.is_running:
            current_frame, delay = next(self.frame_iter)
            self.config(image=current_frame)
            self.master.after(delay, self.animate)
