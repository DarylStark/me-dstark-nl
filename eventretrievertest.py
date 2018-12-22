from database import *
import events
import datetime

a = events.EventRetrieverTivoliVredenburg()
e = a.retrieve_events()
a = Database()

for x in e:
    new = a.add_event(x)
    if new == False:
        print(f'FAIL!   {x.title} stond er al in')
        events = a._session.query(Event).filter(Event.unique == x.unique)
        existing_obj = events[0]

        # Object is already in DB, update the 'existing' object
        existing_obj.title = x.title
        existing_obj.changed = datetime.datetime.utcnow()
        existing_obj.title = x.title
        existing_obj.support = x.support
        existing_obj.venue = x.venue
        existing_obj.stage = x.stage
        existing_obj.date = x.date
        existing_obj.price = x.price
        existing_obj.free = x.free
        existing_obj.soldout = x.soldout
        existing_obj.doorsopen = x.doorsopen
        existing_obj.starttime = x.starttime
        existing_obj.url = x.url
        existing_obj.url_tickets = x.url_tickets
        existing_obj.image = x.image
        existing_obj.unique = x.unique

        # Commit the changes again, so the new information will be set
        a.commit()