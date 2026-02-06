from abc import ABC, abstractmethod
from auth.domain.entities.user import User

class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, user: User) -> User:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, id: str) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, id: str) -> User:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_username(self, username: str) -> User:
        raise NotImplementedError