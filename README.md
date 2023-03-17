# JsthonDb
![logo](https://user-images.githubusercontent.com/65505901/208244282-1815b59f-3d2e-4c96-a963-e778c630d9b4.png)

## Contests
0. [How to download](#how-to-download)
1. [Requirements](#requirements) 
2. [Example json file](#example-json-file) 
3. [All vanila methods usage examples](#all-vanila-methods-usage-examples)
    + [Creating empty JsthonDb](#creating-empty-jsthondb)
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
4. [Encryption of incoming data](#encryption-of-incoming-data)
    + [A little bit about the encryption method](#a-little-bit-about-the-encryption-method)
    + [How to use](#how-to-use)
6. [Errors](#errors)
    + [UnknownKeyError](#unknownkeyerror)
    + [FunctionIsNotCallable](#functionisnotcallable)
    + [WrongIdsListWasGiven](#wrongidslistwasgiven)
    + [IdWasNotFound](#idwasnotfound)
    + [IdIsAlreadyUsed](#idisalreadyused)
    + [NotUniqueNameOfTable](#notuniquenameoftable)
    + [WrongFileName](#wrongfilename)
7. [Leave your feedback](#leave-your-feedback)

## How to download
```cli
git clone https://github.com/terribleMOTHMAN/JsthonDb
cd JsthonDb
python setup.py install
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

## All vanila methods usage examples
### Creating empty JsthonDb
```python
from jsthon import JsthonDb

db = JsthonDb('main.json')
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
```python
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
## Encryption of incoming data
### A little bit about the encryption method
The Russian algorithm "Kuznechik" (in English "Grasshopper") is used for data encryption 
"Kuznechik" is a symmetric block cipher algorithm with a block size of 128 bits and a key length of 256 bits that uses an SP-net to generate round-robin keys.

### How to use
Of course at first create db
Then do next steps:
1) via method set_encryption() set True or False (if True all data that will be added to the db will be encrypted)
2) via method set_encryption_keys() set our password for encryption
Then we create password and via
```python
db = JsthonDb('main.json')

password = 'themostcommonpassword'
db.set_encryption(True)
keys = db.set_encryption_keys(password)
print(keys)
```
Output
```python
[list of keys]
```
Then we can use it like that
```python
db.add({'name': 'Breaking Bad', 'start': 2008})
db.set_encryption(False)
db.add({'name': 'Mr. Robot', 'start': 2015}, "1")
db.set_encryption(True)

db.add_many([{'name': 'Shameless', 'start': 2011}, {'name': 'The Boys', 'start': 2019}])
db.set_encryption(False)
db.add_many([{'name': 'Scrubs', 'start': 2001}, {'name': 'How I Met Your Mother', 'start': 2005}], ("0", "2"))
db.set_encryption(True)

db.update_by_id("0", {"name": "Truckers"})


def func(data):
    if data['name'] == 'How I Met Your Mother':
        return True


db.update_with_function(func, {"name": "Supernatural"})
```
Or you can use encrypt_by_key() to encrypt selected columns(keys)
```python
db.encrypt_by_key('name')
```

Also, you can decrypt data via method decrypt
```python
data = 'some information'
decrypted_data = db.decrypt(data)
```

## Errors
### UnknownKeyError
It's raised when key was unrecognised or missed

### FunctionIsNotCallable
It's raised when function was given to the method is not callable or is not function

### WrongIdsListWasGiven
It's raised when idswas  given to the method have wrong type

### IdWasNotFound
It's raised when id was not found in the table

### IdIsAlreadyUsed
It's raised when id was given to the methon is not unique in the table

### NotUniqueNameOfTable
It's raised when name of table that was given is not unique

### WrongFileName
It's raised when wrong filename was given to a class

## Leave your feedback
I need your review! It will be pleasure for me ^_^

[Survey](https://ru.surveymonkey.com/r/LDR7NHY)
