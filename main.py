from fastapi import FastAPI
from pydantic import BaseModel
import spacy
import re

# 1. Initialisation de l'API et du modèle IA
app = FastAPI(title="DataGuard Semantic API", description="Moteur de détection DLP")

# --- AJOUT DU CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En développement, on autorise tout le monde. En production, on mettra l'URL du frontend.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ---------------------

print("Chargement du modèle linguistique en tâche de fond...")

print("Chargement du modèle linguistique en tâche de fond...")
nlp = spacy.load("en_core_web_sm")

# 2. Définition du format de données que l'API s'attend à recevoir (un simple texte)
class TextRequest(BaseModel):
    text: str

# 3. Création de la route principale d'analyse
@app.post("/analyze")
def analyze_text(request: TextRequest):
    text_input = request.text
    sensible_data = [] # Liste qui va stocker toutes nos trouvailles

    # --- Phase 1: Détection IA (spaCy) ---
    doc = nlp(text_input)
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG"]:
            sensible_data.append({
                "valeur": ent.text,
                "type": ent.label_,
                "moteur": "IA Contextuelle"
            })

    # --- Phase 2: Détection Regex (Secrets) ---
    phone_pattern = r"\d{3}-\d{4}"
    for phone in re.findall(phone_pattern, text_input):
        sensible_data.append({
            "valeur": phone,
            "type": "PHONE_NUMBER",
            "moteur": "Regex"
        })

    password_pattern = r"password is '([^']+)'"
    for pwd in re.findall(password_pattern, text_input):
        sensible_data.append({
            "valeur": pwd,
            "type": "PASSWORD_SECRET",
            "moteur": "Regex"
        })

    # L'API renvoie un dictionnaire (qui sera automatiquement transformé en JSON)
    return {
        "status": "success",
        "total_detecte": len(sensible_data),
        "donnees_sensibles": sensible_data
    }