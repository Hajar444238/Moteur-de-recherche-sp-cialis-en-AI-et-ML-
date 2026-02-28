from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from database_config import DatabaseConfig
import os

app = Flask(__name__)
CORS(app)  # Permet les requêtes depuis le frontend

# Route pour servir le fichier HTML
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Route pour obtenir les statistiques
@app.route('/api/statistiques', methods=['GET'])
def get_statistiques():
    try:
        db = DatabaseConfig()
        db.connect()
        stats = db.get_stats()
        db.close()
        
        return jsonify({
            'success': True,
            'stats_base': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Route pour la recherche
@app.route('/api/rechercher', methods=['POST'])
def rechercher():
    try:
        data = request.get_json()
        query = data.get('q', '')
        type_filter = data.get('type', 'all')
        limit = data.get('limit', 20)
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Requête vide'
            }), 400
        
        db = DatabaseConfig()
        db.connect()
        
        resultats = []
        
        # Recherche dans les documents
        if type_filter in ['all', 'document']:
            db.cursor.execute('''
                SELECT DISTINCT d.id, d.titre, d.contenu, d.type_doc, d.chemin_fichier
                FROM documents d
                LEFT JOIN index_mots_cles i ON d.id = i.doc_id
                WHERE d.titre LIKE ? OR d.contenu LIKE ? OR i.mot_cle LIKE ?
                LIMIT ?
            ''', (f'%{query}%', f'%{query}%', f'%{query}%', limit))
            
            for row in db.cursor.fetchall():
                resultats.append({
                    'id': row[0],
                    'titre': row[1],
                    'contenu': row[2],
                    'type_doc': row[3] or 'document',
                    'chemin_fichier': row[4]
                })
        
        # Recherche dans les images
        if type_filter in ['all', 'image']:
            db.cursor.execute('''
                SELECT DISTINCT i.id, i.titre, i.description, i.type_image, i.chemin_fichier
                FROM images i
                LEFT JOIN index_mots_cles idx ON i.id = idx.img_id
                WHERE i.titre LIKE ? OR i.description LIKE ? OR i.alt_text LIKE ? OR idx.mot_cle LIKE ?
                LIMIT ?
            ''', (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%', limit))
            
            for row in db.cursor.fetchall():
                resultats.append({
                    'id': row[0],
                    'titre': row[1],
                    'contenu': row[2],
                    'type_doc': 'image',
                    'chemin_fichier': row[4]
                })
        
        # Recherche dans les vidéos
        if type_filter in ['all', 'video']:
            db.cursor.execute('''
                SELECT DISTINCT v.id, v.titre, v.description, v.type_video, v.chemin_fichier
                FROM videos v
                LEFT JOIN index_mots_cles idx ON v.id = idx.video_id
                WHERE v.titre LIKE ? OR v.description LIKE ? OR idx.mot_cle LIKE ?
                LIMIT ?
            ''', (f'%{query}%', f'%{query}%', f'%{query}%', limit))
            
            for row in db.cursor.fetchall():
                resultats.append({
                    'id': row[0],
                    'titre': row[1],
                    'contenu': row[2],
                    'type_doc': 'video',
                    'chemin_fichier': row[4]
                })
        
        # Enregistrer la statistique de recherche
        db.cursor.execute('''
            INSERT INTO statistiques_recherche (requete, nb_resultats)
            VALUES (?, ?)
        ''', (query, len(resultats)))
        db.conn.commit()
        
        db.close()
        
        return jsonify({
            'success': True,
            'resultats': resultats,
            'nb_resultats': len(resultats),
            'requete': query
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Démarrage du serveur API...")
    print("📍 Accédez à l'interface : http://localhost:5000")
    print("📊 API Statistiques : http://localhost:5000/api/statistiques")
    print("🔍 API Recherche : http://localhost:5000/api/rechercher")
    print("\n✨ Le serveur est prêt !\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)