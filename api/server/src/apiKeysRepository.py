import redis

class ApiKeysRepository():
    def __init__(self):
        self.connection = redis.StrictRedis(host='redis', port=6379, db=0)

    def getOriginalApiKey(self, publicKey):
        return self.connection.get('user_' + publicKey)

    def setOriginalApiKey(self, apiKey, publicKey):
        return self.connection.set('user_' + apiKey, publicKey)
