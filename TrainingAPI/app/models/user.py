import time


class User:
    def __init__(self, _id='', _username='', _password=''):
        self._id = _id
        self.username = _username
        self.password = _password

    def to_dict(self):
        return {
            '_id': self._id,
            'username': self.username,
            'password': self.password
        }

    def from_dict(self, json_dict: dict):
        self._id = json_dict.get('_id', self._id)
        self.username = json_dict.get('username', '')
        self.password = json_dict.get('password', '')
        return self


user_json_schema = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['username', 'password']
}
