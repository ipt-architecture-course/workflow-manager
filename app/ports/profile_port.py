from abc import ABC, abstractmethod

class ProfilePort(ABC):

    @abstractmethod
    def get_profile(self, user_id: str) -> dict:
        pass

    @abstractmethod
    def update_profile(self, user_id: str, profile_data: dict) -> bool:
        pass

    @abstractmethod
    def delete_profile(self, user_id: str) -> bool:
        pass