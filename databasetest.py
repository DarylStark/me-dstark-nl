
import database

db = database.Database()

a = database.Event()
a.title = 'test' 

print(a.id)
db.add_event(a)
print(a.id)

a.title = 'test2'

db.commit()

print(a.title)