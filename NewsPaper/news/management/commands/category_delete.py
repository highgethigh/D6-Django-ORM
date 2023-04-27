from django.core.management.base import BaseCommand, CommandError
from ...models import Post, Category

class Command(BaseCommand):
    help = 'Deletes all posts from a given category'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str, help='Name of the category to delete posts from')

    def handle(self, *args, **options):
        category_name = options['category']
        confirmation = input(f'Are you sure you want to delete all posts from {category_name}? (y/n) ')
        if confirmation.lower() == 'y':
            try:
                Post.objects.filter(post_link_category__name_category=category_name).delete()
                self.stdout.write(self.style.SUCCESS(f'Successfully deleted all posts from {category_name}'))
            except Exception as e:
                raise CommandError(f'Error deleting posts: {e}')
        else:
            self.stdout.write(self.style.WARNING('Aborted. No posts were deleted.'))
