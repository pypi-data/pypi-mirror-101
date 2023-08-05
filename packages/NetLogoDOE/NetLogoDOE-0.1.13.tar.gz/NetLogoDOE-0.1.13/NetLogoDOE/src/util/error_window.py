import PySimpleGUI as sg


def show_error_window(text, selectable_text=''):
    if selectable_text == '':
        layout = [[sg.Text(text)],
                  [sg.CloseButton('Ok')]]
        error_window = sg.Window('Error', layout=layout, element_justification='c', finalize=True)

    else:
        layout = [[sg.Text(text)],
                  [sg.InputText(selectable_text, use_readonly_for_disable=True, disabled=True,
                                text_color='white', key='select_text')],
                  [sg.CloseButton('Ok')]]
        error_window = sg.Window('Error', layout=layout, element_justification='c', finalize=True)
        error_window['select_text'].Widget.config(readonlybackground=sg.theme_background_color())
        error_window['select_text'].Widget.config(borderwidth=0)

    error_window.read()