from django.test import TestCase

from .models import Poster, SearchHistory


class HomeTestCase(TestCase):

    def test_home_page_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'poster.html')

    def test_home_page_is_clean(self):
        response = self.client.get('/')
        self.assertNotContains(response,
                               'Poster for your movie is not available')
        self.assertNotContains(response,
                               'Please try again')


class PostMixin(object):

    def post_correct_movie(self):
        return self.client.post('/poster/',
                                {'poster-title': "The Godfather"}
                                )

    def post_invalid_input(self):
        return self.client.post('/poster/',
                                {'poster-title': "jsdkfjlskdjfjdsf"}
                                )

    def post_movie_without_poster(self):
        # Movie is in omdb, but doesn't have poster
        return self.client.post('/poster/',
                                {'poster-title': "family man"}
                                )


class PosterTestCase(TestCase, PostMixin):

    def test_render_poster_on_correct_title(self):
        response = self.post_correct_movie()

        self.assertContains(response,
                            'Here is your poster')
        self.assertContains(response,
                            'img src')

    def test_render_error_message_on_invalid_movie(self):
        response = self.post_invalid_input()

        self.assertContains(response,
                            'Please try again')

    def test_render_correct_message_on_movie_without_poster(self):
        response = self.post_movie_without_poster()

        self.assertContains(response,
                            'Poster for your movie is not available')

    def test_save_poster_on_correct_input(self):
        self.post_correct_movie()
        self.assertEqual(Poster.objects.count(), 1)

    def test_doesnt_save_poster_on_invalid_input(self):
        self.post_invalid_input()
        self.assertEqual(Poster.objects.count(), 0)

    def test_doesnt_save_poster_on_movie_without_poster(self):
        self.post_movie_without_poster()
        self.assertEqual(Poster.objects.count(), 0)


class SearchHistoryTestCase(TestCase, PostMixin):

    def test_save_search_history_on_correct_input(self):
        self.post_correct_movie()
        self.assertEqual(SearchHistory.objects.count(), 1)

    def test_save_search_history_on_invalid_input(self):
        self.post_invalid_input()
        self.assertEqual(SearchHistory.objects.count(), 1)

    def test_save_search_history_on_movie_without_poster(self):
        self.post_movie_without_poster()
        self.assertEqual(SearchHistory.objects.count(), 1)
