import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ── Load data ────────────────────────────────────────────────────
df = pd.read_csv('movies.csv')
df.columns = df.columns.str.strip().str.lower()

# ── Fill missing values using exact column names ─────────────────
for col in ['movie_genre', 'movie_keywords', 'movie_overview', 
            'movie_cast', 'movie_director', 'movie_tagline']:
    df[col] = df[col].fillna('')

df['movie_title'] = df['movie_title'].fillna('').str.strip()
df = df[df['movie_title'] != ''].reset_index(drop=True)

# ── Build combined feature string ───────────────────────────────
def build_features(row):
    # Repeat genres 3x and keywords 2x for stronger signal
    genre     = str(row['movie_genre']).replace(',', ' ').replace('|', ' ')
    keywords  = str(row['movie_keywords']).replace(',', ' ')
    overview  = str(row['movie_overview'])
    cast      = str(row['movie_cast']).replace(',', ' ')
    director  = str(row['movie_director'])
    tagline   = str(row['movie_tagline'])
    return f"{genre} {genre} {genre} {keywords} {keywords} {overview} {cast} {director} {tagline}".lower()

df['features'] = df.apply(build_features, axis=1)

# ── TF-IDF + cosine similarity ───────────────────────────────────
tfidf = TfidfVectorizer(
    stop_words='english',
    ngram_range=(1, 2),
    max_features=10000,
    min_df=2
)
matrix = tfidf.fit_transform(df['features'])
cosine_sim = cosine_similarity(matrix, matrix)

# ── Index by lowercase title ─────────────────────────────────────
indices = pd.Series(df.index, index=df['movie_title'].str.lower()).drop_duplicates()

print(f"✅ Loaded {len(df)} movies successfully.")

# ── Public functions ─────────────────────────────────────────────
def search_titles(query, max_results=8):
    q = query.strip().lower()
    matches = [t for t in df['movie_title'].tolist() if q in t.lower()]
    return matches[:max_results]

def get_recommendations(movie_title, n=8):
    title_lower = movie_title.strip().lower()

    # Exact match first
    if title_lower not in indices:
        # Try partial match
        matches = search_titles(title_lower, max_results=1)
        if matches:
            title_lower = matches[0].lower()
        else:
            return None, None

    idx = indices[title_lower]
    actual_title = df['movie_title'].iloc[idx]

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:n+1]

    results = []
    for i, score in sim_scores:
        results.append({
            'title':  df['movie_title'].iloc[i],
            'genres': df['movie_genre'].iloc[i],
            'score':  round(float(score) * 100, 1)
        })
    return actual_title, results
