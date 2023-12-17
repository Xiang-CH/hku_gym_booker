import tkinter as tk
import ttkbootstrap as ttk
from gym import getMetaData
import webbrowser
from pprint import pprint
from datetime import datetime

# create blank window
home = ttk.Window(themename="litera")
home.title("HKU Gym Booking")

# setting window size
home.geometry("500x430")

# get meta data
gymData = {}

# notification data
notificationData = {"flag": False}

def refreshMeta():
    global gymData
    gymData = getMetaData()
    pprint(gymData)
    if checkAvaiable():
        titleVar.set(f"Last Refreshed:" + datetime.now().strftime("%H:%M:%S"))
    gym = tabControl.tab(tabControl.select(), "text")
    dateSelection(gym)
    home.after(15000, refreshMeta)

def initMeta():
    global gymData
    gymData = getMetaData()
    pprint(gymData)
    home.after(15000, refreshMeta)

initMeta()

def popupError(s):
    popupRoot = tk.Tk()
    ttk.Label(popupRoot, text=s).pack()

    gym = notificationData["gym"]
    dateID = notificationData["dateID"]
    sessionID = notificationData["sessionID"]
    link = gymData[gym][gymData[gym][dateID]["sessions"]][sessionID]['link']
    popupButton = ttk.Button(
        popupRoot, text="Book",bootstyle="success", command=lambda link=link: book(link)
    )
    popupButton.pack()
    popupRoot.geometry("400x50+700+500")
    popupRoot.mainloop()

def checkAvaiable():
    global notificationData
    if notificationData["flag"]:
        gym = notificationData["gym"]
        dateID = notificationData["dateID"]
        sessionID = notificationData["sessionID"]

        if gymData[gym][dateID]["sessions"][sessionID]["available"] > 0:
            popupError("Slot Available!")
            notificationData["flag"] = False
            return True
        else:
            return False
    return True

def book(url):
    print(url)
    webbrowser.open("https://fcbooking.cse.hku.hk" + url)

def notify(gym, dateID, date, sessionID, session):
    global notificationData
    notificationData["flag"] = True
    notificationData["gym"] = gym
    notificationData["dateID"] = dateID
    notificationData["session"] = session
    notificationData["sessionID"] = sessionID
    titleVar.set(f"🔔 Notify Session: {date} {session}")


# tab bar
tabControl = ttk.Notebook(bootstyle="info")
tabControl.config(takefocus=0)

bactiveFrame = ttk.Frame(tabControl)
cseFrame = ttk.Frame(tabControl)


tabControl.add(bactiveFrame, text="B-Active")
tabControl.add(cseFrame, text="CSE-Active")
tabControl.pack(expand=1, fill="both")

# selection ui
def dateSelection(gym):
    grids = {"B-Active": bactiveSelectionFrame, "CSE-Active": cseSelectionFrame}
    date = {"B-Active": bactiveDate, "CSE-Active": cseDate}
    variable = {"B-Active": bactiveVariable, "CSE-Active": cseVariable}
    global labelVars, buttonVars

    for widget in grids[gym].winfo_children():
        widget.destroy()

    labelVars[gym] = [
        tk.StringVar()
        for _ in range(
            len(gymData[gym][date[gym].index(variable[gym].get())]["sessions"])
        )
    ]

    buttonVars[gym] = [
        tk.StringVar()
        for _ in range(
            len(gymData[gym][date[gym].index(variable[gym].get())]["sessions"])
        )
    ]

    for i, slot in enumerate(
        gymData[gym][date[gym].index(variable[gym].get())]["sessions"]
    ):
        today_meta = gymData[gym][date[gym].index(variable[gym].get())]
        session_time = slot["time"]
        session_available = slot["available"]
        labelVars[gym][i].set(f"{session_time}    Available:{session_available}")
        ttk.Label(grids[gym], textvariable=labelVars[gym][i]).grid(
            column=0, row=i + 1, padx=30, pady=15
        )

        # pprint(gymData[gym][date[gym].index(variable[gym].get())]["sessions"][i])

        if slot["available"] > 0:
            link = slot["link"]
            buttonVars[gym][i].set("Book")
            button = ttk.Button(
                grids[gym],
                bootstyle="success",
                textvariable=buttonVars[gym][i],
                width=10,
                command=lambda link=link: book(link),
                takefocus = 0,
            )
        else:
            buttonVars[gym][i].set("Notify")
            notifyData = [gym, today_meta['id'], today_meta['date'], today_meta['sessions'].index(slot), slot['time']]
            button = ttk.Button(
                grids[gym],
                bootstyle="primary",
                width=10,
                textvariable=buttonVars[gym][i],
                command=lambda notifyData = notifyData: notify(*notifyData),
                takefocus = 0,
            )
        button.grid(column=1, row=i + 1, padx=30, pady=15)
    grids[gym].pack(padx=30, pady=20)


# B-ACTIVE tab
bactiveDate = [item["date"] for item in gymData["B-Active"]]
bactiveVariable = tk.StringVar(bactiveFrame)
bactiveVariable.set(bactiveDate[0])  # default value

w = ttk.OptionMenu(
    bactiveFrame,
    bactiveVariable,
    bactiveVariable.get(),
    *bactiveDate,
    bootstyle="info",
    command=lambda x: dateSelection("B-Active"),
)
w.config(width=18, takefocus=0)
w.pack(padx=30, pady=(40, 20))

bactiveSelectionFrame = ttk.Frame(bactiveFrame)

# B-ACTIVE tab
cseDate = [item["date"] for item in gymData["B-Active"]]
cseVariable = tk.StringVar(cseFrame)
cseVariable.set(cseDate[0])  # default value

x = ttk.OptionMenu(
    cseFrame,
    cseVariable,
    cseVariable.get(),
    *cseDate,
    bootstyle="info",
    command=lambda x: dateSelection("CSE-Active"),
)
x.config(width=18, takefocus=0)
x.pack(padx=30, pady=(40, 20))

cseSelectionFrame = ttk.Frame(cseFrame)


labelVars = {"B-Active": [], "CSE-Active": []}
buttonVars = {"B-Active": [], "CSE-Active": []}

dateSelection("B-Active")
dateSelection("CSE-Active")

titleVar = tk.StringVar(home)
titleVar.set(f"Last Refreshed:" + datetime.now().strftime("%H:%M:%S"))
title = tk.Label(master=home, textvariable=titleVar, font=("Verdana", 15))
title.pack()

home.unbind_all('<<NextWindow>>')
home.mainloop()
