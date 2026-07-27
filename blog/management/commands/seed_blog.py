import os
from io import BytesIO
from PIL import Image, ImageDraw
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from blog.models import AuthorProfile, Category, Tag, Post, Comment, Like


def generate_sample_image(title, bg_color=(13, 110, 253)):
    """Generate a sample placeholder image in memory using Pillow."""
    img = Image.new('RGB', (800, 450), color=bg_color)
    draw = ImageDraw.Draw(img)
    # Add subtle border box
    draw.rectangle([20, 20, 780, 430], outline=(255, 255, 255), width=4)
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=85)
    return ContentFile(buffer.getvalue(), name=f"{title.lower().replace(' ', '_')}.jpg")


class Command(BaseCommand):
    help = 'Seeds sample data including admin, authors, reader, categories, tags, posts, comments, and likes.'

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

        # Promote admin profile
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
        self.stdout.write(self.style.SUCCESS(f"Created {len(cat_objs)} categories."))

        # 6. Tags
        tags_data = ["Django", "Python", "WebDev", "Tutorial", "Travel", "Productivity"]
        tag_objs = {}
        for name in tags_data:
            t, _ = Tag.objects.get_or_create(name=name)
            tag_objs[name] = t
        self.stdout.write(self.style.SUCCESS(f"Created {len(tag_objs)} tags."))

        # 7. Posts
        posts_data = [
            {
                'title': 'Getting Started with Django 5 and Python',
                'author': author1,
                'category': cat_objs['Technology'],
                'tags': [tag_objs['Django'], tag_objs['Python'], tag_objs['Tutorial']],
                'status': Post.PUBLISHED,
                'content': 'Django makes it easier to build web applications faster with less code. In this comprehensive guide, we explore models, views, templates, and authentication in Django.\n\nSetting up your environment, creating your first app, and defining models are the first essential steps towards building production-grade web applications.',
                'bg_color': (13, 110, 253)
            },
            {
                'title': '10 Essential Productivity Hacks for Developers',
                'author': author2,
                'category': cat_objs['Lifestyle'],
                'tags': [tag_objs['Productivity'], tag_objs['WebDev']],
                'status': Post.PUBLISHED,
                'content': 'Productivity isn\'t about working longer hours; it\'s about working smarter. Discover time-blocking techniques, automated testing practices, and keyboard shortcuts that double your daily output.',
                'bg_color': (25, 135, 84)
            },
            {
                'title': 'Draft: Advanced Query Optimization in Django ORM',
                'author': author1,
                'category': cat_objs['Technology'],
                'tags': [tag_objs['Django'], tag_objs['Python']],
                'status': Post.DRAFT,
                'content': 'This draft explores select_related, prefetch_related, indexing, and raw query optimization techniques in Django. Work in progress - do not publish yet!',
                'bg_color': (220, 53, 69)
            },
            {
                'title': 'Exploring the Serene Mountains of Alpine Valleys',
                'author': author2,
                'category': cat_objs['Travel'],
                'tags': [tag_objs['Travel']],
                'status': Post.PUBLISHED,
                'content': 'Hiking through the Alpine paths offered breathtaking views, pristine glaciers, and tranquil wooden chalets. Join us on this visual journey through high-altitude adventures.',
                'bg_color': (255, 193, 7)
            },
            {
                'title': 'Building Rest APIs with Python and Django',
                'author': author1,
                'category': cat_objs['Education'],
                'tags': [tag_objs['Python'], tag_objs['Tutorial']],
                'status': Post.PUBLISHED,
                'content': 'Learn how to structure JSON endpoints, write serialized models, manage JWT authentication, and build scalable APIs using Django and Python.',
                'bg_color': (13, 202, 240)
            },
        ]

        created_posts = []
        for pdata in posts_data:
            post, p_created = Post.objects.get_or_create(
                title=pdata['title'],
                defaults={
                    'author': pdata['author'],
                    'category': pdata['category'],
                    'status': pdata['status'],
                    'content': pdata['content'],
                }
            )
            if p_created:
                # Add image
                img_file = generate_sample_image(post.title, pdata['bg_color'])
                post.featured_image.save(f"{post.slug}.jpg", img_file, save=False)
                post.save()
                post.tags.set(pdata['tags'])
            created_posts.append(post)

        self.stdout.write(self.style.SUCCESS(f"Created {len(created_posts)} sample posts."))

        # 8. Comments & Likes
        published_posts = [p for p in created_posts if p.status == Post.PUBLISHED]
        if published_posts:
            # Comment from reader1
            Comment.objects.get_or_create(
                post=published_posts[0],
                user=reader1,
                defaults={'content': 'Fantastic tutorial! Really clear explanation of Django basics.'}
            )
            # Comment from author2
            Comment.objects.get_or_create(
                post=published_posts[0],
                user=author2,
                defaults={'content': 'Great writeup Alice! Looking forward to your next post on ORM optimization.'}
            )
            # Likes
            Like.objects.get_or_create(post=published_posts[0], user=reader1)
            Like.objects.get_or_create(post=published_posts[0], user=author2)
            if len(published_posts) > 1:
                Like.objects.get_or_create(post=published_posts[1], user=reader1)

        self.stdout.write(self.style.SUCCESS("Sample comments and likes seeded successfully!"))
        self.stdout.write(self.style.SUCCESS("Seeding completed successfully!"))
