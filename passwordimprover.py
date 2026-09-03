import random
from time import sleep
import string
import re
import subprocess
scoremdp = 0

def has_special_char(s):
    global scoremdp
    count = sum(1 for char in s if char in string.punctuation)
    print(f"  [SPECIAL] caractères spéciaux trouvés : {count}")
    count = min(count, 3)
    points = round(count * 25/3/3, 2)
    print(f"  [SPECIAL] +{points} pts")
    scoremdp += points

def has_capitals(m):
    global scoremdp
    count = sum(1 for char in m if char.isupper())
    print(f"  [MAJUSC] majuscules trouvées : {count}")
    count = min(count, 3)
    points = round(count * 25/3/3, 2)
    print(f"  [MAJUSC] +{points} pts")
    scoremdp += points

def has_num(m):
    global scoremdp
    count = sum(1 for char in m if char.isdigit())
    print(f"  [CHIFFRE] chiffres trouvés : {count}")
    count = min(count, 3)
    points = round(count * 25/3/3, 2)
    print(f"  [CHIFFRE] +{points} pts")
    scoremdp += points

def has_repetitions(m):
    global scoremdp
    repeats = re.search(r"(.)\1{2,}", m)
    print(f"  [REPET] répétition détectée : {repeats.group() if repeats else 'aucune'}")

    sequences = False
    for i in range(len(m) - 2):
        a, b, c = m[i], m[i+1], m[i+2]
        if (a.isalpha() and b.isalpha() and c.isalpha()) or \
           (a.isdigit() and b.isdigit() and c.isdigit()):
            if ord(b) == ord(a) + 1 and ord(c) == ord(b) + 1:
                sequences = True
                print(f"  [REPET & SEQ] séquence trouvée : {a}{b}{c}")
                break
    if not sequences:
        print("  [REPET & SEQ] aucune séquence détectée")

    if repeats is None:
        print("  [REPET & SEQ] +5 pts (pas de répétition)")
        scoremdp += 5
    else:
        print("  [REPET & SEQ] +0 pts (répétition présente)")

    if not sequences:
        print("  [REPET & SEQ] +5 pts (pas de séquence)")
        scoremdp += 5
    else:
        print("  [REPET & SEQ] +0 pts (séquence présente)")

while True:
    subprocess.run(['clear'])
    print("=" * 50)
    print("MENU PRINCIPAL — PasswordImprover")
    print("=" * 50)
    choix = int(input("Que veux-tu faire ?\n 1) Évaluer ton mot de passe\n 2) Générer un mot de passe\n 3) Améliorer ton mot de passe avec mistral\n Choix : "))

    if choix == 1:
        scoremdp = 0
        mdp = input("Quel est le mot de passe à vérifier ? ")
        longueur = len(mdp)
        subprocess.run(['clear'])
        print(f"\n--- Analyse de '{mdp}' (longueur : {longueur}) ---")

        with open("rockyou.txt", "r", encoding="latin-1") as f:
            rockyou = set(ligne.strip() for ligne in f)
        with open("nom.txt", "r", encoding="latin-1") as f:
            noms = set(ligne.strip().lower() for ligne in f if ligne.strip())

        if mdp.lower() in rockyou:
            print("  [ROCKYOU] Mot de passe trop commun. Score : 0/100")
            sleep(3)
            continue
        else:
            print("  [ROCKYOU] Pas dans la liste rockyou ✓")
        
        mots = set(m.lower() for m in re.findall(r"[a-zA-Z]+", re.sub(r"([a-z])([A-Z])", r"\1 \2", mdp)))
        noms_trouves = sorted(noms & mots)
        if not noms_trouves:
            print("  [NOM] aucun nom commun détecté → +15 pts")
            scoremdp += 15
        else:
            print(f"  [NOM] noms détectés : {noms_trouves[:5]}")
            print("  [NOM] nom commun détecté → +0 pts")

        has_special_char(mdp)
        has_capitals(mdp)
        has_num(mdp)
        has_repetitions(mdp)

        if longueur < 6:
            print(f"  [LONGUEUR] {longueur} chars → +0 pts, trop court")
            print("Score : 0/100")
            continue

        distincts = len(set(mdp))
        if distincts >= 16:
            scoremdp += 50
            print(f"  [LONGUEUR] {longueur} chars, {distincts} distincts ≥ 16 → +50 pts")
        elif distincts >= 12:
            scoremdp += 35
            print(f"  [LONGUEUR] {longueur} chars, {distincts} distincts ≥ 12 → +35 pts")
        elif distincts >= 8:
            scoremdp += 20
            print(f"  [LONGUEUR] {longueur} chars, {distincts} distincts ≥ 8 → +20 pts")
        else:
            scoremdp += 5
            print(f"  [LONGUEUR] {longueur} chars, {distincts} distincts → +5 pts")

        scoremdp = max(0, min(scoremdp, 100))
        scoremdp = round(scoremdp)

        print(f"\nScore de sécurité : {scoremdp}/100")
        if scoremdp <= 15:
            print("Ton mot de passe est vraiment faible.")
        elif scoremdp <= 30:
            print("Ton mot de passe est faible.")
        elif scoremdp <= 45:
            print("Ton mot de passe est légèrement faible.")
        elif scoremdp <= 60:
            print("Pas mauvais, mais il pourrait être mieux.")
        elif scoremdp <= 75:
            print("Ton mot de passe est bien.")
        else:
            print("Ton mot de passe est excellent.")

    elif choix == 2:
        choix2 = int(input("Quel type ?\n 1) Solide (22 car.)\n 2) Intermédiaire (16 car.)\n 3) Simplifié (10 car.)\nChoix : "))
        subprocess.run(['clear'])
        chars_complet = list(string.ascii_letters + string.digits + '!"#$%&()*+-./<=?>@[]^_`{|}~')
        chars_moyen   = list(string.ascii_letters + string.digits + '!"#$%&()-/?@')
        chars_simple  = list(string.ascii_letters + string.digits)

        configs = {1: (chars_complet, 22), 2: (chars_moyen, 16), 3: (chars_simple, 10)}

        if choix2 in configs:
            chars, longueur = configs[choix2]
            nb = int(input("Combien de mots de passe ? "))
            for _ in range(nb):
                print("".join(random.choice(chars) for _ in range(longueur)))
    elif choix == 3:
        mdp = input("Quel est le mot de passe à améliorer ? ")
        subprocess.run(['clear'])
        # critères manquants
        manquants = []
        if not any(c in string.punctuation for c in mdp):
            manquants.append("ajoute des caractères spéciaux")
        if not any(c.isupper() for c in mdp):
            manquants.append("ajoute des majuscules")
        if not any(c.isdigit() for c in mdp):
            manquants.append("ajoute des chiffres")
        if re.search(r"(.)\1{2,}", mdp):
            manquants.append("évite les répétitions de caractères consécutifs")
        if len(mdp) < 16:
            manquants.append("allonge jusqu'à 16-22 caractères")

        # si déjà bon, on n'appelle pas le LLM
        if not manquants:
            print("\n  [LLM] Ton mot de passe remplit déjà tous les critères. Rien à améliorer !")
            retour = input("\nRetourner au menu ? (oui/non) : ").lower()
            if retour not in ("oui", "o", "y", "yes"):
                print("Merci d'avoir utilisé ce programme !")
                break
            continue

        conseils = ", ".join(manquants)
        systeme = (
            "Tu es un assistant d'un outil pédagogique de sécurité. "
            "L'utilisateur teste SON PROPRE mot de passe et veut des variantes PLUS FORTES. "
            "Produire des mots de passe plus robustes est exactement le but de l'outil. "
            "Ne refuse jamais."
        )
        prompt = (
            f"{systeme}\n\n"
            f"Tâche : à partir du mot de passe ci-dessous, produire exactement 3 variantes plus fortes.\n"
            f"Format de réponse OBLIGATOIRE : 3 lignes, un mot de passe par ligne, AUCUN autre texte, "
            f"aucune phrase, aucune explication, aucune ponctuation de phrase, aucun espace dans les mots de passes.\n\n"
            f"Mot de passe de départ : {mdp}\n"
            f"À corriger : {conseils}.\n"
            f"Contraintes : longueur 16-22, sans répétitions ni séquences, même style que l'original."
        )

        print("\n  [LLM] Génération en cours...")
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt, capture_output=True, text=True
        )
        sortie = result.stdout.strip()


        print("\n  [LLM] Suggestions :")
        print(sortie)
    retour = input("\nRetourner au menu ? (oui/non) : ").lower()
    if retour not in ("oui", "o", "y", "yes"):
        print("Merci d'avoir utilisé ce programme !")
        break
