
def ask_yes_no(title, question):
    import tkinter
    #root=tkinter.Tk()
    result =tkinter.messagebox.askquestion(title, question)
    #root.withdraw()
    return result=='yes'

def choose_folder():
    import tkinter
    root=tkinter.Tk()
    result =tkinter.filedialog.askdirectory()
    root.withdraw()
    return result

def choose_open_file():
    import tkinter
    root=tkinter.Tk()
    result=tkinter.filedialog.askopenfile()
    root.withdraw()
    return result    

def choose_save_file():
    import tkinter
    root=tkinter.Tk()
    result=tkinter.filedialog.asksaveasfile()
    root.withdraw()
    return result  

def choose_open_files():
    import tkinter
    root=tkinter.Tk()
    result=tkinter.filedialog.askopenfiles()
    root.withdraw()
    return result     
