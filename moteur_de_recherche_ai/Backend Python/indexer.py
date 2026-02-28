import os
import PyPDF2
import docx
from pathlib import Path
from database_config import DatabaseConfig
from text_processor import TextProcessor

class DocumentIndexer:
    """Classe pour l'indexation des documents dans la base de données"""
    
    def __init__(self, db_config):
        self.db = db_config
        self.processor = TextProcessor()
    
    def lire_fichier_texte(self, chemin):
        """Lire un fichier texte simple"""
        try:
            with open(chemin, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            try:
                with open(chemin, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception as e:
                print(f"❌ Erreur lecture {chemin}: {e}")
                return ""
    
    def lire_pdf(self, chemin):
        """Extraire le texte d'un PDF"""
        try:
            texte = ""
            with open(chemin, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    texte += page.extract_text() + "\n"
            return texte
        except Exception as e:
            print(f"❌ Erreur lecture PDF {chemin}: {e}")
            return ""
    
    def lire_docx(self, chemin):
        """Extraire le texte d'un fichier Word"""
        try:
            doc = docx.Document(chemin)
            texte = "\n".join([para.text for para in doc.paragraphs])
            return texte
        except Exception as e:
            print(f"❌ Erreur lecture DOCX {chemin}: {e}")
            return ""
    
    def lire_html(self, chemin):
        """Extraire le texte d'un fichier HTML"""
        try:
            from bs4 import BeautifulSoup
            with open(chemin, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                return soup.get_text()
        except:
            return self.lire_fichier_texte(chemin)
    
    def extraire_contenu(self, chemin):
        """Extraire le contenu selon le type de fichier"""
        ext = Path(chemin).suffix.lower()
        
        if ext == '.txt':
            return self.lire_fichier_texte(chemin)
        elif ext == '.pdf':
            return self.lire_pdf(chemin)
        elif ext == '.docx':
            return self.lire_docx(chemin)
        elif ext in ['.html', '.htm']:
            return self.lire_html(chemin)
        else:
            return ""
    
    def indexer_document(self, chemin, titre=None):
        """Indexer un document dans la base de données"""
        try:
            # Vérifier si le fichier existe
            if not os.path.exists(chemin):
                print(f"❌ Fichier introuvable: {chemin}")
                return False
            
            # Extraire les métadonnées
            ext = Path(chemin).suffix.lower()[1:]  # Enlever le point
            taille = os.path.getsize(chemin)
            titre = titre or Path(chemin).stem
            
            # Extraire le contenu
            contenu = self.extraire_contenu(chemin)
            
            if not contenu:
                print(f"⚠️ Aucun contenu extrait de {chemin}")
            
            # Insérer le document
            self.db.cursor.execute('''
                INSERT OR REPLACE INTO documents 
                (titre, contenu, type_doc, chemin_fichier, taille_octets)
                VALUES (?, ?, ?, ?, ?)
            ''', (titre, contenu, ext, chemin, taille))
            
            doc_id = self.db.cursor.lastrowid
            
            # Extraire et indexer les mots-clés
            mots_cles = []
            if contenu:
                mots_cles = self.processor.extraire_avec_positions(contenu)
                
                for item in mots_cles:
                    self.db.cursor.execute('''
                        INSERT INTO index_mots_cles 
                        (mot_cle, racine, doc_id, position_texte)
                        VALUES (?, ?, ?, ?)
                    ''', (item['mot'], item['racine'], doc_id, item['position']))
            
            self.db.conn.commit()
            print(f"✓ Document indexé: {titre} ({len(mots_cles)} mots-clés)")
            return True
            
        except Exception as e:
            print(f"❌ Erreur indexation {chemin}: {e}")
            return False
    
    def indexer_image(self, chemin, titre=None, description="", alt_text=""):
        """Indexer une image"""
        try:
            if not os.path.exists(chemin):
                print(f"❌ Image introuvable: {chemin}")
                return False
            
            ext = Path(chemin).suffix.lower()[1:]
            taille = os.path.getsize(chemin)
            titre = titre or Path(chemin).stem
            
            self.db.cursor.execute('''
                INSERT OR REPLACE INTO images 
                (titre, description, chemin_fichier, type_image, taille_octets, alt_text)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (titre, description, chemin, ext, taille, alt_text))
            
            img_id = self.db.cursor.lastrowid
            
            # Indexer les mots-clés du titre, description et alt_text
            texte_complet = f"{titre} {description} {alt_text}"
            mots_cles = self.processor.extraire_avec_positions(texte_complet)
            
            for item in mots_cles:
                self.db.cursor.execute('''
                    INSERT INTO index_mots_cles 
                    (mot_cle, racine, img_id, position_texte)
                    VALUES (?, ?, ?, ?)
                ''', (item['mot'], item['racine'], img_id, item['position']))
            
            self.db.conn.commit()
            print(f"✓ Image indexée: {titre}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur indexation image {chemin}: {e}")
            return False
    
    def indexer_video(self, chemin, titre=None, description="", duree=0):
        """Indexer une vidéo"""
        try:
            if not os.path.exists(chemin):
                print(f"❌ Vidéo introuvable: {chemin}")
                return False
            
            ext = Path(chemin).suffix.lower()[1:]
            taille = os.path.getsize(chemin)
            titre = titre or Path(chemin).stem
            
            self.db.cursor.execute('''
                INSERT OR REPLACE INTO videos 
                (titre, description, chemin_fichier, type_video, duree_secondes, taille_octets)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (titre, description, chemin, ext, duree, taille))
            
            video_id = self.db.cursor.lastrowid
            
            # Indexer les mots-clés du titre et description
            texte_complet = f"{titre} {description}"
            mots_cles = self.processor.extraire_avec_positions(texte_complet)
            
            for item in mots_cles:
                self.db.cursor.execute('''
                    INSERT INTO index_mots_cles 
                    (mot_cle, racine, video_id, position_texte)
                    VALUES (?, ?, ?, ?)
                ''', (item['mot'], item['racine'], video_id, item['position']))
            
            self.db.conn.commit()
            print(f"✓ Vidéo indexée: {titre}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur indexation vidéo {chemin}: {e}")
            return False
    
    def indexer_dossier(self, dossier_corpus):
        """Indexer tous les fichiers d'un dossier"""
        if not os.path.exists(dossier_corpus):
            print(f"❌ Dossier introuvable: {dossier_corpus}")
            return
        
        compteurs = {'docs': 0, 'images': 0, 'videos': 0, 'erreurs': 0}
        
        for root, dirs, files in os.walk(dossier_corpus):
            for file in files:
                chemin = os.path.join(root, file)
                ext = Path(file).suffix.lower()
                
                try:
                    # Documents
                    if ext in ['.txt', '.pdf', '.docx', '.html', '.htm']:
                        if self.indexer_document(chemin):
                            compteurs['docs'] += 1
                        else:
                            compteurs['erreurs'] += 1
                    
                    # Images
                    elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg']:
                        if self.indexer_image(chemin):
                            compteurs['images'] += 1
                        else:
                            compteurs['erreurs'] += 1
                    
                    # Vidéos
                    elif ext in ['.mp4', '.avi', '.mov', '.webm']:
                        if self.indexer_video(chemin):
                            compteurs['videos'] += 1
                        else:
                            compteurs['erreurs'] += 1
                
                except Exception as e:
                    print(f"❌ Erreur avec {file}: {e}")
                    compteurs['erreurs'] += 1
        
        print("\n📊 Résumé de l'indexation:")
        print(f"  ✓ Documents indexés: {compteurs['docs']}")
        print(f"  ✓ Images indexées: {compteurs['images']}")
        print(f"  ✓ Vidéos indexées: {compteurs['videos']}")
        print(f"  ❌ Erreurs: {compteurs['erreurs']}")
        
        return compteurs


# Test du module d'indexation
if __name__ == "__main__":
    # Initialiser la base de données
    db = DatabaseConfig()
    db.connect()
    db.create_tables()
    
    # Créer l'indexeur
    indexer = DocumentIndexer(db)
    
    print("\n✓ Module d'indexation prêt à l'emploi")
    print("  Usage: indexer.indexer_dossier('chemin/vers/corpus')")
    
    db.close()