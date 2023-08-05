from django import forms

STATS_PERIODS = [
    ('today', 'Today'),
    ('yesterday', 'Yesterday'),
    ('2daysago', '2 Days Ago'),
    ('3daysago', '3 Days Ago'),
    ('4daysago', '4 Days Ago'),
    ('5daysago', '5 Days Ago'),
    ('last7', 'Last 7 Days'),
    ('last14', 'Last 14 Days'),
    ('last28', 'Last 28 days'),
]

class StatsPeriodForm(forms.Form):

    stats_period_field = forms.ChoiceField(
        choices=STATS_PERIODS
    )

    def __init__(self, *args, **kwargs):
        super(StatsPeriodForm, self).__init__(*args, **kwargs)

        self.fields['stats_period_field'].widget.attrs['class'] = 'custom-select'
