import os
import requests
from pathlib import Path
import yt_dlp
from urllib.parse import urlparse, unquote
import time

class ContentDownloader:
    """Classe pour télécharger les documents, images et vidéos"""
    
    def __init__(self, corpus_dir="corpus"):
        self.corpus_dir = corpus_dir
        self.docs_dir = os.path.join(corpus_dir, "documents")
        self.images_dir = os.path.join(corpus_dir, "images")
        self.videos_dir = os.path.join(corpus_dir, "videos")
        
        # Créer les dossiers si nécessaire (VERSION CORRIGÉE)
        self._create_directories()
        
        # URLs à télécharger
        self.pdf_urls = [
            "https://ai.stanford.edu/~nilsson/MLBOOK.pdf",
            "https://www.lamsade.dauphine.fr/~croyer/ensdocs/FML/PolyFML.pdf",
            "http://www.math-evry.cnrs.fr/_media/members/aguilloux/enseignements/machinelearningpython/slides_v2.pdf",
            "https://www.dane.daneteach.fr/wp-content/uploads/Les-differents-algorithmes-de-lIA.pdf",
            "https://cazencott.info/dotclear/public/lectures/IntroML_Azencott.pdf",
            "https://perso.ensta.fr/~franchi/Cours/MI201/cours_ml_intro_2025.pdf",
            "https://www-verimag.imag.fr/~perin/talks/vulgarisation/perin_2023_IA_generative.pdf",
            "http://web.univ-ubs.fr/lmba/lardjane/python/c3.pdf",
            "https://static.fnac-static.com/multimedia/editorial/pdf/9782409031816.pdf",
            "https://perso.ensta.fr/~manzaner/Cours/MI203/cours_ml_intro.pdf",
            "https://www.mediachimie.org/sites/default/files/Chimie_et-IA-Chap1.pdf"
        ]
        
        self.image_urls = [
            "https://tse4.mm.bing.net/th/id/OIP.wCqabWki10p7aZCkjkcf7gHaEK?pid=Api&P=0&h=180",
            "https://tse4.mm.bing.net/th/id/OIP.J_HmiwHPWxfhOsyVhUuMfgHaDP?pid=Api&P=0&h=180"
        ]
        
        self.video_urls = [
            "https://youtu.be/SfOoRsUj9kQ",
            "https://youtu.be/CoqZxKheSKg",
            "https://youtu.be/0-PWE5O2c5w",
            "https://youtu.be/N6I4SnhO_MY",
            "https://youtu.be/EUD07IiviJg"
        ]
    
    def _create_directories(self):
        """Créer les dossiers de manière sécurisée (CORRECTION)"""
        directories = [self.corpus_dir, self.docs_dir, self.images_dir, self.videos_dir]
        
        for directory in directories:
            try:
                if not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)
                    print(f"✓ Créé: {directory}")
                else:
                    print(f"ℹ️  Existe déjà: {directory}")
            except FileExistsError:
                print(f"ℹ️  Dossier existe déjà: {directory}")
            except Exception as e:
                print(f"⚠️  Erreur création {directory}: {e}")
    
    def telecharger_fichier(self, url, destination_dir, nom_fichier=None):
        """Télécharger un fichier depuis une URL"""
        try:
            print(f"📥 Téléchargement: {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=60, stream=True)
            response.raise_for_status()
            
            # Déterminer le nom du fichier
            if not nom_fichier:
                if 'Content-Disposition' in response.headers:
                    content_disp = response.headers['Content-Disposition']
                    if 'filename=' in content_disp:
                        nom_fichier = content_disp.split('filename=')[1].strip('"')
                
                if not nom_fichier:
                    parsed_url = urlparse(url)
                    nom_fichier = os.path.basename(unquote(parsed_url.path))
                
                if not nom_fichier or nom_fichier == '':
                    ext = '.pdf' if 'pdf' in url.lower() else '.jpg'
                    nom_fichier = f"document_{int(time.time())}{ext}"
            
            chemin_complet = os.path.join(destination_dir, nom_fichier)
            
            # Télécharger avec barre de progression
            taille_totale = int(response.headers.get('content-length', 0))
            taille_telechargee = 0
            
            with open(chemin_complet, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        taille_telechargee += len(chunk)
                        if taille_totale > 0:
                            pourcent = (taille_telechargee / taille_totale) * 100
                            print(f"\r  Progress: {pourcent:.1f}%", end='')
            
            print(f"\n✓ Téléchargé: {nom_fichier} ({taille_telechargee / 1024:.1f} KB)")
            return chemin_complet
            
        except Exception as e:
            print(f"❌ Erreur téléchargement {url}: {e}")
            return None
    
    def telecharger_video_youtube(self, url, destination_dir):
        """Télécharger une vidéo YouTube avec yt-dlp"""
        try:
            print(f"📹 Téléchargement vidéo YouTube: {url}")
            
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': os.path.join(destination_dir, '%(title)s.%(ext)s'),
                'quiet': False,
                'no_warnings': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                nom_fichier = ydl.prepare_filename(info)
                
            print(f"✓ Vidéo téléchargée: {os.path.basename(nom_fichier)}")
            return nom_fichier
            
        except Exception as e:
            print(f"❌ Erreur téléchargement vidéo {url}: {e}")
            print("💡 Astuce: Installez yt-dlp avec: pip install yt-dlp")
            return None
    
    def telecharger_tous_les_pdfs(self):
        """Télécharger tous les PDFs"""
        print("\n" + "="*70)
        print("📚 TÉLÉCHARGEMENT DES DOCUMENTS PDF")
        print("="*70)
        
        fichiers = []
        for i, url in enumerate(self.pdf_urls, 1):
            print(f"\n[{i}/{len(self.pdf_urls)}]")
            fichier = self.telecharger_fichier(url, self.docs_dir)
            if fichier:
                fichiers.append(fichier)
            time.sleep(1)
        
        print(f"\n✓ {len(fichiers)}/{len(self.pdf_urls)} PDFs téléchargés")
        return fichiers
    
    def telecharger_toutes_les_images(self):
        """Télécharger toutes les images"""
        print("\n" + "="*70)
        print("🖼️  TÉLÉCHARGEMENT DES IMAGES")
        print("="*70)
        
        fichiers = []
        for i, url in enumerate(self.image_urls, 1):
            print(f"\n[{i}/{len(self.image_urls)}]")
            nom = f"ai_ml_image_{i}.jpg"
            fichier = self.telecharger_fichier(url, self.images_dir, nom)
            if fichier:
                fichiers.append(fichier)
            time.sleep(1)
        
        print(f"\n✓ {len(fichiers)}/{len(self.image_urls)} images téléchargées")
        return fichiers
    
    def telecharger_toutes_les_videos(self):
        """Télécharger toutes les vidéos YouTube"""
        print("\n" + "="*70)
        print("🎬 TÉLÉCHARGEMENT DES VIDÉOS")
        print("="*70)
        
        fichiers = []
        for i, url in enumerate(self.video_urls, 1):
            print(f"\n[{i}/{len(self.video_urls)}]")
            fichier = self.telecharger_video_youtube(url, self.videos_dir)
            if fichier:
                fichiers.append(fichier)
            time.sleep(2)
        
        print(f"\n✓ {len(fichiers)}/{len(self.video_urls)} vidéos téléchargées")
        return fichiers
    
    def telecharger_tout(self):
        """Télécharger tout le contenu"""
        print("\n" + "="*70)
        print("🚀 TÉLÉCHARGEMENT DU CORPUS COMPLET")
        print("="*70)
        
        resultats = {
            'pdfs': self.telecharger_tous_les_pdfs(),
            'images': self.telecharger_toutes_les_images(),
            'videos': self.telecharger_toutes_les_videos()
        }
        
        print("\n" + "="*70)
        print("📊 RÉSUMÉ DU TÉLÉCHARGEMENT")
        print("="*70)
        print(f"✓ Documents PDF: {len(resultats['pdfs'])}")
        print(f"✓ Images: {len(resultats['images'])}")
        print(f"✓ Vidéos: {len(resultats['videos'])}")
        print(f"✓ Total: {sum(len(v) for v in resultats.values())} fichiers")
        print(f"✓ Dossier corpus: {os.path.abspath(self.corpus_dir)}")
        
        return resultats


if __name__ == "__main__":
    print("\n🎯 MODULE DE TÉLÉCHARGEMENT - MOTEUR DE RECHERCHE AI/ML")
    print("=" * 70)
    
    downloader = ContentDownloader()
    
    print("\n📋 Contenu à télécharger:")
    print(f"  - {len(downloader.pdf_urls)} documents PDF")
    print(f"  - {len(downloader.image_urls)} images")
    print(f"  - {len(downloader.video_urls)} vidéos YouTube")
    
    reponse = input("\n▶️  Commencer le téléchargement ? (o/n): ")
    
    if reponse.lower() == 'o':
        resultats = downloader.telecharger_tout()
        
        print("\n✅ Téléchargement terminé !")
        print(f"📁 Les fichiers sont dans: {os.path.abspath(downloader.corpus_dir)}")
        print("\n💡 Prochaine étape: Exécutez main.py pour indexer le corpus")
    else:
        print("\n⏹️  Téléchargement annulé")