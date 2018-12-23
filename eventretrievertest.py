from database import *
import eventretriever
import datetime

a = Database()

tivolivredenburg = Venue()
tivolivredenburg.name = 'TivoliVredenburg'

paradiso = Venue()
paradiso.name = 'Paradiso'

a._session.add(tivolivredenburg)
a._session.add(paradiso)

a.commit()