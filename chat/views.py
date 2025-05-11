from django.shortcuts import render
from base.models import *
from .models import *
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.urls import reverse
import random



# Create your views here.

def chats(request):
    if request.user.is_authenticated:


        company_name = Company_name.objects.first()
        if request.user.is_superuser:
            sup_chats = Chat.objects.all()
            context = {'company_name': company_name, 'chats':sup_chats}
            return render(request, 'chat/chats.html', context)
        else:
            user, created = ChatUser.objects.get_or_create(user = request.user)
            cus_chats = Chat.objects.filter(user = user)
            user.has_new_message = False
            user.save()

            context = {'company_name': company_name, 'chats':cus_chats}
            return render(request, 'chat/chats.html', context)
    else:
        return HttpResponseRedirect(reverse('base:login'))

def chat(request, c_id):
    if request.user.is_authenticated:
        company_name = Company_name.objects.first()
        chat = Chat.objects.get(chat_id = c_id)
        messages = Message.objects.filter(chat = chat).order_by('time')

        def update_status():
            chat.user.has_new_message = True
            chat.user.save()
            chat.is_read = False
            chat.save()

            return None



        if request.method != 'POST':
            if request.user.is_superuser:
                pass
            else:
                chat.is_read = True
                chat.save()
            context = {'company_name': company_name, 'chat':chat, 'messages':messages}
            return render(request, 'chat/chat.html', context)
        else:
            if request.FILES:
                text = request.POST['text']
                text = text.strip()

                img = request.FILES['picture']

                if request.user.is_superuser:
                    Message.objects.create(chat = chat, text = text, img = img, from_support = True)
                    update_status()
                else:



                    Message.objects.create(chat = chat, text = text, img = img  )
                 

                return HttpResponseRedirect(reverse('chat:single_chat', args=[chat.chat_id,]))
            else:
                text = request.POST['text']
                text = text.strip()
                if text == "":
                    return HttpResponseRedirect(reverse('chat:single_chat', args=[chat.chat_id,]))
                if request.user.is_superuser:
                    Message.objects.create(chat = chat, text = text, from_support = True)
                    update_status()
                   
                else:

                    Message.objects.create(chat = chat, text = text)
                return HttpResponseRedirect(reverse('chat:single_chat', args=[chat.chat_id,]))

    else:
        return HttpResponseRedirect(reverse('base:login'))
    
def create_new_ticket(request):
    if request.user.is_authenticated: #checking that user is authenticated
        if request.method == 'POST': #checking method
            chat_user = ChatUser.objects.get(user = request.user)
            chat_id = random.randint(1111111,9999999999)
            topic = request.POST['topic']
            support = Support.objects.all().order_by('?').first()
            last_message = request.POST['des']

            new_chat = Chat.objects.create(chat_id = chat_id, user = chat_user, topic = topic, support = support, last_message = last_message)
            Message.objects.create(chat = new_chat, text = last_message)
            auto_reply = f'Hello {chat_user.user.first_name}, your message has been received and forwarded to the team in charge. We\'ll update you if any further action is required from you to process your issue ticket. Thanks for your understanding.'

            Message.objects.create(chat = new_chat, text = auto_reply, from_support = True)
            mail = request.POST['email']
            user_obj = User.objects.get(username = request.user.username)
            user_obj.email = mail
            user_obj.save()
            return HttpResponseRedirect(reverse('chat:single_chat', args=[chat_id]))
    else: #if user hasnt been authenticated, force them to.
        return HttpResponseRedirect(reverse('base:login'))
    
