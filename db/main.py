from pathlib import Path
import uuid
from errors import UnknownKeyError, IdWasNotFound, QueryIsNotCallable

try:
    import ujson
    UJSON = True
except:
    import json
    UJSON = False


class JsthonDb:
    def __init__(self, filename):
        self.filename = filename
        self.memory = {'keys': [], 'data': {}}
        self.generate_db_file()

    def load_file(self):
        with open(self.filename, encoding='utf-8', mode='r') as f:
            if UJSON:
                return ujson.load(f)
            else:
                return json.load(f)

    def save_file(self, data):
        with open(self.filename, encoding='utf-8', mode='w') as f:
            if UJSON:
                ujson.dump(data, f)
            else:
                json.dump(data, f)
        return None

    def generate_db_file(self):
        if not Path(self.filename).is_file():
            self.save_file({'keys': [], 'data': {}})

    def generate_id(self):
        return str(int(uuid.uuid4()))[:14]

    def add(self, data):
        if not(isinstance(data, dict)):
            raise TypeError(f'data must be "dict" and not {type(data)}')

        db = self.load_file()
        keys = db['keys']
        if len(keys) == 0:
            db['keys'] = sorted(list(data.keys()))
        else:
            if sorted(keys) != sorted(data.keys()):
                raise UnknownKeyError(f'Urecognized / missed key(s) {set(keys) ^ set(data.keys())}')
        _id = str(self.generate_id())
        if not isinstance(db['data'], dict):
            raise TypeError('data in db must be "dict"')
        db['data'][_id] = data
        self.save_file(db)
        return _id

    def add_many(self, data):
        if not(isinstance(data, list)):
            raise TypeError(f'data must be "list" not {type(data)}')
        if not(all(isinstance(i, dict) for i in data)):
            raise TypeError('all the new data in the data list must "dict"')
        db = self.load_file()
        keys = db['keys']
        _return = {}
        if not keys:
            db['keys'] = sorted(list(data[0].keys()))
            keys = db['keys']
        if not(isinstance(keys, list)):
            raise TypeError(f'keys must be "list" and not {type(keys)}')
        for d in data:
            if not(sorted(keys) == sorted(d.keys())):
                raise UnknownKeyError(f'unrecognized / missed key(s) {set(keys) ^ set(d.keys())}')
        if not(isinstance(db['data'], dict)):
            raise TypeError(f'data key in the db must be "dict" not {type(data)}')
        for d in data:
            id = str(self.generate_id())
            db['data'][id] = d
            _return[id] = d
        self.save_file(db)
        return _return

    def take_all(self):
        data = self.load_file()['data']
        if isinstance(data, dict):
            return data
        else:
            raise TypeError(f'data key must be "dict" not {type(data)}')

    def take_by_id(self, id):
        if not(isinstance(id, str)):
            raise TypeError(f'id must be "str" not {type(id)}')
        data = self.load_file()['data']
        if isinstance(data, dict):
            if id in data:
                return data[id]
            else:
                raise IdWasNotFound(f'{id} was not found')
        else:
            raise TypeError(f'data key in db must be "dict"')

    def take_by_query(self, query):
        if not(callable(query)):
            raise QueryIsNotCallable(f'query must be callable and not {type(query)}')
        new_data = {}
        data = self.load_file()['data']
        if isinstance(data, dict):
            for id, values in data.items():
                if isinstance(values, dict):
                    if query(values):
                        new_data[id] = values
        else:
            return TypeError(f'data key in db must be "dict" not {type(data)}')
        return new_data if new_data != {} else None

    def update_by_id(self, id, new_data):
        if not(isinstance(new_data, dict)):
            raise TypeError(f'new_data must be "dict" not {type(new_data)}')
        data = self.load_file()
        keys = data['keys']
        if isinstance(keys, list):
            if not(all(i in keys for i in new_data)):
                raise UnknownKeyError(f'unrecognised key(s) {[i for i in new_data if i not in keys]}')
        if isinstance(data['data'], dict):
            raise TypeError(f'data in db must be dict not {type(data["data"])}')
        if id not in data['data']:
            raise IdWasNotFound(f'{id} was not found')
        data['data'][id] = {**data['data'][id], **new_data}
        self.save_file(data=data)
        return data['data'][id]

    def update_by_query(self, query, new_data):
        if not(callable(query)):
            raise QueryIsNotCallable(f'query must be callable and not {type(query)}')
        if not(isinstance(new_data, dict)):
            raise TypeError(f'new data must be dict')
        updated_keys = []
        db = self.load_file()
        keys = db['keys']
        if isinstance(keys, list):
            if not all(i in keys for i in new_data):
                raise UnknownKeyError(f'unrecognised / missing key(s) {[i for i in new_data if i not in keys]}')
        else:
            raise TypeError(f'keys key in db must be "list" not {type(keys)}')
        if not(isinstance(db['data'], dict)):
            raise TypeError(f'data key in db must be type "dict" not {type(db["data"])}')
        for key, value in db['data'].items():
            if query(value):
                db['data'][key] = {**db['data'][key], **new_data}
                updated_keys.append(key)
        self.save_file(data=db)
        return updated_keys

    def delete_by_id(self, id):
        data = self.load_file()
        if not isinstance(data['data'], dict):
            raise TypeError(f'data key in db must be dict not {type(data["data"])}')
        if id not in data['data']:
            raise IdWasNotFound(f'{id} was not found')
        del data['data'][id]

        self.save_file(data)

    def delete_by_query(self, query):
        if not callable(query):
            raise QueryIsNotCallable(f'query must be callable and not {type(query)}')
        data = self.load_file()
        if not isinstance(data['data'], dict):
            raise TypeError(f'data key in db must be type dict not {type(data["data"])}')
        ids_to_delete = []
        for id, value in data['data'].items():
            if query(value):
                ids_to_delete.append(id)
        for id in ids_to_delete:
            del data['data'][id]

        self.save_file(data)
        return ids_to_delete

    def clear(self):
        data = self.load_file()
        if not isinstance(data['data'], dict):
            raise TypeError(f'data key in db must be dict not {type(data["data"])}')
        if not isinstance(data['keys'], list):
            raise TypeError(f'keys key in db must be list not {type(data["keys"])}')
        data['data'] = {}
        data['keys'] = []
        self.save_file(data)

    def add_new_key(self, key, value=None):
        if value is not None:
            if not isinstance(type(value), (list, str, int, bool, dict)):
                raise TypeError(f'value field must be of any of types(list, int, str, bool, dict) but not {type(value)}')
        data = self.load_file()
        if isinstance(data['keys'], list):
            data['keys'].append(key)
            data['keys'].sort()
        else:
            raise TypeError(f'keys key in db must be "list" not {type(data["keys"])}')
        if isinstance(data['data'], dict):
            for d in data['data'].values():
                d[key] = value
        else:
            raise TypeError(f'data key in db must be "dict" not {type(data["data"])}')
        self.save_file(data)
