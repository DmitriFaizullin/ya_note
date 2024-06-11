from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()


class TestContent(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Бильбо Бэггинс')
        cls.reader = User.objects.create(username='Фродо Бэггинс')

        cls.note_in_list = (
            (cls.author, True),
            (cls.reader, False),
        )

        cls.note = Note.objects.create(
            title='Запись',
            text='Текст.',
            slug='Zapis',
            author=cls.author
        )
        cls.urls = {
            reverse('notes:add'),
            reverse('notes:edit', args=(cls.note.slug,))
        }

    def test_note_in_object_list(self):
        for user, status in self.note_in_list:
            self.client.force_login(user)
            with self.subTest(user=user):
                response = self.client.get(reverse('notes:list'))
                object_list = response.context['object_list']
                self.assertEqual((self.note in object_list), status)

    def test_page_has_form(self):
        self.client.force_login(self.author)
        for url in self.urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
