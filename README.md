# JsthonDb

## Contests
0. [How to download](#how-to-download)
1. [Requirements](#requirements) 
2. [Example json file](#example-json-file) 
3. [All methods usage examples](#all-methods-usage-examples)
    + [Creating empty JsthonDb](#creating-empty-jsthondb)
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
    + [show](#show)
    + [clear](#clear)
    + [convert_to_csv](#convert_to_csv)
    + [open_csv](#open_csv)

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
  "keys": [
    "name",
    "start",
    "broadcast",
    "ratings",
    "language"
  ],
  "data": {
    "111427139670082062530275901337557814850": {
      "name": "Shameless",
      "start": "2011",
      "broadcast": "True",
      "ratings": "good",
      "language": "english"
    },
    "256970725050456543664090450342998289596": {
      "name": "The Boys",
      "start": "2019",
      "broadcast": "True",
      "ratings": "good",
      "language": "english"
    }
  }
}

```

## All methods usage examples
### Creating empty JsthonDb
```python
from jsthon import JsthonDb

db = JsthonDb('tvshows.json')
```
We created that empty file
```json
{
  "keys": [

  ],
  "data": {

  }
}
```
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
Example usage (data field  must be list with with elements that are dictionaries)
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

### show
Example usage
```python
a = db.show()
print(a)
```
Output
```python
[['name', 'start', 'broadcast', 'ratings', 'language'], ['Better Call Saul', 2015, True, 'good', 'english'], ['The Boys', 2019, True, 'good', 'english']]
```

### clear
Example usage
```python
db.clear()
```
Json file
```json
{
  "keys": [

  ],
  "data": {

  }
}
```

### convert_to_csv
Example usage
```python
print(db.convert_to_csv())
```
Output
```python
[['name', 'start', 'broadcast', 'ratings', 'language'], ['Better Call Saul', 2015, True, 'good', 'english'], ['The Boys', 2019, True, 'good', 'english']]
```
![image](https://user-images.githubusercontent.com/65505901/207400635-d40ac1de-4319-4266-b72e-47c6437610de.png)

### open_csv
Before opening csv file method clear was used

Example usage
```python
db.open_csv('tvshows.csv')
```
Output
```json
{
  "keys": [
    "name",
    "start",
    "broadcast",
    "ratings",
    "language"
  ],
  "data": {
    "142577528007816699812409659394714608584": {
      "name": "Better Call Saul",
      "start": "2015",
      "broadcast": "True",
      "ratings": "good",
      "language": "english"
    },
    "187051371904602478372091759624266292597": {
      "name": "The Boys",
      "start": "2019",
      "broadcast": "True",
      "ratings": "good",
      "language": "english"
    }
  }
}
```
