import PySimpleGUI as sg
from src.util.data_processing.merge_standard_data import merge_data
import plotly.figure_factory as ff
from src.gui.custom_components import title, question_mark, metric3_radio_buttons


class DistributionplotScreen:

    def __init__(self):
        question_mark_padding = ((0, 0), (0, 0))
        self.layout = [[title('Distribution plot')],
                       [sg.Text('Graph Title:'), sg.Input('', key='distplot_title_input')],
                       [sg.Text('Reporters to plot:'), question_mark('Help', padding=question_mark_padding)],
                       [sg.Multiline('', key='distplot_reporter_input')],
                       [sg.Text('Only input a single reporter on each line')],
                       [sg.Text('Metric:'), question_mark('Help', padding=question_mark_padding)],
                       metric3_radio_buttons('distplot'),
                       [sg.Text('Distribution indicators:'), question_mark('Help', padding=question_mark_padding)],
                       [sg.Checkbox('Show curve', key='distplot_curve_checkbox', default=True),
                       sg.Checkbox('Show histogram', key='distplot_histogram_checkbox', default=True),
                       sg.Checkbox('Show rug', key='distplot_rug_checkbox', default=True)],
                       [sg.Button('Generate', key='distplot_generate_button')],
                       [sg.Button('Back', key='distplot_back_button')]]
        self.results = None

    def check_events(self, event, values, window):
        if event == 'standard_write_results_event':
            self.results = values['standard_write_results_event']
        if event == 'distplot_generate_button':
            valid, error_message = self.validate_user_input(values)
            if not valid:
                window.write_event_value('show_error_window', error_message)
                return
            self.generate_histogram(values, window)
        if event == 'distplot_back_button':
            window['distplot_panel'].update(visible=False)
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

        hist_data = []
        for reporter in reporters:
            hist_data.append(merged_data[reporter])

        bin_size = [(max(data)-min(data))/30 for data in hist_data]
        fig = ff.create_distplot(hist_data, reporters, bin_size,
                                 show_curve=values['distplot_curve_checkbox'],
                                 show_hist=values['distplot_histogram_checkbox'],
                                 show_rug=values['distplot_rug_checkbox'],
                                 )
        fig.update_layout(title_text=values['distplot_title_input'],
                          xaxis_title_text='Value',
                          )
        fig.show()

    def get_selected_radio_button(self, values):
        for i in range(3):
            if values[f'distplot_metric_{i + 1}']:
                return i + 1
        return 1

    def format_reporters(self, values):
        reporters = list(filter(('').__ne__, values['distplot_reporter_input'].split('\n')))
        reporters = list(map(lambda x: x.strip(), reporters))
        return reporters

    def validate_user_input(self, values):
        if values['distplot_reporter_input'] == '\n':
            return False, 'Error in input: One or more fields are empty. ' \
                          'Please make sure all options are filled out.'

        return True, ''
