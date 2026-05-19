from django.urls import path
from django.views.generic import TemplateView

from .views import upload_document, chat_page, ask_question


urlpatterns = [
    path(
        '',
        TemplateView.as_view(template_name='knowledge/landing.html'),
        name='landing',
    ),
    path('upload/', upload_document, name='upload'),
    path('chat/', chat_page, name='chat'),
    path('ask/', ask_question),
]
