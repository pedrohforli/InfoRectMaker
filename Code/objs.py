import pygame, time, os, pickle
from tkinter.filedialog import *
from tkinter.messagebox import showwarning
from tkinter import *
from PIL import ImageTk
from PIL import Image

GREEN = "#05e2e2"

class Program(object):
    def __init__(self, root):
        #The root of the tkinter app
        self.root = root

        #We create the first frame for the title of the app
        self.frame1 = Frame(root, pady = 50)
        self.frame1['background'] = GREEN

        #The second frame will maintain the box for the app
        self.frame2 = Frame(root)
        self.frame2['background'] = GREEN

        #The third frame will maintain the status of the app
        self.frame3 = Frame(root, pady = 50)
        self.frame3['background'] = GREEN

        #We initialize a first font
        self.font1 = ('Verdana', '36', 'bold')
        self.font2 = ('Verdana', '20', 'bold')
        self.font3 = ('Verdana', '14', 'bold')

        #We initialize our title
        self.title = Label(self.frame1, text  = "Obtain Rectangles by Pedro Forli", font = self.font1, bg = GREEN)
        self.title.pack()

        #Open the file that contains the info about the program
        try:
            arq = open(os.path.join("conf",'rect.conf'), 'rb')
        except FileNotFoundError:
            self.conf = {"cwd": os.getcwd(), "out": os.getcwd()}
            self.conf_save()
        else:
            self.conf = pickle.load(arq)

        #Label saying about the output
        input_label = Label(self.frame2, text  = "Input Folder", font = self.font2, bg = GREEN, padx = 50)
        input_label.grid(row = 0, column = 0, sticky = W)

        #We put the entry for text containing the path to the folder
        self.folder_entry = Entry(self.frame2, font = self.font3, width = 30)
        self.folder_entry.insert(0, self.conf['cwd'])
        self.folder_entry.grid(row = 0, column = 1)

        #We open the image and add it to the folder button
        self.loaded_img = Image.open(os.path.join("images", "folder.png"))
        self.loaded_img = self.loaded_img.resize((20,20))
        self.folder_img = ImageTk.PhotoImage(image = self.loaded_img)
        self.folder_button = Button(self.frame2, image = self.folder_img, command = self.AskDirectoryInput)
        self.folder_button.grid(row = 0, column = 2)

        #Label saying about the output
        out = Label(self.frame2, text  = "Output Folder", font = self.font2, bg = GREEN, padx = 50)
        out.grid(row = 1, column = 0, sticky = W)

        #We put the entry for text containing the path to the folder
        self.folder_out = Entry(self.frame2, font = self.font3, width = 30)
        self.folder_out.insert(0, self.conf['out'])
        self.folder_out.grid(row = 1, column = 1)

        #We open the image and add it to the folder button
        self.folder_outB = Button(self.frame2, image = self.folder_img, command = self.AskDirectoryOutput)
        self.folder_outB.grid(row = 1, column = 2)

        #And we also create a label and entry to the filename
        file_label = Label(self.frame2, text  = "Filename", font = self.font2, bg = GREEN, padx = 50)
        file_label.grid(row = 2, column = 0, sticky = W)
        self.file_entry = Entry(self.frame2, font = self.font3, width = 30)
        self.file_entry.grid(row = 2, column = 1)

        #And we create a default check button
        self.default = Checkbutton(self.frame2, text = "default", font = self.font3, bg = GREEN, command = self.setFilename)
        self.default.deselect()
        self.default.grid(row = 2, column = 3, sticky = E)
        self.default_var = False

        #Snoopy image to be putted
        self.snoop = MyLabel(self.frame3, os.path.join("images", "snoop.gif"))
        self.snoop.grid(row = 0, rowspan = 2, column = 0, sticky = W, padx = 90)

        #We create a go button
        self.go_button = Button(self.frame3, font = self.font3, text = "GO", command = self.GO, width = 30, height = 2)
        self.go_button.grid(row = 0, column = 1)

        #And we create a label for the status
        self.status = Label(self.frame3, text = "", font = self.font2, bg = GREEN)
        self.status.grid(row = 1, column = 1)

        #Then we pack the frames
        self.frame1.pack()
        self.frame2.pack(fill = BOTH)
        self.frame3.pack(fill = BOTH)

    def conf_save(self):
        arq = open(os.path.join("conf",'rect.conf'), 'wb')
        pickle.dump(self.conf, arq)
        arq.close()

    def setFilename(self):
        """
        Change the default configurations
        :return:
        """
        if self.default_var:
            self.file_entry["bg"] = "white"
            self.file_entry["state"] = NORMAL
        else:
            self.file_entry["bg"] = "gray"
            self.file_entry.delete(0, END)
            self.file_entry.insert(0, "crop_rect")
            self.file_entry["state"] = DISABLED

        self.default_var = not self.default_var

    def AskDirectoryInput(self):
        """
        Sets a given directory to work as input
        """
        directory = askdirectory(initialdir = self.conf["cwd"])
        self.folder_entry.delete(0, END)
        self.folder_entry.insert(0, directory)
        self.conf["cwd"] = directory

    def AskDirectoryOutput(self):
        """
        Sets a given directory to work as output
        """
        directory = askdirectory(initialdir = self.conf["out"])
        self.folder_out.delete(0, END)
        self.folder_out.insert(0, directory)
        self.conf["out"] = directory

    def GO(self, event = None):
        """
        Método que manda tudo o que o usuário digitou
        para o programa, e processa o que foi digitado
        """
        #We get the valid input dir
        self.input_dir = self.folder_entry.get()
        if self.input_dir == "" or not os.path.exists(self.input_dir):
            if os.path.exists(os.path.join(os.getcwd(), self.input_dir)):
                self.input_dir = os.path.join(os.getcwd(), self.input_dir)
            else:
                showwarning(self.root, message = "Please Select a valid input dir")
                return

        #And the valid output dir
        self.output_dir = self.folder_out.get()
        if self.output_dir == "" or not os.path.exists(self.output_dir):
            if os.path.exists(os.path.join(os.getcwd(), self.output_dir)):
                self.output_dir = os.path.join(os.getcwd(), self.output_dir)
            else:
                showwarning(self.root, message = "Please Select a valid output dir")
                return

        #Get the output filename
        name = self.file_entry.get() if self.file_entry.get() != "" else "crop_rect"
        self.filename = os.path.join(self.output_dir, name) + ".txt"

        #We open an archive to store the info
        self.archive = open(self.filename, 'w')

        #We read the images on the directory
        self.lista = os.listdir(self.input_dir)
        supported = ".jpg", '.png', '.gif', '.bmp', '.pcx', '.tga', '.tif', '.lbm', '.pbm', '.pgm', '.ppm', '.xpm'
        #And select only the valid images
        for arq in self.lista.copy():
            #Checks if arq is a file
            if not os.path.isdir(arq):
                #Gets the file extension
                file_extension = os.path.splitext(arq)[1]
                #And check if it is supported
                if file_extension not in supported:
                    #If not remove it
                    self.lista.remove(arq)
            else:
                self.lista.remove(arq)

        #Number of files to run
        self.size = len(self.lista)

        if self.size == 0:
            showwarning(self.root, message = "There is no valid images on the directory")
            return

        #We start a counter of images as 0
        self.cont = 0

        self.snoop.play()

        self.root.after(50, self.Control)

    def Control(self):
        """
        The control method is used to loop throw the images that are inside the folder
        """
        #Then we update the status text
        self.status["text"] = "%i/%i     0%%"%(self.cont, self.size)

        img = self.lista[self.cont]

        #We load the image as an array
        a = pygame.surfarray.array2d(pygame.image.load(os.path.join(self.input_dir, img)))

        #We write a line to the image we are about to take info
        self.archive.write(img)

        #We set the generator
        self.gen = self.readImage(a)

        #The we process the info of the image
        self.root.after(1, self.GetsTheInfo)

        #We reopen the arquive so we can write into it
        self.archive = open(self.filename, 'a')

        #Finally we skip one line
        self.archive.write("\n")

    def GetsTheInfo(self):
        """
        Loop throw all the images on the directory and
        output a file with the rects info
        """
        #Then we should iterate over the read of the image
        try:
            i, j = next(self.gen)
        except StopIteration:
            self.cont += 1
            if self.cont < self.size:
                self.root.after(50, self.Control)
            else:
                self.status["text"] = ""
                self.snoop.stop_it()
        except Exception as E:
            print(E)
        else:
            total = self.img_size[0]*self.img_size[1]
            made = i*self.img_size[1] + j
            self.status["text"] = "%i/%i     %.1f%%"%(self.cont, self.size, 100*made/total)
            self.root.after(50, self.GetsTheInfo)

    def readImage(self, a):
        """
        Generator that reads the image
        """
        t0 = time.time()

        #The rects that has been outputted
        self.rects = {}

        #the id of each rect
        r_id = 1

        #The maximum y
        y_max = len(a[0])

        #We get the img size
        self.img_size = (len(a), y_max)

        for i in range(len(a)):
            j = 0
            while j < y_max:

                #We go throw each rect we defined
                for ids in self.rects:
                    #If the point we are is colliding with a rect
                    if self.rects[ids].collidepoint(i, j):
                        #We update the j value and continue with the loop
                        j = self.rects[ids].bottom + 1
                        continue

                #If we found a pixel that is not white
                if a[i][j] != 0:
                    #We should walk throw the y and x until a new color is hit
                    color = a[i][j]

                    #We save the left and the top
                    k, l = i, j

                    #We go throw the width
                    while a[k][j] == color:
                        k += 1

                    #Then the height
                    while a[i][l] == color:
                        l += 1

                    #We ropen the archive to we can write into it
                    self.archive = open(self.filename, 'a')

                    #Then we write down the rect info
                    self.archive.write("\trect %i = left:%i top:%i width:%i height:%i\n"%(r_id, i, j, k - i, l - j))
                    #Save the rect in the rects dictionary
                    self.rects[r_id] = pygame.rect.Rect(i, j, k - i, l - j)
                    #Update the rect id
                    r_id += 1
                    #Update the j value
                    j += l - j
                    #yield the function
                    yield i, j
                    #And finally continue to the next loop
                    continue

                #If we just spend more then 0.05 sec on this function we should yield it
                tf = time.time()
                if tf - t0 > 0.05:
                    yield i, j
                    #We reset the time for when we started the function
                    t0 = time.time()

                #We update the y direction
                j += 1

class MyLabel(Label):
    def __init__(self, master, filename):
        im = Image.open(filename)
        seq = []
        try:
            while 1:
                seq.append(im.copy())
                im.seek(len(seq)) # skip to next frame
        except EOFError:
            pass # we're done

        try:
            self.delay = im.info['duration']
        except KeyError:
            self.delay = 100

        first = seq[0].convert('RGBA')
        self.frames = [ImageTk.PhotoImage(first)]

        Label.__init__(self, master, image=self.frames[0], bg = GREEN)

        temp = seq[0]
        for image in seq[1:]:
            temp.paste(image)
            frame = temp.convert('RGBA')
            self.frames.append(ImageTk.PhotoImage(frame))

        self.idx = 0

        #self.cancel = self.after(self.delay, self.play)

    def play(self):
        self.config(image=self.frames[self.idx])
        self.idx += 1
        if self.idx == len(self.frames):
            self.idx = 0
        self.cancel = self.after(self.delay, self.play)

    def stop_it(self):
        self.after_cancel(self.cancel)

def terminate():
    """Function that power's off the game"""
    pygame.quit()
    sys.exit()
