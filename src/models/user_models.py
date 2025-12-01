from dataclasses import dataclass
from typing import Optional

@dataclass
class Usuario:
    nome: str
    email: str
    senha: str
    tipo: str
    id_usuario: Optional[int] = None
    criado_em: Optional[str] = None
    atualizado_em: Optional[str] = None

@dataclass
class ProfessorExtra:
    id_prof: int
    biografia: Optional[str] = None
    departamento: Optional[str] = None

@dataclass
class AlunoExtra:
    id_aluno: int
    matricula: str
    id_turma: int