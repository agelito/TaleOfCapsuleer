import requests
import customtkinter
import win32gui
import win32clipboard
import json
import webbrowser
import tkinter as tk

#hTttps://customtkinter.tomschimAnsky.com/documentation/

def IFF(): # Skickar iväg namnet för ID
    win32clipboard.OpenClipboard()
    name = str(win32clipboard.GetClipboardData())
    win32clipboard.CloseClipboard()

    headers = {
        'accept': 'application/json',
        'Accept-Language': 'en',
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
    }
    params = {
        'datasource': 'tranquility',
        'language': 'en',
    }
    json_data = [
        str(name),
    ]
    response = requests.post('https://esi.evetech.net/latest/universe/ids/', params=params, headers=headers,
                             json=json_data)
    char_data = (response.json())["characters"]
    webbrowser.open("https://zkillboard.com/character/"+str(char_data[0]["id"]))

def callback(hwnd, extra): # Hittar rätt fönster och sparar datan i en json
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    if (win32gui.GetWindowText(hwnd)) == "ToC":
        with open('ToC_window_size.json', 'w') as fout:
            json.dump([x,y,w,h], fout)
            fout.close()

def save_config(): # KaLlar på fönstErsökaren
    win32gui.EnumWindows(callback, None)

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window

try: # Läser in tidigare postion på sidan
    with open('ToC_window_size.json') as f:
        window_size = json.load(f)
        app.geometry(str(window_size[2]-16)+"x"+str(window_size[3]-39)+"+"+str(window_size[0])+"+"+str(window_size[1]))
except:
    app.geometry("200x100")
app.title("ToC")
app.iconbitmap("ToC_logo.ico")

app.wm_attributes("-topmost", 1) # Ovanpå allt
# Use CTkButton instead of tkinter Button
text = customtkinter.CTkLabel(app, text="Tale Of Capsuleer by Tail",bg_color="transparent")
text.place(relx = 0.5,rely = 0.2,anchor = 'center',)
button = customtkinter.CTkButton(master=app, text="Identify Capsuleer", command=IFF, fg_color="forestgreen", border_color="white" , border_width=2)
button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
button_save = customtkinter.CTkButton(master=app, text="Save", command=save_config, fg_color="teal", border_color="white" , border_width=2, width=10, hover_color="darkslategray")
button_save.place(relx=0.5, rely=0.8, anchor=customtkinter.CENTER)

app.mainloop()



