import tkinter
import tkinter as tk
from tkinter import messagebox
import cv2
import PIL.Image, PIL.ImageTk
import time
from tkinter.filedialog import asksaveasfilename, askopenfilename

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        # Positioning and Fullscreen
        pad = 3
        # Default 200x200
        #self._geom = '640x480+0+0'
        #window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth() - pad, window.winfo_screenheight() - pad))
        #window.bind('<F11>', self.toggle_geom)

        # Menu
        menu = tkinter.Menu(window)
        # Menu Buttons
        home_item = tkinter.Menu(menu, tearoff=0)
        file_item = tkinter.Menu(menu, tearoff=0)
        edit_item = tkinter.Menu(menu, tearoff=0)
        help_item = tkinter.Menu(menu, tearoff=0)
        # File Buttons
        file_item.add_command(label='Open', command=self.open_file)
        file_item.add_separator()
        file_item.add_command(label='Save', command=self.save_file)
        file_item.add_separator()
        # Edit Buttons
        #Make Full Screen

        # Help Buttons
        help_item.add_command(label="About", command=self.about_help)

        # Edit Buttons
        menu.add_cascade(label='Home', menu=home_item)
        menu.add_cascade(label='File', menu=file_item)
        menu.add_cascade(label='Edit', menu=edit_item)
        menu.add_cascade(label='Run', command=self.run)
        menu.add_cascade(label='Help', menu=help_item)
        menu.add_cascade(label='Exit', command=self.exit)
        window.config(menu=menu)

        with open('myDataFile.text') as f:
            myDataList = f.read().splitlines()

        # Video
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)
        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        print(self.vid.width)
        print(self.vid.height)
        self.canvas.pack()
        # Button that lets the user take a snapshot
        self.btn_snapshot = tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.N, expand=True)
        # Testing a second button
        self.btn_barcode = tkinter.Button(window, text="Scan for Barcode", command=self.barcode)
        self.btn_barcode.pack(anchor=tkinter.N, expand=True)
        self.btn_stop_scan = tkinter.Button(window, text="Stop Scan", command=self.barcode)
        self.btn_stop_scan.pack(anchor=tkinter.N, expand=True)
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            popup = tkinter.Tk()
            popup.wm_title("!")
            label = tkinter.Label(popup, text="Snapshot Taken", font=("Verdana",10))
            label.pack()

    def barcode(self):
        print("Barcode")

    def toggle_geom(self, event):
        geom = self.window.winfo_geometry()
        print(geom, self._geom)
        self.window.geometry(self._geom)
        self._geom = geom

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
        self.window.after(self.delay, self.update)

    # Run
    def run(self):
        tk.messagebox.showinfo('Return', 'Application Run ')

    # Open
    def open_file(self):
        """Open a file for editing."""
        filepath = askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        txt_edit.delete(1.0, tk.END)
        with open(filepath, "r") as input_file:
            text = input_file.read()
            txt_edit.insert(tk.END, text)
        self.window.title(f"Simple Text Editor - {filepath}")

    # Save
    def save_file(self):
        """Save the current file as a new file."""
        filepath = asksaveasfilename(
            defaultextension="txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = txt_edit.get(1.0, tk.END)
            output_file.write(text)
        self.window.title(f"Simple Text Editor - {filepath}")

    def about_help(self):
        about = tkinter.Tk()
        about.wm_title("About")
        label = tkinter.Label(about, text="Version", font=("Verdana", 10))
        label.pack()

    # Exit
    def exit(self):
        MsgBox = tk.messagebox.askquestion('Exit Application', 'Are you sure you want to exit the application?', icon='warning')
        if MsgBox == 'yes':
            self.window.quit()
            self.window.destroy()
        else:
            tk.messagebox.showinfo('Return', 'You will now return to the application')

class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the Application object
App(tkinter.Tk(), "Barcode Scanner")