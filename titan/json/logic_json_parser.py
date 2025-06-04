from typing import List


class LogicJSONParser:
    @staticmethod
    def create_json_string(root, ensure_capacity: int = 20) -> str:
        builder = []
        root.write_to_string(builder)
        return "".join(builder)

    @staticmethod
    def write_string(value: str, builder: List[str]) -> None:
        builder.append('"')
        if value:
            for char in value:
                if char <= "\r" and char >= "\b":
                    if char == "\b":
                        builder.append("\\b")
                    elif char == "\t":
                        builder.append("\\t")
                    elif char == "\n":
                        builder.append("\\n")
                    elif char == "\f":
                        builder.append("\\f")
                    elif char == "\r":
                        builder.append("\\r")
                    else:
                        builder.append(char)
                else:
                    if char == '"':
                        builder.append('\\"')
                    elif char == "/":
                        builder.append("\\/")
                    elif char == "\\":
                        builder.append("\\\\")
                    else:
                        builder.append(char)
        builder.append('"')

    @staticmethod
    def parse_error(error: str) -> None:
        print(f"JSON Parse error: {error}")

    @staticmethod
    def parse(json: str):
        return LogicJSONParser.parse_value(CharStream(json))

    @staticmethod
    def parse_value(stream: "CharStream"):
        stream.skip_whitespace()
        char_value = stream.next_char()
        node = None

        if char_value == "{":
            node = LogicJSONParser.parse_object(stream)
        elif char_value == "[":
            node = LogicJSONParser.parse_array(stream)
        elif char_value == "n":
            node = LogicJSONParser.parse_null(stream)
        elif char_value in ("f", "t"):
            node = LogicJSONParser.parse_boolean(stream)
        elif char_value == '"':
            node = LogicJSONParser.parse_string(stream)
        elif char_value == "-":
            node = LogicJSONParser.parse_number(stream)
        elif char_value.isdigit():
            node = LogicJSONParser.parse_number(stream)
        else:
            LogicJSONParser.parse_error(f"Not of any recognized value: {char_value}")

        return node

    @staticmethod
    def parse_array(json: str):
        return LogicJSONParser.parse_array(CharStream(json))

    @staticmethod
    def _parse_array(stream: "CharStream"):
        stream.skip_whitespace()
        if stream.read() != "[":
            LogicJSONParser.parse_error("Not an array")
            return None

        from .logic_json_array import LogicJSONArray

        json_array = LogicJSONArray()
        stream.skip_whitespace()
        next_char = stream.next_char()

        if next_char:
            if next_char == "]":
                stream.read()
                return json_array

            while True:
                node = LogicJSONParser.parse_value(stream)
                if node:
                    json_array.add(node)
                    stream.skip_whitespace()
                    next_char = stream.read()

                    if next_char != ",":
                        if next_char == "]":
                            return json_array
                        break
                else:
                    break

        LogicJSONParser.parse_error("Not an array")
        return None

    @staticmethod
    def parse_object(json: str):
        return LogicJSONParser._parse_object(CharStream(json))

    @staticmethod
    def _parse_object(stream: "CharStream"):
        stream.skip_whitespace()
        if stream.read() != "{":
            LogicJSONParser.parse_error("Not an object")
            return None

        from . import LogicJSONObject

        json_object = LogicJSONObject()
        stream.skip_whitespace()
        next_char = stream.next_char()

        if next_char:
            if next_char == "}":
                stream.read()
                return json_object

            while True:
                key = LogicJSONParser.parse_string(stream)
                if key:
                    stream.skip_whitespace()
                    next_char = stream.read()

                    if next_char != ":":
                        break

                    node = LogicJSONParser.parse_value(stream)
                    if node:
                        json_object.put(key.get_string_value(), node)
                        stream.skip_whitespace()
                        next_char = stream.read()

                        if next_char != ",":
                            if next_char == "}":
                                return json_object
                            break
                    else:
                        break
                else:
                    break

        LogicJSONParser.parse_error("Not an object")
        return None

    @staticmethod
    def parse_string(stream: "CharStream"):
        stream.skip_whitespace()
        if stream.read() != '"':
            LogicJSONParser.parse_error("Not a string")
            return None

        builder = []
        while True:
            next_char = stream.read()
            if not next_char:
                LogicJSONParser.parse_error("Not a string")
                return None

            if next_char != '"':
                if next_char == "\\":
                    next_char = stream.read()
                    if next_char == "n":
                        next_char = "\n"
                    elif next_char == "r":
                        next_char = "\r"
                    elif next_char == "t":
                        next_char = "\t"
                    elif next_char == "u":
                        hex_str = stream.read(4)
                        if not hex_str:
                            LogicJSONParser.parse_error("Not a string")
                            return None
                        next_char = chr(int(hex_str, 16))
                    elif next_char == "b":
                        next_char = "\b"
                    elif next_char == "f":
                        next_char = "\f"
                    elif not next_char:
                        LogicJSONParser.parse_error("Not a string")
                        return None
                builder.append(next_char)
            else:
                break

        return LogicJSONString("".join(builder))

    @staticmethod
    def parse_boolean(stream: "CharStream"):
        stream.skip_whitespace()
        next_char = stream.read()

        if next_char == "f":
            if (
                stream.read() == "a"
                and stream.read() == "l"
                and stream.read() == "s"
                and stream.read() == "e"
            ):
                return LogicJSONBoolean(False)
        elif next_char == "t":
            if stream.read() == "r" and stream.read() == "u" and stream.read() == "e":
                return LogicJSONBoolean(True)

        LogicJSONParser.parse_error("Not a boolean")
        return None

    @staticmethod
    def parse_null(stream: "CharStream"):
        stream.skip_whitespace()
        next_char = stream.read()

        if next_char == "n":
            if stream.read() == "u" and stream.read() == "l" and stream.read() == "l":
                from .logic_json_null import LogicJSONNull

                return LogicJSONNull()

        LogicJSONParser.parse_error("Not a null")
        return None

    @staticmethod
    def parse_number(stream: "CharStream"):
        stream.skip_whitespace()
        next_char = stream.next_char()
        multiplier = 1

        if next_char == "-":
            multiplier = -1
            next_char = stream.read()

        if next_char != ",":
            value = 0
            while (next_char := stream.read()).isdigit():
                value = int(next_char) + 10 * value
                next_char = stream.next_char()
                if not next_char.isdigit():
                    break

            if next_char in ("e", "E", "."):
                LogicJSONParser.parse_error("JSON floats not supported")
                return None

            from .logic_json_number import LogicJSONNumber

            return LogicJSONNumber(value * multiplier)

        LogicJSONParser.parse_error("Not a number")
        return None


class CharStream:
    def __init__(self, string: str):
        self.m_string = string
        self.m_offset = 0

    def read(self) -> str:
        if self.m_offset >= len(self.m_string):
            return "\0"
        char = self.m_string[self.m_offset]
        self.m_offset += 1
        return char

    def read(self, length: int) -> str:
        if self.m_offset + length > len(self.m_string):
            return None
        substr = self.m_string[self.m_offset : self.m_offset + length]
        self.m_offset += length
        return substr

    def next_char(self) -> str:
        if self.m_offset >= len(self.m_string):
            return "\0"
        return self.m_string[self.m_offset]

    def skip_whitespace(self) -> None:
        while (
            self.m_offset < len(self.m_string) and self.m_string[self.m_offset] <= " "
        ):
            self.m_offset += 1
