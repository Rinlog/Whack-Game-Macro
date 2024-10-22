from tkinter import *
import pyautogui
import cv2 as cv
import numpy as np
import os
import pynput
import pydirectinput
import mss
try:
    from tkinter import Canvas
except ImportError:
    from tkinter import Canvas
    from tkinter.constants import *

from PIL import Image, ImageDraw, ImageTk

# Python 2/3 compatibility
try:
 bleh
except NameError:
  basestring = str

def hex2rgb(str_rgb):
    try:
        rgb = str_rgb[1:]

        if len(rgb) == 6:
            r, g, b = rgb[0:2], rgb[2:4], rgb[4:6]
        elif len(rgb) == 3:
            r, g, b = rgb[0] * 2, rgb[1] * 2, rgb[2] * 2
        else:
            raise ValueError()
    except:
        raise ValueError("Invalid value %r provided for rgb color."% str_rgb)

    return tuple(int(v, 16) for v in (r, g, b))

class GradientFrame(Canvas):

    def __init__(self, master, from_color, to_color, width=None, height=None, orient=HORIZONTAL, steps=None, **kwargs):
        Canvas.__init__(self, master, **kwargs)
        if steps is None:
            if orient == HORIZONTAL:
                steps = height
            else:
                steps = width

        if isinstance(from_color, basestring):
            from_color = hex2rgb(from_color)
            
        if isinstance(to_color, basestring):
            to_color = hex2rgb(to_color)

        r,g,b = from_color
        dr = float(to_color[0] - r)/steps
        dg = float(to_color[1] - g)/steps
        db = float(to_color[2] - b)/steps

        if orient == HORIZONTAL:
            if height is None:
                raise ValueError("height can not be None")
            
            self.configure(height=height)
            
            if width is not None:
                self.configure(width=width)

            img_height = height
            img_width = self.winfo_screenwidth()

            image = Image.new("RGB", (img_width, img_height), "#FFFFFF")
            draw = ImageDraw.Draw(image)

            for i in range(steps):
                r,g,b = r+dr, g+dg, b+db
                y0 = int(float(img_height * i)/steps)
                y1 = int(float(img_height * (i+1))/steps)

                draw.rectangle((0, y0, img_width, y1), fill=(int(r),int(g),int(b)))
        else:
            if width is None:
                raise ValueError("width can not be None")
            self.configure(width=width)
            
            if height is not None:
                self.configure(height=height)

            img_height = self.winfo_screenheight()
            img_width = width
            
            image = Image.new("RGB", (img_width, img_height), "#FFFFFF")
            draw = ImageDraw.Draw(image)

            for i in range(steps):
                r,g,b = r+dr, g+dg, b+db
                x0 = int(float(img_width * i)/steps)
                x1 = int(float(img_width * (i+1))/steps)

                draw.rectangle((x0, 0, x1, img_height), fill=(int(r),int(g),int(b)))
        
        self._gradient_photoimage = ImageTk.PhotoImage(image)

        self.create_image(0, 0, anchor=NW, image=self._gradient_photoimage)

if __name__ == "__main__":

    try:
        import tkinter
        from tkinter import messagebox
    except ImportError:
        import tkinter
        from tkinter import messagebox

    def Macro():
        root.destroy()
        pyautogui.PAUSE = 0.01
        pydirectinput.PAUSE = 0.06
        def on_press(key):
            if key == pynput.keyboard.Key.esc:
                print("Exiting")
                os._exit(0)
        listener = pynput.keyboard.Listener(on_press=on_press)
        listener.start()
        
        ImgToLookFor1 = cv.imread("Img/potato1.JPG", cv.IMREAD_UNCHANGED)
        ImgToLookFor2 = cv.imread("Img/potato2.JPG", cv.IMREAD_UNCHANGED)

        HfirstImgWidth = ImgToLookFor1.shape[1] /2
        HfirstImgHeight = ImgToLookFor1.shape[0] /2

        HsecondImgWidth = ImgToLookFor2.shape[1] /2
        HsecondImgHeight = ImgToLookFor2.shape[0] /2
        screen = {"top":150, "left":320, "width":710, "height":750}
        img = None
        with mss.mss() as sct:
            while True:
                img = sct.grab(screen)
                img = cv.cvtColor(np.array(img), cv.COLOR_BGRA2BGR)

                result1 = cv.matchTemplate(img,ImgToLookFor1,cv.TM_CCOEFF_NORMED)
                result2 = cv.matchTemplate(img,ImgToLookFor2, cv.TM_CCOEFF_NORMED)
                
                min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result1)
                min_val2, max_val2, min_loc2, max_loc2 = cv.minMaxLoc(result2)
                if max_val > 0.9 or max_val2 > 0.9:
                    if max_val > max_val2:
                        TopLeft = max_loc
                        pyautogui.moveTo(TopLeft[0] + HfirstImgWidth + 320, TopLeft[1] + HfirstImgHeight + 150)
                        pydirectinput.click()
                    elif max_val2 > max_val:
                        TopLeft = max_loc2
                        pyautogui.moveTo(TopLeft[0] + HsecondImgWidth + 320, TopLeft[1] + HsecondImgHeight + 150)
                        pydirectinput.click()
        
    root = Tk()
    root.title("Potato Whacker")
    root.geometry("600x420")


    GradientFrame(root, from_color="#000000", to_color="#FFFFFF", height=1000).pack(fill=X)
    description = Label(root, text="Macro for whacking potatos Press ESC to cancel,\n make sure your game screen\n is full window sized(not full screen)", bg="grey", font=("Arial",15))
    description.place(x=80,y=5)


    Start = Button(root, text="Click to Start", bg="grey", font=("Arial",15), command=Macro )
    Start.place(x=230,y=300)
    root.mainloop()