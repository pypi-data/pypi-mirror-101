# esqlite
esqlite means 'easy sqlite', is a sqlite3 wrapper.
method 'execute' for execute any SQL and return result set.
method 'batch_save' for batch insert dict list data. Table will be created if the table not exists.

## install
```cmd
pip install esqlite
```

## example
```python
import esqlite

db = esqlite.DB('test.db')
data = [{'id': 1, 'name': 'Bob'}, {'id': 2, 'name': 'Lena'}]
# batch save, default init table with dict keys
db.batch_save('user', data, cleanup=True)
# insert
db.execute('insert into user(id, name) values (?,?)', [3, 'C++'])
print(db.execute('select * from user'))
# update
db.execute('update user set name=? where id=?', ['Python', 3])
print(db.execute('select * from user'))
# delete
db.execute('delete from user where id=?', [3])
# find
print(db.execute('select * from user order by id desc'))

```
file `test.db` will be created and console will print:
```text
[{'id': 1, 'name': 'Bob'}, {'id': 2, 'name': 'Lena'}, {'id': 3, 'name': 'C++'}]
[{'id': 1, 'name': 'Bob'}, {'id': 2, 'name': 'Lena'}, {'id': 3, 'name': 'Python'}]
[{'id': 2, 'name': 'Lena'}, {'id': 1, 'name': 'Bob'}]
```