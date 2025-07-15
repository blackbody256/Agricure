from django.shortcuts import render, get_object_or_404, redirect
from .models import ChatSession, Message
from users.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

@login_required
def chat_dashboard(request, user_id=None):
    query = request.GET.get('search', '')
    current_user = request.user
    
    # Get users with the opposite role
    if current_user.role.lower() == 'farmer':
        contacts = User.objects.filter(role__iexact='AGRONOMIST').exclude(id=current_user.id)
    else:
        contacts = User.objects.filter(role__iexact='FARMER').exclude(id=current_user.id)

    chats = ChatSession.objects.filter(Q(sender=current_user) | Q(receiver=current_user)).distinct()

    # Chats list
    chats = ChatSession.objects.filter(Q(sender=current_user) | Q(receiver=current_user)).distinct()
    for chat in chats:
        chat.partner = chat.receiver if chat.sender == current_user else chat.sender
        
    
     # New chat creation if user_id is passed
    selected_chat = None
    messages = None
    other_user = None

    if user_id:
        other_user = get_object_or_404(User, id=user_id)
        chat, _ = ChatSession.objects.get_or_create(
            sender=min(current_user, other_user, key=lambda x: x.id),
            receiver=max(current_user, other_user, key=lambda x: x.id)
        )
        selected_chat = chat

        if request.method == 'POST':
            content = request.POST.get('content', '').strip()
            attachment = request.FILES.get('attachment')

            if content or attachment:
                Message.objects.create(
                    chat=chat,
                    sender=current_user,
                    content=content,
                    attachment=attachment
                )
            return redirect('chat:open_chat', user_id=other_user.id)

        messages = Message.objects.filter(chat=chat).order_by('timestamp')
    else:
        messages = None




    # Search logic (optional)
    if query:
        users = User.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query))
        farmers = users.filter(role__iexact='FARMER')
        agronomists = users.filter(role__iexact='AGRONOMIST')
    else:
        farmers = User.objects.filter(role__iexact='FARMER').exclude(id=current_user.id)
        agronomists = User.objects.filter(role__iexact='AGRONOMIST').exclude(id=current_user.id)

    return render(request, 'chat/dashboard.html', {
        'ongoing_chats': chats,
        'farmers': User.objects.filter(role__iexact='FARMER').exclude(id=current_user.id),
        'agronomists': User.objects.filter(role__iexact='AGRONOMIST').exclude(id=current_user.id),
        'contacts': contacts,
        'selected_chat': selected_chat,
        'messages': messages,
        'other_user': other_user,
    })



