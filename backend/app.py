from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import json
import difflib
import heapq

from data_source.get_movie_data import get_movie_data


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# @app.route('/search', methods=['GET'])
# def search_movies():
#     query = request.args.get('query')
#     # Assuming Movie is your SQLAlchemy model and it has a 'name' field
#     # movies = Movie.query.filter(Movie.name.ilike(f'%{query}%')).all()
#     # results = [{'id': movie.id, 'name': movie.name} for movie in movies]
#     # Dummy data for demonstration
#     results = [{'id': 1, 'name': 'Sample Movie'}]
#     return jsonify(results)

# Database credentials
DB_HOST = "localhost"
DB_USER = "postgres"
DB_PASS = "snsnsn252"
DB_NAME = "postgres"

# database connection
def get_db_connection():

    conn = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, dbname=DB_NAME)
    return conn

# insert movies into the database
def test_db_connection():
    conn = get_db_connection()
    cursor = conn.cursor()
    print("test")

    try:
        cursor.execute("SELECT NOW();")
        result = cursor.fetchone()
        print("Current time from the database: ", result)

    except Exception as e:
        print("An error occurred:", e)

    finally:
        cursor.close()
        conn.close()


def create_table(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            adult BOOLEAN,
            backdrop_path VARCHAR(255),
            genre_ids INTEGER[],  -- Array of integers
            original_language VARCHAR(50),
            original_title VARCHAR(255),
            overview TEXT,
            popularity NUMERIC,
            poster_path VARCHAR(255),
            release_date DATE,
            title VARCHAR(255),
            video BOOLEAN,
            vote_average NUMERIC,
            vote_count INTEGER
        );
    """)

    print(f"Table {table_name} created.")

    conn.commit()
    cursor.close()
    conn.close()

def insert_data(json_data):
    conn = get_db_connection()
    cursor = conn.cursor()

    # placeholders and values directly from json_data
    columns = ', '.join(json_data.keys())
    placeholders = ', '.join(['%s'] * len(json_data))
    values = tuple(json_data.values())

    query = f"""
        INSERT INTO movie ({columns}) 
        VALUES ({placeholders})
        ON CONFLICT (id) DO NOTHING;
    """
    cursor.execute(query, values)

    conn.commit()
    cursor.close()
    conn.close()

@app.route('/movies', methods=['GET'])
def movies_title():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT title FROM movie")

    movie_titles = [record[0] for record in cursor.fetchall()]

    cursor.close()
    conn.close()

    print("######")
    #print(movie_titles)
    return jsonify(movie_titles)




@app.route('/discovers', methods=['GET'])
def discover_movies():

    genre_ids = request.args.get('genre_ids')
    print("debug parts;\n")
    print(genre_ids)
    if genre_ids:
        genre_ids = tuple(int(id) for id in genre_ids.split(','))  # Convert to tuple
    print("\n")
    print(genre_ids)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM movie       
        WHERE %s = ANY(genre_ids)
        ORDER BY popularity DESC Limit 12
    """, (genre_ids,))

    rows = cursor.fetchall()

    col_names = [desc[0] for desc in cursor.description]

    movies = [dict(zip(col_names, row)) for row in rows]
    cursor.close()
    conn.close()

    print("dfafasfasf\n")
    print(type(movies))
    return jsonify(movies)


# not useful
@app.route('/search', methods=['GET'])
def search_movies():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'No search query provided'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM movie
        WHERE title ILIKE %s OR overview ILIKE %s
    """, ('%' + query + '%', '%' + query + '%'))

    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    movies = [dict(zip(col_names, row)) for row in rows]

    cursor.close()
    conn.close()

    return jsonify(movies)


def create_similarity_table(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            movie1_id INTEGER REFERENCES movie(id),  -- Foreign key reference to the first movie's ID
            movie1_title VARCHAR(255),  -- Title of the first movie
            movie2_id INTEGER REFERENCES movie(id),  -- Foreign key reference to the second movie's ID
            movie2_title VARCHAR(255),  -- Title of the second movie
            similarity_score NUMERIC
        );
    """)

    print(f"Table {table_name} created.")

    conn.commit()
    cursor.close()
    conn.close()



# similar

def calculate_similarity(title1, title2):
    similarity = difflib.SequenceMatcher(None, title1, title2).ratio()
    return similarity



def generate_similarity():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title FROM movie LIMIT 500")
    movies = cursor.fetchall()

    for i in range(len(movies)):
        for j in range(i + 1, len(movies)):
            movie1_id, movie1_title = movies[i]
            movie2_id, movie2_title = movies[j]

            similarity_score = calculate_similarity(movie1_title, movie2_title)

            cursor.execute("""
                INSERT INTO similarity (movie1_id, movie1_title, movie2_id, movie2_title, similarity_score) 
                VALUES (%s, %s, %s, %s, %s)
            """, (movie1_id, movie1_title, movie2_id, movie2_title, similarity_score))

    conn.commit()
    cursor.close()
    conn.close()

    return "Similarity scores generated successfully"



def construct_graph():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT movie1_id, movie2_id, similarity_score FROM similarity")
    similarities = cursor.fetchall()

    graph = {}
    for movie1_id, movie2_id, similarity_score in similarities:
        heapq.heappush(graph.setdefault(movie1_id, []), (-similarity_score, movie2_id))
        heapq.heappush(graph.setdefault(movie2_id, []), (-similarity_score, movie1_id))

    cursor.close()
    conn.close()

    return graph


def get_similar_movies(graph, movie_id):
    if movie_id not in graph:
        return []

    similar_movies = []
    for _ in range(16):
        if graph[movie_id]:
            score, similar_movie_id = heapq.heappop(graph[movie_id])
            similar_movies.append((similar_movie_id, -score))
    
    return similar_movies

movie_graph = construct_graph()

@app.route('/similar', methods=['GET'])
def api_get_similar_movies():
    movie_title = request.args.get('movie_title')
    if not movie_title:
        return jsonify({'error': 'Movie title is required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM movie WHERE title = %s", (movie_title,))
    movie_record = cursor.fetchone()

    if not movie_record:
        cursor.close()
        conn.close()
        return jsonify({'error': 'Movie not found'}), 404

    movie_id = movie_record[0]
    
    similar_movies = get_similar_movies(movie_graph, movie_id)

    detailed_movies = []
    for similar_movie_id, score in similar_movies:
        cursor.execute("SELECT * FROM movie WHERE id = %s", (similar_movie_id,))
        movie_details = cursor.fetchone()
        if movie_details:
            movie_info = dict(zip([column[0] for column in cursor.description], movie_details))
            movie_info['similarity_score'] = score
            detailed_movies.append(movie_info)

    cursor.close()
    conn.close()

    print(detailed_movies)
    return jsonify({'movies': detailed_movies})







if __name__ == "__main__":

    # test_db_connection()
    # create_table('movie')
    # json_list = get_movie_data()

    # for json_data in json_list:
    #     insert_data(json_data)

    # create_similarity_table('similarity')
    # generate_similarity()

    #graph = construct_graph()
    #m = get_similar_movies(graph, 238)
    #print(m)


    #api_get_similar_movies('The Godfather')
    app.run(host='127.0.0.1', port=5002, debug=True)



