#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'Installation et de Configuration
Moteur de Recherche AI & Machine Learning
"""

import os
import sys
import subprocess
import platform

def print_header(text):
    """Afficher un en-tête stylisé"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def check_python_version():
    """Vérifier la version de Python"""
    print_header("🐍 Vérification de Python")
    
    version = sys.version_info
    print(f"Version Python détectée: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 ou supérieur est requis !")
        print("💡 Téléchargez Python sur: https://www.python.org/downloads/")
        return False
    
    print("✅ Version Python compatible")
    return True

def check_pip():
    """Vérifier que pip est installé"""
    print_header("📦 Vérification de pip")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print("✅ pip est installé")
        return True
    except:
        print("❌ pip n'est pas installé !")
        print("💡 Installation de pip...")
        try:
            subprocess.run([sys.executable, "-m", "ensurepip", "--default-pip"],
                         check=True)
            print("✅ pip installé avec succès")
            return True
        except:
            print("❌ Impossible d'installer pip automatiquement")
            return False

def create_directory_structure():
    """Créer la structure de dossiers"""
    print_header("📁 Création de la structure de dossiers")
    
    directories = [
        "corpus",
        "corpus/documents",
        "corpus/images",
        "corpus/videos",
        "templates",
        "static",
        "static/css",
        "static/js"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Créé: {directory}")
        else:
            print(f"ℹ️  Existe déjà: {directory}")
    
    return True

def install_dependencies():
    """Installer les dépendances Python"""
    print_header("⬇️  Installation des dépendances")
    
    packages = [
        "Flask==3.0.0",
        "PyPDF2==3.0.1",
        "python-docx==1.1.0",
        "beautifulsoup4==4.12.2",
        "lxml==4.9.3",
        "requests==2.31.0",
        "yt-dlp"
    ]
    
    print("📦 Installation des packages Python...")
    
    for package in packages:
        print(f"\n  ⬇️  Installation de {package.split('==')[0]}...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", package, "--quiet"],
                check=True
            )
            print(f"  ✅ {package.split('==')[0]} installé")
        except subprocess.CalledProcessError:
            print(f"  ⚠️  Erreur avec {package}, tentative sans version...")
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", package.split('==')[0], "--quiet"],
                    check=True
                )
                print(f"  ✅ {package.split('==')[0]} installé")
            except:
                print(f"  ❌ Impossible d'installer {package.split('==')[0]}")
    
    return True

def create_html_template():
    """Créer le template HTML si nécessaire"""
    print_header("📄 Vérification du template HTML")
    
    template_path = os.path.join("templates", "index.html")
    
    if os.path.exists(template_path):
        print("✅ Template HTML existe déjà")
        return True
    
    print("⚠️  Template HTML manquant")
    print("💡 Veuillez copier le contenu HTML fourni dans templates/index.html")
    return False

def verify_files():
    """Vérifier que tous les fichiers nécessaires existent"""
    print_header("🔍 Vérification des fichiers")
    
    required_files = [
        "database_config.py",
        "text_processor.py",
        "indexer.py",
        "search_engine.py",
        "downloader.py",
        "app.py",
        "main.py"
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MANQUANT")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  Fichiers manquants: {len(missing_files)}")
        print("💡 Veuillez copier tous les fichiers Python fournis")
        return False
    
    return True

def test_imports():
    """Tester que tous les modules s'importent correctement"""
    print_header("🧪 Test des imports")
    
    modules = [
        ("Flask", "flask"),
        ("PyPDF2", "PyPDF2"),
        ("python-docx", "docx"),
        ("BeautifulSoup", "bs4"),
        ("requests", "requests"),
        ("yt-dlp", "yt_dlp")
    ]
    
    all_ok = True
    
    for name, module in modules:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - Non disponible")
            all_ok = False
    
    return all_ok

def display_next_steps():
    """Afficher les prochaines étapes"""
    print_header("🎯 PROCHAINES ÉTAPES")
    
    print("\n✅ Installation terminée avec succès !\n")
    print("📋 Pour utiliser le moteur de recherche:\n")
    print("1️⃣  Lancer le script principal:")
    print("    python main.py")
    print("\n2️⃣  Dans le menu, choisir l'option 7 (mode automatique):")
    print("    - Télécharge le corpus complet")
    print("    - Indexe tous les documents")
    print("    - Lance l'interface web")
    print("\n3️⃣  Ouvrir votre navigateur:")
    print("    http://localhost:5000")
    print("\n" + "="*70)
    print("\n💡 ASTUCES:")
    print("   - Le téléchargement peut prendre 5-10 minutes")
    print("   - Assurez-vous d'avoir une connexion Internet")
    print("   - Pour tester: python test_queries.py")
    print("\n" + "="*70)

def main():
    """Fonction principale du script d'installation"""
    print("\n" + "="*70)
    print("🚀 INSTALLATION - MOTEUR DE RECHERCHE AI & ML")
    print("="*70)
    print("\nCe script va:")
    print("  ✓ Vérifier Python et pip")
    print("  ✓ Créer la structure de dossiers")
    print("  ✓ Installer les dépendances")
    print("  ✓ Vérifier les fichiers nécessaires")
    
    response = input("\n▶️  Continuer ? (o/n): ")
    if response.lower() != 'o':
        print("\n❌ Installation annulée")
        return
    
    # Étape 1: Vérifier Python
    if not check_python_version():
        return
    
    # Étape 2: Vérifier pip
    if not check_pip():
        return
    
    # Étape 3: Créer les dossiers
    create_directory_structure()
    
    # Étape 4: Installer les dépendances
    install_dependencies()
    
    # Étape 5: Vérifier les fichiers
    files_ok = verify_files()
    
    # Étape 6: Vérifier le template HTML
    html_ok = create_html_template()
    
    # Étape 7: Tester les imports
    imports_ok = test_imports()
    
    # Résumé
    print("\n" + "="*70)
    print("📊 RÉSUMÉ DE L'INSTALLATION")
    print("="*70)
    print(f"  Python: ✅")
    print(f"  pip: ✅")
    print(f"  Structure dossiers: ✅")
    print(f"  Dépendances: ✅")
    print(f"  Fichiers Python: {'✅' if files_ok else '❌'}")
    print(f"  Template HTML: {'✅' if html_ok else '⚠️'}")
    print(f"  Imports: {'✅' if imports_ok else '⚠️'}")
    
    if files_ok and imports_ok:
        print("\n🎉 Installation réussie !")
        display_next_steps()
    else:
        print("\n⚠️  Installation incomplète")
        print("💡 Veuillez corriger les erreurs ci-dessus avant de continuer")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Installation interrompue")
    except Exception as e:
        print(f"\n❌ Erreur durant l'installation: {e}")
        print("💡 Veuillez réessayer ou installer manuellement")