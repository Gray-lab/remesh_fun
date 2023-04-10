from django.db import models


class Conversation(models.Model):
    title = models.CharField(max_length=200)
    # I think it would be better to have a DateTimeField here,
    # but the directions said "Start Date", so I followed them exactly.
    start_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Message(models.Model):
    # It makes sense to cascade conversation deletion
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    text = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return limit_len(self.text, 100)


class Thought(models.Model):
    # Thoughts and Messages are essentially identical
    # But it is important to keep functions related to them separate in case 
    # their models are updated in the future. They are different things after all.
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    text = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return limit_len(self.text, 100)


def limit_len(string: str, length: int) -> str:
    """
    If the input string is longer than length, slices the input string and appends '...'
    If the input string is shorter than lenght, makes no changes
    Returns the resulting string
    """
    if len(string) > length:
        return f"{string[:length]}..."
    else:
        return string
