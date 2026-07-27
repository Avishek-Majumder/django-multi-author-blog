# Multi-Author Blogging Platform Using Django

A robust, full-featured multi-author blogging web application built with Python 3, Django, SQLite, and Bootstrap 5.

This project implements user role management (Readers vs. Authors), blog post lifecycle management (Drafts & Published), Category & Tag filtering, interactive comments, a like system, search with pagination, an Author Dashboard with post analytics, and a comprehensive Django Admin integration.

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
- Required featured image upload handled cleanly via Pillow.
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
│   │       └── seed_blog.py   # Seed script for sample users, categories, posts, comments
│   ├── migrations/            # Database migration scripts
│   ├── templates/blog/        # HTML Templates
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
│   ├── admin.py               # Django Admin configuration & list displays
│   ├── apps.py                # App config & signals loader
│   ├── decorators.py          # Custom @author_required view decorator
│   ├── forms.py               # Registration, Post, and Comment forms
│   ├── models.py              # AuthorProfile, Category, Tag, Post, Comment, Like models
│   ├── signals.py             # Auto-create AuthorProfile on User creation
│   ├── tests.py               # Automated unit test suite
│   ├── urls.py                # Application URL routing
│   └── views.py               # Application logic & controller views
│
├── config/                    # Django Project Settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── media/                     # Uploaded media files (featured images)
├── static/
│   └── css/
│       └── style.css          # Custom styling additions
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
Ensure your `.env` contains:
```env
SECRET_KEY=django-insecure-your-custom-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
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
Follow the prompts to enter a username, email, and password.

### 7. Seed Sample Data (Optional but Recommended)
Run the built-in management command to automatically populate sample users, categories, tags, published posts, drafts, comments, and likes:
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
5. The user will immediately gain access to the **Author Dashboard** (`/dashboard/`) and post creation tools.

---

## 🧪 Running Automated Tests

The repository includes comprehensive automated unit tests covering user role authorization, post creation/editing restrictions, draft privacy, comment moderation, and duplicate like prevention.

Run the test suite with:
```bash
python manage.py test blog
```

---

## 🛡️ Security & Git Hygiene

The following items are strictly excluded from version control via `.gitignore`:
- Real `.env` files with API keys or secret tokens
- Virtual environment directory (`venv/`)
- Local SQLite database (`db.sqlite3`)
- User-uploaded media files (`media/`)
- Python bytecode (`__pycache__/`, `*.pyc`)

---

## 📤 Submission & GitHub Upload Commands

To initialize and push your project to GitHub:

```bash
git init
git add .
git commit -m "Complete Django multi-author blogging platform"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/django-multi-author-blog.git
git push -u origin main
```

---

## 🌐 Optional Deployment Notes

### Deploying on Render / PythonAnywhere:
1. Set `DEBUG=False` in environment variables on your deployment platform.
2. Set a secure `SECRET_KEY` and set `ALLOWED_HOSTS` to your live domain (e.g. `your-app.onrender.com`).
3. Set up static file collection using `python manage.py collectstatic` or `whitenoise`.
