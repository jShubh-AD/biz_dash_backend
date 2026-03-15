SCHEMA = """
Table: videos

Columns:
timestamp (timestamp)
video_id (text, primary key)
category (text)
language (text)
region (text) -- examples: US, UK, IN
views (integer)
likes (integer)
comments (integer)
shares (integer)
duration_sec (integer)
sentiment_score (double precision)
ads_enabled (boolean)
"""