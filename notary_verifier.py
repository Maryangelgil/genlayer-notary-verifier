# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

# Always put above lines as first in the contract file
from genlayer import *

class NotaryVerifier(gl.Contract):
    # Declaración de campos de estado persistentes compatibles con el motor
    documents_keys: str
    documents_vals: str

    def __init__(self):
        # Inicialización de diccionarios internos en memoria del contrato
        self.documents = {}
        self.metadata = {}

    @gl.public.write
    def register_document(self, doc_hash: str, doc_info: str) -> None:
        if not hasattr(self, 'documents'):
            self.documents = {}
        if not hasattr(self, 'metadata'):
            self.metadata = {}

        if doc_hash in self.documents:
            raise Exception("El documento ya está registrado en el sistema.")
        
        self.documents[doc_hash] = str(Env.msg_sender())
        self.metadata[doc_hash] = doc_info

    @gl.public.view
    def verify_document_authenticity(self, doc_hash: str, expected_owner: str) -> bool:
        if not hasattr(self, 'documents'):
            self.documents = {}

        if doc_hash not in self.documents:
            return False
            
        current_owner = self.documents[doc_hash]
        return str(current_owner) == str(expected_owner)
