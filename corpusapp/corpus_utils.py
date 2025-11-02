import re
from collections import Counter
from django.db import transaction
from django.db.models import F


def process_and_update_corpus_text(text_source):
    """
    Splits the input text into words, checks if each word exists as an Entry,
    creates it if missing, and increments its frequency count.
    """
    # Import model locally to break circular dependency
    from .models import Entry

    if not text_source:
        return 0

    # 1. Tokenize the text
    tokens = re.findall(r'\b\w+\b', text_source.lower())
    word_counts = Counter(tokens)

    if not word_counts:
        return 0

    # Use a transaction block to ensure atomic updates (all succeed or all fail)
    with transaction.atomic():
        total_updates = 0

        for word_token, count in word_counts.items():
            # Standardize the word for display (e.g., capitalize)
            display_word = word_token.capitalize()

            # 2. Check if the word Entry already exists (case-insensitive lookup)
            # We use get_or_create to handle both cases efficiently
            entry, created = Entry.objects.get_or_create(
                isizulu__iexact=word_token,  # Search filter
                defaults={'isizulu': display_word,
                          'english': f"Definition for {display_word}",
                          'word': 0  # Initial frequency will be updated next
                          }
            )

            # 3. Append to the frequency
            # We use F() expression to atomically add the count to the frequency field ('word')
            Entry.objects.filter(pk=entry.pk).update(
                word=F('word') + count
            )
            total_updates += 1

    return total_updates