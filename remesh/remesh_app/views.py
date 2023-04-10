from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Conversation, Message, Thought
from .forms import ConversationForm, MessageForm, ThoughtForm


def index(request):
    """
    Home page for the remesh app
    """
    return render(request, "remesh_app/index.html")


def conversations(request):
    """
    Returns a page showing all the conversations
    """
    conversations = Conversation.objects.all().order_by("-start_date")
    return render(
        request, "remesh_app/conversations.html", {"conversations": conversations}
    )


def conversation(request, conversation_id):
    """
    Returns a page for a conversation, showing the messages and shortened thoughts
    """
    convo = Conversation.objects.get(id=conversation_id)
    messages = convo.message_set.order_by("-sent_date")
    message_dict = {}
    # Showing all the thoughts for each message is pretty inefficient.
    # It would be better to allow the thoughts to be loaded only in the message page.
    # Or dynamically by using some kind of accordion
    for message in messages:
        thoughts = message.thought_set.order_by("-sent_date")
        message_dict[str(message.id)] = (message, thoughts)
    return render(
        request,
        "remesh_app/conversation.html",
        {"conversation": convo, "message_dict": message_dict},
    )


def message(request, message_id):
    """
    Returns a page for a message, showing the thoughts
    """
    message = Message.objects.get(id=message_id)
    thoughts = message.thought_set.order_by("-sent_date")
    return render(
        request,
        "remesh_app/message.html",
        {
            "message": message,
            "thoughts": thoughts,
        },
    )


def new_conversation(request):
    """
    Creates a new conversation
    """
    if request.method == "POST":
        form = ConversationForm(data=request.POST)
        # validate before saving
        if form.is_valid():
            form.save()
            return redirect("remesh_app:conversations")
    else:
        # if not POST, create a new blank form
        form = ConversationForm()

    # if not POST or invalid form, display form
    return render(
        request,
        "remesh_app/new_conversation.html",
        {
            "form": form,
        },
    )


def new_message(request, conversation_id):
    """
    Creates a new message in a conversation
    """
    convo = Conversation.objects.get(id=conversation_id)
    if request.method == "POST":
        form = MessageForm(data=request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.conversation = convo
            new_message.save()
            return redirect("remesh_app:conversation", conversation_id=conversation_id)
    else:
        form = MessageForm()

    return render(
        request,
        "remesh_app/new_message.html",
        {
            "conversation": convo,
            "form": form,
        },
    )


# There is definite repetition here, and it is possible to combine
# new_message and new_thought into one function. I am chosing not
# to do that because they are fundamentally different objects,
# and if one model changed, it will become much more difficult to
# maintain code where they are sharing functions.
def new_thought(request, message_id):
    """
    Creates a new thought in a message
    """
    msg = Message.objects.get(id=message_id)
    if request.method == "POST":
        form = ThoughtForm(data=request.POST)
        if form.is_valid():
            new_thought = form.save(commit=False)
            new_thought.message = msg
            new_thought.save()
            return redirect("remesh_app:message", message_id=message_id)
    else:
        form = ThoughtForm()

    return render(
        request, "remesh_app/new_thought.html", {"message": msg, "form": form}
    )


# search for messages and conversations could also have been separated,
# initially I thought it would be better to separate them, but now I am
# not sure. I kept this since it shows a different approach than I used
# previously.
def search(request, search_type, object_id=None):
    """
    Searches for objects based on their type
    object_id is an optional argument for searches within an element of another model
    """
    query = request.GET.get("q")
    context = {}
    if search_type == "messages":
        convo = Conversation.objects.get(id=object_id)
        results = convo.message_set.filter(text__contains=query)
        context = {
            "results": results,
            "search_type": search_type,
            "conversation_id": object_id,
        }
    elif search_type == "conversations":
        results = Conversation.objects.filter(title__contains=query)
        context = {
            "results": results,
            "search_type": search_type,
        }
    else:
        # This should not be reached! (Could also have it raise an error)
        return HttpResponse(
            "Invalid search type. Please contact the developer and tell them to fix their app."
        )

    return render(request, "remesh_app/search_results.html", context)
