# Team Training and Consultancy Service PLC

A Django-based corporate website for training, consultancy, and human resource services in Ethiopia.

## Features

- **Services**: Management consultancy, strategic leadership, HR sourcing, investment, and organizational development
- **Training & Events**: Event listings, calendar, registration, and brochure downloads
- **Operational Showcases**: Case studies with project timelines
- **Team Profiles**: Founders, trainers, and associate consultants
- **Media Gallery**: Grouped photo and video albums
- **Corporate Blog**: Searchable articles with categories and meta-tag filters
- **Contact**: Secure forms, working hours, and Google Maps integration
- **Admin Panel**: Full content management via Django Jazzmin

## Installation

1. **Create a virtual environment** (recommended):
```bash
python -m venv venv
venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run migrations**:
```bash
python manage.py migrate
```

4. **Seed initial company data**:
```bash
python manage.py seed_ttcs_data
```

5. **Create a superuser**:
```bash
python manage.py createsuperuser
```

6. **Run the development server**:
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/

## Project Structure

```
TTC/
├── properties/           # Main app (services, events, team, gallery, etc.)
├── blog/                 # Corporate blog
├── accounts/             # User authentication
├── templates/            # HTML templates
├── static/               # CSS, JS, images (team-training-logo.jpg)
└── ttcs_site/            # Django project settings
```

## Admin

Access the admin panel at `/admin/` to manage all site content.

## Contact

- Phone: +251969055405 / +251911744353
- Email: teamconsultency@gmail.com
- Location: Adama City, Ethiopia
