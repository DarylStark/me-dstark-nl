from database import *
import events
import datetime

a = events.EventRetrieverTivoliVredenburg()
e = a.retrieve_events()
a = Database()

for x in e:
    new = a.sync_event(x)