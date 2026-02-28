import re
import string
from collections import Counter

class TextProcessor:
    """Classe pour le traitement et l'indexation du texte"""
    
    def __init__(self):
        # Anti-dictionnaire (mots vides) en français et anglais
        self.stop_words_fr = {
            'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'et', 'ou', 'mais',
            'donc', 'car', 'ni', 'est', 'sont', 'a', 'au', 'aux', 'ce', 'cette',
            'ces', 'mon', 'ma', 'mes', 'ton', 'ta', 'tes', 'son', 'sa', 'ses',
            'notre', 'nos', 'votre', 'vos', 'leur', 'leurs', 'je', 'tu', 'il',
            'elle', 'nous', 'vous', 'ils', 'elles', 'on', 'qui', 'que', 'quoi',
            'dont', 'où', 'pour', 'par', 'dans', 'sur', 'avec', 'sans', 'sous',
            'entre', 'vers', 'chez', 'être', 'avoir', 'faire', 'dire', 'aller',
            'voir', 'savoir', 'pouvoir', 'falloir', 'vouloir', 'devoir', 'plus',
            'moins', 'très', 'aussi', 'encore', 'déjà', 'ici', 'là', 'alors'
        }
        
        self.stop_words_en = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this',
            'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'what', 'which', 'who', 'when', 'where', 'why', 'how', 'all', 'each',
            'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
            'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very'
        }
        
        self.stop_words = self.stop_words_fr.union(self.stop_words_en)
        
        # Règles de racinisation simplifiées (stemming)
        self.suffixes_fr = [
            'ement', 'ation', 'ateur', 'atrice', 'ique', 'isme', 'able', 'ible',
            'eux', 'euse', 'ance', 'ence', 'ité', 'age', 'ment', 'ant', 'ent',
            'ais', 'ait', 'aient', 'era', 'erai', 'erais', 'erait', 'és', 'ées',
            'er', 'ez', 'é', 'ée', 's', 'x'
        ]
        
        self.suffixes_en = [
            'ing', 'ed', 'es', 's', 'er', 'est', 'ly', 'ness', 'ment', 
            'tion', 'sion', 'ance', 'ence', 'able', 'ible', 'al', 'ful',
            'less', 'ous', 'ive', 'ize', 'ise'
        ]
    
    def nettoyer_texte(self, texte):
        """Nettoyer le texte: minuscules, suppression ponctuation"""
        if not texte:
            return ""
        
        # Convertir en minuscules
        texte = texte.lower()
        
        # Remplacer les caractères spéciaux par des espaces
        texte = re.sub(r'[^\w\sàâäéèêëïîôùûüÿæœç]', ' ', texte)
        
        # Supprimer les espaces multiples
        texte = re.sub(r'\s+', ' ', texte)
        
        return texte.strip()
    
    def tokeniser(self, texte):
        """Diviser le texte en tokens (mots)"""
        texte_propre = self.nettoyer_texte(texte)
        tokens = texte_propre.split()
        return tokens
    
    def appliquer_anti_dictionnaire(self, tokens):
        """Supprimer les mots vides (stop words)"""
        return [token for token in tokens if token not in self.stop_words and len(token) > 2]
    
    def raciniser(self, mot):
        """
        Racinisation (stemming): réduire un mot à sa racine
        Algorithme simplifié inspiré de Porter
        """
        if len(mot) <= 3:
            return mot
        
        # Essayer les suffixes français
        for suffixe in sorted(self.suffixes_fr, key=len, reverse=True):
            if mot.endswith(suffixe) and len(mot) - len(suffixe) >= 3:
                return mot[:-len(suffixe)]
        
        # Essayer les suffixes anglais
        for suffixe in sorted(self.suffixes_en, key=len, reverse=True):
            if mot.endswith(suffixe) and len(mot) - len(suffixe) >= 3:
                return mot[:-len(suffixe)]
        
        return mot
    
    def lemmatiser_simple(self, mot):
        """
        Lemmatisation simplifiée
        (Pour une vraie lemmatisation, utiliser spaCy ou NLTK)
        """
        # Dictionnaire de lemmes courants pour l'IA/ML
        lemmes = {
            'algorithmes': 'algorithme',
            'réseaux': 'réseau',
            'neurones': 'neurone',
            'données': 'donnée',
            'modèles': 'modèle',
            'apprentissage': 'apprendre',
            'entraînement': 'entraîner',
            'prédictions': 'prédiction',
            'classifications': 'classification',
            'optimisations': 'optimisation',
            'networks': 'network',
            'models': 'model',
            'algorithms': 'algorithm',
            'predictions': 'prediction',
            'training': 'train',
            'learning': 'learn'
        }
        
        return lemmes.get(mot, mot)
    
    def extraire_mots_cles(self, texte, min_freq=1):
        """
        Pipeline complet d'extraction de mots-clés
        1. Nettoyage
        2. Tokenisation
        3. Anti-dictionnaire
        4. Lemmatisation
        5. Racinisation
        """
        # Tokenisation
        tokens = self.tokeniser(texte)
        
        # Appliquer l'anti-dictionnaire
        tokens_filtres = self.appliquer_anti_dictionnaire(tokens)
        
        # Lemmatisation et racinisation
        mots_cles = []
        racines = []
        
        for token in tokens_filtres:
            lemme = self.lemmatiser_simple(token)
            racine = self.raciniser(lemme)
            mots_cles.append(token)
            racines.append(racine)
        
        # Calculer les fréquences
        freq_mots = Counter(zip(mots_cles, racines))
        
        # Filtrer par fréquence minimale
        resultats = [
            (mot, racine, freq) 
            for (mot, racine), freq in freq_mots.items() 
            if freq >= min_freq
        ]
        
        return sorted(resultats, key=lambda x: x[2], reverse=True)
    
    def extraire_avec_positions(self, texte):
        """
        Extraire les mots-clés avec leurs positions dans le texte
        CETTE MÉTHODE ÉTAIT MANQUANTE - C'EST LA CAUSE DE L'ERREUR
        """
        tokens = self.tokeniser(texte)
        tokens_filtres_avec_pos = []
        
        position = 0
        for i, token in enumerate(tokens):
            if token not in self.stop_words and len(token) > 2:
                lemme = self.lemmatiser_simple(token)
                racine = self.raciniser(lemme)
                tokens_filtres_avec_pos.append({
                    'mot': token,
                    'racine': racine,
                    'position': i
                })
        
        return tokens_filtres_avec_pos


# Test du processeur de texte
if __name__ == "__main__":
    processor = TextProcessor()
    
    # Texte de test sur l'IA
    texte_test = """
    L'intelligence artificielle et le machine learning révolutionnent 
    le monde de la technologie. Les réseaux de neurones profonds 
    permettent d'entraîner des modèles sophistiqués pour la classification 
    et la prédiction. Les algorithmes d'apprentissage automatique analysent 
    de grandes quantités de données pour optimiser les performances.
    """
    
    print("📝 Texte original:")
    print(texte_test)
    
    print("\n🔍 Extraction des mots-clés:")
    mots_cles = processor.extraire_mots_cles(texte_test)
    
    print(f"\n{'Mot-clé':<25} {'Racine':<20} {'Fréquence':<10}")
    print("-" * 60)
    for mot, racine, freq in mots_cles[:15]:
        print(f"{mot:<25} {racine:<20} {freq:<10}")
    
    print("\n📍 Extraction avec positions:")
    avec_pos = processor.extraire_avec_positions(texte_test)
    for item in avec_pos[:10]:
        print(f"Position {item['position']:3d}: {item['mot']} → {item['racine']}")