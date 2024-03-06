import tkinter as tk, tkinter.filedialog
from PIL import ImageTk, Image
import numpy as np
import cv2 as cv
from sklearn.cluster import KMeans
import os
import shutil

"""
TODO: 
1. Thresholding

used this for writing the oop code
https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter

"""

filepath = "C:\\Users\\Pranav\\Downloads\\1_phase.jpg"
DEFAULT_BUTTON_WIDTH = 20
DEFAULT_BUTTON_HEIGHT = 10


# HELPER
def save_image(self):
    file_path = tkinter.filedialog.asksaveasfilename(
        defaultextension=".jpg", filetypes=(("JPG file", "*.jpg"), ("All Files", "*.*"))
    )
    if not file_path:
        return
    self.image.save(file_path)

def upload_image(self):
    file_path = tkinter.filedialog.askopenfilename()
    if file_path:
        try:
            with open(file_path, "rb") as f:
                self.image = Image.open(f)
                tk_img = ImageTk.PhotoImage(self.image)
        except IOError:
            print("Unable to open image file:", file_path)
        except Exception as e:
            print("An error occurred:", e)
        self.img_label.configure(image=tk_img)
        self.img_label.image = tk_img


class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # self.geometry("600x600")
        self.frames = {}
        for F in (StartPage, Canny, KMs):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Menu")

        to_canny = tk.Button(
            self, text="Canny", command=lambda: controller.show_frame("Canny")
        )
        to_kmeans = tk.Button(
            self, text="K-Means", command=lambda: controller.show_frame("KMs")
        )
        label.grid(row=0, column=0, sticky="nsew")
        to_canny.grid(row=1, column=0, sticky="nsew")
        to_kmeans.grid(row=2, column=0, sticky="nsew")


class Canny(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.down = 0
        self.up = 0
        label = tk.Label(self, text="Canny")
        self.image = Image.open(filepath)
        self.tk_img = ImageTk.PhotoImage(self.image)
        self.img_label = tk.Label(self, image=self.tk_img)

        self.test_label = tk.Label(self, bg="white", fg="black", width=20, text="")
        low_thres = tk.Scale(
            self,
            label="Lower Threshold",
            from_=0,
            to=255,
            orient=tk.HORIZONTAL,
            length=200,
            showvalue=0,
            command=self.slider_output_low,
        )
        up_thres = tk.Scale(
            self,
            label="Upper Threshold",
            from_=0,
            to=255,
            orient=tk.HORIZONTAL,
            length=200,
            showvalue=0,
            command=self.slider_output_up,
        )
        save_button = tk.Button(self, text="Save", command=lambda: save_image(self))
        upload_button = tk.Button(
            self, text="Upload", command=lambda: upload_image(self)
        )
        to_menu = tk.Button(
            self, text="Menu", command=lambda: controller.show_frame("StartPage")
        )

        self.img_label.grid(row=0, column=0, rowspan=3, columnspan=3, sticky="nesw")

        to_menu.grid(row=3, column=0, sticky="nesw")
        self.test_label.grid(row=6,column = 0, columnspan=3)
        up_thres.grid(row=4,column = 0, columnspan=3)
        low_thres.grid(row=5,column = 0, columnspan=3)
        label.grid(row=7, column=1, sticky="nesw")
        save_button.grid(row=3, column=1, sticky="nesw")
        upload_button.grid(row=3, column=2, sticky="nsew")


    def slider_output_low(self, v):
        self.down = v
        self.canny_wrapper()
    def slider_output_up(self, v):
        self.up = v
        self.canny_wrapper()
    def canny_wrapper(self):
        edge = cv.Canny(image=np.array(self.image), threshold1=int(self.down),threshold2=int(self.up), apertureSize=3) 
        cv.imshow('Canny Filtered', edge) 

class KMs(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="K-Means")
        self.image = Image.open(filepath)
        self.tk_img = ImageTk.PhotoImage(self.image)
        self.img_label = tk.Label(self, image=self.tk_img)
        denoise_button = tk.Button(
            self, text="Non-Local Means+K-Means", command=self.denoise
        )
        to_menu = tk.Button(
            self,
            text="Back to Menu",
            command=lambda: controller.show_frame("StartPage"),
        )
        save_button = tk.Button(self, text="Save", command=lambda: save_image(self))
        upload_button = tk.Button(
            self, text="Upload Image", command=lambda: upload_image(self)
        )

        self.img_label.grid(row=0, column=0, rowspan=3, columnspan=3, sticky="nesw")

        to_menu.grid(row=3, column=0, sticky="nesw")
        save_button.grid(row=3, column=1, sticky="nesw")
        denoise_button.grid(row=3, column=2, sticky="nesw")

        upload_button.grid(row=4, column=1, sticky="nsew")

        label.grid(row=5, column=1, sticky="nesw")

    def denoise(self):
        im_array = cv.fastNlMeansDenoisingColored(
            np.array(self.image), None, 5, 5, 3, 10
        )
        im_array_copy = im_array.copy()
        # what are the parameters in the above denoising thing

        w, h = self.image.size
        pix_val = list((Image.fromarray(im_array)).getdata())
        channels = 3
        pix_val = np.array(pix_val).reshape((w, h, channels))

        clt = KMeans(n_clusters=5)  # currently arbitrary
        clt.fit(im_array_copy.reshape(-1, 3))

        mini = [
            i
            for i in clt.cluster_centers_
            if (i.sum() == np.min([i.sum() for i in clt.cluster_centers_]))
        ][0]
        maxi = [
            i
            for i in clt.cluster_centers_
            if (i.sum() == np.max([i.sum() for i in clt.cluster_centers_]))
        ][0]
        for y in range(0, h):
            for x in range(0, w):
                pix_arr = pix_val[x, y]
                r = pix_arr[0]
                g = pix_arr[1]
                b = pix_arr[2]
                delta = 12
                if (
                    ((mini[0] - delta) <= r <= (mini[0] + delta))
                    or ((mini[1] - delta) <= g <= (mini[1] + delta))
                    or ((mini[2] - delta) <= b <= (mini[2] + delta))
                ):
                    pix_val[x, y] = [222, 131, 45]
                if (
                    ((maxi[0] - delta) <= r <= (maxi[0] + delta))
                    or ((maxi[1] - delta) <= g <= (maxi[1] + delta))
                    or ((maxi[2] - delta) <= b <= (maxi[2] + delta))
                ):
                    pix_val[x, y] = [235, 168, 75]

        self.image = Image.fromarray(pix_val.astype("uint8"), "RGB")
        tk_img2 = ImageTk.PhotoImage(self.image)
        self.img_label.configure(image=tk_img2)
        self.img_label.image = tk_img2


def main():
    app = SampleApp()
    app.mainloop()


if __name__ == "__main__":
    main()
