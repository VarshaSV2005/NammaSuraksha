class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

class Incident:
    def __init__(self, title, description, location, priority):
        self.title = title
        self.description = description
        self.location = location
        self.priority = priority

class Vehicle:
    def __init__(self, type, location, status):
        self.type = type
        self.location = location
        self.status = status
