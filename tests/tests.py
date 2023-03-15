# from jsthon import JsthonDb

# db = JsthonDb('main.json')

# db.create_table('tvshows')
# db.create_table('films')
#
# db.choose_table('tvshows')
#
# id = db.add({'name': 'Breaking Bad', 'start': 2008})
# print(id)
# id = db.add({'name': 'Mr. Robot', 'start': 2015}, "1")
# print(id)

# added_values = db.add_many([{'name': 'Shameless', 'start': 2011}, {'name': 'The Boys', 'start': 2019}])
# print(added_values)
# added_values = db.add_many([{'name': 'Scrubs', 'start': 2001}, {'name': 'How I Met Your Mother', 'start': 2005}], ("0", "2"))
# print(added_values)

# all = db.take_all()
# print(all)

# element = db.take_by_id("1")
# print(element)

# def func1(data):
#     if data['start'] > 2010:
#         return True
#
#
# print(db.take_with_function(func1))

# updated_data = db.update_by_id("1", {'name': 'Better Call Saul'})
# print(updated_data)
# print(db.take_by_id("1"))

# def func2(data):
#     if data['name'] == 'Shameless':
#         return True
#
# updated_data = db.update_with_function(func2, {'name': '$hameless'})
# print(updated_data)

# deleted_data = db.delete_by_id("2")
# print(deleted_data)

# def func3(data):
#     if data['start'] < 2015:
#         return True
#
#
# deleted_data = db.delete_with_function(func3)
# print(deleted_data)

# db.add_new_key('broadcast', True)

# db.add_new_keys(['ratings', 'language'], ['good', 'english'])

# a = db.show_table()
# print(a)

# db.clear_table()
# db.clear_db()

# password = 'themostcommonpassword'
#
# db = JsthonDb('main.json')
#
# db.set_encryption(True)
# db.set_encryption_keys(password)
#
# db.create_table('tvshows')
# db.create_table('films')
#
# db.choose_table('tvshows')
#
# db.add({'name': 'Breaking Bad', 'start': 2008})
# db.set_encryption(False)
# db.add({'name': 'Mr. Robot', 'start': 2015}, "1")
# db.set_encryption(True)
#
# db.add_many([{'name': 'Shameless', 'start': 2011}, {'name': 'The Boys', 'start': 2019}])
# db.set_encryption(False)
# db.add_many([{'name': 'Scrubs', 'start': 2001}, {'name': 'How I Met Your Mother', 'start': 2005}], ("0", "2"))
# db.set_encryption(True)
#
# db.update_by_id("0", {"name": "Truckers"})
#
#
# def func(data):
#     if data['name'] == 'How I Met Your Mother':
#         return True
#
#
# db.update_with_function(func, {"name": "Supernatural"})

