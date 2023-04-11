from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse

from .models import Conversation, Message, Thought

from .forms import ConversationForm, MessageForm, ThoughtForm


class ConversationModelTests(TestCase):
    def setUp(self):
        """
        Set up a Conversation, Message, and Thought for use in the tests
        """
        self.title = "First Test Conversation"
        self.start_date = timezone.now().date()
        self.conversation = Conversation.objects.create(
            title=self.title, start_date=self.start_date
        )

        self.message_1 = Message.objects.create(
            conversation=self.conversation,
            text="Test message 1",
        )
        self.message_2 = Message.objects.create(
            conversation=self.conversation,
            text="Test message 2",
        )

    def test_conversation_creation(self):
        """
        Test that a Conversation can be created with a title and a start date
        """
        self.assertEqual(self.conversation.title, self.title)
        self.assertEqual(self.conversation.start_date, self.start_date)

    def test_conversation_str(self):
        """
        Test that the string representation of a Conversation returns the title
        """
        self.assertEqual(str(self.conversation), self.title)

    def test_conversation_get_messages(self):
        """
        Test that a Messages can be created for a Conversation and retrieved through get_messages() in reverse chronological order (most recent first)
        """
        messages = self.conversation.get_messages()
        self.assertIn(self.message_1, messages)
        self.assertIn(self.message_2, messages)
        self.assertEqual(messages[0], self.message_2)
        self.assertEqual(messages[1], self.message_1)
        self.assertEqual(messages.count(), 2)


class MessageModelTests(TestCase):
    def setUp(self):
        """
        Set up a Conversation, Messages and Thoughts for use in the tests
        """
        self.conversation = Conversation.objects.create(title="Test Conversation")
        self.message_text_short = "Short test message"
        self.message_text_long = "Long test message. This is a test message that is longer than 100 characters. In order to make it that long I need to keep typing more and more and more things."

        self.message_time = timezone.now()
        self.message_short = Message.objects.create(
            conversation=self.conversation,
            text=self.message_text_short,
        )
        self.message_long = Message.objects.create(
            conversation=self.conversation,
            text=self.message_text_long,
        )

        self.thought_1 = Thought.objects.create(
            message=self.message_short,
            text="Test thought 1",
        )
        self.thought_2 = Thought.objects.create(
            message=self.message_short,
            text="Test thought 2",
        )

    def test_message_creation(self):
        """
        Test that Messages can be created with a conversation, text
        """
        self.assertEqual(self.message_short.conversation, self.conversation)
        self.assertEqual(self.message_short.text, self.message_text_short)
        self.assertEqual(self.message_long.text, self.message_text_long)

    def test_message_str_long(self):
        """
        Test that the string representation of a Message returns the first 100 characters of the text
        """
        self.assertEqual(str(self.message_long), self.message_text_long[:100] + "...")

    def test_message_str_short(self):
        """
        Test that the string representation of a short Message returns the whole message
        """
        self.assertEqual(str(self.message_short), self.message_text_short)

    def test_message_get_thoughts(self):
        """
        Test that a Thoughts can be created for a Message and retrieved through get_thoughts() in reverse chronological order (most recent first)
        """
        thoughts = self.message_short.get_thoughts()
        self.assertIn(self.thought_1, thoughts)
        self.assertIn(self.thought_2, thoughts)
        self.assertEqual(thoughts[0], self.thought_2)
        self.assertEqual(thoughts[1], self.thought_1)
        self.assertEqual(thoughts.count(), 2)


class ThoughtModelTests(TestCase):
    def setUp(self):
        """
        Set up a Conversation, Message, and Thought for use in the tests
        """
        self.conversation = Conversation.objects.create(
            title="Test Conversation", start_date=timezone.now().date()
        )
        self.message_text = "Test message"
        self.message = Message.objects.create(
            conversation=self.conversation, text=self.message_text
        )
        self.thought_text_short = "Short test thought"
        self.thought_text_long = "Long test thought. This is a test thought that is longer than 100 characters. In order to make it that long I need to keep typing more and more and more things."
        self.thought_short = Thought.objects.create(
            message=self.message, text=self.thought_text_short
        )
        self.thought_long = Thought.objects.create(
            message=self.message, text=self.thought_text_long
        )

    def test_thought_creation(self):
        """
        Test that a Thought can be created with a message and text
        """
        self.assertEqual(self.thought_short.message, self.message)
        self.assertEqual(self.thought_long.message, self.message)
        self.assertEqual(self.thought_short.text, self.thought_text_short)
        self.assertEqual(self.thought_long.text, self.thought_text_long)

    def test_thought_str_long(self):
        """
        Test that the string representation of a long Thought returns the first 100 characters of the text
        """
        self.assertEqual(str(self.thought_long), self.thought_text_long[:100] + "...")

    def test_thought_str_short(self):
        """
        Test that the string representation of a long Thought returns the first 100 characters of the text
        """
        self.assertEqual(str(self.thought_short), self.thought_text_short)


class FormsTestCase(TestCase):
    def test_conversation_form_valid_data(self):
        form_data = {"title": "Test Conversation Title"}
        form = ConversationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_conversation_form_invalid_data_empty(self):
        form_data = {"title": ""}
        form = ConversationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_conversation_form_invalid_data_long(self):
        form_data = {
            "title": "A title that is more than 200 characters. --------------------------------------------------------------------------------------------------------------------------------------------------------------------------wow, that is a lot"
        }
        form = ConversationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_message_form_valid_data(self):
        conversation = Conversation.objects.create(title="Test Conversation")
        form_data = {"text": "Test message text", "conversation": conversation.pk}
        form = MessageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_message_form_invalid_data(self):
        conversation = Conversation.objects.create(title="Test Conversation")
        form_data = {"text": "", "conversation": conversation.pk}
        form = MessageForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_thought_form_valid_data(self):
        conversation = Conversation.objects.create(title="Test Conversation")
        message = Message.objects.create(
            text="Test message text", conversation=conversation
        )
        form_data = {"text": "Test thought text", "message": message.pk}
        form = ThoughtForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_thought_form_invalid_data(self):
        conversation = Conversation.objects.create(title="Test Conversation")
        message = Message.objects.create(
            text="Test message text", conversation=conversation
        )
        form_data = {"text": "", "message": message.pk}
        form = ThoughtForm(data=form_data)
        self.assertFalse(form.is_valid())


class RemeshAppViewsTestCase(TestCase):
    def setUp(self):
        self.convo = Conversation.objects.create(title="Test Conversation")
        self.convo_empty = Conversation.objects.create(title="Test Empty Conversation")
        self.convo_empty_message = Conversation.objects.create(
            title="Test Conversation Empty Message"
        )
        self.msg = Message.objects.create(conversation=self.convo, text="Test Message")
        self.msg_empty = Message.objects.create(
            conversation=self.convo_empty_message, text="Test Message Empty"
        )
        self.thought_1 = Thought.objects.create(message=self.msg, text="Test Thought 1")
        self.thought_2 = Thought.objects.create(message=self.msg, text="Test Thought 2")

        self.convo_form_data = {"title": "New Conversation"}
        self.msg_form_data = {"text": "New Message"}
        self.thought_form_data = {"text": "New Thought"}

    def test_index_view(self):
        url = reverse("remesh_app:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "remesh_app/index.html")
        # Test front-end elements
        self.assertContains(
            response, "Welcome to the Remesh take home problem homepage."
        )

    def test_conversations_view(self):
        url = reverse("remesh_app:conversations")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "remesh_app/conversations.html")
        self.assertQuerysetEqual(
            response.context["conversations"],
            [self.convo, self.convo_empty, self.convo_empty_message],
        )
        # Test front-end elements
        self.assertContains(response, "Test Conversation")
        self.assertContains(response, "Test Empty Conversation")
        self.assertContains(response, "Test Conversation Empty Message")

    def test_conversation_view(self):
        url = reverse("remesh_app:conversation", args=[self.convo.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "remesh_app/conversation.html")
        self.assertEqual(response.context["conversation"], self.convo)
        self.assertEqual(
            response.context["message_dict"][str(self.msg.id)][0], self.msg
        )
        self.assertQuerysetEqual(
            response.context["message_dict"][str(self.msg.id)][1],
            [self.thought_2, self.thought_1],
        )
        # Test front-end elements
        self.assertContains(response, "Test Conversation")
        self.assertContains(response, "Test Message")

    def test_conversation_view_empty(self):
        url = reverse("remesh_app:conversation", args=[self.convo_empty.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "remesh_app/conversation.html")
        self.assertEqual(response.context["conversation"], self.convo_empty)
        self.assertEqual(response.context["message_dict"], {})
        # Test front-end elements
        self.assertContains(response, "Test Empty Conversation")
        self.assertContains(response, "No messages have been sent yet.")

    def test_conversation_view_empty_message(self):
        url = reverse("remesh_app:conversation", args=[self.convo_empty_message.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "remesh_app/conversation.html")
        self.assertEqual(response.context["conversation"], self.convo_empty_message)
        self.assertEqual(
            response.context["message_dict"][str(self.msg_empty.id)][0], self.msg_empty
        )
        self.assertQuerysetEqual(
            response.context["message_dict"][str(self.msg_empty.id)][1], []
        )
        # Test front-end elements
        self.assertContains(response, "Test Conversation Empty Message")
        self.assertContains(response, "Test Message Empty")
        self.assertContains(response, "No thoughts")

    def test_message_view(self):
        url = reverse("remesh_app:message", args=[self.msg.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "remesh_app/message.html")
        self.assertEqual(response.context["message"], self.msg)
        self.assertQuerysetEqual(
            response.context["thoughts"], [self.thought_2, self.thought_1]
        )
        # Test front-end elements
        self.assertContains(response, "Test Thought 1")
        self.assertContains(response, "Test Thought 2")
        self.assertContains(response, "Test Message")

    def test_message_view_empty(self):
        url = reverse("remesh_app:message", args=[self.msg_empty.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "remesh_app/message.html")
        self.assertEqual(response.context["message"], self.msg_empty)
        self.assertQuerysetEqual(response.context["thoughts"], [])
        # Test front-end elements
        self.assertContains(response, "No thoughts have been created yet!")
        self.assertContains(response, "Test Message Empty")

    def test_new_conversation_view(self):
        url = reverse("remesh_app:new_conversation")
        # test GET request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "remesh_app/new_conversation.html")
        self.assertIsInstance(response.context["form"], ConversationForm)
        # test POST request with valid form data
        response = self.client.post(url, data=self.convo_form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("remesh_app:conversations"))
        self.assertEqual(
            Conversation.objects.filter(title="New Conversation")[0].title,
            "New Conversation",
        )
        self.assertRedirects(response, reverse("remesh_app:conversations"))

        # test POST request with invalid form data
        invalid_form_data = {"title": ""}
        response = self.client.post(url, data=invalid_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "remesh_app/new_conversation.html")
        self.assertIsInstance(response.context["form"], ConversationForm)

    def test_new_message_view(self):
        url = reverse(
            "remesh_app:new_message", kwargs={"conversation_id": self.convo.id}
        )
        # test GET request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "remesh_app/new_message.html")
        self.assertIsInstance(response.context["form"], MessageForm)
        # test POST request with valid form data
        response = self.client.post(url, data=self.msg_form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse(
                "remesh_app:conversation", kwargs={"conversation_id": self.convo.id}
            ),
        )
        self.assertEqual(
            Message.objects.filter(text="New Message")[0].text, "New Message"
        )
        self.assertRedirects(
            response,
            reverse(
                "remesh_app:conversation", kwargs={"conversation_id": self.convo.id}
            ),
        )

        # test POST request with invalid form data
        invalid_form_data = {"text": ""}
        response = self.client.post(url, data=invalid_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "remesh_app/new_message.html")
        self.assertIsInstance(response.context["form"], MessageForm)

    def test_new_thought_view(self):
        url = reverse("remesh_app:new_thought", kwargs={"message_id": self.msg.id})
        # test GET request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "remesh_app/new_thought.html")
        self.assertIsInstance(response.context["form"], ThoughtForm)
        # test POST request with valid form data
        response = self.client.post(url, data=self.thought_form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse("remesh_app:message", kwargs={"message_id": self.msg.id}),
        )
        self.assertEqual(
            Thought.objects.filter(text="New Thought")[0].text, "New Thought"
        )
        self.assertRedirects(
            response,
            reverse("remesh_app:message", kwargs={"message_id": self.msg.id}),
        )

        # test POST request with invalid form data
        invalid_form_data = {"text": ""}
        response = self.client.post(url, data=invalid_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "remesh_app/new_thought.html")
        self.assertIsInstance(response.context["form"], ThoughtForm)


class SearchViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.conversation = Conversation.objects.create(title="Test Conversation")
        self.message = Message.objects.create(
            conversation=self.conversation, text="Test Message"
        )

    def test_search_messages(self):
        url = reverse(
            "remesh_app:search",
            args=["messages", self.conversation.id],
        )

        response = self.client.get(url, {"q": "Test Message"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Message")

        response = self.client.get(url, {"q": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Message")

        response = self.client.get(url, {"q": "essage"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Message")

        response = self.client.get(url, {"q": "3ssage"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test Message")

    def test_search_conversations(self):
        url = reverse("remesh_app:search", args=["conversations"])

        response = self.client.get(url, {"q": "Test Conversation"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Conversation")

        response = self.client.get(url, {"q": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Conversation")

        response = self.client.get(url, {"q": "ersation"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Conversation")

        response = self.client.get(url, {"q": "Cookies"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test Conversation")

    def test_invalid_search_type(self):
        url = reverse("remesh_app:search", args=["invalid"])
        response = self.client.get(url, {"q": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Invalid search type. Please contact the developer and tell them to fix their app.",
        )
