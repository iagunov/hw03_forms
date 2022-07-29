from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Post, Group

User = get_user_model()


class TaskPagesTests(TestCase):
    #создаем пользователя
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='myuser')
        #создаем тестовую группу поста
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        #создаем тестовый поста
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый текст',
            pub_date='14.07.2022',
        )
        #авторизируем пользователя
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            (reverse(
                'posts:group_list',
                kwargs={'slug': f'{self.post.group.slug}'
                        })): 'posts/group_list.html',
            (reverse(
                'posts:post_detail',
                kwargs={'post_id': f'{self.post.pk}'
                        })): 'posts/post_detail.html',
            (reverse(
                'posts:post_edit',
                kwargs={'post_id': f'{self.post.pk}'
                        })): 'posts/create_post.html',
            (reverse(
                'posts:profile',
                kwargs={'username': f'{self.post.author}'
                        })): 'posts/profile.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        post = response.context['page_obj'][0].text
        self.assertEqual(post, 'Тестовый текст')

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = (self.authorized_client.get(
            reverse('posts:group_list',
                    kwargs={'slug': 'test_slug'})))
        group = response.context['page_obj'][0].group.title
        self.assertEqual(group, 'Тестовая группа')

    def test_user_list_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = (self.authorized_client.get(
            reverse('posts:profile',
                    kwargs={'username': 'myuser'})))
        user = response.context['page_obj'][0].author
        self.assertEqual(user, self.user)

    def test_post_detail_list_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = (self.authorized_client.get(
            reverse('posts:post_detail',
                    kwargs={'post_id': '1'})))
        post_detail = response.context['post'].text
        self.assertEqual(post_detail, 'Тестовый текст')


