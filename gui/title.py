import tkinter as tk
from PIL import ImageTk, Image
import numpy as np
import cv2 as cv
from sklearn.cluster import KMeans

"""
TODO: 
1. implement persistence and saving the image

used this for writing the oop code
https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter

"""

filepath = "1_phase.jpg"


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
        label.pack(side="top", fill="x", pady=10)

        to_canny = tk.Button(
            self, text="Canny", command=lambda: controller.show_frame("Canny")
        )
        to_canny.pack()
        to_kmeans = tk.Button(
            self, text="K-Means", command=lambda: controller.show_frame("KMs")
        )
        to_kmeans.pack()


class Canny(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Canny")
        label.pack(side="top", fill="x", pady=10)

        self.image = Image.open(filepath)
        self.tk_img = ImageTk.PhotoImage(self.image)
        label2 = tk.Label(self, image=self.tk_img)
        label2.pack()

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
        low_thres.pack()
        up_thres.pack()
        self.test_label.pack()

        to_menu = tk.Button(
            self, text="Menu", command=lambda: controller.show_frame("StartPage")
        )
        to_menu.pack()

    def slider_output_low(self, v):
        self.test_label.config(text=v)

    def slider_output_up(self, v):
        self.test_label.config(text=v)


class KMs(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="K-Means")
        label.pack(side="top", fill="x", pady=10)

        self.image = Image.open(filepath)
        self.tk_img = ImageTk.PhotoImage(self.image)
        self.img_label = tk.Label(self, image=self.tk_img)
        self.img_label.pack()

        denoise_button = tk.Button(self, text="denoise", command=self.denoise)
        denoise_button.pack()

        to_menu = tk.Button(
            self, text="Menu", command=lambda: controller.show_frame("StartPage")
        )
        to_menu.pack()

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
        # print(clt.cluster_centers_)
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
        tk_img2 = ImageTk.PhotoImage(Image.fromarray(pix_val.astype("uint8"), "RGB"))
        self.img_label.configure(image=tk_img2)
        self.img_label.image = tk_img2


def main():
    app = SampleApp()
    app.mainloop()


if __name__ == "__main__":
    main()
