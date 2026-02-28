#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Principal - Moteur de Recherche AI & Machine Learning
Ce script orchestre le téléchargement, l'indexation et le lancement du moteur
"""
print("🔥 FICHIER MAIN.PY CHARGÉ 🔥")

import os
import sys
from database_config import DatabaseConfig
from downloader import ContentDownloader
from indexer import DocumentIndexer
from search_engine import SearchEngine

def afficher_menu():
    """Afficher le menu principal"""
    print("\n" + "="*70)
    print("🤖 MOTEUR DE RECHERCHE AI & MACHINE LEARNING")
    print("="*70)
    print("\n📋 Menu Principal:")
    print("  1. 📥 Télécharger le corpus complet")
    print("  2. 📇 Indexer le corpus dans la base de données")
    print("  3. 🔍 Tester des requêtes de recherche")
    print("  4. 🌐 Lancer l'interface web")
    print("  5. 📊 Afficher les statistiques")
    print("  6. 🔄 Réinitialiser la base de données")
    print("  7. ⚙️  Tout faire automatiquement (1+2+4)")
    print("  0. ❌ Quitter")
    print("="*70)

def telecharger_corpus():
    """Télécharger tout le corpus"""
    print("\n🚀 Démarrage du téléchargement...")
    downloader = ContentDownloader()
    resultats = downloader.telecharger_tout()
    return resultats

def indexer_corpus(db):
    """Indexer tout le corpus"""
    print("\n📇 Indexation du corpus...")
    
    indexer = DocumentIndexer(db)
    corpus_dir = "corpus"
    
    if not os.path.exists(corpus_dir):
        print(f"❌ Le dossier corpus n'existe pas: {corpus_dir}")
        print("💡 Veuillez d'abord télécharger le corpus (option 1)")
        return False
    
    # Indexer le dossier complet
    compteurs = indexer.indexer_dossier(corpus_dir)
    
    print("\n✅ Indexation terminée !")
    return compteurs

def tester_recherches(db):
    """Tester des recherches"""
    print("\n🔍 Tests de recherche")
    print("="*70)
    
    engine = SearchEngine(db)
    
    # Requêtes de test
    requetes_fructueuses = [
        "apprentissage automatique",
        "réseaux de neurones",
        "intelligence artificielle",
        "algorithme classification",
        "deep learning"
    ]
    
    requetes_non_fructueuses = [
        "cuisine italienne",
        "football",
        "astronomie",
        "xyzabc123",
        "voiture électrique"
    ]
    
    print("\n✅ REQUÊTES FRUCTUEUSES (qui devraient donner des résultats):")
    print("-" * 70)
    
    for i, requete in enumerate(requetes_fructueuses, 1):
        print(f"\n{i}. Requête: '{requete}'")
        resultats = engine.rechercher(requete, limit=3)
        
        print(f"   ⏱️  Temps: {resultats['temps_ms']:.2f} ms")
        print(f"   📊 Résultats trouvés: {resultats['nb_total']}")
        
        if resultats['resultats']:
            print(f"   🎯 Top résultat: [{resultats['resultats'][0]['type']}] {resultats['resultats'][0]['titre']}")
            print(f"   💯 Score: {resultats['resultats'][0]['score']}")
        
        print("   ✓ SUCCÈS - Résultats trouvés")
    
    print("\n" + "="*70)
    print("\n❌ REQUÊTES NON FRUCTUEUSES (qui ne devraient PAS donner de résultats):")
    print("-" * 70)
    
    for i, requete in enumerate(requetes_non_fructueuses, 1):
        print(f"\n{i}. Requête: '{requete}'")
        resultats = engine.rechercher(requete, limit=3)
        
        print(f"   ⏱️  Temps: {resultats['temps_ms']:.2f} ms")
        print(f"   📊 Résultats trouvés: {resultats['nb_total']}")
        
        if resultats['nb_total'] == 0:
            print("   ✓ SUCCÈS - Aucun résultat (comme attendu)")
        else:
            print("   ⚠️  Des résultats ont été trouvés (inattendu)")
            if resultats['resultats']:
                print(f"   📄 Premier résultat: {resultats['resultats'][0]['titre']}")
    
    print("\n" + "="*70)
    print("\n💡 Tests de recherche terminés")

def afficher_stats(db):
    """Afficher les statistiques"""
    print("\n📊 STATISTIQUES DE LA BASE DE DONNÉES")
    print("="*70)
    
    stats = db.get_stats()
    
    print("\n📚 Contenu indexé:")
    print(f"  - Documents: {stats['nb_documents']}")
    print(f"  - Images: {stats['nb_images']}")
    print(f"  - Vidéos: {stats['nb_videos']}")
    print(f"  - Mots-clés uniques: {stats['nb_mots_cles_uniques']}")
    
    # Statistiques de recherche
    engine = SearchEngine(db)
    recherches = engine.obtenir_statistiques(limit=10)
    
    if recherches:
        print("\n🔍 Recherches populaires:")
        print(f"  {'Requête':<30} {'Nb recherches':<15} {'Moy résultats':<15}")
        print("  " + "-"*60)
        for r in recherches[:5]:
            print(f"  {r[0]:<30} {r[1]:<15} {r[2]:<15.1f}")
    
    print("\n" + "="*70)

def reinitialiser_db(db):
    """Réinitialiser la base de données"""
    print("\n⚠️  ATTENTION: Cette action va supprimer toutes les données !")
    reponse = input("Confirmer la réinitialisation ? (oui/non): ")
    
    if reponse.lower() == 'oui':
        db.drop_tables()
        db.create_tables()
        print("✅ Base de données réinitialisée")
    else:
        print("❌ Réinitialisation annulée")

def lancer_interface_web():
    """Lancer l'interface web Flask avec API"""
    print("\n🌐 Lancement de l'interface web...")
    print("="*70)
    print("📍 L'interface sera accessible sur:")
    print("   - http://localhost:5000")
    print("   - http://127.0.0.1:5000")
    print("\n⏹️  Appuyez sur Ctrl+C pour arrêter le serveur")
    print("="*70)
    
    try:
        # Essayer d'abord d'importer depuis app.py s'il existe
        try:
            from app import app
            print("✅ Utilisation de app.py")
        except ImportError:
            # Sinon créer l'application Flask ici
            print("✅ Création de l'application Flask intégrée")
            from flask import Flask, jsonify, request, send_from_directory
            from flask_cors import CORS
            
            app = Flask(__name__)
            CORS(app)
            
            # Route pour servir le fichier HTML
            @app.route('/')
            def index():
                if os.path.exists('index.html'):
                    return send_from_directory('.', 'index.html')
                elif os.path.exists('templates/index.html'):
                    return send_from_directory('templates', 'index.html')
                else:
                    return "<h1>Interface Web</h1><p>Fichier index.html introuvable</p>", 404
            
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
        
        # Lancer le serveur
        app.run(debug=False, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Serveur arrêté")
    except Exception as e:
        print(f"\n❌ Erreur lors du lancement du serveur: {e}")
        print(f"💡 Assurez-vous d'avoir installé Flask: pip install flask flask-cors")

def tout_automatique(db):
    """Exécuter tout le processus automatiquement"""
    print("\n🤖 MODE AUTOMATIQUE COMPLET")
    print("="*70)
    print("Ce processus va:")
    print("  1. Télécharger le corpus")
    print("  2. Indexer les fichiers")
    print("  3. Lancer l'interface web")
    print("\n⏰ Cela peut prendre plusieurs minutes...")
    
    reponse = input("\n▶️  Continuer ? (o/n): ")
    
    if reponse.lower() != 'o':
        print("❌ Annulé")
        return
    
    # Étape 1: Téléchargement
    print("\n📥 ÉTAPE 1/3 - Téléchargement")
    telecharger_corpus()
    
    # Étape 2: Indexation
    print("\n📇 ÉTAPE 2/3 - Indexation")
    indexer_corpus(db)
    
    # Étape 3: Interface web
    print("\n🌐 ÉTAPE 3/3 - Lancement interface web")
    lancer_interface_web()

def main():
    """Fonction principale"""
    # Initialiser la base de données
    db = DatabaseConfig()
    db.connect()
    db.create_tables()
    
    try:
        while True:
            afficher_menu()
            choix = input("\n▶️  Votre choix: ").strip()
            
            if choix == '1':
                telecharger_corpus()
            
            elif choix == '2':
                indexer_corpus(db)
            
            elif choix == '3':
                tester_recherches(db)
            
            elif choix == '4':
                lancer_interface_web()
            
            elif choix == '5':
                afficher_stats(db)
            
            elif choix == '6':
                reinitialiser_db(db)
            
            elif choix == '7':
                tout_automatique(db)
            
            elif choix == '0':
                print("\n👋 Au revoir !")
                break
            
            else:
                print("\n❌ Choix invalide. Veuillez réessayer.")
            
            input("\n⏸️  Appuyez sur Entrée pour continuer...")
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Programme interrompu")
    
    finally:
        db.close()
        print("\n✅ Connexion à la base de données fermée")

if __name__ == "__main__":
    main()