# JsthonDb

## Contests
0. [How to download](#how-to-download)
1. [Requirements](#requirements) 
2. [Example json file](#example-json-file) 
3. [All methods usage examples](#all-methods-usage-examples)
    + [Creating empty JsthonDb named main.json](#creating-empty-jsthondb-named-main)
    + [create_table](#create_table)
    + [choose_table](#choose_table)
    + [add](#add)
    + [add_many](#add_many)
    + [take_all](#take_all)
    + [take_by_id](#take_by_id)
    + [take_with_function](#take_with_function)
    + [update_by_id](#update_by_id)
    + [update_with_function](#update_with_function)
    + [delete_by_id](#delete_by_id)
    + [delete_with_function](#delete_with_function)
    + [add_new_key](#add_new_key)
    + [add_new_keys](#add_new_keys)
    + [show_table](#show_table)
    + [clear_table](#clear_table)
    + [clear_db](#clear_db)
4. [Leave your feedback](#leave-your-feedback)

## How to download
```cli
git clone https://github.com/terribleMOTHMAN/JsthonDb
```

## Requirements 
+ `uuid` >= 1.30
+ `ujson` >= 5.6.0

## Example json file
```json

{
  "tvshows": {
    "keys": [

    ],
    "data": {

    }
  },
  "films": {
    "keys": [

    ],
    "data": {

    }
  }
}

```

## All methods usage examples
### Creating empty JsthonDb named main
```python
from jsthon import JsthonDb

db = JsthonDb('tvshows.json')
```
We created that empty file
```json
{

}
```
### create_table
Example usage (name field must be str)
```python
db.create_table('tvshows')
db.create_table('films')
```
```json
{
  "tvshows": {
    "keys": [

    ],
    "data": {

    }
  },
  "films": {
    "keys": [

    ],
    "data": {

    }
  }
}
```
You need to know that after using this method table that will be changed by the default methods will be films. Because it was created last
### choose_table
Example usage (table field must be str)
```python
db.choose_table('tvshows')
```
All the methods we will use will change the table 'tvshows' because we have chosen it
### add
Example usage (data field must be dict)
```python
id = db.add({'name': 'Breaking Bad', 'start': 2008})
print(id)
```
Output
```python
279161855443486914901758992112454064004
```
Also we can use our own id without generating it (id field must be string)
```python
id = db.add({'name': 'Mr. Robot', 'start': 2015}, "1")
print(id)
```
Output
```
1
```
### add_many
Example usage (data field  must be list with elements that are dictionaries)
```python
added_values = db.add_many([{'name': 'Shameless', 'start': 2011}, {'name': 'The Boys', 'start': 2019}])
print(added_values)
```
Output
```python
{'227987855254015167042504673548582084559': {'name': 'Shameless', 'start': 2011}, '334561175396969661937858438600623257934': {'name': 'The Boys', 'start': 2019}}
```
Also we can use our own ids without generating it (id field must be tuple with ids that are strings). Also, each id must correspond to a value in the data field
```python
added_values = db.add_many([{'name': 'Scrubs', 'start': 2001}, {'name': 'How I Met Your Mother', 'start': 2005}], ("0", "2"))
print(added_values)
```
Output
```python
{'0': {'name': 'Scrubs', 'start': 2001}, '2': {'name': 'How I Met Your Mother', 'start': 2005}}
```

### take_all
Example usage
```python
all = db.take_all()
print(all)
```
Output
```python
{'279161855443486914901758992112454064004': {'name': 'Breaking Bad', 'start': 2008}, '1': {'name': 'Mr. Robot', 'start': 2015}, '227987855254015167042504673548582084559': {'name': 'Shameless', 'start': 2011}, '334561175396969661937858438600623257934': {'name': 'The Boys', 'start': 2019}, '0': {'name': 'Scrubs', 'start': 2001}, '2': {'name': 'How I Met Your Mother', 'start': 2005}}
```

### take_by_id
Example usage
```python
element = db.take_by_id("1")
print(element)
```
Output
```python
{'name': 'Mr. Robot', 'start': 2015}
```

### take_with_function
Example usage
```python
def func(data):
    if data['start'] > 2010:
        return True

print(db.take_with_function(func))
```
Output
```python
{'1': {'name': 'Mr. Robot', 'start': 2015}, '227987855254015167042504673548582084559': {'name': 'Shameless', 'start': 2011}, '334561175396969661937858438600623257934': {'name': 'The Boys', 'start': 2019}}
```

### update_by_id
Example usage
```python
updated_data = db.update_by_id("1", {'name': 'Better Call Saul'})
print(updated_data)
print(db.take_by_id("1"))
```
Output
```python
{'name': 'Better Call Saul', 'start': 2015}
{'name': 'Better Call Saul', 'start': 2015}
```

### update_with_function
Example usage
```python
def func(data):
    if data['name'] == 'Shameless':
        return True

updated_data = db.update_with_function(func, {'name': '$hameless'})
print(updated_data)
```
Output
```python
['227987855254015167042504673548582084559']
```

### delete_by_id
Example usage
```python
deleted_data = db.delete_by_id("227987855254015167042504673548582084559")
print(deleted_data)
```
Output
```python
{'name': '$hameless', 'start': 2011}
```

### delete_with_function
Example usage
```python
def func(data):
    if data['start'] < 2015:
        return True


deleted_data = db.delete_with_function(func)
print(deleted_data)
```
Output
```python
[{'name': 'Scrubs', 'start': 2001}, {'name': 'How I Met Your Mother', 'start': 2005}, {'name': 'Breaking Bad', 'start': 2008}]
```

### add_new_key
Example usage
```python
db.add_new_key('broadcast', True)
print(db.take_all())
```
Output
```python
{'1': {'name': 'Better Call Saul', 'start': 2015, 'broadcast': True}, '334561175396969661937858438600623257934': {'name': 'The Boys', 'start': 2019, 'broadcast': True}}
```

### add_new_keys
Example usage
```python
db.add_new_keys(['ratings', 'language'], ['good', 'english'])
print(db.take_all())
```
Output
```python
{'1': {'name': 'Better Call Saul', 'start': 2015, 'broadcast': True, 'ratings': 'good', 'language': 'english'}, '334561175396969661937858438600623257934': {'name': 'The Boys', 'start': 2019, 'broadcast': True, 'ratings': 'good', 'language': 'english'}}
```

### show_table
Example usage
```python
a = db.show_table()
print(a)
```
Output
```python
[['name', 'start', 'broadcast', 'ratings', 'language'], ['Better Call Saul', 2015, True, 'good', 'english'], ['The Boys', 2019, True, 'good', 'english']]
```

### clear_table
Example usage
```python
db.clear_table()
```
Json file
```json
{
  "tvshows": {
    "keys": [

    ],
    "data": {

    }
  },
  "films": {
    "keys": [

    ],
    "data": {

    }
  }
}
```

### clear_db
Example usage
```python
db.clear_db()
```
Json file
```json
{

}
```

## Leave your feedback
I need your review! It will be pleasure for me ^_^

[Survey](https://ru.surveymonkey.com/r/LDR7NHY)
