import django_tables2 as tables
from .models import Page
from django.urls import reverse
from django.utils.html import format_html

class PageTable(tables.Table):
    class Meta:
        model = Page
        template_name = 'htmx-table.html'
        dive_name = 't-page_div'

    def render_name(self, value, record):
        url = reverse('tiles:detail', kwargs={'page_id':record.pk})
        return format_html("<a hx-get='{}' hx-target='#t-page-detail-area' class='link-primary' style='cursor: pointer;'>{}</a>", url, value)