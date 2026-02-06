from abc import ABC, abstractmethod

class IdGeneratorService(ABC):
    """Service abstrak untuk menghasilkan ID unik di berbagai entity."""

    @abstractmethod
    def generate_id(self) -> str:
        """Menghasilkan ID unik secara konsisten."""
        pass


class PasswordService(ABC):
    """Service abstrak untuk hashing dan verifikasi password."""

    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Mengubah password menjadi hash yang aman."""
        pass

    @abstractmethod
    def check_password(self, password: str, hashed_password: str) -> bool:
        """Memverifikasi kecocokan password dengan hash."""
        pass
