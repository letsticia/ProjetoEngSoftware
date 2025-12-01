from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from src.db.supabase_class import SupabaseClient

class UserRepository:
    def __init__(self):
        self.client = SupabaseClient().client

    def _timestamp(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def create_usuario(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        payload["criado_em"] = payload["atualizado_em"] = self._timestamp()
        response = self.client.table("usuarios").insert(payload).execute()
        return response.data[0]

    def list_usuarios(self) -> List[Dict[str, Any]]:
        response = self.client.table("usuarios").select("*").order("criado_em", desc=True).execute()
        return response.data

    def get_usuario(self, usuario_id: int) -> Optional[Dict[str, Any]]:
        response = self.client.table("usuarios").select("*").eq("id_usuario", usuario_id).execute()
        return response.data[0] if response.data else None

    def update_usuario(self, usuario_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        payload["atualizado_em"] = self._timestamp()
        response = self.client.table("usuarios").update(payload).eq("id_usuario", usuario_id).execute()
        return response.data[0]

    def delete_usuario(self, usuario_id: int) -> None:
        self.client.table("usuarios").delete().eq("id_usuario", usuario_id).execute()