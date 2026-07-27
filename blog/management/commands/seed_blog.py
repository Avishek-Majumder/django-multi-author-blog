from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import AuthorProfile, Category, Tag, Post, Comment, Like


def is_generated_seed_placeholder(image_name):
    if not image_name:
        return False
    name_str = str(image_name).lower()
    return 'building-rest-apis' in name_str or 'building_rest_apis' in name_str or 'posts/' in name_str


class Command(BaseCommand):
    help = 'Seeds sample data including admin, authors, reader, categories, tags, posts with real stock images, comments, and likes.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Starting database seeding process..."))

        # 1. Superuser / Admin
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
                'first_name': 'Site',
                'last_name': 'Admin'
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Superuser created: username 'admin', password 'admin123'"))

        admin_profile, _ = AuthorProfile.objects.get_or_create(user=admin_user)
        admin_profile.is_author = True
        admin_profile.bio = "Master Administrator and Lead Editor."
        admin_profile.save()

        # 2. Author 1
        author1, created = User.objects.get_or_create(
            username='author1',
            defaults={
                'email': 'author1@example.com',
                'first_name': 'Alice',
                'last_name': 'Smith'
            }
        )
        if created:
            author1.set_password('author123')
            author1.save()
            self.stdout.write(self.style.SUCCESS("Author created: username 'author1', password 'author123'"))

        prof1, _ = AuthorProfile.objects.get_or_create(user=author1)
        prof1.is_author = True
        prof1.bio = "Tech enthusiast writing about Django, Python, and backend architecture."
        prof1.save()

        # 3. Author 2
        author2, created = User.objects.get_or_create(
            username='author2',
            defaults={
                'email': 'author2@example.com',
                'first_name': 'Bob',
                'last_name': 'Johnson'
            }
        )
        if created:
            author2.set_password('author234')
            author2.save()
            self.stdout.write(self.style.SUCCESS("Author created: username 'author2', password 'author234'"))

        prof2, _ = AuthorProfile.objects.get_or_create(user=author2)
        prof2.is_author = True
        prof2.bio = "Traveler, lifestyle blogger, and web designer."
        prof2.save()

        # 4. Reader 1
        reader1, created = User.objects.get_or_create(
            username='reader1',
            defaults={
                'email': 'reader1@example.com',
                'first_name': 'Charlie',
                'last_name': 'Brown'
            }
        )
        if created:
            reader1.set_password('reader123')
            reader1.save()
            self.stdout.write(self.style.SUCCESS("Reader created: username 'reader1', password 'reader123'"))

        prof3, _ = AuthorProfile.objects.get_or_create(user=reader1)
        prof3.is_author = False
        prof3.bio = "Avid reader and commenter."
        prof3.save()

        # 5. Categories
        categories_data = [
            ("Technology", "Insights on software engineering and web development."),
            ("Lifestyle", "Daily life, wellness, and productivity tips."),
            ("Travel", "Exploring destinations around the world."),
            ("Education", "Tutorials and step-by-step guides for learners.")
        ]
        cat_objs = {}
        for name, desc in categories_data:
            cat, _ = Category.objects.get_or_create(name=name)
            cat_objs[name] = cat
        self.stdout.write(self.style.SUCCESS(f"Created/verified {len(cat_objs)} categories."))

        # 6. Tags
        tags_data = ["Django", "Python", "WebDev", "Tutorial", "Travel", "Productivity"]
        tag_objs = {}
        for name in tags_data:
            t, _ = Tag.objects.get_or_create(name=name)
            tag_objs[name] = t
        self.stdout.write(self.style.SUCCESS(f"Created/verified {len(tag_objs)} tags."))

        # Deduplicate any post created with slight capitalization variation ('Building Rest APIs' vs 'Building REST APIs')
        rest_api_posts = list(Post.objects.filter(title__iexact='Building REST APIs with Python and Django'))
        if len(rest_api_posts) > 1:
            primary_post = rest_api_posts[0]
            for dup in rest_api_posts[1:]:
                # Reassign comments/likes if any
                dup.comments.update(post=primary_post)
                dup.likes.update(post=primary_post)
                dup.delete()

        # 7. Posts with High-Quality Free Stock Photo URLs (Unsplash License)
        posts_data = [
            {
                'title': 'Getting Started with Django 5 and Python',
                'author': author1,
                'category': cat_objs['Technology'],
                'tags': [tag_objs['Django'], tag_objs['Python'], tag_objs['Tutorial']],
                'status': Post.PUBLISHED,
                'content': 'Django makes it easier to build web applications faster with less code. In this comprehensive guide, we explore models, views, templates, and authentication in Django.\n\nSetting up your environment, creating your first app, and defining models are the first essential steps towards building production-grade web applications.',
                'external_image_url': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1200&q=80',
                'image_credit_name': 'Domenico Loia',
                'image_credit_url': 'https://unsplash.com/photos/hGV2TfOh0ns',
            },
            {
                'title': '10 Essential Productivity Hacks for Developers',
                'author': author2,
                'category': cat_objs['Lifestyle'],
                'tags': [tag_objs['Productivity'], tag_objs['WebDev']],
                'status': Post.PUBLISHED,
                'content': 'Productivity isn\'t about working longer hours; it\'s about working smarter. Discover time-blocking techniques, automated testing practices, and keyboard shortcuts that double your daily output.',
                'external_image_url': 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=1200&q=80',
                'image_credit_name': 'Andrew Neel',
                'image_credit_url': 'https://unsplash.com/photos/cckf433-14g',
            },
            {
                'title': 'Draft: Advanced Query Optimization in Django ORM',
                'author': author1,
                'category': cat_objs['Technology'],
                'tags': [tag_objs['Django'], tag_objs['Python']],
                'status': Post.DRAFT,
                'content': 'This draft explores select_related, prefetch_related, indexing, and raw query optimization techniques in Django. Work in progress - do not publish yet!',
                'external_image_url': 'https://images.unsplash.com/photo-1542831371-29b0f74f9713?auto=format&fit=crop&w=1200&q=80',
                'image_credit_name': 'Florian Olivo',
                'image_credit_url': 'https://unsplash.com/photos/4hb8-eymZ-E',
            },
            {
                'title': 'Exploring the Serene Mountains of Alpine Valleys',
                'author': author2,
                'category': cat_objs['Travel'],
                'tags': [tag_objs['Travel']],
                'status': Post.PUBLISHED,
                'content': 'Hiking through the Alpine paths offered breathtaking views, pristine glaciers, and tranquil wooden chalets. Join us on this visual journey through high-altitude adventures.',
                'external_image_url': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=80',
                'image_credit_name': 'Kalen Emsley',
                'image_credit_url': 'https://unsplash.com/photos/Bkci_8qcdvQ',
            },
            {
                'title': 'Building Rest APIs with Python and Django',
                'author': author1,
                'category': cat_objs['Education'],
                'tags': [tag_objs['Python'], tag_objs['Tutorial']],
                'status': Post.PUBLISHED,
                'content': 'Learn how to structure JSON endpoints, write serialized models, manage JWT authentication, and build scalable APIs using Django and Python.',
                'external_image_url': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=1200&q=80',
                'image_credit_name': 'Clement Helvez',
                'image_credit_url': 'https://unsplash.com/photos/95YRwf6CNw8',
            },
        ]

        created_posts = []
        for pdata in posts_data:
            # Case-insensitive check to avoid duplicate creation on capitalization mismatch
            existing = Post.objects.filter(title__iexact=pdata['title']).first()
            if existing:
                post = existing
                post.title = pdata['title']
                post.author = pdata['author']
                post.category = pdata['category']
                post.status = pdata['status']
                post.content = pdata['content']
                post.external_image_url = pdata['external_image_url']
                post.image_credit_name = pdata['image_credit_name']
                post.image_credit_url = pdata['image_credit_url']
            else:
                post = Post(
                    title=pdata['title'],
                    author=pdata['author'],
                    category=pdata['category'],
                    status=pdata['status'],
                    content=pdata['content'],
                    external_image_url=pdata['external_image_url'],
                    image_credit_name=pdata['image_credit_name'],
                    image_credit_url=pdata['image_credit_url'],
                )

            # If post contains old generated seed placeholder, clear featured_image so external stock photo displays
            if post.featured_image and is_generated_seed_placeholder(post.featured_image.name):
                try:
                    post.featured_image.delete(save=False)
                except Exception:
                    pass
                post.featured_image = None

            post.save()
            post.tags.set(pdata['tags'])
            created_posts.append(post)

        self.stdout.write(self.style.SUCCESS(f"Seeded/updated {len(created_posts)} sample posts with stock images."))

        # 8. Comments & Likes
        published_posts = [p for p in created_posts if p.status == Post.PUBLISHED]
        if published_posts:
            Comment.objects.get_or_create(
                post=published_posts[0],
                user=reader1,
                defaults={'content': 'Fantastic tutorial! Really clear explanation of Django basics.'}
            )
            Comment.objects.get_or_create(
                post=published_posts[0],
                user=author2,
                defaults={'content': 'Great writeup Alice! Looking forward to your next post on ORM optimization.'}
            )
            Like.objects.get_or_create(post=published_posts[0], user=reader1)
            Like.objects.get_or_create(post=published_posts[0], user=author2)
            if len(published_posts) > 1:
                Like.objects.get_or_create(post=published_posts[1], user=reader1)

        self.stdout.write(self.style.SUCCESS("Sample comments and likes seeded successfully!"))
        self.stdout.write(self.style.SUCCESS("Seeding completed successfully!"))
