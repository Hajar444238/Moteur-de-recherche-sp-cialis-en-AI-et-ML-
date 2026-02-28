from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from database_config import DatabaseConfig
from search_engine import SearchEngine
from indexer import DocumentIndexer

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'votre_cle_secrete_ici'
app.config['JSON_AS_ASCII'] = False  # Support UTF-8 dans JSON

# Fonction helper pour obtenir une nouvelle connexion DB
def get_db():
    """Créer une nouvelle connexion à la base de données"""
    db = DatabaseConfig()
    db.connect()
    return db

@app.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html')

@app.route('/video/<path:filepath>')
def video_player(filepath):
    """Page lecteur vidéo"""
    try:
        print(f"🎬 Demande de lecture vidéo: {filepath}")
        
        # Décoder correctement le chemin
        from urllib.parse import unquote
        filepath = unquote(filepath)
        filepath = filepath.replace('/', '\\')
        
        print(f"🎬 Chemin décodé: {filepath}")
        
        if not os.path.exists(filepath):
            print(f"❌ Vidéo introuvable: {filepath}")
            return f"Vidéo introuvable: {filepath}", 404
        
        filename = os.path.basename(filepath)
        
        # Détecter le type MIME
        import mimetypes
        mimetype, _ = mimetypes.guess_type(filename)
        
        if not mimetype:
            ext = filename.lower().split('.')[-1]
            mime_map = {
                'mp4': 'video/mp4',
                'webm': 'video/webm',
                'ogg': 'video/ogg',
                'avi': 'video/x-msvideo',
                'mov': 'video/quicktime',
                'mkv': 'video/x-matroska'
            }
            mimetype = mime_map.get(ext, 'video/mp4')
        
        # Construire l'URL correcte pour le fichier vidéo
        encoded_path = filepath.replace('\\', '/')
        video_url = f"/file/{encoded_path}"
        
        print(f"✅ URL vidéo générée: {video_url}")
        print(f"✅ Type MIME: {mimetype}")
        print(f"✅ Extension: {filename.split('.')[-1]}")
        
        # Ajouter des infos sur la compatibilité
        ext = filename.lower().split('.')[-1]
        compatible_formats = ['mp4', 'webm', 'ogg']
        description = ""
        
        if ext not in compatible_formats:
            description = f"⚠️ Format {ext.upper()} peut ne pas être supporté par tous les navigateurs. MP4/WebM recommandés."
        
        return render_template('video_player.html', 
                             titre=filename,
                             video_url=video_url,
                             mime_type=mimetype,
                             description=description)
    except Exception as e:
        print(f"❌ Erreur lecteur vidéo: {e}")
        import traceback
        traceback.print_exc()
        return f"Erreur: {e}", 500

@app.route('/open-external/<path:filepath>')
def open_external(filepath):
    """Ouvrir le fichier avec l'application système"""
    try:
        from urllib.parse import unquote
        import subprocess
        
        filepath = unquote(filepath)
        filepath = filepath.replace('/', '\\')
        
        print(f"🚀 Ouverture externe: {filepath}")
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'Fichier introuvable'}), 404
        
        # Ouvrir avec l'application par défaut (Windows)
        subprocess.Popen(['start', '', filepath], shell=True)
        
        return jsonify({'success': True, 'message': 'Fichier ouvert avec l\'application système'})
    except Exception as e:
        print(f"❌ Erreur ouverture externe: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/file/<path:filepath>')
def serve_file(filepath):
    """Servir un fichier local"""
    try:
        print(f"📂 Tentative d'ouverture du fichier: {filepath}")
        
        # Décoder le chemin proprement
        from urllib.parse import unquote
        filepath = unquote(filepath)
        
        # Le chemin arrive encodé, le décoder
        filepath = filepath.replace('/', '\\')
        
        print(f"📂 Chemin final: {filepath}")
        
        # Vérifier que le fichier existe
        if not os.path.exists(filepath):
            print(f"❌ Fichier introuvable: {filepath}")
            return jsonify({'error': 'Fichier introuvable', 'path': filepath}), 404
        
        # Obtenir le dossier et le nom du fichier
        directory = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        
        # Détecter le type MIME basé sur l'extension
        import mimetypes
        mimetype, _ = mimetypes.guess_type(filename)
        
        # Forcer les types MIME pour les vidéos si non détectés
        if not mimetype:
            ext = filename.lower().split('.')[-1]
            mime_map = {
                'mp4': 'video/mp4',
                'webm': 'video/webm',
                'ogg': 'video/ogg',
                'avi': 'video/x-msvideo',
                'mov': 'video/quicktime',
                'mkv': 'video/x-matroska',
                'pdf': 'application/pdf',
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'png': 'image/png',
                'gif': 'image/gif'
            }
            mimetype = mime_map.get(ext, 'application/octet-stream')
        
        print(f"✅ Envoi du fichier: {filename} (type: {mimetype}) depuis {directory}")
        
        # Servir le fichier avec le bon type MIME
        return send_from_directory(directory, filename, mimetype=mimetype)
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi du fichier: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistiques')
def api_statistiques():
    """API des statistiques"""
    db = None
    try:
        # Créer une nouvelle connexion pour cette requête
        db = get_db()
        
        stats_db = {
            'nb_documents': 0,
            'nb_images': 0,
            'nb_videos': 0,
            'nb_mots_cles_uniques': 0
        }
        
        # Compter les documents
        db.cursor.execute("SELECT COUNT(*) FROM documents")
        result = db.cursor.fetchone()
        stats_db['nb_documents'] = result[0] if result else 0
        
        # Compter les images
        db.cursor.execute("SELECT COUNT(*) FROM images")
        result = db.cursor.fetchone()
        stats_db['nb_images'] = result[0] if result else 0
        
        # Compter les vidéos
        db.cursor.execute("SELECT COUNT(*) FROM videos")
        result = db.cursor.fetchone()
        stats_db['nb_videos'] = result[0] if result else 0
        
        # Compter les mots-clés uniques
        db.cursor.execute("SELECT COUNT(DISTINCT mot_cle) FROM index_mots_cles")
        result = db.cursor.fetchone()
        stats_db['nb_mots_cles_uniques'] = result[0] if result else 0
        
        print(f"✅ Stats récupérées: {stats_db}")
        
        # Stats de recherche
        try:
            search_engine = SearchEngine(db)
            stats_recherches = search_engine.obtenir_statistiques(limit=10)
            recherches_populaires = [
                {
                    'requete': s[0],
                    'nb_recherches': s[1],
                    'moy_resultats': round(s[2], 1),
                    'moy_temps_ms': round(s[3], 2)
                }
                for s in stats_recherches
            ]
        except Exception as e:
            print(f"⚠️  Erreur stats recherches: {e}")
            recherches_populaires = []
        
        return jsonify({
            'recherches_populaires': recherches_populaires,
            'stats_base': stats_db
        })
        
    except Exception as e:
        print(f"❌ Erreur API statistiques: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'stats_base': {
                'nb_documents': 0,
                'nb_images': 0,
                'nb_videos': 0,
                'nb_mots_cles_uniques': 0
            },
            'recherches_populaires': []
        })
    finally:
        if db:
            db.close()

@app.route('/api/rechercher', methods=['GET', 'POST'])
def api_rechercher():
    """API de recherche"""
    db = None
    try:
        # Créer une nouvelle connexion pour cette requête
        db = get_db()
        search_engine = SearchEngine(db)
        
        if request.method == 'POST':
            data = request.get_json()
            requete = data.get('q', '')
            type_contenu = data.get('type', 'all')
            limit = data.get('limit', 20)
        else:
            requete = request.args.get('q', '')
            type_contenu = request.args.get('type', 'all')
            limit = int(request.args.get('limit', 20))
        
        if not requete:
            return jsonify({'error': 'Requête vide'}), 400
        
        print(f"🔍 Recherche: '{requete}' (type: {type_contenu}, limit: {limit})")
        
        # Effectuer la recherche
        resultats = search_engine.rechercher(requete, type_contenu, limit)
        
        print(f"✅ {resultats.get('nb_total', 0)} résultats trouvés en {resultats.get('temps_ms', 0)}ms")
        
        return jsonify(resultats)
        
    except Exception as e:
        print(f"❌ Erreur recherche: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'resultats': [],
            'temps_ms': 0,
            'nb_total': 0
        }), 500
    finally:
        if db:
            db.close()

@app.route('/api/suggestions')
def api_suggestions():
    """API d'autocomplétion"""
    db = None
    try:
        db = get_db()
        search_engine = SearchEngine(db)
        
        debut = request.args.get('q', '')
        
        if len(debut) < 2:
            return jsonify({'suggestions': []})
        
        suggestions = search_engine.suggestions_recherche(debut, limit=5)
        
        return jsonify({'suggestions': suggestions})
        
    except Exception as e:
        print(f"❌ Erreur suggestions: {e}")
        return jsonify({'suggestions': []})
    finally:
        if db:
            db.close()

@app.route('/api/indexer', methods=['POST'])
def api_indexer():
    """API pour indexer un nouveau fichier ou dossier"""
    db = None
    try:
        db = get_db()
        indexer = DocumentIndexer(db)
        
        data = request.get_json()
        chemin = data.get('chemin', '')
        
        if not chemin or not os.path.exists(chemin):
            return jsonify({'error': 'Chemin invalide'}), 400
        
        if os.path.isdir(chemin):
            # Indexer un dossier complet
            compteurs = indexer.indexer_dossier(chemin)
            return jsonify({
                'success': True,
                'message': 'Dossier indexé avec succès',
                'compteurs': compteurs
            })
        else:
            # Indexer un fichier unique
            success = indexer.indexer_document(chemin)
            return jsonify({
                'success': success,
                'message': 'Fichier indexé' if success else 'Erreur d\'indexation'
            })
            
    except Exception as e:
        print(f"❌ Erreur indexation: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if db:
            db.close()

@app.errorhandler(404)
def page_non_trouvee(e):
    return jsonify({'error': 'Page non trouvée'}), 404

@app.errorhandler(500)
def erreur_serveur(e):
    return jsonify({'error': 'Erreur serveur'}), 500

if __name__ == '__main__':
    print("\n🚀 Démarrage du moteur de recherche AI & Machine Learning")
    print("📊 Statistiques de la base:")
    
    # Connexion temporaire pour afficher les stats au démarrage
    db_init = get_db()
    try:
        stats = db_init.get_stats()
        for key, value in stats.items():
            print(f"   - {key}: {value}")
    except Exception as e:
        print(f"   ⚠️ Erreur lecture stats: {e}")
    finally:
        db_init.close()
    
    print("\n🌐 Serveur web démarré sur http://localhost:5000")
    print("   - Page d'accueil: http://localhost:5000")
    print("   - API Stats: http://localhost:5000/api/statistiques")
    print("\n⏹️  Appuyez sur Ctrl+C pour arrêter\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)