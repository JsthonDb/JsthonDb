from jsthon import JsthonDb

db = JsthonDb('tvshows.json')

print(db.take_all())

id = db.add({'name': 'Breaking Bad', 'start': 2008})
print(id)
id = db.add({'name': 'Mr. Robot', 'start': 2015}, "1")
print(id)

added_values = db.add_many([{'name': 'Shameless', 'start': 2011}, {'name': 'The Boys', 'start': 2019}])
print(added_values)
added_values = db.add_many([{'name': 'Scrubs', 'start': 2001}, {'name': 'How I Met Your Mother', 'start': 2005}], ("0", "2"))
print(added_values)

all = db.take_all()
print(all)

element = db.take_by_id("1")
print(element)

def func1(data):
    if data['start'] > 2010:
        return True


print(db.take_with_function(func1))

updated_data = db.update_by_id("1", {'name': 'Better Call Saul'})
print(updated_data)
print(db.take_by_id("1"))

def func2(data):
    if data['name'] == 'Shameless':
        return True

updated_data = db.update_with_function(func2, {'name': '$hameless'})
print(updated_data)

deleted_data = db.delete_by_id("227987855254015167042504673548582084559")
print(deleted_data)

def func3(data):
    if data['start'] < 2015:
        return True


deleted_data = db.delete_with_function(func3)
print(deleted_data)

db.add_new_key('broadcast', True)
print(db.take_all())

db.add_new_keys(['ratings', 'language'], ['good', 'english'])
print(db.take_all())

a = db.show()
print(a)


print(db.convert_to_csv())

db.clear()

db.open_csv('tvshows.csv')
