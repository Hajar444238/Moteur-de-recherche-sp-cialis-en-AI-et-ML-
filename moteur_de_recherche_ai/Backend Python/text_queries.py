#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests de Requêtes - Moteur de Recherche AI & ML
Ce script teste les requêtes fructueuses et non fructueuses
"""

import time
from database_config import DatabaseConfig
from search_engine import SearchEngine

class QueryTester:
    """Classe pour tester les requêtes de recherche"""
    
    def __init__(self, db_config):
        self.db = db_config
        self.engine = SearchEngine(db_config)
        self.results = {
            'fructueuses': [],
            'non_fructueuses': []
        }
    
    def test_requete(self, requete, attendu_fructueux=True):
        """
        Tester une requête et enregistrer les résultats
        
        Args:
            requete: La requête à tester
            attendu_fructueux: True si on attend des résultats, False sinon
        """
        print(f"\n{'='*80}")
        print(f"🔍 Test: '{requete}'")
        print(f"📋 Attendu: {'RÉSULTATS TROUVÉS' if attendu_fructueux else 'AUCUN RÉSULTAT'}")
        print('='*80)
        
        # Effectuer la recherche
        debut = time.time()
        resultats = self.engine.rechercher(requete, limit=20)
        duree = time.time() - debut
        
        # Analyser les résultats
        nb_resultats = resultats['nb_total']
        succes = (nb_resultats > 0) == attendu_fructueux
        
        # Afficher les détails
        print(f"\n📊 Résultats:")
        print(f"   - Nombre de résultats: {nb_resultats}")
        print(f"   - Temps d'exécution: {resultats['temps_ms']:.2f} ms")
        print(f"   - Temps total: {duree*1000:.2f} ms")
        
        if resultats['requete_traitee']:
            print(f"\n🔤 Traitement de la requête:")
            print(f"   - Mots-clés extraits: {len(resultats['requete_traitee'])}")
            for mot, racine, freq in resultats['requete_traitee'][:5]:
                print(f"     • {mot} → {racine}")
        
        if nb_resultats > 0:
            print(f"\n📄 Top 3 résultats:")
            for i, res in enumerate(resultats['resultats'][:3], 1):
                print(f"\n   {i}. [{res['type'].upper()}] {res['titre']}")
                print(f"      Score: {res['score']} | Correspondances: {res['nb_correspondances']}")
                if 'extrait' in res and res['extrait']:
                    extrait = res['extrait'][:100] + "..." if len(res['extrait']) > 100 else res['extrait']
                    print(f"      Extrait: {extrait}")
        
        # Verdict
        print(f"\n{'✅' if succes else '❌'} Verdict: ", end='')
        if succes:
            if attendu_fructueux:
                print("SUCCÈS - Résultats trouvés comme attendu")
            else:
                print("SUCCÈS - Aucun résultat comme attendu")
        else:
            if attendu_fructueux:
                print("ÉCHEC - Aucun résultat alors qu'on en attendait")
            else:
                print("ÉCHEC - Résultats trouvés alors qu'on n'en attendait pas")
        
        # Enregistrer le résultat
        info = {
            'requete': requete,
            'nb_resultats': nb_resultats,
            'temps_ms': resultats['temps_ms'],
            'succes': succes,
            'top_result': resultats['resultats'][0] if resultats['resultats'] else None
        }
        
        if attendu_fructueux:
            self.results['fructueuses'].append(info)
        else:
            self.results['non_fructueuses'].append(info)
        
        return succes
    
    def run_all_tests(self):
        """Exécuter tous les tests"""
        print("\n" + "="*80)
        print("🧪 SUITE DE TESTS COMPLÈTE")
        print("="*80)
        
        # Tests fructueux
        print("\n" + "="*80)
        print("✅ PARTIE 1: REQUÊTES FRUCTUEUSES")
        print("="*80)
        print("Ces requêtes devraient retourner des résultats pertinents\n")
        
        requetes_fructueuses = [
            "apprentissage automatique",
            "réseaux de neurones",
            "intelligence artificielle",
            "algorithme classification",
            "deep learning",
            "machine learning",
            "neural network",
            "gradient descent",
            "supervised learning",
            "data science",
            "python",
            "régression",
            "clustering",
            "optimisation",
            "modèle prédictif"
        ]
        
        succes_fructueux = 0
        for requete in requetes_fructueuses:
            if self.test_requete(requete, attendu_fructueux=True):
                succes_fructueux += 1
            time.sleep(0.5)  # Petite pause entre les tests
        
        # Tests non fructueux
        print("\n\n" + "="*80)
        print("❌ PARTIE 2: REQUÊTES NON FRUCTUEUSES")
        print("="*80)
        print("Ces requêtes NE devraient PAS retourner de résultats\n")
        
        requetes_non_fructueuses = [
            "cuisine italienne",
            "football champions league",
            "astronomie galaxie",
            "xyzabc123qwerty",
            "voiture électrique tesla",
            "recette gâteau chocolat",
            "voyage paris new york",
            "film cinéma action",
            "musique rock metal",
            "jardinage plantes",
            "architecture moderne",
            "histoire napoléon",
            "géographie afrique",
            "biologie cellule",
            "chimie organique"
        ]
        
        succes_non_fructueux = 0
        for requete in requetes_non_fructueuses:
            if self.test_requete(requete, attendu_fructueux=False):
                succes_non_fructueux += 1
            time.sleep(0.5)
        
        # Résumé global
        self.afficher_resume(
            succes_fructueux, 
            len(requetes_fructueuses),
            succes_non_fructueux,
            len(requetes_non_fructueuses)
        )
    
    def afficher_resume(self, succes_f, total_f, succes_nf, total_nf):
        """Afficher le résumé des tests"""
        print("\n\n" + "="*80)
        print("📊 RÉSUMÉ DES TESTS")
        print("="*80)
        
        print(f"\n✅ Requêtes Fructueuses:")
        print(f"   - Tests réussis: {succes_f}/{total_f}")
        print(f"   - Taux de succès: {(succes_f/total_f)*100:.1f}%")
        
        if self.results['fructueuses']:
            moy_resultats = sum(r['nb_resultats'] for r in self.results['fructueuses']) / len(self.results['fructueuses'])
            moy_temps = sum(r['temps_ms'] for r in self.results['fructueuses']) / len(self.results['fructueuses'])
            print(f"   - Moyenne résultats: {moy_resultats:.1f}")
            print(f"   - Temps moyen: {moy_temps:.2f} ms")
        
        print(f"\n❌ Requêtes Non Fructueuses:")
        print(f"   - Tests réussis: {succes_nf}/{total_nf}")
        print(f"   - Taux de succès: {(succes_nf/total_nf)*100:.1f}%")
        
        if self.results['non_fructueuses']:
            moy_resultats = sum(r['nb_resultats'] for r in self.results['non_fructueuses']) / len(self.results['non_fructueuses'])
            moy_temps = sum(r['temps_ms'] for r in self.results['non_fructueuses']) / len(self.results['non_fructueuses'])
            print(f"   - Moyenne résultats: {moy_resultats:.1f}")
            print(f"   - Temps moyen: {moy_temps:.2f} ms")
        
        total_succes = succes_f + succes_nf
        total_tests = total_f + total_nf
        
        print(f"\n🎯 Score Global:")
        print(f"   - Total réussi: {total_succes}/{total_tests}")
        print(f"   - Taux de succès global: {(total_succes/total_tests)*100:.1f}%")
        
        # Verdict final
        print(f"\n{'='*80}")
        if (total_succes / total_tests) >= 0.8:
            print("🎉 EXCELLENT ! Le moteur de recherche fonctionne très bien !")
        elif (total_succes / total_tests) >= 0.6:
            print("👍 BIEN ! Le moteur de recherche fonctionne correctement.")
        else:
            print("⚠️  ATTENTION ! Le moteur nécessite des améliorations.")
        print("="*80)
        
        # Top requêtes fructueuses
        if self.results['fructueuses']:
            print("\n🏆 Top 5 Requêtes Fructueuses (par nombre de résultats):")
            top = sorted(self.results['fructueuses'], key=lambda x: x['nb_resultats'], reverse=True)[:5]
            for i, r in enumerate(top, 1):
                print(f"   {i}. '{r['requete']}' - {r['nb_resultats']} résultats")
    
    def export_results(self, filename="test_results.txt"):
        """Exporter les résultats dans un fichier"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("RAPPORT DE TESTS - MOTEUR DE RECHERCHE AI & ML\n")
            f.write("="*80 + "\n\n")
            
            f.write("REQUÊTES FRUCTUEUSES:\n")
            f.write("-"*80 + "\n")
            for r in self.results['fructueuses']:
                f.write(f"\nRequête: {r['requete']}\n")
                f.write(f"  Résultats: {r['nb_resultats']}\n")
                f.write(f"  Temps: {r['temps_ms']:.2f} ms\n")
                f.write(f"  Succès: {'✓' if r['succes'] else '✗'}\n")
            
            f.write("\n\n" + "="*80 + "\n")
            f.write("REQUÊTES NON FRUCTUEUSES:\n")
            f.write("-"*80 + "\n")
            for r in self.results['non_fructueuses']:
                f.write(f"\nRequête: {r['requete']}\n")
                f.write(f"  Résultats: {r['nb_resultats']}\n")
                f.write(f"  Temps: {r['temps_ms']:.2f} ms\n")
                f.write(f"  Succès: {'✓' if r['succes'] else '✗'}\n")
        
        print(f"\n📄 Résultats exportés vers: {filename}")


def main():
    """Fonction principale"""
    print("\n" + "="*80)
    print("🧪 MODULE DE TESTS - MOTEUR DE RECHERCHE AI & ML")
    print("="*80)
    
    # Initialiser la base
    db = DatabaseConfig()
    db.connect()
    
    # Vérifier qu'il y a des données
    stats = db.get_stats()
    if stats['nb_documents'] == 0 and stats['nb_images'] == 0 and stats['nb_videos'] == 0:
        print("\n⚠️  ATTENTION: La base de données est vide !")
        print("💡 Veuillez d'abord:")
        print("   1. Télécharger le corpus (python downloader.py)")
        print("   2. Indexer les fichiers (python main.py - option 2)")
        db.close()
        return
    
    print(f"\n📊 Base de données:")
    print(f"   - Documents: {stats['nb_documents']}")
    print(f"   - Images: {stats['nb_images']}")
    print(f"   - Vidéos: {stats['nb_videos']}")
    print(f"   - Mots-clés: {stats['nb_mots_cles_uniques']}")
    
    input("\n▶️  Appuyez sur Entrée pour commencer les tests...")
    
    # Créer le testeur
    tester = QueryTester(db)
    
    # Lancer tous les tests
    tester.run_all_tests()
    
    # Exporter les résultats
    tester.export_results()
    
    db.close()
    
    print("\n✅ Tests terminés !")

if __name__ == "__main__":
    main()