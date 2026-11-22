from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


# --- UTILISATEUR & AUTHENTIFICATION ---
class UtilisateurCreate(BaseModel):
    nom: str
    email: str
    mot_de_passe: str
    role: str = "agriculteur"  # 'agriculteur' ou 'administrateur'


class UtilisateurLogin(BaseModel):
    email: str
    mot_de_passe: str


class UtilisateurOut(BaseModel):
    id_user: int
    nom: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    nom: str


# --- EXPLOITATION ---
class ExploitationOut(BaseModel):
    id_ferme: int
    nom: str
    localisation: str
    superficie_totale: float

    model_config = ConfigDict(from_attributes=True)


# --- SEUIL CULTURE ---
class SeuilCultureCreate(BaseModel):
    type_culture: str
    seuil_humidite_min: float
    seuil_temp_max: float


class SeuilCultureOut(SeuilCultureCreate):
    id_seuil: int

    model_config = ConfigDict(from_attributes=True)


# --- PARCELLE ---
class ParcelleCreate(BaseModel):
    nom: str
    superficie: float
    type_culture: str
    id_user: Optional[int] = None
    id_ferme: int
    id_seuil: int


class ParcelleOut(ParcelleCreate):
    id_parcelle: int

    model_config = ConfigDict(from_attributes=True)


# --- CAPTEUR ---
class CapteurCreate(BaseModel):
    reference: str
    type_capteur: str  # 'Sol Surface', 'Sol Racine', 'Temp Air', 'Pluie', 'Débitmètre'
    unite_mesure: str  # '%', '°C', 'mm', 'L/min'
    statut: str = "Actif"
    id_parcelle: int


class CapteurOut(CapteurCreate):
    id_capteur: int

    model_config = ConfigDict(from_attributes=True)


# --- MESURE ---
class MesureCreate(BaseModel):
    id_capteur: int
    valeur: float


class MesureOut(BaseModel):
    id_mesure: int
    id_capteur: int
    valeur: float
    date_heure: datetime

    model_config = ConfigDict(from_attributes=True)


# --- ALERTE ---
class AlerteOut(BaseModel):
    id_alerte: int
    type_alerte: str
    message: str
    date_heure: datetime
    statut: str
    id_parcelle: int

    model_config = ConfigDict(from_attributes=True)


# --- RECOMMANDATION ---
class RecommandationOut(BaseModel):
    id_recommandation: int
    message: str
    date_heure: datetime
    statut: str
    action_conseillee: str
    id_parcelle: int

    model_config = ConfigDict(from_attributes=True)