import os
import camera
import image_select
import PySimpleGUI as sg
import prediction

#Define first window
win_get_cam2 = sg.Window('Which method?',[[sg.T('Which method?')],[sg.Combo(['Camera', 'Folder'], default_value='Camera', font='any 20')],[sg.T(size=(1,2))], [sg.Ok()]], location=(0,0))
event, values = win_get_cam2.read()
win_get_cam2.close()

if event == 'Ok':
    if values[0] == 'Camera': 
        method = 'C'
    elif values[0] == 'Folder':
        method = 'F'


if method == 'C':
    img = camera.capture() #img = file path
elif method == 'F':
    img = image_select.select()

cat_breed = prediction.predicts(img)

#Define layout
layout = [[sg.Text('Your cat breed is most likely a: ')],
          [sg.Text(cat_breed)],
          [sg.Button('Information')]]

window = sg.Window('Prediction', layout, resizable=True)

while True:
    #Event loop
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    if event == 'Information':
        path = rf'C:\Users\johnj\OneDrive\Desktop\Coding\Cat Recognition APP\Cat Information\{cat_breed}.txt'
        with open(rf"{path}", 'r', encoding='utf8') as fp:
            lines = ""
            for line in fp:
                lines += (line.strip())
                lines += "\n"

        #Define second window
        win_get_cam3 = sg.Window(f'{cat_breed}',[[sg.Text(lines)], [sg.Ok()]], location=(0,0))
        event2, values2 = win_get_cam3.read()
        win_get_cam2.close()

        if event2 == 'Ok':
            exit()
