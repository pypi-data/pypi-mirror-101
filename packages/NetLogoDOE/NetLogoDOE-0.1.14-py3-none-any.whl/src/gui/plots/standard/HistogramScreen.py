import PySimpleGUI as sg
import plotly.graph_objects as go
from src.util.data_processing.merge_standard_data import merge_data
from src.gui.custom_components import title, question_mark, metric3_radio_buttons


class HistogramScreen:

    def __init__(self):
        question_mark_padding = ((0, 0), (0, 0))
        self.layout = [[title('Histogram')],
                       [sg.Text('Graph Title: '), sg.Input('', key='histogram_title_input')],
                       [sg.Text('Reporters to plot:'), question_mark('Help', padding=question_mark_padding)],
                       [sg.Multiline('', key='histogram_reporter_input')],
                       [sg.Text('Only input a single reporter on each line')],
                       [sg.Text('Metric:'), question_mark('Help', padding=question_mark_padding)],
                       metric3_radio_buttons('histogram'),
                       [sg.Button('Generate', key='histogram_generate_button')],
                       [sg.Button('Back', key='histogram_back_button')]]
        self.results = None

    def check_events(self, event, values, window):
        if event == 'standard_write_results_event':
            self.results = values['standard_write_results_event']
        if event == 'histogram_generate_button':
            valid, error_message = self.validate_user_input(values)
            if not valid:
                window.write_event_value('show_error_window', error_message)
                return
            self.generate_histogram(values, window)
        if event == 'histogram_back_button':
            window['histogram_panel'].update(visible=False)
            window['standard_result_panel'].update(visible=True)

    def generate_histogram(self, values, window):
        reporters = self.format_reporters(values)
        metric = self.get_selected_radio_button(values)
        merged_data = merge_data(self.results[1], metric)
        try:
            [merged_data[reporter] for reporter in reporters]
        except KeyError:
            window.write_event_value('show_error_window', 'Error in input: Invalid reporter name.\nPlease make '
                                                          'sure all reporters are valid with the current run '
                                                          'configuration.')
            return
        fig = go.Figure()
        for reporter in reporters:
            fig.add_trace(go.Histogram(x=merged_data[reporter], name=reporter))

        fig.update_layout(title_text=values['histogram_title_input'],
                          xaxis_title_text='Value',
                          yaxis_title_text='Count'
                          )
        fig.show()

    def get_selected_radio_button(self, values):
        for i in range(3):
            if values[f'histogram_metric_{i + 1}']:
                return i + 1
        return 1

    def format_reporters(self, values):
        reporters = list(filter(('').__ne__, values['histogram_reporter_input'].split('\n')))
        reporters = list(map(lambda x: x.strip(), reporters))
        return reporters

    def validate_user_input(self, values):
        if values['histogram_reporter_input'] == '\n':
            return False, 'Error in input: One or more fields are empty. ' \
                          'Please make sure all options are filled out.'

        return True, ''
