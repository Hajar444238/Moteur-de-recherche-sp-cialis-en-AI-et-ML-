import time
from database_config import DatabaseConfig
from text_processor import TextProcessor

class SearchEngine:
    """Moteur de recherche pour interroger la base de données"""
    
    def __init__(self, db_config):
        self.db = db_config
        self.processor = TextProcessor()
    
    def normalize_query(self, query):
        """Normalise les requêtes AI/ML pour inclure les synonymes"""
        query_lower = query.lower().strip()
        
        # Dictionnaire des termes équivalents
        ai_ml_terms = {
            'ai': ['intelligence artificielle', 'artificial intelligence', 'ai', 'ia'],
            'ia': ['intelligence artificielle', 'artificial intelligence', 'ai', 'ia'],
            'ml': ['machine learning', 'apprentissage automatique', 'ml'],
            'ai&ml' :['machine learning' , 'intelligence artificielle' ,'machine learning et intelligence artificielle'],
            'deep learning': ['deep learning', 'apprentissage profond'],
            'neural': ['neural network', 'réseau de neurones', 'neural'],
            'tensorflow': ['tensorflow', 'tensor flow'],
            'pytorch': ['pytorch', 'py torch'],
            'nlp': ['natural language processing', 'traitement du langage naturel', 'nlp'],
            'cnn': ['convolutional neural network', 'réseau de neurones convolutif', 'cnn'],
            'rnn': ['recurrent neural network', 'réseau de neurones récurrent', 'rnn'],
            'data science': ['data science', 'science des données'],
            'algorithm': ['algorithm', 'algorithme'],
            'model': ['model', 'modèle', 'modelling', 'modélisation']
        }
        
        # Si la requête correspond à un terme AI/ML, retourner tous les synonymes
        for key, terms in ai_ml_terms.items():
            if query_lower == key:
                return ' '.join(terms)  # Joindre tous les termes avec des espaces
        
        return query  # Retourner la requête originale si pas de correspondance
    
    def rechercher(self, requete, type_contenu='all', limit=20):
        """Recherche principale"""
        debut = time.time()
        
        # AJOUT : Normaliser la requête pour les termes AI/ML
        requete_normalisee = self.normalize_query(requete)
        
        # Traiter la requête normalisée
        mots_requete = self.processor.extraire_mots_cles(requete_normalisee, min_freq=1)
        
        if not mots_requete:
            return {
                'resultats': [],
                'temps_ms': 0,
                'nb_total': 0,
                'requete_traitee': []
            }
        
        # Extraire les mots et racines
        mots = [m[0] for m in mots_requete]
        racines = [m[1] for m in mots_requete]
        
        resultats = []
        
        # Rechercher dans les documents (accepter 'document' ou 'documents')
        if type_contenu in ['document', 'documents', 'all']:
            resultats.extend(self._rechercher_documents(mots, racines, limit))
        
        # Rechercher dans les images (accepter 'image' ou 'images')
        if type_contenu in ['image', 'images', 'all']:
            resultats.extend(self._rechercher_images(mots, racines, limit))
        
        # Rechercher dans les vidéos (accepter 'video' ou 'videos')
        if type_contenu in ['video', 'videos', 'all']:
            resultats.extend(self._rechercher_videos(mots, racines, limit))
        
        # Trier par score de pertinence
        resultats.sort(key=lambda x: x['score'], reverse=True)
        
        # Limiter les résultats
        resultats = resultats[:limit]
        
        # Calculer le temps d'exécution
        temps_ms = (time.time() - debut) * 1000
        
        # Enregistrer les statistiques avec la requête originale
        self._enregistrer_statistique(requete, len(resultats), temps_ms)
        
        return {
            'resultats': resultats,
            'temps_ms': temps_ms,
            'nb_total': len(resultats),
            'requete_traitee': mots_requete
        }
    
    def _rechercher_documents(self, mots, racines, limit):
        """Rechercher dans les documents"""
        resultats = []
        
        # Construire la requête SQL
        placeholders_mots = ','.join(['?'] * len(mots))
        placeholders_racines = ','.join(['?'] * len(racines))
        
        query = f'''
            SELECT 
                d.id,
                d.titre,
                d.contenu,
                d.type_doc,
                d.chemin_fichier,
                COUNT(DISTINCT i.id) as nb_correspondances,
                SUM(i.frequence) as score_total
            FROM documents d
            JOIN index_mots_cles i ON d.id = i.doc_id
            WHERE i.mot_cle IN ({placeholders_mots})
               OR i.racine IN ({placeholders_racines})
            GROUP BY d.id
            ORDER BY score_total DESC, nb_correspondances DESC
            LIMIT ?
        '''
        
        self.db.cursor.execute(query, mots + racines + [limit])
        
        for row in self.db.cursor.fetchall():
            # Extraire un extrait pertinent
            extrait = self._extraire_extrait(row[2], mots, racines) if row[2] else ""
            
            resultats.append({
                'type': 'document',
                'id': row[0],
                'titre': row[1],
                'extrait': extrait,
                'contenu': row[2][:500] if row[2] else "",  # Ajouter contenu pour compatibilité
                'type_fichier': row[3],
                'chemin': row[4],
                'nb_correspondances': row[5],
                'score': row[6] if row[6] else 0
            })
        
        return resultats
    
    def _rechercher_images(self, mots, racines, limit):
        """Rechercher dans les images"""
        resultats = []
        
        placeholders_mots = ','.join(['?'] * len(mots))
        placeholders_racines = ','.join(['?'] * len(racines))
        
        query = f'''
            SELECT 
                img.id,
                img.titre,
                img.description,
                img.type_image,
                img.chemin_fichier,
                img.alt_text,
                COUNT(DISTINCT i.id) as nb_correspondances,
                SUM(i.frequence) as score_total
            FROM images img
            JOIN index_mots_cles i ON img.id = i.img_id
            WHERE i.mot_cle IN ({placeholders_mots})
               OR i.racine IN ({placeholders_racines})
            GROUP BY img.id
            ORDER BY score_total DESC, nb_correspondances DESC
            LIMIT ?
        '''
        
        self.db.cursor.execute(query, mots + racines + [limit])
        
        for row in self.db.cursor.fetchall():
            resultats.append({
                'type': 'image',
                'id': row[0],
                'titre': row[1],
                'extrait': row[2] or "",  # Ajouter extrait pour compatibilité
                'description': row[2] or "",
                'contenu': row[2] or "",  # Ajouter contenu pour compatibilité
                'type_fichier': row[3],
                'chemin': row[4],
                'alt_text': row[5] or "",
                'nb_correspondances': row[6],
                'score': row[7] if row[7] else 0
            })
        
        return resultats
    
    def _rechercher_videos(self, mots, racines, limit):
        """Rechercher dans les vidéos"""
        resultats = []
        
        placeholders_mots = ','.join(['?'] * len(mots))
        placeholders_racines = ','.join(['?'] * len(racines))
        
        query = f'''
            SELECT 
                v.id,
                v.titre,
                v.description,
                v.type_video,
                v.chemin_fichier,
                v.duree_secondes,
                COUNT(DISTINCT i.id) as nb_correspondances,
                SUM(i.frequence) as score_total
            FROM videos v
            JOIN index_mots_cles i ON v.id = i.video_id
            WHERE i.mot_cle IN ({placeholders_mots})
               OR i.racine IN ({placeholders_racines})
            GROUP BY v.id
            ORDER BY score_total DESC, nb_correspondances DESC
            LIMIT ?
        '''
        
        self.db.cursor.execute(query, mots + racines + [limit])
        
        for row in self.db.cursor.fetchall():
            resultats.append({
                'type': 'video',
                'id': row[0],
                'titre': row[1],
                'extrait': row[2] or "",  # Ajouter extrait pour compatibilité
                'description': row[2] or "",
                'contenu': row[2] or "",  # Ajouter contenu pour compatibilité
                'type_fichier': row[3],
                'chemin': row[4],
                'duree_secondes': row[5] or 0,
                'nb_correspondances': row[6],
                'score': row[7] if row[7] else 0
            })
        
        return resultats
    
    def _extraire_extrait(self, contenu, mots, racines, taille_extrait=200):
        """Extraire un extrait pertinent du contenu"""
        if not contenu:
            return ""
        
        contenu_lower = contenu.lower()
        
        # Trouver la première occurrence d'un mot de la requête
        premiere_pos = -1
        for mot in mots:
            pos = contenu_lower.find(mot.lower())
            if pos != -1 and (premiere_pos == -1 or pos < premiere_pos):
                premiere_pos = pos
        
        if premiere_pos == -1:
            return contenu[:taille_extrait] + "..."
        
        # Extraire autour de la correspondance
        debut = max(0, premiere_pos - taille_extrait // 2)
        fin = min(len(contenu), premiere_pos + taille_extrait // 2)
        
        extrait = contenu[debut:fin]
        
        if debut > 0:
            extrait = "..." + extrait
        if fin < len(contenu):
            extrait = extrait + "..."
        
        return extrait
    
    def _enregistrer_statistique(self, requete, nb_resultats, temps_ms):
        """Enregistrer les statistiques de recherche"""
        try:
            self.db.cursor.execute('''
                INSERT INTO statistiques_recherche 
                (requete, nb_resultats, temps_execution_ms)
                VALUES (?, ?, ?)
            ''', (requete, nb_resultats, temps_ms))
            self.db.conn.commit()
        except Exception as e:
            print(f"⚠️ Erreur enregistrement statistiques: {e}")
    
    def obtenir_statistiques(self, limit=10):
        """Obtenir les statistiques des recherches récentes"""
        self.db.cursor.execute('''
            SELECT 
                requete,
                COUNT(*) as nb_recherches,
                AVG(nb_resultats) as moy_resultats,
                AVG(temps_execution_ms) as moy_temps_ms
            FROM statistiques_recherche
            GROUP BY requete
            ORDER BY nb_recherches DESC
            LIMIT ?
        ''', (limit,))
        
        return self.db.cursor.fetchall()
    
    def suggestions_recherche(self, debut_mot, limit=5):
        """Suggérer des mots-clés basés sur le début de la saisie"""
        self.db.cursor.execute('''
            SELECT DISTINCT mot_cle, COUNT(*) as freq
            FROM index_mots_cles
            WHERE mot_cle LIKE ?
            GROUP BY mot_cle
            ORDER BY freq DESC
            LIMIT ?
        ''', (debut_mot + '%', limit))
        
        return [row[0] for row in self.db.cursor.fetchall()]