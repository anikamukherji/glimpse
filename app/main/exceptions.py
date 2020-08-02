class UserNotFound(Exception):
    error_code = 404

    def __init__(self, message):
        self.message = message


class ChatNotFound(Exception):
    error_code = 404

    def __init__(self, message):
        self.message = message


class ChatRoomNotFound(Exception):
    error_code = 404

    def __init__(self, message):
        self.message = message
