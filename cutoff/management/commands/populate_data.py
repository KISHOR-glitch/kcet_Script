from django.core.management.base import BaseCommand
from cutoff.models import Category, Round, Year


class Command(BaseCommand):
    help = 'Populate initial data for KCET cutoff system'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data initialization...'))

        # Create categories
        categories = [
            ('1G', 'General Merit - 1st'),
            ('1K', 'Kannada Medium - 1st'),
            ('1R', 'Reserved - 1st'),
            ('2AG', 'OBC - 2nd'),
            ('2AK', 'OBC Kannada - 2nd'),
            ('2AR', 'OBC Reserved - 2nd'),
            ('3BG', 'SC - 3rd'),
            ('3BK', 'SC Kannada - 3rd'),
            ('3BR', 'SC Reserved - 3rd'),
            ('4G', 'ST - 4th'),
            ('4K', 'ST Kannada - 4th'),
            ('4R', 'ST Reserved - 4th'),
            ('STG', 'Special Category General'),
            ('STK', 'Special Category Kannada'),
            ('STR', 'Special Category Reserved'),
            ('GM', 'General Merit'),
        ]

        for code, desc in categories:
            Category.objects.get_or_create(code=code, defaults={'description': desc})
            self.stdout.write(f'✓ Category: {code}')

        # Create rounds
        rounds = [
            ('Round 1', 1),
            ('Round 2', 2),
            ('Round 3', 3),
            ('Spot Admission', 4),
        ]

        for name, num in rounds:
            Round.objects.get_or_create(name=name, defaults={'round_number': num})
            self.stdout.write(f'✓ Round: {name}')

        # Create years (last 10 years)
        from datetime import datetime
        current_year = datetime.now().year
        for year in range(current_year, current_year - 10, -1):
            Year.objects.get_or_create(year=year)
            self.stdout.write(f'✓ Year: {year}')

        self.stdout.write(self.style.SUCCESS('\n✓ Data initialization completed successfully!'))
        self.stdout.write(self.style.WARNING('\nNext steps:'))
        self.stdout.write('1. Create a superuser: python manage.py createsuperuser')
        self.stdout.write('2. Run development server: python manage.py runserver')
        self.stdout.write('3. Visit http://127.0.0.1:8000/login/')
