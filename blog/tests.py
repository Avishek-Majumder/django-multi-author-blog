from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from blog.models import AuthorProfile, Category, Tag, Post, Comment, Like


class BlogPlatformTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Users
        self.admin = User.objects.create_superuser(username='admin_test', email='admin@test.com', password='password123')
        self.author1 = User.objects.create_user(username='author1_test', email='author1@test.com', password='password123')
        self.author2 = User.objects.create_user(username='author2_test', email='author2@test.com', password='password123')
        self.reader = User.objects.create_user(username='reader_test', email='reader@test.com', password='password123')

        # Promote authors
        self.author1.author_profile.is_author = True
        self.author1.author_profile.save()
        self.author2.author_profile.is_author = True
        self.author2.author_profile.save()

        # Category & Tag
        self.category = Category.objects.create(name='Tech')
        self.tag = Tag.objects.create(name='Python')

        # Valid 1x1 GIF bytes for Pillow validation
        self.valid_gif_bytes = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
        self.test_image = SimpleUploadedFile(
            name='test_image.gif',
            content=self.valid_gif_bytes,
            content_type='image/gif'
        )

        # Published post by author1 with uploaded image & external image URL
        self.published_post = Post.objects.create(
            title='Published Post Title',
            content='This is published content for tech readers.',
            author=self.author1,
            category=self.category,
            status=Post.PUBLISHED,
            featured_image=self.test_image,
            external_image_url='https://example.com/external-stock.jpg',
            image_credit_name='Sample Photographer',
            image_credit_url='https://example.com/photo-credit'
        )
        self.published_post.tags.add(self.tag)

        # Draft post by author1
        self.draft_post = Post.objects.create(
            title='Secret Draft Title',
            content='This is draft content.',
            author=self.author1,
            category=self.category,
            status=Post.DRAFT,
            featured_image=self.test_image
        )

    def test_image_display_priority_uploaded_over_external(self):
        # Post has both uploaded featured_image and external_image_url
        post = Post.objects.create(
            title='Priority Test Post',
            content='Testing priority',
            author=self.author1,
            category=self.category,
            status=Post.PUBLISHED,
            featured_image=self.test_image,
            external_image_url='https://images.unsplash.com/sample.jpg'
        )
        # Uploaded image takes top priority
        self.assertEqual(post.display_image_url, post.featured_image.url)

    def test_image_display_external_url_when_no_uploaded_image(self):
        post = Post.objects.create(
            title='External URL Post',
            content='Testing external URL',
            author=self.author1,
            category=self.category,
            status=Post.PUBLISHED,
            external_image_url='https://images.unsplash.com/sample-stock.jpg'
        )
        self.assertEqual(post.display_image_url, 'https://images.unsplash.com/sample-stock.jpg')

    def test_image_display_default_fallback_when_neither_present(self):
        post = Post.objects.create(
            title='No Image Post',
            content='Testing fallback',
            author=self.author1,
            category=self.category,
            status=Post.PUBLISHED
        )
        self.assertEqual(post.display_image_url, '/static/images/default-post.jpg')

    def test_homepage_includes_external_image_url_for_seeded_post(self):
        post = Post.objects.create(
            title='Stock Image Post',
            content='Content here',
            author=self.author1,
            category=self.category,
            status=Post.PUBLISHED,
            external_image_url='https://images.unsplash.com/sample-stock-photo.jpg'
        )
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'https://images.unsplash.com/sample-stock-photo.jpg')

    def test_seed_command_idempotency(self):
        # Running seed command twice should not crash or duplicate users
        call_command('seed_blog')
        count_first = Post.objects.count()
        call_command('seed_blog')
        count_second = Post.objects.count()
        self.assertEqual(count_first, count_second)

    def test_reader_cannot_create_post(self):
        self.client.login(username='reader_test', password='password123')
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 403)

    def test_author_can_create_post(self):
        self.client.login(username='author1_test', password='password123')
        new_img = SimpleUploadedFile(
            name='new_post_img.gif',
            content=self.valid_gif_bytes,
            content_type='image/gif'
        )
        response = self.client.post(reverse('post_create'), {
            'title': 'New Author Post',
            'content': 'Some content for the new post.',
            'category': self.category.pk,
            'tags': [self.tag.pk],
            'status': Post.PUBLISHED,
            'featured_image': new_img
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='New Author Post').exists())

    def test_author_cannot_edit_another_authors_post(self):
        self.client.login(username='author2_test', password='password123')
        response = self.client.get(reverse('post_edit', kwargs={'slug': self.published_post.slug}))
        self.assertEqual(response.status_code, 403)

    def test_draft_post_hidden_publicly(self):
        # Homepage check
        response = self.client.get(reverse('home'))
        self.assertContains(response, self.published_post.title)
        self.assertNotContains(response, self.draft_post.title)

        # Category page check
        response = self.client.get(reverse('category_posts', kwargs={'slug': self.category.slug}))
        self.assertNotContains(response, self.draft_post.title)

        # Search check
        response = self.client.get(reverse('search') + '?q=Secret')
        self.assertNotContains(response, self.draft_post.title)

        # Public author profile check
        response = self.client.get(reverse('author_profile', kwargs={'username': self.author1.username}))
        self.assertNotContains(response, self.draft_post.title)

        # Detail page for unauthenticated or other user returns 404
        response = self.client.get(reverse('post_detail', kwargs={'slug': self.draft_post.slug}))
        self.assertEqual(response.status_code, 404)

    def test_published_post_visible_publicly(self):
        response = self.client.get(reverse('post_detail', kwargs={'slug': self.published_post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.published_post.title)

    def test_anonymous_user_cannot_comment(self):
        response = self.client.post(
            reverse('comment_create', kwargs={'slug': self.published_post.slug}),
            {'content': 'Anonymous comment text'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
        self.assertEqual(Comment.objects.count(), 0)

    def test_duplicate_likes_prevented_and_toggle(self):
        self.client.login(username='reader_test', password='password123')
        like_url = reverse('like_toggle', kwargs={'slug': self.published_post.slug})

        # First click -> Likes post
        response = self.client.post(like_url)
        self.assertEqual(Like.objects.filter(post=self.published_post, user=self.reader).count(), 1)

        # Second click -> Unlikes post (toggle)
        response = self.client.post(like_url)
        self.assertEqual(Like.objects.filter(post=self.published_post, user=self.reader).count(), 0)

    def test_comment_deletion_permissions(self):
        # Reader creates comment
        comment = Comment.objects.create(post=self.published_post, user=self.reader, content='Reader comment')

        # Author2 (unrelated user) attempts delete -> 403
        self.client.login(username='author2_test', password='password123')
        response = self.client.post(reverse('comment_delete', kwargs={'pk': comment.pk}))
        self.assertEqual(response.status_code, 403)

        # Comment owner (reader) attempts delete -> allowed
        self.client.login(username='reader_test', password='password123')
        response = self.client.post(reverse('comment_delete', kwargs={'pk': comment.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())

    def test_search_and_taxonomies(self):
        # Search
        response = self.client.get(reverse('search') + '?q=tech')
        self.assertContains(response, self.published_post.title)

        # Category
        response = self.client.get(reverse('category_posts', kwargs={'slug': self.category.slug}))
        self.assertContains(response, self.published_post.title)

        # Tag
        response = self.client.get(reverse('tag_posts', kwargs={'slug': self.tag.slug}))
        self.assertContains(response, self.published_post.title)
