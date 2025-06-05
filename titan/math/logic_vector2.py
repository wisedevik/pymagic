class LogicVector2:
    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.y = y

    def destruct(self) -> None:
        self.x = 0
        self.y = 0

    def add(self, vector: "LogicVector2") -> None:
        self.x += vector.x
        self.y += vector.y

    def multiply(self, vector: "LogicVector2") -> None:
        self.x *= vector.x
        self.y *= vector.y

    def get_distance_squared_to(self, x: int, y: int) -> int:
        distance = 0x7FFFFFFF

        x -= self.x

        if 0 <= (x + 46340) <= 92680:
            y -= self.y

            if 0 <= (y + 46340) <= 92680:
                distance_x = x * x
                distance_y = y * y

                if distance_y < (distance_x ^ 0x7FFFFFFF):
                    distance = distance_x + distance_y

        return distance