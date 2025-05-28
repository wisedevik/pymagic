import importlib
import pathlib

message_registry = {}

def piranha_message(message_type: int):
    def decorator(cls):
        message_registry[message_type] = cls
        return cls
    return decorator

def auto_import_messages():
    base_path = pathlib.Path(__file__).parent  # logic/messages
    root_path = base_path.parent.parent  # logic

    for py_file in base_path.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
        rel_path = py_file.relative_to(root_path).with_suffix('')
        module_path = ".".join(rel_path.parts)
        importlib.import_module(module_path)
