import PySimpleGUI as sg
import cv2
import os

def capture():
    CAMERA_FRONT = 1
    CAMERA_REAR = 0

    win_get_cam = sg.Window('Which method?',[[sg.T('Which method?')],[sg.Combo(['Camera', 'Folder'], default_value='Camera', font='any 20')],[sg.T(size=(1,2))], [sg.Ok()]], location=(0,0))
    event, values = win_get_cam.read()
    win_get_cam.close()

    if event != 'Ok': 
        exit()

    USE_CAMERA = [CAMERA_FRONT, CAMERA_REAR][values[0]=='Rear']


    # define the window layout
    layout = [
            [sg.Image(filename='', key='-IMAGE-')],
            [sg.Button('Save')],
            [sg.Exit()]
            ]
    layout2 = [
            [sg.Text('File name:', size =(15, 1)), sg.InputText()],
            [sg.Button('Confirm')]
            ]

    # create the window
    window = sg.Window('Demo Application - OpenCV Integration', layout, location=(0, 0),
                    no_titlebar=True, grab_anywhere=True)
    window2 = sg.Window('filename', layout2)

    cap = cv2.VideoCapture(USE_CAMERA) 
    while True:
        event, values = window.read(timeout=20)
        ret, frame = cap.read()                      
        imgbytes=cv2.imencode('.png', frame)[1].tobytes() 
        window['-IMAGE-'].update(data=imgbytes)

        if event in ('Exit', None):
            break

        elif event == ('Save'):
            while True:
                event2, value2 = window2.read()
                if event2 == ('Confirm'):
                    FILENAME=f'{value2[0]}.jpg'
                    cv2.imwrite(filename=FILENAME, img=frame)
                    return os.getcwd(FILENAME) #returns file path
                
                if event2 == sg.WIN_CLOSED:
                    break

    window.close()
    window2.close()
