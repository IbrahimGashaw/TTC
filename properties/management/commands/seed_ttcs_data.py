from datetime import datetime, time, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from properties.models import (
    SiteSettings, HomePageSettings, Service, TrainingEvent, CaseStudy,
    CaseStudyTimeline, Testimonial, Partner, Milestone, TeamMember, WorkingSchedule,
)
from blog.models import BlogCategory, BlogPost


class Command(BaseCommand):
    help = 'Seed initial data for Team Training and Consultancy Service PLC'

    def handle(self, *args, **options):
        self.stdout.write('Seeding TTCS data...')

        site = SiteSettings.load()
        site.company_name = 'Team Training and Consultancy Service PLC'
        site.company_tagline = 'Guiding your Success, Every step of the way!'
        site.company_phone = '+251969055405'
        site.company_phone_secondary = '+251911744353'
        site.company_email = 'teamconsultency@gmail.com'
        site.company_address = 'Adama City, Ethiopia'
        site.latitude = 8.5400
        site.longitude = 39.2700
        site.whatsapp_number = '+251969055405'
        site.whatsapp_default_message = 'Hello! I am interested in your training and consultancy services.'
        site.save()

        homepage = HomePageSettings.load()
        # Keep existing video settings; only enable video on first seed when none is configured.
        if not homepage.hero_video and not homepage.get_video_url():
            homepage.hero_video_enabled = True
            homepage.save()

        services_data = [
            {
                'title': 'Management Consultancy',
                'slug': 'management-consultancy',
                'category': 'management_consultancy',
                'icon': 'bi-briefcase',
                'short_description': 'Expert management consultancy services to optimize organizational performance and drive sustainable business growth.',
                'full_description': 'Our management consultancy services help organizations identify challenges, develop strategic solutions, and implement effective management practices. We work with leadership teams to enhance decision-making, streamline operations, and achieve measurable results across all business functions.',
            },
            {
                'title': 'Strategic Leadership Training',
                'slug': 'strategic-leadership',
                'category': 'strategic_leadership',
                'icon': 'bi-graph-up-arrow',
                'short_description': 'High-level leadership and strategic management training programs designed for executives and management teams.',
                'full_description': 'We deliver impactful leadership and strategic management training tailored to address complex organizational challenges. Our programs enhance the leadership capabilities of management teams, fostering strategic thinking, effective decision-making, and organizational transformation.',
            },
            {
                'title': 'HR Sourcing & Recruitment',
                'slug': 'hr-sourcing',
                'category': 'hr_sourcing',
                'icon': 'bi-people',
                'short_description': 'Local labor recruitment, hiring services, and human resource linkage activities for businesses across Ethiopia.',
                'full_description': 'TTC provides comprehensive labor recruitment and hiring services to various companies, primarily based in Adama. We connect organizations with qualified talent through our extensive professional networks and rigorous selection processes.',
            },
            {
                'title': 'Investment Consultancy',
                'slug': 'investment-consultancy',
                'category': 'investment',
                'icon': 'bi-cash-stack',
                'short_description': 'Economic development, business, and investment consultancy to guide informed financial decisions.',
                'full_description': 'Our investment consultancy services cover economic development analysis, business feasibility studies, and investment advisory. We help clients navigate complex economic landscapes and make data-driven investment decisions that foster growth and sustainability.',
            },
            {
                'title': 'Organizational Development',
                'slug': 'organizational-development',
                'category': 'organizational_development',
                'icon': 'bi-building',
                'short_description': 'Personality development, management training, and organizational capacity building programs.',
                'full_description': 'We offer personality development training, management and business training programs designed to build organizational capacity. Our approach combines theoretical frameworks with practical applications to create lasting organizational change and employee development.',
            },
        ]

        for i, data in enumerate(services_data):
            Service.objects.update_or_create(slug=data['slug'], defaults={**data, 'is_featured': True, 'order': i})

        founders = [
            {
                'name': 'Dr. Nuru Mohammed (Ph.D.)',
                'role': 'founder',
                'title': 'Founder & Manager',
                'is_founder': True,
                'order': 1,
                'years_experience': 15,
                'bio': 'Dr. Nuru Mohammed holds a doctorate from the University of International Business and Economics in China, specializing in Business Management. He has served as an Assistant Professor of Management (Strategic Management) at Aresi University\'s College of Business and Economics. His industry experience includes roles as a Business Development Manager at Edao International Trading (EIT) and Teysser Technology Group PLC (TTG). He holds professional licenses issued by the Ethiopian Management Institute.',
                'credentials': 'Ph.D. in Business Management, University of International Business and Economics, China. Assistant Professor of Strategic Management. TOT certifications in Management, Employability Skills, Personality Development, Business, and Consultancy. Licensed by Ethiopian Management Institute.',
            },
            {
                'name': 'Mr. Nejat Kemal',
                'role': 'deputy_manager',
                'title': 'Founder & Deputy Manager',
                'is_founder': True,
                'order': 2,
                'years_experience': 12,
                'bio': 'Mr. Nejat Kemal is a multidisciplinary professional with an educational background in Marketing Management, Business Administration, and Leadership. He has over a decade of teaching experience at various private higher education institutions in Adama City, including Rift Valley University, Royal College, and Unity University. He also owns a successful business in Adama City and has extensive experience as a freelance trainer and consultant.',
                'credentials': 'Marketing Management, Business Administration, and Leadership qualifications. 10+ years teaching experience. Extensive freelance training and consultancy experience.',
            },
        ]

        for data in founders:
            TeamMember.objects.update_or_create(name=data['name'], defaults=data)

        milestones = [
            {'year': '2024', 'title': 'Company Established', 'description': 'Team Training and Consultancy Service PLC was established on April 18, 2024.', 'order': 1},
            {'year': '2024', 'title': 'Operations Begin', 'description': 'Official operations commenced on May 7, 2024.', 'order': 2},
            {'year': '2024', 'title': 'GIZ SIC-II Partnership', 'description': 'Successful collaboration with GIZ Sustainable Industrial Cluster Project delivering leadership training to Adama Development PLC, Buluko Textile, and Special Economic Zone management teams.', 'order': 3},
        ]
        for data in milestones:
            Milestone.objects.update_or_create(year=data['year'], title=data['title'], defaults=data)

        partners = [
            {'name': 'GIZ Sustainable Industrial Cluster', 'order': 1},
            {'name': 'Adama Development PLC', 'order': 2},
            {'name': 'Buluko Textile Share Company', 'order': 3},
            {'name': 'Bulbula Special Economic Zone', 'order': 4},
            {'name': 'Hawassa Special Economic Zone', 'order': 5},
            {'name': 'Ethiopian Management Institute', 'order': 6},
        ]
        for data in partners:
            Partner.objects.update_or_create(name=data['name'], defaults=data)

        case, _ = CaseStudy.objects.update_or_create(
            slug='giz-sic-ii-leadership-training',
            defaults={
                'title': 'GIZ SIC-II Leadership & Strategic Management Training',
                'client_name': 'GIZ Sustainable Industrial Cluster Project',
                'industry': 'International Development',
                'challenge': 'Management teams of industrial cluster enterprises needed enhanced leadership and strategic management capabilities to address complex organizational challenges.',
                'solution': 'TTC designed and delivered high-level leadership and strategic management training and consultancy services tailored to each participating institution.',
                'results': 'Enhanced leadership and strategic capabilities across Adama Development PLC, Buluko Textile Share Company, Bulbula SEZ Management, and Hawassa SEZ Management. Established TTC as a trusted partner in organizational capacity development.',
                'excerpt': 'Successful delivery of leadership training under GIZ SIC-II project across multiple industrial enterprises.',
                'is_featured': True,
                'project_start': datetime(2024, 6, 1).date(),
                'project_end': datetime(2024, 12, 31).date(),
            }
        )
        CaseStudyTimeline.objects.get_or_create(
            case_study=case, title='Project Initiation',
            defaults={'description': 'Partnership established with GIZ SIC-II project.', 'date': datetime(2024, 6, 1).date(), 'order': 1}
        )
        CaseStudyTimeline.objects.get_or_create(
            case_study=case, title='Training Delivery',
            defaults={'description': 'Leadership programs delivered to all participating institutions.', 'date': datetime(2024, 9, 1).date(), 'order': 2}
        )

        Testimonial.objects.update_or_create(
            client_name='GIZ SIC-II Project Team',
            organization='Deutsche Gesellschaft für Internationale Zusammenarbeit',
            defaults={
                'position': 'Project Coordinator',
                'content': 'TTC demonstrated strong capacity to design and implement impactful training programs tailored to address complex organizational challenges. Their work significantly enhanced the leadership capabilities of participating institutions.',
                'rating': 5,
                'is_featured': True,
                'order': 1,
            }
        )

        now = timezone.now()
        TrainingEvent.objects.update_or_create(
            slug='strategic-leadership-masterclass',
            defaults={
                'title': 'Strategic Leadership Masterclass',
                'event_type': 'training',
                'short_description': 'A comprehensive leadership program for senior managers and executives.',
                'description': 'This masterclass covers strategic thinking, organizational leadership, change management, and executive decision-making. Designed for senior managers seeking to enhance their leadership effectiveness.',
                'start_date': now + timedelta(days=30),
                'end_date': now + timedelta(days=32),
                'location': 'Adama City',
                'venue': 'TTCS Training Center',
                'max_participants': 30,
                'registration_deadline': now + timedelta(days=25),
                'is_published': True,
                'is_featured': True,
            }
        )
        TrainingEvent.objects.update_or_create(
            slug='management-consultancy-workshop',
            defaults={
                'title': 'Management Consultancy Workshop',
                'event_type': 'workshop',
                'short_description': 'Hands-on workshop on modern management consultancy practices.',
                'description': 'Learn practical consultancy frameworks, client engagement strategies, and solution design methodologies used by top consulting firms.',
                'start_date': now + timedelta(days=60),
                'end_date': now + timedelta(days=61),
                'location': 'Adama City',
                'venue': 'TTCS Training Center',
                'max_participants': 25,
                'registration_deadline': now + timedelta(days=55),
                'is_published': True,
                'is_featured': True,
            }
        )

        schedule_data = [
            (0, time(8, 30), time(17, 30), False),
            (1, time(8, 30), time(17, 30), False),
            (2, time(8, 30), time(17, 30), False),
            (3, time(8, 30), time(17, 30), False),
            (4, time(8, 30), time(17, 30), False),
            (5, time(9, 0), time(13, 0), False),
            (6, None, None, True),
        ]
        for day, open_t, close_t, closed in schedule_data:
            WorkingSchedule.objects.update_or_create(
                day_of_week=day,
                defaults={'open_time': open_t, 'close_time': close_t, 'is_closed': closed}
            )

        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'teamconsultency@gmail.com', 'is_staff': True, 'is_superuser': True}
        )

        cat, _ = BlogCategory.objects.get_or_create(
            slug='training-insights',
            defaults={'name': 'Training Insights', 'description': 'Articles about training and professional development'}
        )
        BlogPost.objects.update_or_create(
            slug='welcome-to-ttcs',
            defaults={
                'title': 'Welcome to Team Training and Consultancy Service PLC',
                'author': admin_user,
                'category': cat,
                'excerpt': 'Introducing our mission to guide your success, every step of the way.',
                'content': 'Team Training and Consultancy Service PLC was established to provide specialized training, consultancy, and human resource sourcing solutions. We empower organizations through practical and innovative strategies that foster growth, productivity, and sustainable success.',
                'meta_tags': 'training, consultancy, Ethiopia, organizational development',
                'published': True,
            }
        )

        self.stdout.write(self.style.SUCCESS('TTCS data seeded successfully!'))
