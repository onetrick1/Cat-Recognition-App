import PySimpleGUI as sg
# import PySimpleGUIQt as sg
import os.path
import PIL.Image
import io
import base64

def select():
    def convert_to_bytes(file_or_bytes, resize=None):
        '''
        Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
        Turns into  PNG format in the process so that can be displayed by tkinter
        :param file_or_bytes: either a string filename or a bytes base64 image object
        :type file_or_bytes:  (Union[str, bytes])
        :param resize:  optional new size
        :type resize: (Tuple[int, int] or None)
        :return: (bytes) a byte-string object
        :rtype: (bytes)
        '''
        if isinstance(file_or_bytes, str):
            img = PIL.Image.open(file_or_bytes)
        else:
            try:
                img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
            except Exception as e:
                dataBytesIO = io.BytesIO(file_or_bytes)
                img = PIL.Image.open(dataBytesIO)

        cur_width, cur_height = img.size
        if resize:
            new_width, new_height = resize
            scale = min(new_height/cur_height, new_width/cur_width)
            img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
        with io.BytesIO() as bio:
            img.save(bio, format="PNG")
            del img
            return bio.getvalue()



    #Define layout
    left_col = [[sg.Text('Folder'), sg.In(size=(25,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse()],
                [sg.Listbox(values=[], enable_events=True, size=(40,20),key='-FILE LIST-')],
                [sg.Text('Resize to'), sg.In(key='-W-', size=(5,1)), sg.In(key='-H-', size=(5,1))]]

    images_col = [[sg.Text('You choose from the list:')],
                [sg.Text(size=(40,1), key='-TOUT-')],
                [sg.Image(key='-IMAGE-')]]

    selection = [
        [sg.Button('Select')]
    ]

 
    layout = [[sg.Column(left_col, element_justification='c'), sg.VSeperator(),sg.Column(images_col, element_justification='c'), sg.Column(selection)]]

    #Create window
    window = sg.Window('Multiple Format Image Viewer', layout,resizable=True)

    #Event loop
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        if event == 'Select':
            return os.path.join(values['-FOLDER-'], values['-FILE LIST-'][0]) #returns the selected image path

        if event == '-FOLDER-': 
            folder = values['-FOLDER-']
            try:
                file_list = os.listdir(folder)
            except:
                file_list = []
            fnames = [f for f in file_list if os.path.isfile(
                os.path.join(folder, f)) and f.lower().endswith((".png", ".jpg", "jpeg", ".tiff", ".bmp"))]
            window['-FILE LIST-'].update(fnames)

        elif event == '-FILE LIST-':    # A file was chosen from the listbox
            try:
                filename = os.path.join(values['-FOLDER-'], values['-FILE LIST-'][0])
                window['-TOUT-'].update(filename)
                if values['-W-'] and values['-H-']:
                    new_size = int(values['-W-']), int(values['-H-'])
                else:
                    new_size = None
                window['-IMAGE-'].update(data=convert_to_bytes(filename, resize=new_size))

            except Exception as E:
                print(f'** Error {E} **')
                pass        # something weird happened making the full filename
        
        try:
            if event == 'Select':
                window.close()
                return filename
        except:
            pass

    window.close()
