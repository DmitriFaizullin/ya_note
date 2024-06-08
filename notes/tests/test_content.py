from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()


class TestNotesList(TestCase):
    NOTES_LIST_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Бильбо Бэггинс')
        all_notes = [
            Note(
                title=f'Запись {index}',
                text='Текст.',
                slug=f'Zapis_{index}',
                author=cls.author
            )
            for index in range(2)
        ]
        Note.objects.bulk_create(all_notes)

    def test_notes_order(self):
        self.client.force_login(self.author)
        response = self.client.get(self.NOTES_LIST_URL)
        object_list = response.context['object_list']
        all_id = [note.id for note in object_list]
        sorted_id = sorted(all_id)
        self.assertEqual(all_id, sorted_id)


class TestHasForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Бильбо Бэггинс')
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

    def test_page_has_form(self):
        self.client.force_login(self.author)
        for url in self.urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
