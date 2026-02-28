from database_config import DatabaseConfig
from indexer import DocumentIndexer
import os

print("🔄 Réindexation des documents...")

# Connexion à la base
db = DatabaseConfig()
db.connect()
db.create_tables()

# Créer l'indexeur
indexer = DocumentIndexer(db)

# Chemin du dossier corpus
corpus_path = os.path.join(os.path.dirname(__file__), 'corpus')  # ← Corrigé ici

if os.path.exists(corpus_path):
    print(f"📂 Indexation du dossier: {corpus_path}")
    compteurs = indexer.indexer_dossier(corpus_path)
    print("\n✅ Indexation terminée !")
    print(f"   - Documents indexés: {compteurs.get('documents', 0)}")
    print(f"   - Images: {compteurs.get('images', 0)}")
    print(f"   - Vidéos: {compteurs.get('videos', 0)}")
    
    # Afficher les nouvelles stats
    stats = db.get_stats()
    print("\n📊 Statistiques de la base:")
    for key, value in stats.items():
        print(f"   - {key}: {value}")
else:
    print(f"❌ Dossier corpus introuvable: {corpus_path}")
    print("💡 Créez un dossier 'corpus' et placez-y vos documents à indexer")

db.close()