# Andromeda Properties - Real Estate Website

A Django-based real estate website featuring property listings, project management, blog, and team pages.

## Features

- **Property Management**: List, search, and filter properties by location, type, bedrooms, and status
- **Project Listings**: Organize properties by projects
- **Blog System**: Publish and manage blog posts
- **Team Management**: Display sales officers and agents
- **User Authentication**: Login, register, and password reset functionality
- **Contact Forms**: Property inquiries and general contact
- **Modern UI**: Responsive design with Bootstrap 5

## Installation

1. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Create a superuser**:
```bash
python manage.py createsuperuser
```

5. **Collect static files**:
```bash
python manage.py collectstatic
```

6. **Run the development server**:
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see the website.

## Admin Access

Access the admin panel at `http://127.0.0.1:8000/admin/` using your superuser credentials.

## Project Structure

```
andromedaproperties/
├── properties/          # Main app for properties, projects, team
├── blog/                # Blog app
├── accounts/            # Authentication app
├── templates/           # HTML templates
├── static/              # CSS, JS, images
├── media/               # User uploaded files
└── andromedaproperties/  # Project settings
```

## Models

- **Property**: Real estate listings with details (bedrooms, bathrooms, size, etc.)
- **Project**: Property projects/developments
- **PropertyImage**: Multiple images per property
- **Contact**: Contact form submissions and property inquiries
- **TeamMember**: Sales officers and agents
- **BlogPost**: Blog articles

## Usage

1. **Add Properties**: Use the admin panel to add properties, projects, and team members
2. **Manage Blog**: Create and publish blog posts through the admin
3. **View Properties**: Browse properties on the home page or property list page
4. **Search**: Use the search form to filter properties
5. **Contact**: Users can submit inquiries through property detail pages or contact form

## Development

The project uses:
- Django 4.2.7
- Bootstrap 5.3.0
- Bootstrap Icons
- Pillow for image handling
- Crispy Forms for form styling

## Notes

- Make sure to set up proper media file handling in production
- Configure email settings for password reset functionality
- Add your own images to the `static/images/` directory
- Customize the styling in `static/css/style.css`

## License

This project is for educational/demonstration purposes.

