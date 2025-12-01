from typing import Dict, Any, Optional, List
import re
from src.repositories.user_repository import UserRepository
from src.db.supabase_class import SupabaseClient
from postgrest.exceptions import APIError

class UserService:
    def __init__(self):
        self.repo = UserRepository()
        self.client = SupabaseClient().client

    def _validar_email(self, email: str) -> bool:
        """Valida formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def _validar_senha(self, senha: str) -> bool:
        """Valida senha (mínimo 6 caracteres)"""
        return len(senha) >= 6

    def _validar_usuario_basico(self, payload: Dict[str, Any]) -> None:
        """Validações comuns para todos os usuários"""
        if not payload.get("nome"):
            raise ValueError("Nome é obrigatório")
        
        if not payload.get("email"):
            raise ValueError("Email é obrigatório")
        
        if not self._validar_email(payload["email"]):
            raise ValueError("Email inválido")
        
        if not payload.get("senha"):
            raise ValueError("Senha é obrigatória")
        
        if not self._validar_senha(payload["senha"]):
            raise ValueError("Senha deve ter no mínimo 6 caracteres")
        
        if not payload.get("tipo"):
            raise ValueError("Tipo de usuário é obrigatório")
        
        if payload["tipo"] not in ["aluno", "professor"]:
            raise ValueError("Tipo deve ser 'aluno' ou 'professor'")

    def criar_usuario_basico(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            self._validar_usuario_basico(payload)
            return self.repo.create_usuario(payload)
        except ValueError as e:
            raise Exception(f"Validação falhou: {str(e)}")
        except APIError as e:
            raise Exception(f"Erro ao criar usuário: {e.message}")
        except Exception as e:
            raise Exception(f"Erro inesperado ao criar usuário: {str(e)}")

    def criar_professor(self, payload_usuario: Dict[str, Any], payload_prof: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Validações do usuário base
            self._validar_usuario_basico(payload_usuario)
            
            # Validações específicas do professor
            if payload_prof.get("departamento") and len(payload_prof["departamento"]) < 2:
                raise ValueError("Departamento deve ter no mínimo 2 caracteres")
            
            payload_usuario["tipo"] = "professor"
            usuario = self.repo.create_usuario(payload_usuario)
            payload_prof["id_prof"] = usuario["id_usuario"]
            prof_data = self.client.table("professores").insert(payload_prof).execute()
            return {**usuario, "detalhes_professor": prof_data.data[0]}
        except ValueError as e:
            raise Exception(f"Validação falhou: {str(e)}")
        except APIError as e:
            raise Exception(f"Erro ao criar professor: {e.message}")
        except Exception as e:
            raise Exception(f"Erro inesperado ao criar professor: {str(e)}")

    def criar_aluno(self, payload_usuario: Dict[str, Any], payload_aluno: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Validações do usuário base
            self._validar_usuario_basico(payload_usuario)
            
            # Validações específicas do aluno
            if not payload_aluno.get("matricula"):
                raise ValueError("Matrícula é obrigatória")
            
            if len(payload_aluno["matricula"]) < 3:
                raise ValueError("Matrícula deve ter no mínimo 3 caracteres")
            
            if not payload_aluno.get("id_turma"):
                raise ValueError("Turma é obrigatória")
            
            if not isinstance(payload_aluno["id_turma"], int) or payload_aluno["id_turma"] <= 0:
                raise ValueError("ID da turma deve ser um número positivo")
            
            payload_usuario["tipo"] = "aluno"
            usuario = self.repo.create_usuario(payload_usuario)
            payload_aluno["id_aluno"] = usuario["id_usuario"]
            aluno_data = self.client.table("alunos").insert(payload_aluno).execute()
            return {**usuario, "detalhes_aluno": aluno_data.data[0]}
        except ValueError as e:
            raise Exception(f"Validação falhou: {str(e)}")
        except APIError as e:
            raise Exception(f"Erro ao criar aluno: {e.message}")
        except Exception as e:
            raise Exception(f"Erro inesperado ao criar aluno: {str(e)}")

    def listar(self) -> List[Dict[str, Any]]:
        try:
            return self.repo.list_usuarios()
        except APIError as e:
            raise Exception(f"Erro ao listar usuários: {e.message}")
        except Exception as e:
            raise Exception(f"Erro inesperado ao listar usuários: {str(e)}")

    def obter(self, usuario_id: int) -> Optional[Dict[str, Any]]:
        try:
            if not isinstance(usuario_id, int) or usuario_id <= 0:
                raise ValueError("ID do usuário deve ser um número positivo")
            
            return self.repo.get_usuario(usuario_id)
        except ValueError as e:
            raise Exception(f"Validação falhou: {str(e)}")
        except APIError as e:
            raise Exception(f"Erro ao obter usuário: {e.message}")
        except Exception as e:
            raise Exception(f"Erro inesperado ao obter usuário: {str(e)}")

    def atualizar(self, usuario_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if not isinstance(usuario_id, int) or usuario_id <= 0:
                raise ValueError("ID do usuário deve ser um número positivo")
            
            # Validações opcionais (apenas se os campos estiverem presentes)
            if "email" in payload and not self._validar_email(payload["email"]):
                raise ValueError("Email inválido")
            
            if "senha" in payload and not self._validar_senha(payload["senha"]):
                raise ValueError("Senha deve ter no mínimo 6 caracteres")
            
            if "nome" in payload and len(payload["nome"]) < 2:
                raise ValueError("Nome deve ter no mínimo 2 caracteres")
            
            return self.repo.update_usuario(usuario_id, payload)
        except ValueError as e:
            raise Exception(f"Validação falhou: {str(e)}")
        except APIError as e:
            raise Exception(f"Erro ao atualizar usuário: {e.message}")
        except Exception as e:
            raise Exception(f"Erro inesperado ao atualizar usuário: {str(e)}")

    def deletar(self, usuario_id: int) -> None:
        try:
            if not isinstance(usuario_id, int) or usuario_id <= 0:
                raise ValueError("ID do usuário deve ser um número positivo")
            
            self.repo.delete_usuario(usuario_id)
        except ValueError as e:
            raise Exception(f"Validação falhou: {str(e)}")
        except APIError as e:
            raise Exception(f"Erro ao deletar usuário: {e.message}")
        except Exception as e:
            raise Exception(f"Erro inesperado ao deletar usuário: {str(e)}")