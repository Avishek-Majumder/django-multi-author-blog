# Multi-Author Blogging Platform

Developed by **Avishek Majumder**

A multi-author blogging web application built using Python 3, Django, SQLite, and Bootstrap 5.

This application provides role-based access control separating regular readers from approved authors. Visitors can browse published articles, search content, filter by categories and tags, view public author profiles, submit comments, and like posts. Approved authors gain access to a dedicated dashboard where they can write, edit, publish, and manage their blog posts while keeping drafts strictly private.

---

## Key Features

### User Authentication and Role Management
- **Reader (Default Role):** Newly registered users start as Readers. Registered readers can browse published posts, search, filter by category/tag, view public author profiles, post comments, and like or unlike articles.
- **Author:** Readers promoted by the site administrator gain access to the Author Dashboard (`/dashboard/`). Authors can create posts, edit or delete their own posts, view their drafts, and moderate comments on their articles.
- **Administrator:** Site administrators manage users, promote or revoke author privileges, manage categories and tags, moderate comments, and oversee all posts through the Django Admin panel.

### Category and Tag Management
- **Categories:** Single category per post using Django ForeignKeys. Categories can be managed by administrators with auto-generated unique slugs.
- **Tags:** Multiple tags per post using Django ManyToManyField relationships. Tags are managed through the admin panel with auto-generated unique slugs.

### Post Lifecycle and Draft Privacy
- **Status Options:** Posts can be saved as `Draft` or published as `Published`.
- **Slug Handling:** Unique slugs are auto-generated from post titles, with automatic collision resolution for identical titles.
- **Draft Protection:** Draft posts are strictly private. They do not appear on the homepage, search results, category pages, tag pages, or public author profiles. Drafts are accessible only to the post's author or site administrators.

### Author Dashboard and Analytics
- **Dashboard Access:** Dedicated management view located at `/dashboard/` for approved authors.
- **Post Metrics:** Displays summary analytics including total posts, published count, draft count, total view count, like count, and comment count.
- **Management Tools:** Provides actions to create, update, or remove articles.

### Interactive Features
- **Comment System:** Authenticated users can leave comments on published posts. Comments are ordered chronologically. Comment deletion is restricted to the comment author, the post author, or site administrators.
- **Like Toggle:** Authenticated users can like or unlike articles. Duplicate likes are prevented at both database and application levels using Django unique constraints.
- **Search and Pagination:** Case-insensitive search across post titles and content using Django Q objects, with paginated results that preserve active search query parameters.
- **Public Author Profiles:** Dedicated profile pages at `/author/<username>/` displaying author metadata and published articles.

---

## Image Handling and Fallback Logic

### Image Selection Priority
When displaying a post image, the application follows a 3-tier priority sequence:
1. **Uploaded Featured Image:** Local image file uploaded by an author takes top priority.
2. **External Stock Image URL:** Direct CDN URL used for sample posts when no local file has been uploaded.
3. **Local Default Fallback:** Default image located at `/static/images/default-post.jpg` displayed if neither source is available or if an image loading error occurs (`onerror` fallback).

### Stock Photo Credits
Sample posts use royalty-free images from Unsplash under the Unsplash free-use license:
- **Domenico Loia** ([Unsplash Photo Page](https://unsplash.com/photos/hGV2TfOh0ns)) - *Getting Started with Django 5 and Python*
- **Andrew Neel** ([Unsplash Photo Page](https://unsplash.com/photos/cckf433-14g)) - *10 Essential Productivity Hacks for Developers*
- **Florian Olivo** ([Unsplash Photo Page](https://unsplash.com/photos/4hb8-eymZ-E)) - *Draft: Advanced Query Optimization in Django ORM*
- **Kalen Emsley** ([Unsplash Photo Page](https://unsplash.com/photos/Bkci_8qcdvQ)) - *Exploring the Serene Mountains of Alpine Valleys*
- **Clement Helvez** ([Unsplash Photo Page](https://unsplash.com/photos/95YRwf6CNw8)) - *Building REST APIs with Python and Django*

---

## Technology Stack

- **Backend:** Python 3, Django 5.x
- **Database:** SQLite3
- **Frontend:** HTML5, CSS3, Bootstrap 5, Bootstrap Icons
- **Image Processing:** Pillow
- **Environment Management:** python-dotenv

---

## Project Structure

```text
django-multi-author-blog/
├── blog/                      # Django application directory
│   ├── management/
│   │   └── commands/
│   │       └── seed_blog.py   # Database seeder for sample users, posts, and taxonomies
│   ├── migrations/            # Database migration files
│   ├── templates/blog/        # HTML templates and partials
│   │   ├── includes/
│   │   │   └── post_image.html # Reusable post image component
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── post_detail.html
│   │   ├── author_dashboard.html
│   │   ├── post_form.html
│   │   ├── post_confirm_delete.html
│   │   ├── comment_confirm_delete.html
│   │   ├── category_posts.html
│   │   ├── tag_posts.html
│   │   ├── search_results.html
│   │   ├── author_profile.html
│   │   ├── register.html
│   │   └── login.html
│   ├── admin.py               # Django Admin configuration and list displays
│   ├── apps.py                # App configuration and signal registry
│   ├── decorators.py          # View decorator for author authorization
│   ├── forms.py               # Registration, post, and comment forms
│   ├── models.py              # AuthorProfile, Category, Tag, Post, Comment, Like models
│   ├── signals.py             # User post-save signal for profile generation
│   ├── tests.py               # Automated unit test suite
│   ├── urls.py                # Application URL routing
│   └── views.py               # Application views and business logic
├── config/                    # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── media/                     # Uploaded media files
├── static/
│   ├── css/
│   │   └── style.css          # Custom CSS styling and responsive layout rules
│   └── images/
│       └── default-post.jpg   # Fallback post image
├── .env                       # Local environment variables (ignored by Git)
├── .env.example               # Environment template file
├── .gitignore                 # Git ignore rules
├── manage.py                  # Django management CLI script
├── requirements.txt           # Dependency requirements file
└── README.md                  # Project documentation
```

---

## Local Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/django-multi-author-blog.git
cd django-multi-author-blog
```

### 2. Create and Activate a Virtual Environment

**On Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**On macOS and Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Ensure your local `.env` file contains valid configurations:
```env
SECRET_KEY=django-insecure-dev-secret-key-multi-author-blog-2026-secure
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser (Administrator)
```bash
python manage.py createsuperuser
```

### 7. Seed Sample Data (Optional)
Populate sample users, categories, tags, published posts, drafts, comments, and likes:
```bash
python manage.py seed_blog
```

#### Development Credentials (Created by `seed_blog`)
| Role | Username | Password | Notes |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | Full Django Admin access and Author privileges |
| **Author 1** | `author1` | `author123` | Approved Author with sample tech posts and draft |
| **Author 2** | `author2` | `author234` | Approved Author with travel and lifestyle posts |
| **Reader 1** | `reader1` | `reader123` | Standard Reader account |

### 8. Start the Development Server
```bash
python manage.py runserver
```
Open `http://127.0.0.1:8000/` in your browser.

---

## Admin Author Promotion Guide

To promote a registered Reader to Author status:
1. Log in to the Django Admin panel at `http://127.0.0.1:8000/admin/` using an administrator account.
2. Navigate to **Blog > Author profiles**.
3. Select the target user profile.
4. Check the **Is author** checkbox and save the changes.
5. The user will immediately have access to the Author Dashboard at `/dashboard/` and post creation tools.

---

## Running Automated Tests

Execute the automated test suite to verify application functionality, role authorizations, draft privacy, and image handling:
```bash
python manage.py test blog
```

---

## Security and Git Hygiene

The following files are excluded from Git tracking via `.gitignore`:
- `.env` (contains sensitive keys and configuration)
- `venv/` (virtual environment directory)
- `db.sqlite3` (local database file)
- `media/` (user-uploaded media files)
- `__pycache__/` (Python compiled bytecode)

---

## GitHub Submission Commands

To push this repository to GitHub:

```bash
git init
git add .
git commit -m "Complete Django multi-author blogging platform"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/django-multi-author-blog.git
git push -u origin main
```

---

## Optional Deployment Guidance

When deploying to platforms such as Render or PythonAnywhere:
1. Set `DEBUG=False` in environment settings.
2. Configure a secure `SECRET_KEY` and set `ALLOWED_HOSTS` to your production domain.
3. Collect static files using `python manage.py collectstatic`.
