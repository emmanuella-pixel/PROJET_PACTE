from sqlalchemy import Column, Integer, BigInteger, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Utilisateur(Base):
    __tablename__ = "Utilisateur"

    id_user = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    mot_de_passe = Column(String(255), nullable=False)
    role = Column(String(30), nullable=False, default="agriculteur")

    parcelles = relationship("Parcelle", back_populates="agriculteur")


class Exploitation(Base):
    __tablename__ = "Exploitation"

    id_ferme = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    localisation = Column(String(150), nullable=False)
    superficie_totale = Column(Float, nullable=False)

    parcelles = relationship("Parcelle", back_populates="exploitation")


class SeuilCulture(Base):
    __tablename__ = "SeuilCulture"

    id_seuil = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type_culture = Column(String(50), nullable=False)
    seuil_humidite_min = Column(Float, nullable=False)
    seuil_temp_max = Column(Float, nullable=False)

    parcelles = relationship("Parcelle", back_populates="seuil")


class Parcelle(Base):
    __tablename__ = "Parcelle"

    id_parcelle = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    superficie = Column(Float, nullable=False)
    type_culture = Column(String(50), nullable=False)

    id_user = Column(Integer, ForeignKey("Utilisateur.id_user", ondelete="SET NULL"), nullable=True)
    id_ferme = Column(Integer, ForeignKey("Exploitation.id_ferme", ondelete="CASCADE"), nullable=False)
    id_seuil = Column(Integer, ForeignKey("SeuilCulture.id_seuil", ondelete="RESTRICT"), nullable=False)

    agriculteur = relationship("Utilisateur", back_populates="parcelles")
    exploitation = relationship("Exploitation", back_populates="parcelles")
    seuil = relationship("SeuilCulture", back_populates="parcelles")
    capteurs = relationship("Capteur", back_populates="parcelle", cascade="all, delete-orphan")
    alertes = relationship("Alerte", back_populates="parcelle", cascade="all, delete-orphan")
    recommandations = relationship("Recommandation", back_populates="parcelle", cascade="all, delete-orphan")


class Capteur(Base):
    __tablename__ = "Capteur"

    id_capteur = Column(Integer, primary_key=True, index=True, autoincrement=True)
    reference = Column(String(50), unique=True, nullable=False)
    type_capteur = Column(String(50), nullable=False)  # 'Sol Surface', 'Sol Racine', 'Temp Air', 'Pluie', 'Débitmètre'
    unite_mesure = Column(String(20), nullable=False)  # '%', '°C', 'mm', 'L/min'
    statut = Column(String(30), nullable=False, default="Actif")
    id_parcelle = Column(Integer, ForeignKey("Parcelle.id_parcelle", ondelete="CASCADE"), nullable=False)

    parcelle = relationship("Parcelle", back_populates="capteurs")
    mesures = relationship("Mesure", back_populates="capteur", cascade="all, delete-orphan")


class Mesure(Base):
    __tablename__ = "Mesure"

    id_mesure = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    valeur = Column(Float, nullable=False)
    date_heure = Column(DateTime, nullable=False, server_default=func.now())
    id_capteur = Column(Integer, ForeignKey("Capteur.id_capteur", ondelete="CASCADE"), nullable=False)

    capteur = relationship("Capteur", back_populates="mesures")


class Alerte(Base):
    __tablename__ = "Alerte"

    id_alerte = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type_alerte = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    date_heure = Column(DateTime, nullable=False, server_default=func.now())
    statut = Column(String(30), nullable=False, default="Non lue")
    id_parcelle = Column(Integer, ForeignKey("Parcelle.id_parcelle", ondelete="CASCADE"), nullable=False)

    parcelle = relationship("Parcelle", back_populates="alertes")


class Recommandation(Base):
    __tablename__ = "Recommandation"

    id_recommandation = Column(Integer, primary_key=True, index=True, autoincrement=True)
    message = Column(Text, nullable=False)
    date_heure = Column(DateTime, nullable=False, server_default=func.now())
    statut = Column(String(30), nullable=False, default="Émise")
    action_conseillee = Column(String(255), nullable=False)
    id_parcelle = Column(Integer, ForeignKey("Parcelle.id_parcelle", ondelete="CASCADE"), nullable=False)

    parcelle = relationship("Parcelle", back_populates="recommandations")