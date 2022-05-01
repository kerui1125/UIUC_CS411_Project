import json


class secretloader:
    def __init__(self, databaseType):
        #f = open('dbsecret.json')
        secret_file_path = '/Users/juntaoyu/Documents/GitHub/UIUC_CS411_Project/uiuc_411_project/db/dbsecret.json'
        f = open(secret_file_path)
        self.secretData = json.load(f)
        self.loadSecretPerDBType(databaseType)

    def loadSecretPerDBType(self, databaseType):
        isDBTypeSupported = databaseType in self.secretData
        self.host = self.secretData[databaseType]['host'] if isDBTypeSupported else ''
        self.user = self.secretData[databaseType]['user'] if isDBTypeSupported else ''
        self.password = self.secretData[databaseType]['password'] if isDBTypeSupported else ''
        self.db = self.secretData[databaseType]['db'] if isDBTypeSupported else ''
        self.port = self.secretData[databaseType]['port'] if isDBTypeSupported else ''
        self.charset = self.secretData[databaseType]['charset'] if isDBTypeSupported else ''
