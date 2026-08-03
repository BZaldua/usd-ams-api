class MockAsset:
    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = type


class MockTask:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class MockPublish:
    def __init__(self, asset, task, version, author):
        self.asset = asset
        self.task = task
        self.version = version
        self.author = author
