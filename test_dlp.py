import spacy
import re

print("Chargement du modèle linguistique...")
nlp = spacy.load("en_core_web_sm")

# Nouveau texte de test avec des secrets cachés
email_text = "John Doe, CEO of Apple, sent an email from Paris on January 15th. His temporary password is 'P@ssw0rd2026!' and his direct phone number is 555-1234."

doc = nlp(email_text)

print("\n--- Analyse hybride du texte ---")
print(f"Texte original : '{email_text}'\n")

# 1. Détection via l'IA (Contexte et Grammaire)
print("🤖 Détection IA (spaCy) :")
for entite in doc.ents:
    # On filtre pour ne garder que les entités vraiment sensibles (Personnes, Organisations)
    if entite.label_ in ["PERSON", "ORG"]:
        print(f"  - {entite.text} (Type : {entite.label_})")

# 2. Détection via Regex (Règles strictes pour les secrets)
print("\n🔍 Détection Regex (Secrets et Formats stricts) :")

# Recherche d'un numéro de téléphone (Format simple : 3 chiffres, un tiret, 4 chiffres)
phone_pattern = r"\d{3}-\d{4}"
phones = re.findall(phone_pattern, email_text)
for phone in phones:
    print(f"  - {phone} (Type : PHONE_NUMBER)")

# Recherche d'un mot de passe (Cherche le mot 'password is' suivi du mot de passe entre guillemets)
password_pattern = r"password is '([^']+)'"
passwords = re.findall(password_pattern, email_text)
for pwd in passwords:
    print(f"  - {pwd} (Type : PASSWORD_SECRET)")