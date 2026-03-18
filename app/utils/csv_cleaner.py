import re

def clean_columns(columns):
    cleaned = []
    for col in columns:
        col = col.strip().lower()
        col = re.sub(r'\s+', '_', col)        # spaces → _
        col = re.sub(r'[^a-z0-9_]', '', col)  # remove special chars
        cleaned.append(col)
    return cleaned