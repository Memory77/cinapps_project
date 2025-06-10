from pydantic import BaseModel
from typing import Optional

class AvisCreate(BaseModel):
    id_film: int
    username: str
    note: int
    commentaire: Optional[str] = None
