import tkinter as tk
"""
1. main window
2. canny filters

used this for writing the oop code
https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter

"""
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

        self.frames = {}
        for F in (StartPage, Canny):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text = "Menu")
        label.pack(side="top", fill="x", pady=10)

        to_canny = tk.Button(self, text="Canny",
                            command=lambda: controller.show_frame("Canny"))
        to_canny.pack()
        
class Canny(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Canny")
        label.pack(side="top", fill="x", pady=10)

        self.test_label = tk.Label(self, bg='white', fg='black', width=20, text='')
        low_thres = tk.Scale(self, label='Lower Threshold', from_= 0, to = 255, orient=tk.HORIZONTAL, length= 200, showvalue=0, command=self.slider_output_low)
        up_thres = tk.Scale(self, label='Upper Threshold', from_= 0, to = 255, orient=tk.HORIZONTAL, length= 200, showvalue=0, command=self.slider_output_up)
        low_thres.pack()
        up_thres.pack()
        self.test_label.pack()
        
        to_menu = tk.Button(self, text="Menu",
                           command=lambda: controller.show_frame("StartPage"))
        to_menu.pack()

    def slider_output_low(self, v):
        self.test_label.config(text = v)

    def slider_output_up(self, v):
        self.test_label.config(text = v)

def main(): 
    app = SampleApp()

    app.mainloop()

if __name__ == '__main__':
    main()