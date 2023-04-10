from django.db import models


class Conversation(models.Model):
    title = models.CharField(max_length=200)
    # I think it would be better to have a DateTimeField here,
    # but the directions said "Start Date", so I followed them exactly.
    start_date = models.DateField(auto_now_add=True)


class Message(models.Model):
    # It makes sense to cascade converstion deletion
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    text = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)


class Thought(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    text = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
