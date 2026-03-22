from flask import Flask, render_template, request, jsonify
from recommender import get_recommendations, search_titles

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    movie = request.form.get('movie', '').strip()
    if not movie:
        return render_template('index.html', error="Please enter a movie title.")

    actual_title, results = get_recommendations(movie)

    if results is None:
        return render_template('index.html',
            error=f'"{movie}" was not found. Check spelling or try a suggestion below.',
            movie=movie,
            suggestions=search_titles(movie, max_results=5))

    return render_template('results.html',
        movie=actual_title,
        recommendations=results,
        query=movie)

@app.route('/autocomplete')
def autocomplete():
    q = request.args.get('q', '')
    return jsonify(search_titles(q))

if __name__ == '__main__':
    app.run(debug=True)
