from jsthon import JsthonDb

db = JsthonDb('tvshows.json')
print(db.take_all())
print()

id = db.add({'name': 'Breaking Bad', 'start': 2008})
print(id)
print(db.take_by_id(id))
print()

added_values = db.add_many([{'name': 'Shameless', 'start': 2011}, {'name': 'The Boys', 'start': 2019}])
print(added_values)
print(db.take_all())
print()


def func(data):
    if data['start'] > 2010:
        return True


print(db.take_with_function(func))
print()

updated_data = db.update_by_id(id, {'name': 'Better Call Saul', 'start': [2015]})
print(updated_data)
print(db.take_by_id(id))
print()

db.delete_by_id(id)
print(db.take_all())
print()

db.add_new_key('broadcast', True)
print(db.take_all())
print()

db.add_new_keys(['ratings', 'language'], ['good', 'english'])
print(db.take_all())
print()

a = db.show()
print(a)

print(db.convert_to_csv())
for row in a:
    print(row)

db.clear()
print(db.take_all())

db.open_csv('tvshows.csv')
