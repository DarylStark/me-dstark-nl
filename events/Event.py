#---------------------------------------------------------------------------------------------------
# Event.py
#
# Date: 2018-12-20
#
# Class for a Event
#---------------------------------------------------------------------------------------------------
class Event:
    """ Class to create 'Event' objects. A Event object contains all details about events """

    def __init__(self,
                 title = None,
                 url = None,
                 image = None,
                 date = None,
                 supportact = None,
                 venue = None,
                 stage = None,
                 price = None,
                 free = None,
                 soldout = None,
                 timedoorsopen = None,
                 timestart = None,
                 url_tickets = None,
                 uniq_value = None
    ):
        """ Sets default values """

        self.title = title
        self.url = url
        self.image = image
        self.date = date
        self.supportact = supportact
        self.venue = venue
        self.stage = stage
        self.price = price
        self.free = free
        self.soldout = soldout
        self.timedoorsopen = timedoorsopen
        self.timestart = timestart
        self.url_tickets = url_tickets
        self.uniq_value = uniq_value
#---------------------------------------------------------------------------------------------------