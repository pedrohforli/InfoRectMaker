from objs import *

if __name__ == '__main__':
    #Initialize pygame
    pygame.init()

    #Create Tk instance
    r = Tk()

    #Inicialize program
    p = Program(r)

    #Colocamos um titulo nela
    r.title("CRIADOR DE INFO RECT")
    r.bind('<Escape>', terminate)

    #Definimos sua geometria
    r.geometry = ("800x600")
    r.resizable(False, False)
    r.minsize(width = 800, height = 600)

    #Definimos uma cor de fundo
    r['background'] = GREEN

    def terminate():
        """Function that power's off the game"""
        p.conf_save()
        pygame.quit()
        sys.exit()

    r.protocol("WM_DELETE_WINDOW", terminate)

    #And we set the icon
    icon = Image.open(os.path.join('images','icone.ico'))
    icon = ImageTk.PhotoImage(image = icon)
    r.tk.call('wm', 'iconphoto', r._w, icon)

    #And we inicialize the app
    r.mainloop()
