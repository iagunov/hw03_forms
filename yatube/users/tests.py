# from http import HTTPStatus
#
# from django.contrib.auth import get_user_model
# from django.test import TestCase, Client
#
# from posts.models import Group, Post
#
# User = get_user_model()
#
#
# class TaskURLTests(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.author = User.objects.create_user(username='author')
#         cls.not_author = User.objects.create_user(username='not_author')
#         cls.group = Group.objects.create(
#             title='Тестовая группа',
#             slug='test_slug',
#             description='Тестовое описание',
#         )
#         cls.post = Post.objects.create(
#             author=cls.author,
#             group=cls.group,
#             text='Тестовый текст',
#             pub_date='14.07.2022',
#         )
#         cls.authorized_client = Client()
#         cls.authorized_client.force_login(cls.author)
#         cls.authorized_client_not_author = Client()
#         cls.authorized_client_not_author.force_login(cls.not_author)
#
#     def test_urls_all_users(self):
#         """URL-адрес доступен для всех пользователей."""
#         templates_url_names = {
#             'users/signup.html': '/signup/',
#             'users/logged_out.html': '/logout/',
#             'users/login.html': '/login/',
#             'users/password_change_form.html': '/password_change/',
#             'users/password_change_done.html': '/password_change/done/',
#             'users/password_reset_form.html': '/password_reset/',
#             'users/password_reset_done.html': '/password_reset/done/',
#             'users/password_reset_confirm.html': '/reset/<uidb64>/<token>',
#             'users/password_reset_complete.html': '/reset/done/',
#         }
#         for template, url in templates_url_names.items():
#             with self.subTest(url=url):
#                 response = Client().get(url)
#                 self.assertEqual(response.status_code, HTTPStatus.OK)
