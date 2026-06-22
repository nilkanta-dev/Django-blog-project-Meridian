# Meridian- A Complete Django Blog Platform

A **feature-rich blogging platform** built with **Django**, **Django REST Framework**, and **Supabase** for media storage — deployed seamlessly on **Render**.  
It supports user accounts, post management with rich text editing (TinyMCE), nested comments with voting, and REST APIs with API key authentication and Swagger documentation.

---

## Features

### User System
- Register, log in, and manage your profile.
- Create, edit, and delete your own blog posts.
- Each user has a dashboard to manage their content and generate API keys.

### Blog Functionality
- Home page lists all published posts with pagination.
- Detailed post page with content, author info, and comment section.
- Supports **nested comments** (replies within replies).
- Users can **vote** (like/dislike) comments.
- Rich text post editing powered by **TinyMCE**.

### Role-Based Access
- **Admin/Staff users** have elevated privileges:
  - View all registered users(Admin).
  - Delete or moderate any user’s post or comment(Admin/Staff).
  - Manage user permissions(Admin).

### API System
- Built using **Django REST Framework (DRF)**.
- Each user can generate a unique **API key** from their dashboard.
- API is read-only.
- Includes interactive **Swagger Documentation** accessible via the main menu.

### Storage & Deployment
- Hosted on **Render** for production deployment.
- Uses **Supabase Storage** for hosting and serving image files.
- Static files handled using **Whitenoise**.
- PostgreSQL database managed by Render.

---

## Tech Stack

| Tool | Purpose |
|------|----------|
| **Django 5.2** | Web framework |
| **Django REST Framework** | RESTful API support |
| **TinyMCE** | Rich text editor for posts |
| **Supabase** | Cloud storage for images |
| **Render** | Cloud deployment platform |
| **Whitenoise** | Static file management |
| **Gunicorn** | WSGI server for Render |
| **PyJWT + DRF SimpleJWT** | Token-based authentication |
| **drf-spectacular** | Swagger/OpenAPI documentation |
| **PostgreSQL** | Production database |

---

## Getting Started

### Clone the repository

```bash
git clone https://github.com/nilkanta-dev/Django-blog-project-Meridian.git
cd Django-blog-project-Meridian
```

### Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # (Linux/macOS)
venv\Scripts\activate     # (Windows)
```

### Set up environment variables

```bash
DEBUG=True
SECRET_KEY=your_django_secret_key
DATABASE_URL=your_render_postgres_url

AWS_ACCESS_KEY='your-supabase-access-key'
AWS_SECRET_ACCESS_KEY='your-supabase-secret-key'
AWS_STORAGE_BUCKET_NAME='your-supabase-storage-name'
AWS_S3_ENDPOINT_URL='your-supabase-endpoint-url'
AWS_S3_REGION_NAME='your-supabase-region-name'
SUPABASE_PROJECT_REF=<your-supabase-project-id>
SUPABASE_URL=https://<your-supabase-project-id>.storage.supabase.co/storage/v1/s3
SUPABASE_KEY=your_supabase_api_key
```

### Run migrations and start the server

```bash
python manage.py migrate
python manage.py runserver
```

Then visit http://localhost:8000/

## API Documentation

Once the server is running, open:
```bash
http://localhost:8000/api/v1
```
to access the DRF api view.

If you want to access the **SwaggerUI** documentation of the api, click on the **API** option in the **Homepage**.

### API Authentication

Users can create and manage their API keys directly from their dashboard.
These keys are required for accessing protected API endpoints.

## License

This project is licensed under the MIT License.

## Author

**Nilkanta@33**<br>
*Full-Stack Python Developer*

