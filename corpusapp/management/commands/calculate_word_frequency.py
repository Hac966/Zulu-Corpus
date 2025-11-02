# In corpusapp/management/commands/calculate_word_frequency.py

from django.core.management.base import BaseCommand
import logging

from corpusapp.models import Entry
# IMPORT ONLY THE NEW FUNCTION
from corpusapp.corpus_utils import process_and_update_corpus_text  # <--- THIS IS THE ONLY FUNCTION NAME YOU NEED

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Recalculates word frequencies across the entire corpus by reprocessing all entries.'

    def handle(self, *args, **options):
        self.stdout.write("Starting full corpus word frequency calculation...")

        # 1. Reset all counts to 0 before reprocessing
        self.stdout.write("Resetting all existing word frequencies to 0...")
        Entry.objects.update(word=0)

        # 2. Re-process every single entry in the database
        total_reprocessed = 0

        # Get all entries (this uses Entry.objects.all())
        all_entries = Entry.objects.all()

        for entry in all_entries:
            # Process the isizulu field
            process_and_update_corpus_text(entry.isizulu)

            # Also process the word_usage field
            if entry.word_usage:
                process_and_update_corpus_text(entry.word_usage)

            total_reprocessed += 1

        self.stdout.write(self.style.SUCCESS(
            f'Successfully reprocessed and calculated frequencies for {total_reprocessed} entries.'
        ))