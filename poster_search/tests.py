from django.test import TestCase

from .models import Poster, SearchHistory


class HomeTestCase(TestCase):

    def test_home_page_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'poster.html')

    def test_home_page_is_clean(self):
        response = self.client.get('/')
        self.assertNotContains(response.content,
                               'Poster for your movie is not available')
        self.assertNotContains(response.content,
                               'Please try again')

# class PosterTestCase(TestCase):

#     def test_can_save_item_after_POST_request(self):
#         other_list = List.objects.create()
#         correct_list = List.objects.create()

#         self.client.post(
#             "/lists/{}/".format(correct_list.id),
#             data={'text': "A new item for an existing list"}
#         )

#         self.assertEqual(Item.objects.count(), 1)
#         new_item = Item.objects.first()
#         self.assertEqual(
#             new_item.text, "A new item for an existing list")
#         self.assertEqual(new_item.list, correct_list)
