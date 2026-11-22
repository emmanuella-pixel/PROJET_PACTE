from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Utilisateur
from ..schemas import UtilisateurCreate, UtilisateurLogin, UtilisateurOut, Token
from ..security import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post("/register", response_model=UtilisateurOut, status_code=status.HTTP_201_CREATED)
def register(user_data: UtilisateurCreate, db: Session = Depends(get_db)):
    existing = db.query(Utilisateur).filter(Utilisateur.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Cet email est déjà utilisé.")

    if user_data.role not in ["agriculteur", "administrateur"]:
        raise HTTPException(status_code=400, detail="Rôle invalide.")

    new_user = Utilisateur(
        nom=user_data.nom,
        email=user_data.email,
        mot_de_passe=hash_password(user_data.mot_de_passe),
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(credentials: UtilisateurLogin, db: Session = Depends(get_db)):
    user = db.query(Utilisateur).filter(Utilisateur.email == credentials.email).first()
    if not user or not verify_password(credentials.mot_de_passe, user.mot_de_passe):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect."
        )

    token = create_access_token(data={"sub": user.email, "role": user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "nom": user.nom
    }


@router.get("/me", response_model=UtilisateurOut)
def read_current_user(current_user: Utilisateur = Depends(get_current_user)):
    return current_user