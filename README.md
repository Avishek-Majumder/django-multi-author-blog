# Multi-Author Blogging Platform Using Django

A robust, full-featured multi-author blogging web application built with Python 3, Django, SQLite, and Bootstrap 5.

This project implements user role management (Readers vs. Authors), blog post lifecycle management (Drafts & Published), Category & Tag filtering, interactive comments, a like system, search with pagination, an Author Dashboard with post analytics, and a comprehensive Django Admin integration.

---

## 📸 Sample Post Images

Seeded blog posts are configured with high-quality, free public stock images sourced from Unsplash under the Unsplash free-use license.

### Image Display Priority Logic
When rendering a blog post image, the application follows a strict 3-tier priority sequence:
1. **Author-Uploaded Image (`featured_image`):** Local file uploaded by an author takes top priority.
2. **External Sample Image URL (`external_image_url`):** Direct HTTPS stock image CDN URL used when no local file is uploaded.
3. **Local Default Fallback (`/static/images/default-post.jpg`):** Clean neutral graphic displayed if neither uploaded file nor external URL exists, or if browser loading encounters a network error (`onerror` fallback).

> **Note:** External stock images require an active internet connection to load. Authors can upload local images at any time to override external images.

### Stock Photo Credits
We gratefully acknowledge the photographers on Unsplash for providing royalty-free images:
- **Domenico Loia** ([Unsplash Photo Page](https://unsplash.com/photos/hGV2TfOh0ns)) – *Getting Started with Django 5 and Python*
- **Andrew Neel** ([Unsplash Photo Page](https://unsplash.com/photos/cckf433-14g)) – *10 Essential Productivity Hacks for Developers*
- **Florian Olivo** ([Unsplash Photo Page](https://unsplash.com/photos/4hb8-eymZ-E)) – *Draft: Advanced Query Optimization in Django ORM*
- **Kalen Emsley** ([Unsplash Photo Page](https://unsplash.com/photos/Bkci_8qcdvQ)) – *Exploring the Serene Mountains of Alpine Valleys*
- **Clement Helvez** ([Unsplash Photo Page](https://unsplash.com/photos/95YRwf6CNw8)) – *Building REST APIs with Python and Django*

---

## 🌟 Key Features

### 1. User Authentication & Role Management
- **Reader (Default Role):** All newly registered users are Readers. Readers can browse published posts, search, filter by category/tag, view public author profiles, submit comments, and like/unlike posts.
- **Author:** Readers who are promoted by the site Administrator via Django Admin. Authors gain access to the **Author Dashboard**, can create new posts, edit/delete only their own posts, view draft & published posts, and moderate comments on their articles.
- **Administrator / Superuser:** Full control over the platform via the Django Admin panel (manage all users, promote/revoke Author status, manage categories, tags, posts, and comments).

### 2. Category & Tag Taxonomies
- **Categories:** Single relationship per post (`ForeignKey`). Admin-managed via Django Admin with auto-generated unique slugs.
- **Tags:** Many-to-many relationship per post (`ManyToManyField`). Admin-managed via Django Admin with auto-generated unique slugs.

### 3. Blog Post Lifecycle & Draft Privacy
- Posts support status: **Draft** or **Published**.
- Auto-generated unique slugs with duplicate title collision protection.
- Required/optional featured image upload handled cleanly via Pillow with display fallback logic.
- **Strict Privacy:** Draft posts are strictly hidden from the homepage, category pages, tag pages, search results, and public author profiles. Drafts are accessible only to their author in their Author Dashboard or to superusers.

### 4. Author Dashboard & Analytics
- Dedicated, role-protected dashboard for approved Authors (`/dashboard/`).
- Shows post metrics: total posts, published count, draft count, view count, like count, comment count.
- Provides fast action links to create, edit, or delete posts.

### 5. Interactive Features
- **Comment System:** Logged-in users can comment on published posts. Comment deletion is permitted for the comment creator, the post author, or the site admin.
- **Like Toggle System:** Logged-in users can like or unlike posts. Unique database constraint (`UniqueConstraint(fields=['post', 'user'])`) prevents duplicate likes.
- **Search & Pagination:** Case-insensitive search across post title and content (`Q` objects) with 10 items per page pagination preserving query parameters.
- **Public Author Profiles:** Publicly accessible page (`/author/<username>/`) displaying author bio and published articles.

---

## 🛠️ Technology Stack

- **Backend:** Python 3.10+, Django 5.x / 6.x
- **Database:** SQLite3
- **Frontend:** HTML5, CSS3, Bootstrap 5 (via CDN), Bootstrap Icons
- **Image Processing:** Pillow
- **Environment Management:** `python-dotenv`

---

## 📁 Project Structure

```text
django-multi-author-blog/
│
├── blog/                      # Main Django Application
│   ├── management/
│   │   └── commands/
│   │       └── seed_blog.py   # Seed script for sample users, categories, stock photos
│   ├── migrations/            # Database migration scripts
│   ├── templates/blog/        # HTML Templates & Partial Include
│   │   ├── includes/
│   │   │   └── post_image.html # Reusable post image partial with onerror fallback
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
│   ├── admin.py               # Django Admin configuration & image preview
│   ├── apps.py                # App config & signals loader
│   ├── decorators.py          # Custom @author_required view decorator
│   ├── forms.py               # Registration, Post, and Comment forms
│   ├── models.py              # AuthorProfile, Category, Tag, Post, Comment, Like models
│   ├── signals.py             # Auto-create AuthorProfile on User creation
│   ├── tests.py               # Automated unit test suite (14 tests)
│   ├── urls.py                # Application URL routing
│   └── views.py               # Application logic & controller views
│
├── config/                    # Django Project Settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── media/                     # Uploaded media files
├── static/
│   ├── css/
│   │   └── style.css          # Custom responsive image & card styling
│   └── images/
│       └── default-post.jpg   # Default fallback image
│
├── .env                       # Environment secrets (ignored by Git)
├── .env.example               # Template environment configuration file
├── .gitignore                 # Git ignore rules
├── manage.py                  # Django management script
├── requirements.txt           # Dependency requirements file
└── README.md                  # Project documentation
```

---

## 🚀 Local Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/django-multi-author-blog.git
cd django-multi-author-blog
```

### 2. Create and Activate Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables Setup
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

### 5. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```

### 7. Seed Sample Data with Real Stock Photos
```bash
python manage.py seed_blog
```

**Sample Credentials created by `seed_blog` (Development only):**
| Role | Username | Password | Notes |
| :--- | :--- | :--- | :--- |
| **Admin / Superuser** | `admin` | `admin123` | Full Django Admin access & Author privileges |
| **Author 1** | `author1` | `author123` | Approved Author with sample tech posts & draft |
| **Author 2** | `author2` | `author234` | Approved Author with travel & lifestyle posts |
| **Reader 1** | `reader1` | `reader123` | Regular Reader user |

### 8. Start Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your web browser.

---

## 👤 Admin Author Promotion Guide

To promote a regular Reader to an Author:
1. Log in to Django Admin at `http://127.0.0.1:8000/admin/` using your superuser account.
2. Go to **Blog > Author profiles**.
3. Locate the user you wish to promote.
4. Check the **Is author** box and click **Save**.

---

## 🧪 Running Automated Tests

Run the test suite (14 unit tests):
```bash
python manage.py test blog
```

---

## 🛡️ Security & Git Hygiene

Excluded from version control via `.gitignore`: `.env`, `venv/`, `db.sqlite3`, `media/`, `__pycache__/`.

---

## 📤 Submission & GitHub Upload Commands

```bash
git init
git add .
git commit -m "Complete Django multi-author blogging platform with stock images"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/django-multi-author-blog.git
git push -u origin main
```
