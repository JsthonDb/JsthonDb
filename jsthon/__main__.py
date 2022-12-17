from pathlib import Path
import uuid
from filelock import FileLock
from jsthon.__errors__ import UnknownKeyError, IdWasNotFound, FunctionIsNotCallable, IdIsAlreadyUsed, WrongIdsListWasGiven, WrongFileName, NotUniqueNameOfTable

try:
    import ujson
    UJSON = True
except:
    import json
    UJSON = False


class JsthonDb:
    def __init__(self, filename):
        if not(isinstance(filename, str)):
            raise WrongFileName(f'filename must be "str" not {type(filename)}')
        if filename[-5:] != '.json':
            raise WrongFileName('filename must end with .json')
        self.filename = filename
        self.table = None
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

    def generate_db_file(self):
        if not Path(self.filename).is_file():
            self.save_file({})

    def generate_id(self):
        return str(int(uuid.uuid4()))

    def create_table(self, name):
        db = self.load_file()
        if not(isinstance(name, str)):
            raise TypeError(f'name must be "str" not {type(name)}')
        if name in db.keys():
            raise NotUniqueNameOfTable(f'{name} is already represented in the db')
        db[name] = {'keys': [], 'data': {}}
        self.save_file(db)
        self.table = name

    def choose_table(self, table):
        db = self.load_file()
        if not(table in db.keys()):
            raise UnknownKeyError(f'{table} is not name of any table in db')
        self.table = table

    def add(self, data, id=None):
        db = self.load_file()
        if not(isinstance(data, dict)):
            raise TypeError(f'data must be "dict" not {type(data)}')
        if id is not None:
            if not(isinstance(id, str)):
                raise TypeError(f'id must be "str" not {type(id)}')
            elif id in db[self.table]['data']:
                raise IdIsAlreadyUsed('id is already used in db (please change the id argument or leave it empty for automatic filling)')
        else:
            id = self.generate_id()
        keys = db[self.table]['keys']
        if len(keys) == 0:
            db[self.table]['keys'] = list(data.keys())
        else:
            if sorted(keys) != sorted(data.keys()):
                raise UnknownKeyError(f'unrecognized / missed key(s) {set(keys) ^ set(data.keys())}')
        if not isinstance(db[self.table]['data'], dict):
            raise TypeError('data in db must be "dict"')
        db[self.table]['data'][id] = data
        self.save_file(db)
        return id

    def add_many(self, data, id=None):
        if not(isinstance(id, tuple)) and not(isinstance(id, type(None))):
            raise TypeError(f'id must be "list" not {type(id)}')
        if not(isinstance(data, list)):
            raise TypeError(f'data must be "list" not {type(data)}')
        if not(all(isinstance(i, dict) for i in data)):
            raise TypeError('all the new data in the data list must "dict"')
        db = self.load_file()
        keys = db[self.table]['keys']
        _return = {}
        if not(isinstance(keys, list)):
            raise TypeError(f'keys must be "list" and not {type(keys)}')
        for d in data:
            if not(sorted(keys) == sorted(d.keys())):
                raise UnknownKeyError(f'unrecognized / missed key(s) {set(keys) ^ set(d.keys())}')
        if not(isinstance(db[self.table]['data'], dict)):
            raise TypeError(f'data key in the db must be "dict" not {type(data)}')
        if id is None:
            for d in data:
                id = self.generate_id()
                db[self.table]['data'][id] = d
                _return[id] = d
        else:
            i = 0
            for d in data:
                if not (isinstance(id[i], str)):
                    raise TypeError(f'id must be "str" not {type(id)}')
                elif id.count(id[i]) > 1:
                    raise WrongIdsListWasGiven('it seems similar ids were given in list')
                elif id[i] in db[self.table]['data'].keys():
                    raise IdIsAlreadyUsed(
                        'id is already used in db (please change the id argument or leave it empty for automatic filling)')
                db[self.table]['data'][id[i]] = d
                _return[id[i]] = d
                i += 1
        self.save_file(db)
        return _return

    def take_all(self):
        data = self.load_file()[self.table]['data']
        if isinstance(data, dict):
            return data
        else:
            raise TypeError(f'data key must be "dict" not {type(data)}')

    def take_by_id(self, id):
        if not(isinstance(id, str)):
            raise TypeError(f'id must be "str" not {type(id)}')
        data = self.load_file()[self.table]['data']
        if isinstance(data, dict):
            if id in data:
                return data[id]
            else:
                raise IdWasNotFound(f'{id} was not found')
        else:
            raise TypeError(f'data key in db must be "dict"')

    def take_with_function(self, function):
        if not(callable(function)):
            raise FunctionIsNotCallable(f'function must be callable and not {type(function)}')
        new_data = {}
        data = self.load_file()[self.table]['data']
        if isinstance(data, dict):
            for id, values in data.items():
                if isinstance(values, dict):
                    if function(values):
                        new_data[id] = values
        else:
            return TypeError(f'data key in db must be "dict" not {type(data)}')
        return new_data if new_data != {} else None

    def update_by_id(self, id, new_data):
        if not(isinstance(new_data, dict)):
            raise TypeError(f'new_data must be "dict" not {type(new_data)}')
        data = self.load_file()
        keys = data[self.table]['keys']
        if isinstance(keys, list):
            if not(all(i in keys for i in new_data)):
                raise UnknownKeyError(f'unrecognised key(s) {[i for i in new_data if i not in keys]}')
        if not isinstance(data[self.table]['data'], dict):
            raise TypeError(f'data in db must be dict not {type(data[self.table]["data"])}')
        if id not in data[self.table]['data']:
            raise IdWasNotFound(f'{id} was not found')
        data[self.table]['data'][id] = {**data[self.table]['data'][id], **new_data}
        self.save_file(data=data)
        return data[self.table]['data'][id]

    def update_with_function(self, function, new_data):
        if not(callable(function)):
            raise FunctionIsNotCallable('function must be callable and not {type(query)}')
        if not(isinstance(new_data, dict)):
            raise TypeError(f'new data must be dict')
        updated_keys = []
        db = self.load_file()
        keys = db[self.table]['keys']
        if isinstance(keys, list):
            if not all(i in keys for i in new_data):
                raise UnknownKeyError(f'unrecognised / missing key(s) {[i for i in new_data if i not in keys]}')
        else:
            raise TypeError(f'keys key in db must be "list" not {type(keys)}')
        if not(isinstance(db[self.table]['data'], dict)):
            raise TypeError(f'data key in db must be type "dict" not {type(db[self.table]["data"])}')
        for key, value in db[self.table]['data'].items():
            if function(value):
                db[self.table]['data'][key] = {**db[self.table]['data'][key], **new_data}
                updated_keys.append(key)
        self.save_file(data=db)
        return updated_keys

    def delete_by_id(self, id):
        data = self.load_file()
        if not isinstance(data[self.table]['data'], dict):
            raise TypeError(f'data key in db must be dict not {type(data[self.table]["data"])}')
        if id not in data[self.table]['data']:
            raise IdWasNotFound(f'{id} was not found')
        ret = self.take_by_id(id)
        del data[self.table]['data'][id]
        self.save_file(data)
        return ret

    def delete_with_function(self, function):
        ret = []
        ids_to_delete = []
        if not callable(function):
            raise FunctionIsNotCallable(f'function must be callable and not {type(function)}')
        data = self.load_file()
        if not isinstance(data[self.table]['data'], dict):
            raise TypeError(f'data key in db must be type dict not {type(data[self.table]["data"])}')
        for id, value in data[self.table]['data'].items():
            if function(value):
                ids_to_delete.append(id)
        for id in ids_to_delete:
            ret.append(self.take_by_id(id))
            del data[self.table]['data'][id]

        self.save_file(data)
        return ret

    def add_new_key(self, key, value=None):
        if not isinstance(key, str):
            raise TypeError(f'key field must bе string not {type(key)}')
        db = self.load_file()
        if isinstance(db[self.table]['keys'], list):
            db[self.table]['keys'].append(key)
        else:
            raise TypeError(f'keys key in db must be "list" not {type(db[self.table]["keys"])}')
        if isinstance(db[self.table]['data'], dict):
            for d in db[self.table]['data'].values():
                d[key] = value
        else:
            raise TypeError(f'data key in db must be "dict" not {type(db[self.table]["data"])}')
        self.save_file(db)

    def add_new_keys(self, keys, values=None):
        if not isinstance(keys, list):
            raise TypeError(f'keys field must be list not {type(keys)}')
        if not isinstance(values, list) or values is None:
            raise TypeError(f'values field must be one of the (list, None) types {type(values)}')
        if all(not isinstance(i, str) for i in keys):
            raise TypeError(f'keys in list must bе string types')
        db = self.load_file()
        if isinstance(db[self.table]['keys'], list):
            for i in keys:
                db[self.table]['keys'].append(i)
        else:
            raise TypeError(f'keys key in db must be "list" not {type(db[self.table]["keys"])}')
        if isinstance(db[self.table]['data'], dict):
            if values is None:
                for d in db[self.table]['data'].values():
                    for i in keys:
                        d[i] = None
            elif isinstance(values, list):
                for d in db[self.table]['data'].values():
                    for i in range(len(keys)):
                        d[keys[i]] = values[i]
        else:
            raise TypeError(f'data key in db must be "dict" not {type(db[self.table]["data"])}')
        self.save_file(db)

    def clear_table(self):
        data = self.load_file()
        data[self.table]['data'] = {}
        data[self.table]['keys'] = []
        self.save_file(data)

    def clear_db(self):
        data = {}
        self.save_file(data)

    def show_table(self):
        ret = []
        db = self.load_file()
        ret.append(db[self.table]['keys'])
        for i in db[self.table]['data']:
            ret.append(list(db[self.table]['data'][i].values()))
        return ret