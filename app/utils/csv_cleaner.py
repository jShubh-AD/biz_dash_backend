import re

def clean_columns(columns):
    cleaned = []
    for col in columns:
        col = col.strip().lower()
        col = re.sub(r'\s+', '_', col)        # spaces → _
        col = re.sub(r'[^a-z0-9_]', '', col)  # remove special chars
        cleaned.append(col)
    return cleaned

def detect_date_format(series):
    sample = series.dropna().astype(str).head(200)

    dmy = sample.str.match(r'^\d{2}/\d{2}/\d{4}').mean()
    iso = sample.str.match(r'^\d{4}-\d{2}-\d{2}').mean()

    if dmy > 0.8:
        return "DD/MM/YYYY HH24:MI"
    elif iso > 0.8:
        return "ISO"
    return None