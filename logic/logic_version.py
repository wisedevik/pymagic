from server.config import Configuration


class LogicVersion:
    content_version = Configuration.game.content_version
    major_version = Configuration.game.major_version
    build = Configuration.game.build
