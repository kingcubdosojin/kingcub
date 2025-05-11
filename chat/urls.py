from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'chat'

urlpatterns = [
    path('', views.chats, name='chat'),
    path('chat/support-ticket<str:c_id>', views.chat, name = 'single_chat'),
    path('chat/create-new-chat', views.create_new_ticket, name='new_chat'),
]


#if settings.DEBUG:
 #   urlpatterns +=  static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
  #  urlpatterns+= static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)