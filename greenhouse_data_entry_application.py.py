import tkinter as tk
# from tkinter import ttk
import ttkbootstrap as ttk
import csv
from pathlib import Path
from datetime import datetime

def initialize():
    global rec_info, env_info, plant_info
    frame = [rec_info, env_info, plant_info]
    for f in frame:
        for w in f.winfo_children():
            w.focus()
def on_submit():
    global variables, notes, invalid
    initialize()

    ### CHECKING invalid varaible is sync with validation 
    for k, v in invalid.items():
        print(f'{k}: {v}')
    
    if all([v for k, v in invalid.items()]):
        d = {}
        for k, v in variables.items():
            d[k] = v.get()
        d['Notes'] = notes.get('1.0', tk.END).strip()
        
        datestr = datetime.today().strftime('%Y-%m-%d')
        filename = f'abq-{datestr}.csv'
        newfile = not Path(filename).exists()

        with open(filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=d.keys())
            if newfile:
                writer.writeheader()
            writer.writerow(d)
        on_reset()
    else:
        print("NO SUBMIT")
    
    # print(d)

def on_reset():
    global variables, notes, timelist, labstr
    for k, v in variables.items():
        if k=='Equipment Fault':
            v.set(False)
        else:
            v.set('')
    variables['Date'].set(datetime.today().strftime('%Y-%m-%d'))
    variables['Time'].set(timelist[0])
    variables['Lab'].set(labstr[0])
    notes.delete('1.0', tk.END)

 ## VALIDATIONS   

def valid_date(entry):
    global invalid
    valid = False
    if len(entry) == 10 and entry[4]=='-' and entry[7]=='-' and entry.replace('-', '').isdigit():
        valid = True
    invalid['Date'] = valid
    return valid


def valid_time(entry):
    global invalid, timelist
    valid = False
    if entry in timelist:
        valid = True
    invalid['Time'] = valid
    return valid


def valid_lab(entry):
    global invalid
    valid = False
    if True:
        valid = True
    invalid['Lab'] = valid
    return valid

## BEGINNING TEMPLATES FOR VALIDATION

def valid_technician(entry):
    global invalid
    valid = False
    entry = entry.strip()
    if entry.count(' ')==1 and entry.replace(' ', '').isalpha():
        valid = True
    invalid['Technician'] = valid
    return valid


def valid_plot(entry):
    global invalid
    valid = False
    if entry.isdigit():
            value = int(entry)
            if value>=0 and value<=20:
                valid = True
    invalid['Plot'] = valid
    return valid


def valid_seed_sample(entry):
    global invalid
    valid = False
    if entry.isalnum() and len(entry)==6:
        valid = True
    invalid['Seed Sample'] = valid
    return valid

## BEGINNING ME

def valid_humidity(entry):
    global invalid, variables
    valid = False
    entry = entry.strip()
    if not variables['Equipment Fault'].get():
        if entry.count('.')<=1 and entry.replace('.', '').isdigit():
            value = float(entry)
            if value>=0.5 and value<=52:
                valid = True
    else:
        valid = True
    invalid['Humidity'] = valid
    return valid


def valid_light(entry):
    global invalid, variables
    valid = False
    if not variables['Equipment Fault'].get():
        if entry.count('.')<=1 and entry.replace('.', '').isdigit():
            value = float(entry)
            if value>=0 and value<=100:
                valid = True
    else:
        valid = True
    invalid['Light'] = valid
    return valid


def valid_temperature(entry):
    global invalid, variables
    valid = False
    if not variables['Equipment Fault'].get():
        if entry.count('.')<=1 and entry.replace('.', '').isdigit():
            value = float(entry)
            if value>=4 and value<=40:
                valid = True
    else:
        valid = True
    invalid['Temperature'] = valid
    return valid


## ENDING ME


def valid_plants(entry):
    global invalid
    valid = False
    if entry.isdigit():
            value = int(entry)
            if value>=0 and value<=20:
                valid = True
    invalid['Plants'] = valid
    return valid


def valid_blossoms(entry):
    global invalid
    valid = False
    if entry.isdigit():
            value = int(entry)
            if value>=0 and value<=1000:
                valid = True
    invalid['Blossoms'] = valid
    return valid


def valid_fruit(entry):
    global invalid
    valid = False
    if entry.isdigit():
            value = int(entry)
            if value>=0 and value<=1000:
                valid = True
    invalid['Fruit'] = valid
    return valid


def valid_min_height(entry):
    global invalid
    valid = False
    if entry.count('.')<=1 and entry.replace('.', '').isdigit():
        value = float(entry)
        if value>=0 and value<=1000:
            valid = True
    invalid['Min Height'] = valid
    return valid


def valid_max_height(entry):
    global invalid
    valid = False
    if entry.count('.')<=1 and entry.replace('.', '').isdigit():
        value = float(entry)
        if value>=0 and value<=1000:
            valid = True
    invalid['Max Height'] = valid
    return valid


def valid_median_height(entry):
    global invalid
    valid = False
    if entry.count('.')<=1 and entry.replace('.', '').isdigit():
        value = float(entry)
        if value>=0 and value<=1000:
            valid = True
    invalid['Median Height'] = valid
    return valid

## END TEMPLATES FOR VALIDATION
    

root = tk.Tk()
root.title('ABQ Data Entry Application')
root.columnconfigure(0, weight=1)

HEADERS = ['Date', 'Time', 'Technician', 'Lab', 'Plot', 'Seed Sample', 'Humidity', 'Light', 'Temperature', 'Equipment Fault', 'Plants', 'Blossoms', 'Fruit', 'Min Height', 'Max Height', 'Median Height']

variables = {h: tk.StringVar() for h in HEADERS if h != 'Equipment Fault'}
variables['Equipment Fault'] = tk.BooleanVar()
invalid = {h: False for h in HEADERS}
invalid['Lab'] = True
invalid['Equipment Fault'] = True

timelist = ['8:00', '12:00', '16:00', '20:00']

labstr = "ABC"

ttk.Label(
    root,
    text='ABQ Data Entry Application',
    font=('TkDefaultFont', 16),
).grid()

drf = ttk.Frame(root)
drf.grid(
    padx=10,
    sticky=tk.E+tk.W
)
drf.columnconfigure(0, weight=1)


# RECORD INFORMATION

rec_info = ttk.LabelFrame(
    drf,
    text='Record Information',
)
rec_info.grid(pady=5, sticky=tk.E+tk.W)
for i in range(3):
    rec_info.columnconfigure(i, weight=1)

ttk.Label(
    rec_info,
    text='Date',
    anchor=tk.W,
    justify=tk.LEFT,
).grid(row=0, column=0, sticky=tk.E+tk.W)
ttk.Entry(
    rec_info,
    textvariable=variables['Date'],
    validate='focusout',
    validatecommand=(root.register(valid_date), '%P')
).grid(row=1, column=0, sticky=tk.E+tk.W)

ttk.Label(
    rec_info,
    text='Time',
    anchor=tk.W,
    justify=tk.LEFT,
).grid(row=0, column=1, sticky=tk.E+tk.W)
ttk.Combobox(
    rec_info,
    values=timelist,
    textvariable=variables['Time'],
    validate='focusout',
    validatecommand=(root.register(valid_time), '%P'),
).grid(row=1, column=1, sticky=tk.E+tk.W)

ttk.Label(
    rec_info,
    text='Technician',
    anchor=tk.W,
    justify=tk.LEFT,
).grid(row=0, column=2, sticky=tk.E+tk.W)
ttk.Entry(
    rec_info,
    textvariable=variables['Technician'],
    validate='focusout',
    validatecommand=(root.register(valid_technician), '%P'),
).grid(row=1, column=2, sticky=tk.E+tk.W)

ttk.Label(
    rec_info,
    text='Lab',
    anchor=tk.W,
    justify=tk.LEFT,
).grid(row=2, column=0, sticky=tk.E+tk.W)

rbf = ttk.Frame(
    rec_info
)
rbf.grid(row=3, column=0, sticky=tk.E+tk.W)

for i, v in enumerate(labstr):
    rbf.columnconfigure(i, weight=1)
    ttk.Radiobutton(
        rbf,
        text=v,
        value=v,
    ).grid(row=0, column=i, sticky=tk.E+tk.W)

ttk.Label(
    rec_info,
    text='Plot',
    anchor=tk.W,
    justify=tk.LEFT,
).grid(row=2, column=1, sticky=tk.E+tk.W)
ttk.Combobox(
    rec_info,
    values=list(range(1, 21)),
    textvariable=variables['Plot'],
    validate='focusout',
    validatecommand=(root.register(valid_plot), '%P'),
).grid(row=3, column=1, sticky=tk.E+tk.W)

ttk.Label(
    rec_info,
    text='Seed Sample',
    anchor=tk.W,
    justify=tk.LEFT,
).grid(row=2, column=2, sticky=tk.E+tk.W)
ttk.Entry(
    rec_info,
    textvariable=variables['Seed Sample'],
    validate='focusout',
    validatecommand=(root.register(valid_seed_sample), '%P')
).grid(row=3, column=2, sticky=tk.E+tk.W)


# ENVIRONMENTAL DATA


env_info = ttk.LabelFrame(
    drf,
    text='Environmental Data'
)
env_info.grid(pady=5, sticky=tk.E+tk.W)
for i in range(3):
    env_info.columnconfigure(i, weight=1)

ttk.Label(
    env_info,
    text='Humidity',
    anchor=tk.W,
    justify=tk.LEFT,
).grid(row=0, column=0, sticky=tk.E+tk.W)
ttk.Spinbox(
    env_info,
    from_=0.5,
    to=52.0,
    increment=0.1,
    textvariable=variables['Humidity'],
    validate='focusout',
    validatecommand=(root.register(valid_humidity), '%P'),
).grid(row=1, column=0, sticky=tk.E+tk.W)

ttk.Label(
    env_info,
    text='Light',
    anchor=tk.W,
    justify=tk.LEFT,
).grid(row=0, column=1, sticky=tk.E+tk.W)
ttk.Spinbox(
    env_info,
    from_=0.0,
    to=100.0,
    increment=0.1,
    textvariable=variables['Light'],
    validate='focusout',
    validatecommand=(root.register(valid_light), '%P'),
).grid(row=1, column=1, sticky=tk.E+tk.W)

ttk.Label(
    env_info,
    text='Temperature',
    anchor=tk.W,
    justify=tk.LEFT,
).grid(row=0, column=2, sticky=tk.E+tk.W)
ttk.Spinbox(
    env_info,
    from_=4.0,
    to=40.0,
    increment=0.1,
    textvariable=variables['Temperature'],
    validate='focusout',
    validatecommand=(root.register(valid_temperature), '%P'),
).grid(row=1, column=2, sticky=tk.E+tk.W)

ttk.Checkbutton(
    env_info,
    text='Equipment Fault',
    variable=variables['Equipment Fault'],
    bootstyle="round-toggle"
).grid(row=2, column=0, sticky=tk.E+tk.W)


# PLANT DATA


plant_info = ttk.LabelFrame(
    drf,
    text='Plant Data'
)
plant_info.grid(pady=5, sticky=tk.E+tk.W)
for i in range(3):
    plant_info.columnconfigure(i, weight=1)

ttk.Label(
    plant_info,
    text='Plants',
    anchor=tk.W,
    justify=tk.LEFT,
).grid(row=0, column=0, sticky=tk.E+tk.W)
ttk.Spinbox(
    plant_info,
    from_=0,
    to=20,
    increment=1,
    textvariable=variables['Plants'],
    validate='focusout',
    validatecommand=(root.register(valid_plants), '%P')
).grid(row=1, column=0, sticky=tk.E+tk.W)

ttk.Label(
    plant_info,
    text='Blossoms',
    anchor=tk.W,
    justify=tk.LEFT,
).grid(row=0, column=1, sticky=tk.E+tk.W)
ttk.Spinbox(
    plant_info,
    from_=0,
    to=1000,
    increment=1,
    textvariable=variables['Blossoms'],
    validate='focusout',
    validatecommand=(root.register(valid_blossoms), '%P')
).grid(row=1, column=1, sticky=tk.E+tk.W)

ttk.Label(
    plant_info,
    text='Fruit',
    anchor=tk.W,
    justify=tk.LEFT,
).grid(row=0, column=2, sticky=tk.E+tk.W)
ttk.Spinbox(
    plant_info,
    from_=0,
    to=1000,
    increment=1,
    textvariable=variables['Fruit'],
    validate='focusout',
    validatecommand=(root.register(valid_fruit), '%P')
).grid(row=1, column=2, sticky=tk.E+tk.W)

ttk.Label(
    plant_info,
    text='Min Height',
    anchor=tk.W,
    justify=tk.LEFT,
).grid(row=2, column=0, sticky=tk.E+tk.W)
ttk.Spinbox(
    plant_info,
    from_=0.0,
    to=1000.0,
    increment=0.5,
    textvariable=variables['Min Height'],
    validate='focusout',
    validatecommand=(root.register(valid_min_height), '%P')
).grid(row=3, column=0, sticky=tk.E+tk.W)

ttk.Label(
    plant_info,
    text='Max Height',
    anchor=tk.W,
    justify=tk.LEFT,
).grid(row=2, column=1, sticky=tk.E+tk.W)
ttk.Spinbox(
    plant_info,
    from_=0.0,
    to=1000.0,
    increment=0.5,
    textvariable=variables['Max Height'],
    validate='focusout',
    validatecommand=(root.register(valid_max_height), '%P')
).grid(row=3, column=1, sticky=tk.E+tk.W)

ttk.Label(
    plant_info,
    text='Median Height',
    anchor=tk.W,
    justify=tk.LEFT,
).grid(row=2, column=2, sticky=tk.E+tk.W)
ttk.Spinbox(
    plant_info,
    from_=0.0,
    to=1000.0,
    increment=0.5,
    textvariable=variables['Median Height'],
    validate='focusout',
    validatecommand=(root.register(valid_median_height), '%P')
).grid(row=3, column=2, sticky=tk.E+tk.W)

# NOTES

note_info = ttk.LabelFrame(
    drf,
    text='Notes'
)
note_info.grid(pady=5, sticky=tk.E+tk.W)
note_info.columnconfigure(0, weight=1)
notes = tk.Text(
    note_info,
    height=10,
    width=80
)
notes.grid(sticky=tk.E+tk.W)

# BUTTONS

bframe = ttk.Frame(
    drf
)
bframe.grid(sticky=tk.E+tk.W)
for i in range(3):
    bframe.columnconfigure(i, weight=1, uniform='b')

buttons = ttk.Frame(
    bframe
)
buttons.grid(row=0, column=2, sticky=tk.E+tk.W)
for i in range(2):
    buttons.columnconfigure(i, weight=1)

ttk.Button(
    buttons,
    text='Reset',
    command=on_reset
).grid(row=0, column=0, padx=5, sticky=tk.E+tk.W)

ttk.Button(
    buttons,
    text='Submit',
    command=on_submit
).grid(row=0, column=1, padx=5, sticky=tk.E+tk.W)


on_reset()
root.after(100, initialize)
root.mainloop()