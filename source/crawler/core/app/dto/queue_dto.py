class ParserTaskDto(object):
    def __init__(self, authenticated_user, content):
        self.username = authenticated_user
        self.content = content