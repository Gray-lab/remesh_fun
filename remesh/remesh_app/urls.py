from django.urls import path

from . import views

app_name = "remesh_app"

urlpatterns = [
    # Home view will have a link to conversations
    path("", views.index, name="index"),
    # Conversations view will show all conversations
    path("conversations/", views.conversations, name="conversations"),
    # Conversation view will show messages and thoughts for the conversation
    path(
        "conversation/<int:conversation_id>/", views.conversation, name="conversation"
    ),
    # Thoughts view will show thoughts for each message
    path("message/<int:message_id>/", views.message, name="message"),
    # New conversation
    path("new_conversation/", views.new_conversation, name="new_conversation"),
    # New message
    path("new_message/<int:conversation_id>", views.new_message, name="new_message"),
    # New thought
    path("new_thought/<int:message_id>/", views.new_thought, name="new_thought"),
    # Search
    path("search/<str:search_type>/", views.search, name="search"),
    path("search/<str:search_type>/<int:conversation_id>", views.search, name="search"),
]
