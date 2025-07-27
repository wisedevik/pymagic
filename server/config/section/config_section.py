from typing import Dict, Any, Generic, T


class ConfigSection(Generic[T]):
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def __getattr__(self, name: str) -> Any:
        value = self.data[name]
        if isinstance(value, dict):
            return ConfigSection(value)
        return value

    def as_dict(self) -> Dict[str, Any]:
        return self.data
