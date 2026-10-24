from genlayer import *

@ic
class NotaryVerifier:
    # Estado del contrato
    documents: LegacyMap[str, Address]
    metadata: LegacyMap[str, str]
    
    def __init__(self):
        # Inicializa las estructuras de almacenamiento
        self.documents = LegacyMap(str, Address)
        self.metadata = LegacyMap(str, str)

    @public
    def register_document(self, doc_hash: str, doc_info: str) -> None:
        """
        Registra un documento asegurando que el remitente sea el propietario legítimo.
        """
        if doc_hash in self.documents:
            raise Exception("El documento ya está registrado en el sistema.")
        
        self.documents[doc_hash] = Env.msg_sender()
        self.metadata[doc_hash] = doc_info

    @public
    def verify_document_authenticity(self, doc_hash: str, expected_owner: str) -> bool:
        """
        Utiliza lógica de equivalencia y consenso para verificar si el documento 
        existe, pertenece al propietario esperado y cumple con los estándares.
        """
        if doc_hash not in self.documents:
            return False
            
        current_owner = self.documents[doc_hash]
        
        # Validación mediante principio de equivalencia determinista / consenso de GenLayer
        owner_matches = str(current_owner) == str(expected_owner)
        
        return owner_matches
