from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Create a database connection
conn = sqlite3.connect('artwork.db')
c = conn.cursor()

# Create the artworks table
c.execute('''CREATE TABLE IF NOT EXISTS artworks
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              description TEXT,
              artist_name TEXT NOT NULL,
              art_style TEXT NOT NULL,
              source_artworks TEXT NOT NULL,
              royalties REAL DEFAULT 0)''')
conn.commit()


@app.route('/generate-artwork', methods=['POST'])
def generate_artwork():
    # Get the request data
    title = request.json['title']
    description = request.json['description']
    artist_name = request.json['artist_name']
    art_style = request.json['art_style']
    source_artworks = request.json['source_artworks']

    # Insert the artwork metadata into the database
    c.execute("INSERT INTO artworks (title, description, artist_name, art_style, source_artworks) VALUES (?, ?, ?, ?, ?)",
              (title, description, artist_name, art_style, source_artworks))
    conn.commit()

    # Calculate the contribution percentage for each source artwork
    total_pixels = sum([s['pixels'] for s in source_artworks])
    for s in source_artworks:
        percentage = s['pixels'] / total_pixels
        artist_name = s['artist_name']
        # Update the royalties for the source artwork artist
        c.execute("UPDATE artworks SET royalties = royalties + ? WHERE artist_name = ?", (percentage, artist_name))
        conn.commit()

    return jsonify({'success': True})


@app.route('/get-artwork/<int:artwork_id>', methods=['GET'])
def get_artwork(artwork_id):
    # Get the artwork metadata from the database
    c.execute("SELECT * FROM artworks WHERE id = ?", (artwork_id,))
    artwork = c.fetchone()

    if artwork is None:
        return jsonify({'error': 'Artwork not found'})

    return jsonify({
        'id': artwork[0],
        'title': artwork[1],
        'description': artwork[2],
        'artist_name': artwork[3],
        'art_style': artwork[4],
        'source_artworks': artwork[5],
        'royalties': artwork[6]
    })


if __name__ == '__main__':
    app.run(debug=True)
