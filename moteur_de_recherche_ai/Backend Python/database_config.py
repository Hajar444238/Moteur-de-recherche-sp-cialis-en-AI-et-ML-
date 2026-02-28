import sqlite3
import os

class DatabaseConfig:
    """Configuration et initialisation de la base de données SQLite"""
    
    def __init__(self, db_name="ai_search_engine.db"):
    # Utiliser le dossier courant (là où on lance le script)
        self.db_path = os.path.abspath(db_name)
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        print(f"🗄️  Base de données: {self.db_path}")
        
    def connect(self):
        """Établir la connexion à la base de données"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        print(f"✓ Connexion établie à {self.db_path}")
        return self.conn, self.cursor
    
    def create_tables(self):
        """Créer les tables nécessaires"""
        
        # Table des documents
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                contenu TEXT,
                type_doc TEXT CHECK(type_doc IN ('pdf', 'txt', 'docx', 'html')),
                chemin_fichier TEXT UNIQUE,
                date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                taille_octets INTEGER,
                langue TEXT DEFAULT 'fr'
            )
        ''')
        
        # Table des images
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                description TEXT,
                chemin_fichier TEXT UNIQUE,
                type_image TEXT CHECK(type_image IN ('jpg', 'jpeg', 'png', 'gif', 'svg')),
                date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                taille_octets INTEGER,
                alt_text TEXT
            )
        ''')
        
        # Table des vidéos
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                description TEXT,
                chemin_fichier TEXT UNIQUE,
                type_video TEXT CHECK(type_video IN ('mp4', 'avi', 'mov', 'webm')),
                duree_secondes INTEGER,
                date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                taille_octets INTEGER
            )
        ''')
        
        # Table d'index des mots-clés
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS index_mots_cles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mot_cle TEXT NOT NULL,
                racine TEXT NOT NULL,
                doc_id INTEGER,
                img_id INTEGER,
                video_id INTEGER,
                frequence INTEGER DEFAULT 1,
                position_texte INTEGER,
                FOREIGN KEY (doc_id) REFERENCES documents(id) ON DELETE CASCADE,
                FOREIGN KEY (img_id) REFERENCES images(id) ON DELETE CASCADE,
                FOREIGN KEY (video_id) REFERENCES videos(id) ON DELETE CASCADE
            )
        ''')
        
        # Index pour améliorer les performances de recherche
        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_mot_cle 
            ON index_mots_cles(mot_cle)
        ''')
        
        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_racine 
            ON index_mots_cles(racine)
        ''')
        
        # Table des statistiques de recherche
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistiques_recherche (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                requete TEXT NOT NULL,
                nb_resultats INTEGER,
                date_recherche TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                temps_execution_ms REAL
            )
        ''')
        
        self.conn.commit()
        print("✓ Tables créées avec succès")
    
    def drop_tables(self):
        """Supprimer toutes les tables (pour réinitialisation)"""
        tables = ['statistiques_recherche', 'index_mots_cles', 'videos', 'images', 'documents']
        for table in tables:
            self.cursor.execute(f'DROP TABLE IF EXISTS {table}')
        self.conn.commit()
        print("✓ Tables supprimées")
    
    def close(self):
        """Fermer la connexion"""
        if self.conn:
            self.conn.close()
            print("✓ Connexion fermée")
    
    def get_stats(self):
        """Obtenir des statistiques sur la base de données"""
        stats = {}
        
        try:
            self.cursor.execute("SELECT COUNT(*) FROM documents")
            stats['nb_documents'] = self.cursor.fetchone()[0]
        except:
            stats['nb_documents'] = 0
        
        try:
            self.cursor.execute("SELECT COUNT(*) FROM images")
            stats['nb_images'] = self.cursor.fetchone()[0]
        except:
            stats['nb_images'] = 0
        
        try:
            self.cursor.execute("SELECT COUNT(*) FROM videos")
            stats['nb_videos'] = self.cursor.fetchone()[0]
        except:
            stats['nb_videos'] = 0
        
        try:
            self.cursor.execute("SELECT COUNT(DISTINCT mot_cle) FROM index_mots_cles")
            stats['nb_mots_cles_uniques'] = self.cursor.fetchone()[0]
        except:
            stats['nb_mots_cles_uniques'] = 0
        
        return stats


# Test de la configuration
if __name__ == "__main__":
    db = DatabaseConfig()
    db.connect()
    db.create_tables()
    
    stats = db.get_stats()
    print("\n📊 Statistiques de la base de données:")
    for key, value in stats.items():
        print(f"  - {key}: {value}")
    
    db.close()