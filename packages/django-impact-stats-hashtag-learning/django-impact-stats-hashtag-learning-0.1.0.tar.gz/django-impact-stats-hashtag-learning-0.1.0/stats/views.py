from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView

from tracking.models import Visitor, Pageview

from .forms import StatsPeriodForm

from django.utils.timezone import now, make_aware
from datetime import datetime, timedelta

from config.settings.base import PROGRAM_NAME

class TrackingDashboard(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'stats/dashboard.html'
    permission_required = 'stats.can_view_stats'

    def get(self, request, *args, **kwargs):

        if not request.user.is_staff:
            raise PermissionDenied

        start_time, end_time = get_start_time_end_time_today()
        user_stats = Visitor.objects.user_stats(start_time, end_time)
        visitor_stats = Visitor.objects.stats(start_time, end_time)
        pageview_stats = Pageview.objects.stats(start_time, end_time)

        stats_period_form = StatsPeriodForm()

        context = {
            'stats_period_form': stats_period_form,
            'visitor_stats': visitor_stats,
            'user_stats': user_stats,
            'pageview_stats': pageview_stats,
            'program_name': PROGRAM_NAME
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_stats = None
        pageview_stats = None
        visitor_stats = None

        stats_period_form = StatsPeriodForm(request.POST)
        if 'submit' in request.POST:
            start_time, end_time = handle_stats_period_form(stats_period_form)


            user_stats = Visitor.objects.user_stats(start_time, end_time)
            visitor_stats = Visitor.objects.stats(start_time, end_time)
            pageview_stats = Pageview.objects.stats(start_time, end_time)


        context = {
            'stats_period_form': stats_period_form,
            'user_stats': user_stats,
            'visitor_stats': visitor_stats,
            'pageview_stats': pageview_stats,
        }

        return render(request, self.template_name, context)

def get_start_time_end_time_today():
    end_time = now()
    today = datetime.today()
    start_time = make_aware(datetime(year=today.year, month=today.month, day=today.day, hour=0, second=0))

    return start_time, end_time

def handle_stats_period_form(stats_period_form):

    start_time = None
    end_time = None

    if stats_period_form.is_valid():
        cleaned_form = stats_period_form.cleaned_data
        stats_period = cleaned_form.get('stats_period_field')

        start_time, end_time = get_start_time_end_time_today()

        if stats_period == 'yesterday':
            start_time -= timedelta(days=1)
            end_time = start_time + timedelta(days=1)

        if stats_period == '2daysago':
            start_time -= timedelta(days=2)
            end_time = start_time + timedelta(days=1)

        if stats_period == '3daysago':
            start_time -= timedelta(days=3)
            end_time = start_time + timedelta(days=1)

        if stats_period == '4daysago':
            start_time -= timedelta(days=4)
            end_time = start_time + timedelta(days=1)

        if stats_period == '5daysago':
            start_time -= timedelta(days=5)
            end_time = start_time + timedelta(days=1)

        elif stats_period == 'last7':
            start_time -= timedelta(days=6)

        elif stats_period == 'last14':
            start_time -= timedelta(days=13)

        elif stats_period == 'last28':
            start_time -= timedelta(days=27)

    return start_time, end_time
