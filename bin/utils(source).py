from tkinter.constants import END
import tkinter.filedialog
from PIL import Image
from shutil import rmtree, copy2
from os import makedirs, name, path, getcwd, chdir
from pdf2image import convert_from_path
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=1)


SIZE = dict([
    ['A4', (3500, 2480)],
    ['A5', (2480, 1748)],
    ['A6', (1748, 1240)],
    ['A7', (1240, 874)],
])

WIDTH, HEIGHT = 0, 1


def generate_name(IMG1, IMG2):
    return '_'.join([str(elem) for elem in list(map(lambda img: img[:-len('.jpg')], (IMG1, IMG2)))]) + '.jpg'


def stringify(sublist):
    sublist_ = []
    for num in sublist:
        sublist_.append(str(num) + '.jpg')
    return sublist_


class App:
    def __init__(self, root, _func):
        chdir('res')
        self.main_function = _func
        # setting title
        root.title("Pdf2Booklet")
        # setting window size
        width = 382
        height = 168
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        self.SAVEPATH, self.PATH = "", ""
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        root.configure(bg="#ffffff")

        self.OPEN_IMG = tk.PhotoImage(file='import.png')
        GButton_958 = tk.Button(root, relief='groove', image=self.OPEN_IMG)
        GButton_958["bg"] = "#ffffff"
        GButton_958["fg"] = "#000000"
        GButton_958["justify"] = "center"
        GButton_958["image"] = self.OPEN_IMG
        GButton_958.place(x=220, y=40, width=70, height=30)
        GButton_958["command"] = self.GButton_958_command

        self.SAVE_IMG = tk.PhotoImage(file='export.png')
        GButton_841 = tk.Button(root, relief='groove', image=self.SAVE_IMG)
        GButton_841["bg"] = "#ffffff"
        GButton_841["fg"] = "#000000"
        GButton_841["justify"] = "center"
        GButton_841["image"] = self.SAVE_IMG
        GButton_841.place(x=220, y=100, width=73, height=30)
        GButton_841["command"] = lambda *args: self.GButton_841_command(root)

###############################################################################
        self.GLabel_828 = tk.Label(root)
        self.GLabel_828["fg"] = "#333333"
        self.GLabel_828["text"] = ""
        self.GLabel_828.place(x=10, y=40, width=205, height=30)

        self.GLabel_44 = tk.Label(root)
        self.GLabel_44["fg"] = "#333333"
        self.GLabel_44["text"] = ""
        self.GLabel_44.place(x=10, y=100, width=205, height=30)

        self.page_size = ttk.Combobox(root, width=5, state="readonly")

        # Adding combobox drop down list
        self.page_size['values'] = ('A4', 'A5', 'A6', 'A7')
        self.page_size.place(x=320, y=70)

        # Shows february as a default value
        self.page_size.current(0)

        GLabel_70 = tk.Label(root)
        GLabel_70["bg"] = "#ffffff"
        GLabel_70["fg"] = "#333333"
        GLabel_70["justify"] = "left"
        GLabel_70.place(x=10, y=20, width=70, height=10)
        GLabel_70["text"] = "Source :"

        GLabel_720 = tk.Label(root)
        GLabel_720["bg"] = "#ffffff"
        GLabel_720["fg"] = "#333333"
        GLabel_720["justify"] = "left"
        GLabel_720.place(x=10, y=80, width=78, height=10)
        GLabel_720["text"] = "Destination :"

        GLabel_240 = tk.Label(root)
        GLabel_240["bg"] = "#ffffff"
        GLabel_240["fg"] = "#bfbfbf"
        GLabel_240["text"] = "Pdf2Booklet : bruhmesepython"
        GLabel_240.place(x=220, y=140, width=162, height=30)

        GLabel_163 = tk.Label(root)
        GLabel_163["bg"] = "#ffffff"
        GLabel_163["fg"] = "#333333"
        GLabel_163["text"] = "dpi"
        GLabel_163.place(x=350, y=100, width=35, height=30)

        self.Gtext_dpi = tk.Text(root)
        self.Gtext_dpi.insert(1.0, 100)
        self.Gtext_dpi.place(x=325, y=100, width=35, height=20)
###############################################################################

    def GButton_958_command(self):
        self.PATH = tk.filedialog.askopenfilename()
        self.GLabel_828["text"] = self.PATH

    def GButton_841_command(self, root):
        if path.exists(self.PATH) and self.PATH != "":
            self.SAVEPATH = tk.filedialog.asksaveasfilename()
            if self.SAVEPATH != "":

                self.GLabel_574 = tk.Label(root)
                self.GLabel_574["bg"] = "#ffffff"
                self.GLabel_574["fg"] = "#333333"
                self.GLabel_574["justify"] = "center"
                self.GLabel_574["text"] = "Converting.."
                self.GLabel_574.place(x=0, y=0, width=380, height=157)

                self.GLabel_44["text"] = self.SAVEPATH
                self.main_function(self.PATH, self.SAVEPATH,
                                   self.page_size.get(), int(self.Gtext_dpi.get(1.0, END)))
                messagebox.showinfo("Conversion complete",
                                    "File saved as " + self.SAVEPATH + ".pdf")
                self.GLabel_574.destroy()
        else:
            messagebox.showerror("Error", "Error : Bad Path")
