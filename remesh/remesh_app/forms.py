from django import forms

from .models import Conversation, Message, Thought

class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ["title"]
        labels = {"title": "Title"}
        widgets = {"title": forms.TextInput(attrs={"size":100})}


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["text"]
        labels = {"text": ""}
        widgets = {"text": forms.Textarea(attrs={"cols":100})}


class ThoughtForm(forms.ModelForm):
    class Meta:
        model = Thought
        fields = ["text"]
        labels = {"text": ""}
        widgets = {"text": forms.Textarea(attrs={"cols":100})}