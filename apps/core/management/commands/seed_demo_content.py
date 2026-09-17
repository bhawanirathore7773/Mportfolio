"""Seeds a small amount of demo content so the site isn't empty on first
deploy. Every piece of text is clearly generic/demo and uses the neutral
example from the build brief ("Botanical Harmony") rather than anything
that could be mistaken for a real client project. Safe to run once;
running again just updates the same rows instead of duplicating them.

Usage: python manage.py seed_demo_content
"""
from django.core.management.base import BaseCommand

from apps.core.models import HomepageSettings, ProcessStep, SiteSettings
from apps.portfolio.models import Category, Project
from apps.profiles.models import Service, Skill


class Command(BaseCommand):
    help = "Seed minimal, clearly-marked demo content for local preview."

    def handle(self, *args, **options):
        site = SiteSettings.load()
        if not site.site_name or site.site_name == "Manish Kanwar":
            site.site_name = "Manish Kanwar"
            site.tagline = "Textile Designer & CAD Designer"
            site.location = "Jaipur, Rajasthan, India"
            site.contact_phone = "+91 96644 83527"
            site.default_seo_title = "Manish Kanwar | Textile & CAD Designer"
            site.default_seo_description = (
                "Portfolio of Manish Kanwar, a Textile Designer & CAD Designer creating "
                "contemporary textile prints, surface patterns and CAD artwork."
            )
            site.open_to_freelance = True
            site.save()

        HomepageSettings.load()

        category, _ = Category.objects.get_or_create(
            slug="surface-pattern-design",
            defaults={
                "name": "Surface Pattern Design",
                "description": (
                    "Explore a curated selection of surface pattern designs featuring repeat "
                    "structures, decorative motifs and contemporary compositions developed for "
                    "textile applications."
                ),
                "display_order": 1,
            },
        )

        Project.objects.get_or_create(
            category=category,
            slug="botanical-harmony",
            defaults={
                "title": "Botanical Harmony [DEMO — replace or delete]",
                "short_description": (
                    "A contemporary botanical surface pattern exploring organic floral motifs, "
                    "balanced composition and a refined repeat structure."
                ),
                "description": (
                    "Botanical Harmony explores the relationship between organic floral motifs and "
                    "structured repeat composition. The design uses layered botanical elements to "
                    "create a balanced surface suitable for contemporary textile applications."
                ),
                "design_type": "Floral / Botanical",
                "technique": "Digital Design",
                "application": "Fashion Textile",
                "year": 2026,
                "is_published": True,
                "is_featured": True,
            },
        )

        steps = [
            (1, "Brief", "Understanding the collection, design direction, application and requirements."),
            (2, "Research", "Exploring references, trends, motifs, colour directions and visual inspiration."),
            (3, "Concept Development", "Developing initial ideas, motifs and compositions."),
            (4, "Design Development", "Refining the selected direction into detailed textile artwork."),
            (5, "Review & Refinement", "Applying feedback and developing final variations."),
            (6, "Final Artwork", "Preparing the final approved design files according to project requirements."),
        ]
        for number, title, description in steps:
            ProcessStep.objects.get_or_create(
                step_number=number, defaults={"title": title, "description": description, "display_order": number}
            )

        services = [
            ("Textile Print Design", "Custom textile print concepts developed around your collection direction, visual references and target application."),
            ("Surface Pattern Design", "Seamless repeats, motifs and surface compositions created for continuous textile applications."),
            ("CAD Textile Design", "Detailed CAD artwork developed for textile and fashion design requirements."),
        ]
        for title, description in services:
            Service.objects.get_or_create(title=title, defaults={"short_description": description})

        skills = [
            ("Textile Print Design", "design"), ("Surface Pattern Design", "design"),
            ("CAD Design", "software"), ("Motif Development", "technique"),
        ]
        for name, category_choice in skills:
            Skill.objects.get_or_create(name=name, defaults={"category": category_choice})

        self.stdout.write(self.style.SUCCESS(
            "Demo content seeded. The demo project is clearly labelled — replace or delete it "
            "from /admin/ once you add real work."
        ))
