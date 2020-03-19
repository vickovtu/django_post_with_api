from django.test import TestCase
from django.contrib.auth.models import User
from post.models import Post


class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = User.objects.create_user(
            username='testuser1',
            password='abc123',
            email='admin@admin.com'
        )
        testuser1.save()
        test_post = Post.objects.create(
            author=testuser1,
            title='Blog title',
            body='Body content...',
            status='draft')
        test_post.save()

    def test_blog_content(self):
        post = Post.objects.get(id=1)
        expected_author = f'{post.author}'
        expected_title = f'{post.title}'
        expected_body = f'{post.body}'
        self.assertEqual(expected_author, 'testuser1')
        self.assertEqual(expected_title, 'Blog title')
        self.assertEqual(expected_body, 'Body content...')
