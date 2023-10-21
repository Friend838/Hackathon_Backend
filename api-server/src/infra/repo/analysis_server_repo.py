from src.infra.database.mongo_db import MongoDB

class AnalysisServerRepo:
    def __init__(self) -> None:
        self.db = MongoDB()
    
    def getData(self, collection, query):
        return self.db.find(collection, query)