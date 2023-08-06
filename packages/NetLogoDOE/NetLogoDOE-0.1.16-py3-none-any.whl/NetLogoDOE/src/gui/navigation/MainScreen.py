import PySimpleGUI as sg
from NetLogoDOE.src.gui.custom_components import header, explanation, question_mark


class MainScreen:

    def __init__(self):
        button_size = (25, 1)
        button_pad = ((0, 0), (20, 0))
        self.layout = [[header('NetLogoDOE')],
                       [sg.Button('Experimental runs', key='main_experiment_button', size=button_size, pad=button_pad),
                        question_mark('Help')],
                       [explanation('whatever needs ot be said')],
                       [sg.Button('Standard runs', key='main_standard_button', size=button_size, pad=button_pad),
                        question_mark('Help')],
                       [explanation('whatever needs ot be said')],
                       [sg.Button('Import results', key='main_import_button', size=button_size, pad=button_pad),
                        question_mark('Help')],
                       [explanation('whatever needs ot be said')],
                       [sg.Button('Close', key='main_close_button', pad=button_pad)]]

    def check_events(self, event, values, window):
        if event == 'main_experiment_button':
            window['main_panel'].update(visible=False)
            window['experiment_panel'].update(visible=True)
        if event == 'main_standard_button':
            window['main_panel'].update(visible=False)
            window['standard_panel'].update(visible=True)
        if event == 'main_import_button':
            window['main_panel'].update(visible=False)
            window['import_panel'].update(visible=True)
