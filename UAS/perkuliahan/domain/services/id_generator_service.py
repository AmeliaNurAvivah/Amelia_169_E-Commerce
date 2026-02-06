from abc import ABC, abstractmethod

class IdGeneratorService(ABC):
    

    @abstractmethod
    def generate_id(self) -> str:
        pass
