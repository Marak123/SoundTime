from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from apis.user.models import User


class SongAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create(username='testuser', password='testpass', email="user@test.cc")
        self.refresh = RefreshToken.for_user(self.user)
        self.auth_header = f'Bearer {str(self.refresh.access_token)}'


        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)


    def test_song_create_and_add_download_task_to_background(self):
        """
            Create new object Song by URL and test adding downloading task to background
        """

        song_data = {
            'url': 'https://music.youtube.com/watch?v=xtOYyTsP5y4'
        }

        print(self.auth_header)
        response = self.client.post('/api/songs/', song_data, format='json')#, HTTP_AUTHORIZATION=self.auth_header)

        self.assertEqual(response.status_code, 200)



# class SongAPITestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#     def test_send_post_request_to_song_endpoint(self):
#         # Dane do przesłania w ciele żądania POST
#         song_data = {
#             'title': 'Test Song',
#             'artist': 'Test Artist',
#             'genre': 'Test Genre',
#         }

#         # Wysyłamy żądanie POST na endpoint '/song/'
#         response = self.client.post(reverse('song_view'), song_data, format='json')

#         # Sprawdzamy, czy odpowiedź ma status HTTP 200 OK (lub inny oczekiwany status)
#         self.assertEqual(response.status_code, 200)

#         # Dodatkowe asercje, jeśli potrzebujesz sprawdzić zawartość odpowiedzi
#         # self.assertEqual(response.data['some_key'], 'expected_value')
#         # self.assert...

