/*------------------------------------------------------------------------------
- Object with all the days
------------------------------------------------------------------------------*/
days = [
  'sunday', 'monday', 'tuesday', 'wednesday',
  'thursday', 'friday', 'saturday'
]
/*------------------------------------------------------------------------------
- Object with all the months
------------------------------------------------------------------------------*/
months = [
  { 'short': 'jan', 'long': 'january' },
  { 'short': 'feb', 'long': 'february' },
  { 'short': 'mar', 'long': 'march' },
  { 'short': 'apr', 'long': 'april' },
  { 'short': 'may', 'long': 'may' },
  { 'short': 'jun', 'long': 'june' },
  { 'short': 'jul', 'long': 'july' },
  { 'short': 'aug', 'long': 'august' },
  { 'short': 'sep', 'long': 'september' },
  { 'short': 'oct', 'long': 'october' },
  { 'short': 'nov', 'long': 'november' },
  { 'short': 'dec', 'long': 'december' }
]
/*------------------------------------------------------------------------------
- The object with all the pages
------------------------------------------------------------------------------*/
pages = {
  'feed': {
    'menuitemid': 'feed',
    'url': 'feed',
    'title': 'Feed',
    'method': 'pageFeed'
  },
  'planning': {
    'menuitemid': 'planning',
    'url': 'planning',
    'title': 'Planning',
    'method': 'pagePlanning'
  },
  'concerts': {
    'menuitemid': 'concerts',
    'url': 'concerts',
    'title': 'Concerts',
    'method': 'pageConcerts'
  }
}
/*------------------------------------------------------------------------------
- The object for the template cache
------------------------------------------------------------------------------*/
tpl_cache = {}
/*------------------------------------------------------------------------------
- Main JavaScript file for the GUI
------------------------------------------------------------------------------*/
function GUI() {
  this.loading = false;
  this.done = 0;
  this.donecounter = 0;
}
/*----------------------------------------------------------------------------*/
// Method that is fired when a item in the menu is clicked
GUI.prototype.clickMenuItem = function(menuitemid) {
  // Hide the menu, but only if the current layout is optimized for a small
  // screen.
  if ($('.mdl-layout').hasClass('is-small-screen'))
  {
    // is-small-screen
    var layout = document.querySelector('.mdl-js-layout');
    if (layout) { layout.MaterialLayout.toggleDrawer(); }
  }

  // Change the page to the new selected page
  this.changePage(menuitemid);
}
/*----------------------------------------------------------------------------*/
GUI.prototype.changePage = function(menuitemid = '', checkloading = true) {
  // Check if the page is loading
  if (this.loading && checkloading) {
    // Give an error that the page is still loading
    this.showNotification('Page is still loading');
    return;
  }

  // Show the progress bar
  this.startLoading();

  // Set the current item to nothing
  current_item = null;

  // Find the correct page by using the menuitem id
  if (menuitemid != '') {
    $.each(pages, function(key, value) {
      if (value['menuitemid'] == menuitemid) {
        current_item = value
      }
    });
  } else {
    // Get the first part of the URL
    currenturl = window.location.pathname.split('/')[1];

    // Find the correct page by using the URL
    $.each(pages, function(key, value) {
      if (value['url'] == currenturl) {
        current_item = value
      }
    });
  }

  // If we found the page, proceed
  if (current_item != null) {
    // Remove the 'active' attribute from all menuitems with this attribute
    $('.me-navigation__link_active').removeClass('me-navigation__link_active');

    // Set the 'active' attribute to the right menuitem
    $('#' + current_item['menuitemid']).addClass('me-navigation__link_active');

    // If this came from the menu, we have to update the history of the user
    if (menuitemid != '') {
      // update history
      window.history.pushState({ 'current_item': current_item }, current_item['title'], '/' + current_item['url'])
    }

    // Next, we update the title
    document.title = 'Daryl Stark - ' + current_item['title'];
    $('#main_title').html(current_item['title']);

    // Find the method for the current page and start it
    fn = this[current_item['method']];
    if (typeof fn === 'function') {
      // Remove the scroll handler
      $('#scroller').off('scroll');

      // Start the page
      this[current_item['method']]();
    } else {
      // Give a error
      this.stopLoading();
      this.showNotification('JavaScript error.', 'Reload', function() { location.reload(); } );
    }
  } else {
    if (menuitemid == '') {
      // Redirect to the mainpage
      this.changePage('feed', false);
      return;
    } else {
      // Give a error
      this.stopLoading();
      this.showNotification('JavaScript error.', 'Reload', function() { location.reload(); } );
    }
  }
}
/*----------------------------------------------------------------------------*/
// Method to display a loading bar
GUI.prototype.startLoading = function() {
  // Set the 'loading' var to true
  this.loading = true;

  // Show the loading bar
  $('#ui-progress-empty').hide();
  $('#ui-progress').show();
}
/*----------------------------------------------------------------------------*/
// Method to remove the loading bar
GUI.prototype.stopLoading = function() {
  // Set the 'loading' var to false
  this.loading = false;
  // Remove the loading bar
  $('#ui-progress').hide();
  $('#ui-progress-empty').show();
}
/*----------------------------------------------------------------------------*/
// Method to load a template from the cache, or to fill the cache if it isn't in
// the cache yet. After the template is loaded, the callback method is called
GUI.prototype.getTemplate = function(template, success = undefined, error = undefined) {
  // Check if the template is already in the cache
  if (tpl_cache[template] == undefined) {
    // If it isn't, use an API call to load it
    this.apiCall('templates.Get', { 'template': template }, function(data, status, request) {
        // Got the template, fill the cache
        template_text = data['data']['data'][0];
        tpl_cache[template] = template_text;

        // Call the callback method
        if (success) { success(); }
      }, function(request, status, http_error) {
        // The template couldn't be loaded
        if (error) { error(); }
      }, function() {}
    );
  } else {
    if (success) { success(); }
  }
}
/*----------------------------------------------------------------------------*/
// Method to upgrade all elements for MDL
GUI.prototype.upgradeElement = function(htmlelement) {
  // Upgrade all parent elements
  htmlelement.each(function(index, element) {
    try { componentHandler.upgradeElement(element); } catch(err) {}
  });

  // Upgrade all child elements
  htmlelement.find('*').each(function(index, element) {
    try { componentHandler.upgradeElement(element); } catch(err) {}
  });
}
/*----------------------------------------------------------------------------*/
// Method to call a API
GUI.prototype.apiCall = function(api, parameters = {}, success = undefined, error = undefined, complete = undefined) {
  // Check the parameters and create a URL component
  pars = [];
  uricomponent = '';

  // Loop through the given parameters
  for (key in parameters) {
    newvar = key + '=' + parameters[key];
    pars.push(newvar);
  }

  // If we have parameters, create a uri component
  if (pars.length > 0) {
    uricomponent = '?' + pars.join('&');
  }

  // Create the URL
  url = '/api/' + api + uricomponent;

  // Do the request
  $.ajax({
    url: url,
    success: function(data, status, request) {
      // Got a response, check the error code
      if (data['error']['code'] == 0) {
        // API was success. Start the 'success' callback
        if (success) { success(data, status, request); }
      } else {
        // The API gave an error. Start the 'error' callback
        if (error) { error(); }
      }
    },
    error: function(request, status, error) {
      // The template couldn't be loaded
      if (error) { error(); }
    },
    complete: function() {
      // Done with the API call, start the 'complete' callback
      if (complete) { complete(); }
    }
  });
}
/*----------------------------------------------------------------------------*/
// Method to preload templates
GUI.prototype.preloadTemplates = function(templates, success, failed) {
  // A variable for the callback methods below
  t = this;

  // Reset the counters
  this.done = templates.length;
  this.donecounter = 0;
  this.success = true;

  // Walk through the templates
  $.each(templates, function(index, template) {
    // Download the template
    t.getTemplate(template, function() {
        // Template loaded, increase the counter and run the callback when we
        // are done
        t.donecounter += 1;
        if (t.donecounter == t.done) {
            if (t.success) { success(); } else { failed(); }
        }
    }, function() {
        // Template not loaded, increase the counter and run the callback when
        // we are done
        t.donecounter += 1;
        t.success = false;
        if (t.donecounter == t.done) {
            if (t.success) { success(); } else { failed(); }
        }
    });
  });
}
/*----------------------------------------------------------------------------*/
// Method to show an error on screen
GUI.prototype.showNotification = function(error, actionText = undefined, actionHandler = undefined)
{
  // Define the snackbar
  var toast = document.querySelector('.mdl-js-snackbar');
  var data = {
    message: error,
    timeout: 2000
  };

  // If a action is set, add the action
  if (actionText)
  {
    data['actionHandler'] = actionHandler;
    data['actionText'] = actionText;
  }

  // Show it again
  toast.MaterialSnackbar.showSnackbar(data);
}
/*----------------------------------------------------------------------------*/
// Method to update the count of new feed items in the menu
GUI.prototype.updateFeedCount = function() {
  // A variable for the callback methods below
  t = this;

  // Get the amount of new items in the feed
  this.apiCall('feed.Get', { 'limit': 0 }, function(data) {
    // Check how many items are in the queue
    unreadcount = data['data']['length'];

    // Update the badge
    t.updateBadge(unreadcount);
  });
}
/*----------------------------------------------------------------------------*/
// Method to update the badge every minute
GUI.prototype.setTimerUpdate = function() {
  // A variable for the callback methods below
  t = this;

  // Set the timer
  setTimeout(function() {
    t.updateFeedCount();
    t.setTimerUpdate();
  }, 60000);
}
/*----------------------------------------------------------------------------*/
// Method to update the badge in the menu
GUI.prototype.updateBadge = function(newvalue) {
  if (newvalue > 0) {
    // Add the badge to the menuitem
    $('#feed_icon').addClass('mdl-badge');
    $('#feed_icon').attr('data-badge', newvalue);
  } else {
    // Remove the badge
    $('#feed_icon').removeClass('mdl-badge');
  }
}
/*----------------------------------------------------------------------------*/
// Method to format a UTC datetime in nice format
GUI.prototype.getDateTime = function(datetime, format) {
  // Create a datetime object
  datetime = new Date(datetime);

  // Get the variables
  year = datetime.getFullYear();
  month = datetime.getMonth() + 1;
  date = datetime.getDate();
  hours = datetime.getHours();
  minutes = datetime.getMinutes();
  seconds = datetime.getSeconds();

  // Check if all values are correct
  if (isNaN(year) || isNaN(month) || isNaN(date) || isNaN(hours) || isNaN(minutes) || isNaN(seconds)) {
    return '';
  }

  // Set the leading zeros to empty values
  monthleadingzeros = '';
  dateleadingzeros = '';
  hoursleadingzeros = '';
  minutesleadingzeros = '';
  secondsleadingzeros = '';

  // Check if we need to add leading zeros
  if (month < 10) { monthleadingzeros = '0'; }
  if (date < 10) { dateleadingzeros = '0'; }
  if (hours < 10) { hoursleadingzeros = '0'; }
  if (minutes < 10) { minutesleadingzeros = '0'; }
  if (seconds < 10) { secondsleadingzeros = '0'; }

  // Create the string
  format = format.replace(/yyyy/g, year);
  format = format.replace(/mm/g, monthleadingzeros + month);
  format = format.replace(/dd/g, dateleadingzeros + date);
  format = format.replace(/hh/g, hoursleadingzeros + hours);
  format = format.replace(/ii/g, minutesleadingzeros + minutes);
  format = format.replace(/ss/g, secondsleadingzeros + seconds);

  // Return the string
  return(format);
}
/*----------------------------------------------------------------------------*/
// The method to show the feed
GUI.prototype.pageFeed = function() {
  // A variable for the callback methods below
  t = this;

  // Update the badge
  this.updateFeedCount();

  // Retrieve the parts of the page URLs
  currenturl = window.location.pathname.split('/');

  // Set the feeds settings and properties
  this.feed = {
    'items_on_screen': 0,
    'current_page': 0,
    'limit': 15,
    'loading_for_page': 1,
    'max_page': 0,
    'to_top_button': false,
    'empty': false,
    'showarchive': false
  };

  // Check if we need to show the archive
  if (currenturl.indexOf('archive') > -1) {
    this.feed['showarchive'] = true;
  }

  // Preload the templates
  this.preloadTemplates([ 'feed', 'feed_item_newevent', 'feed_item_newevent_archive', 'feed_empty' ], function () {
    // The feed for the template is loaded. Clear the content div
    $('#content').html('');

    // Convert the template to a DOM object
    feed = $($.parseHTML(tpl_cache['feed']));

    // Upgrade the element for MDL
    t.upgradeElement(feed);

    // Set the switch to the correct state
    if (t.feed['showarchive']) {
      feed.find('#label-archive')[0].MaterialSwitch.on();
    }

    // Attach the new element to the content div
    $('#content').append(feed);

    // Attach a handler to the switch for the archive
    $('#switch-archive').change(function() {
      // Check the new position of the switch
      newstate_archive = $('#switch-archive').prop('checked');

      // Show the loading bar
      t.startLoading();

      // Check if the switch is set to 'archive' or to 'not archive'

      // Reset the feed settings
      // TODO: do this better.. maybe a default method or something
      t.feed = {
        'items_on_screen': 0,
        'current_page': 0,
        'limit': 15,
        'loading_for_page': 1,
        'max_page': 0,
        'to_top_button': false,
        'empty': false
      }

      // If the switch is set to 'show archive', show the archive. Otherwise,
      // don't show the archive but the new items.
      t.feed['showarchive'] = newstate_archive;

      // Set the new feed settings
      t.feed['current_page'] = 1;

      // Remove the current elements (after the filter)
      $('.last-filter').nextAll().remove();

      // TODO: Update the URL
      if ($('#switch-archive').prop('checked')) {
        window.history.pushState({ 'current_item': 'feed' }, 'Feed', '/feed/archive');
      } else {
        window.history.pushState({ 'current_item': 'feed' }, 'Feed', '/feed');
      }

      // Add the new elements
      t.pageFeedLoaditems(t.feed['limit'], t.feed['current_page']);
    });

    // Attach a handler to the 'go up' button
    $('.me-upbutton').click(function() {
      $('#scroller').animate({
        scrollTop: 0
      });
    });

    // Add a handler to retrieve the next page when scrolling
    $('#scroller').on('scroll', function() {
      // If we scroll beneauth the top of the page, show a button to go to the
      // top of the page. Otherwise, remove it
      if ($(this).scrollTop() > 0 && t.feed['to_top_button'] == false) {
        // Show the button
        t.feed['to_top_button'] = true;
        $('.me-upbutton').fadeIn(400);
      } else if ($(this).scrollTop() == 0 && t.feed['to_top_button'] == true) {
        // Hide the button
        t.feed['to_top_button'] = false;
        $('.me-upbutton').fadeOut(200);
      }

      // When we are 100px from the bottom, start loading the next
      if($(this).scrollTop() + $(this).innerHeight() + 100 >= $(this)[0].scrollHeight) {
        // Only when we're not already loading that page
        if (t.feed['loading_for_page'] != (t.feed['current_page'] + 1)) {
          // Check if we didn't reach the max page yet
          if (t.feed['max_page'] >= (t.feed['current_page'] + 1)) {
            // Show the loading bar
            t.startLoading();

            // Set the page we are loading for
            t.feed['loading_for_page'] = t.feed['current_page'] + 1;

            // Load the new page
            t.pageFeedLoaditems(t.feed['limit'], t.feed['loading_for_page'], function() {
              // And set the new current page
              t.feed['current_page'] = t.feed['loading_for_page'];
            });
          }
        }
      }
    });

    // Get the first page of the feed
    t.pageFeedLoaditems(t.feed['limit'], t.feed['current_page'] + 1, function() {
      t.feed['current_page'] = 1;
    });
  }, function() {
    // The templates couldn't be loaded
    // Give an error to the user
    t.showNotification('Could not load the needed templates');
    t.stopLoading();
  });
}
/*----------------------------------------------------------------------------*/
// Method to dismiss a speficic feed item, or undimiss it
GUI.prototype.pageFeedItemDismiss = function(itemid, undismiss = false) {
  // A variable for the callback methods below
  t = this;

  // Check if the page is loading
  if (this.loading) {
    // Give an error that the page is still loading
    this.showNotification('Page is still loading');
    return;
  }

  // Show the loading bar
  this.startLoading();

  // Check which API call to use
  api = 'feed.Dismiss';
  if (undismiss) {
    api = 'feed.SetNew';
  }

  this.apiCall(api, { 'id': itemid }, function(data, status, request) {
    // Reset the counter
    t.done = $('.me-js-card_' + itemid).length;
    t.donecounter = 0;

    // First, fade out the card by changing it's opacity. Then slide it up, so
    // the feed slides up
    $('.me-js-card_inner_' + itemid).animate({ opacity: 0 }, 200);
    $('.me-js-card_' + itemid).slideUp(200, function() {
      // Increase the counter
      t.donecounter += 1;

      // When we're done, do the rest
      if (t.donecounter == t.done) {
        // Subtract it from the number of items on the page
        t.feed['items_on_screen'] -= 1;

        // Add one new item to the queue
        if (t.feed['max_page'] > (t.feed['current_page'])) {
          t.pageFeedLoaditems(1, (t.feed['items_on_screen'] + 1));
        }

        if (t.feed['items_on_screen'] == 0) {
          t.pageFeedEmpty();
        }

        // Update the badge with the amount of items
        t.updateFeedCount();

        // Stop the loading bar
        t.stopLoading();
      }
    });
  }, function(request, status, error) {
    // The item couldn't be dismissed
    t.showNotification('Could not dismiss this item');
    t.stopLoading();
  });
}
/*----------------------------------------------------------------------------*/
// Method to set the tracked state for a event in the feed correct
GUI.prototype.pageFeedItemEventTogglesSetTracked = function(eventid, tracked, item = $) {
  if (tracked == 1) {
    // Event is tracked
    item.find('#label-tracked-' + eventid)[0].MaterialSwitch.on();
    item.find('#label-going-' + eventid)[0].MaterialSwitch.off();
  } else if (tracked == 2) {
    // Event is going
    item.find('#label-tracked-' + eventid)[0].MaterialSwitch.on();
    item.find('#label-going-' + eventid)[0].MaterialSwitch.on();
  } else {
    // Event is going
    item.find('#label-tracked-' + eventid)[0].MaterialSwitch.off();
    item.find('#label-going-' + eventid)[0].MaterialSwitch.off();
  }
}
/*----------------------------------------------------------------------------*/
// Method to set the tracked state for a event
GUI.prototype.pageFeedItemEventSetTracked = function(eventid, tracked) {
  // A variable for the callback methods below
  t = this;

  // Check if the page is loading
  if (this.loading) {
    // Give an error that the page is still loading
    this.showNotification('Page is still loading');
    return;
  }

  // Pick the right API
  if (tracked == 1)      { api = 'events.SetTracked'; }
  else if (tracked == 2) { api = 'events.SetGoing'; }
  else                   { api = 'events.SetNotTracked'; }

  // Perform the API
  this.startLoading();
  this.apiCall(api, { 'id': eventid }, function() {
    // Everything went fine, stop processing
    t.stopLoading();
  }, function() {
    // When something went wrong, give an error
    t.showNotification('Couldn\'t change the item');

    // Then, set the toggles to not tracked
    t.pageFeedItemEventTogglesSetTracked(eventid, 0);

    // And stop loading
    t.stopLoading();
  })
}
/*----------------------------------------------------------------------------*/
// Method that happends when a tracking toggle is changed in a event feed item
GUI.prototype.pageFeedItemEventTrackedToggle = function(eventid, trackedtoggle = false) {
  // Check the new state
  newstate_tracked = $('#switch-tracked-' + eventid).prop('checked');
  newstate_going = $('#switch-going-' + eventid).prop('checked');

  // Perform the correct action for the toggles
  if (newstate_tracked == false && newstate_going == false) { newtracked = 0; }
  else if (newstate_tracked == true && newstate_going == false) { newtracked = 1; }
  else if (newstate_tracked == true && newstate_going == true) { newtracked = 2; }
  else if (newstate_tracked == false && newstate_going == true) { if (trackedtoggle) { newtracked = 0; } else { newtracked = 2; } }

  // Set the toggles correct
  t.pageFeedItemEventTogglesSetTracked(eventid, newtracked);

  // Perform the API
  t.pageFeedItemEventSetTracked(eventid, newtracked);
}
/*----------------------------------------------------------------------------*/
// Method to return a feed item for events
// TODO: Remove this
GUI.prototype.pageFeedItemEvent = function(feeditem) {
  // Get the correct template from the cache
  if (this.feed['showarchive']) {
    item = tpl_cache['feed_item_newevent_archive'];
  } else {
    item = tpl_cache['feed_item_newevent'];
  }

  // Get the correct type
  if (feeditem['itemtype'] == 1) { type = 'New event'; }
  if (feeditem['itemtype'] == 3) { type = 'Support act for event changed'; }
  if (feeditem['itemtype'] == 2) { type = 'Tracked event changed'; }

  // Get the datetime for the feeditem in UTC
  itemdate = feeditem['date']
  date = itemdate.split('T')[0]
  time = itemdate.split('T')[1].substring(0, 8)
  feed_datetime_formatted = this.getDateTime(date + ' ' + time + ' UTC', 'yyyy-mm-dd hh:ii:ss');

  // Get the datetime for when the item was changed
  itemdate = feeditem['changedate']
  date = itemdate.split('T')[0]
  time = itemdate.split('T')[1].substring(0, 8)
  dismiss_datetime_formatted = this.getDateTime(date + ' ' + time + ' UTC', 'yyyy-mm-dd hh:ii:ss');

  // Get the date for the event
  date = new Date(feeditem['event']['date']);
  date_formatted = date.getDate() + ' ' + months[date.getMonth()]['short'] + ' ' + date.getFullYear();

  // Get the weekday for the event
  day_formatted = days[date.getDay()];

  // Get the doors start time
  starttime = feeditem['event']['starttime'];
  if (starttime != null) {
    starttime_formatted = starttime.split(':')[0] + ':' + starttime.split(':')[1];
  } else {
    starttime_formatted = 'unknown time'
  }

  // Get the price
  if (feeditem['event']['free'] == false) {
    if (feeditem['event']['price'] > 0) {
      price_formatted = '&euro; ' + parseFloat(feeditem['event']['price'] / 100).toFixed(2);
    } else {
      price_formatted = 'unknown price';
    }
  } else {
    price_formatted = 'free';
  }

  // Check if this is sold out
  if (feeditem['event']['soldout'] == false) {
    soldout_formatted = 'not sold oud';
  } else {
    soldout_formatted = 'sold out';
  }

  // Replace the variables in the template item
  item = item.replace(/{{ feed_type }}/g, type);
  item = item.replace(/{{ feed_datetime }}/g, feed_datetime_formatted);
  item = item.replace(/{{ feed_dismissdatetime }}/g, dismiss_datetime_formatted);

  item = item.replace(/{{ title }}/g, feeditem['event']['title']);
  item = item.replace(/{{ id }}/g, feeditem['event']['id']);
  item = item.replace(/{{ event_id }}/g, feeditem['event']['id']);
  item = item.replace(/{{ support }}/g, feeditem['event']['support']);
  item = item.replace(/{{ venue }}/g, feeditem['event']['venue']);
  item = item.replace(/{{ stage }}/g, feeditem['event']['stage']);
  item = item.replace(/{{ day }}/g, day_formatted);
  item = item.replace(/{{ date }}/g, date_formatted);
  item = item.replace(/{{ starttime }}/g, starttime_formatted);
  item = item.replace(/{{ price }}/g, price_formatted);
  item = item.replace(/{{ soldout }}/g, soldout_formatted);

  // Convert the item to a DOM object
  newitem = $($.parseHTML(item));

  // Set the URL for the website
  newitem.find('#button-website').attr('href', feeditem['event']['url']);

  // Set the URL for tickets, if there is one
  if (feeditem['event']['url_tickets']) {
    newitem.find('#button-buy').attr('href', feeditem['event']['url_tickets']);
  } else {
    newitem.find('#button-buy').hide();
  }

  // If there is an image, change the background of the title
  if (feeditem['event']['image']) {
    newitem.find('.mdl-card__title').css('background-image', 'url(' + feeditem['event']['image'] + ')');
  }

  // Upgrade the element for MDL
  t.upgradeElement(newitem);

  // Set the 'tracked' and 'going' state
  t.pageFeedItemEventTogglesSetTracked(feeditem['event']['id'], feeditem['event']['tracked'], newitem);

  // Add a onclick element for the dismiss button
  newitem.find('.dismiss').click(function() {
    t.pageFeedItemDismiss(feeditem['id']);
  });

  // Add a onclick element for the undismiss button
  newitem.find('.undismiss').click(function() {
    t.pageFeedItemDismiss(feeditem['event']['id'], true);
  });

  // Add a onclick element for the 'tracked' toggle
  newitem.find('#switch-tracked-' + feeditem['event']['id']).change(function() {
    t.pageFeedItemEventTrackedToggle(feeditem['event']['id'], true);
  });

  // Add a onclick element for the 'going' toggle
  newitem.find('#switch-going-' + feeditem['event']['id']).change(function() {
    t.pageFeedItemEventTrackedToggle(feeditem['event']['id'], false);
  });

  return newitem;
}
/*----------------------------------------------------------------------------*/
// Method to load the feed items from the API and put them in the queue
GUI.prototype.pageFeedLoaditems = function(limit, page, complete) {
  // A variable for the callback methods below
  t = this;

  // Start the loading
  t.startLoading();

  // Options for the API call
  apioptions = { 'limit': limit, 'page': page }

  // Check if we need to load the archive or the 'normal' feed
  if (this.feed['showarchive'] == true) {
    apioptions['dismissed'] = '1';
    apioptions['sort'] = 'dismissed';
  }

  // Start the API call
  this.apiCall('feed.Get', apioptions, function(data, status, request) {
    // Set the 'done' to the number of elements, so we can calculate
    // we are done and remove the progressbar
    t.done = (data['data']['data_len']);
    t.donecounter = 0;

    // Set the max page to the new item, but only if we try to retrieve a
    // new page. Otherwise, don't.
    if (limit == t.feed['limit']) {
      t.feed['max_page'] = data['data']['maxpage'];
    }

    if (data['data']['data_len'] > 0) {
      // Walk through the items and add them to the feed
      $.each(data['data']['data'], function(index, feeditem) {
        // Get the type for the item
        type = feeditem['itemtype'];

        // If the item is a event (new, support changed or tracked changed)
        if (type == 1 || type == 2 || type == 3) {
          newitem = t.pageFeedItemEvent(feeditem);

          // Append the item to the feed
          $('#feedItems').append(newitem);
          t.feed['items_on_screen'] += 1;
        }

        // Increase the donecounter
        t.donecounter += 1;

        // If we are done, remove the progressbar
        if (t.donecounter == t.done) {
          t.stopLoading();
          t.donecounter = 0;
          t.done = 0;

          // Call the callback
          if (complete) { complete(); }
        }
      });
    } else {
      if (t.feed['items_on_screen'] == 0) {
        // Nothing on the screen; show an 'empty' screen
        t.pageFeedEmpty();
        t.stopLoading();
      }
    }
  }, function() {
    // The data couldn't be loaded
    // Give an error to the user
    t.showNotification('Could not load the feed items');
    t.stopLoading();

    // Set the counters to zero
    t.donecounter = 0;
    t.done = 0;
  });
}
/*----------------------------------------------------------------------------*/
// Method to show an 'empty' page whene there are no feed items
GUI.prototype.pageFeedEmpty = function() {
  if (this.feed['empty'] == false) {
    this.feed['empty'] = true;
    // Convert the template to a DOM object
    feed_empty = $($.parseHTML(tpl_cache['feed_empty']));

    // Upgrade the element for MDL
    t.upgradeElement(feed_empty);

    // Attach the new element to the content div
    $('#feedItems').append(feed_empty);
  }
}
/*----------------------------------------------------------------------------*/
// The method to show the planning
GUI.prototype.pagePlanning = function() {
  // Check if we got a date in the URL. If we don't, it should be today's date
  today = new Date();

  currenturl = window.location.pathname.split('/');
  if (currenturl[2]) {
    date = this.getDateTime(currenturl[2] + ' 00:00:00 UTC', 'yyyy-mm-dd')
  } else {
    date = this.getDateTime(today, 'yyyy-mm-dd');
  }

  if (date != '') {
    // Start the real method for this date
    this.pagePlanningStart(date);
  } else {
    // TODO: Give error (date incorrect)
    // Stop the loading
    this.stopLoading();
  }
}
/*----------------------------------------------------------------------------*/
// The real method to show the planning
GUI.prototype.pagePlanningStart = function(date, seturl = false) {
  // A variable for the callback methods below
  t = this;

  // Set the current date
  this.planning = {
    'date': date,
    'date_obj': new Date(date + ' 00:00:00 UTC')
  }

  // Preload the templates
  this.preloadTemplates([ 'planning', 'planning_event' ], function () {
    // See if we need to change the URL
    if (seturl) {
      window.history.pushState({ 'current_item': 'planning' }, 'Planning', '/planning/' + date);
    }

    // The feed for the template is loaded. Clear the content div
    $('#content').html('');

    // Get the template
    planning = tpl_cache['planning'];

    // Replace the variables
    planning = planning.replace(/{{ weekday }}/g, days[t.planning['date_obj'].getDay()]);
    planning = planning.replace(/{{ month }}/g, months[t.planning['date_obj'].getMonth()]['long']);
    planning = planning.replace(/{{ day }}/g, t.planning['date_obj'].getDate());
    planning = planning.replace(/{{ year }}/g, t.planning['date_obj'].getFullYear());

    // Convert the template to a DOM object
    planning = $($.parseHTML(planning));

    // Hide the event elements
    planning.find('#events').hide();
    planning.find('#events-tracked').hide();
    planning.find('#events-going').hide();

    // Upgrade the element for MDL
    t.upgradeElement(planning);

    // Attach the new element to the content div
    $('#content').append(planning);

    // Add handler to the 'next' button
    $('.next_day').click(function() {
      // Go to the next day
      t.pagePlanningMove(1);
    });

    // Add handler to the 'previous' button
    $('.prev_day').click(function() {
      // Go to the previous day
      t.pagePlanningMove(-1);
    });

    // Add handler to the 'next week' button
    $('.next_week').click(function() {
      // Go to the next day
      t.pagePlanningMove(7);
    });

    // Add handler to the 'previous week' button
    $('.prev_week').click(function() {
      // Go to the previous day
      t.pagePlanningMove(-7);
    });

    // Add handler to the 'previous month' button
    $('.next_month').click(function() {
      // Go to the previous day
      t.pagePlanningMove(0, 1);
    });

    // Add handler to the 'previous month' button
    $('.prev_month').click(function() {
      // Go to the previous day
      t.pagePlanningMove(0, -1);
    });

    $('.today').click(function() {
      // Check if we are still loading
      if (t.loading) {
        // Give an error that the page is still loading
        t.showNotification('Page is still loading');
        return;
      }

      // Start the loading
      t.startLoading();

      // Start the page
      t.pagePlanningStart(t.getDateTime(new Date(), 'yyyy-mm-dd'), true);
    });

    // Reset the counters
    t.done = 3;
    t.donecounter = 0;

    // Get the events for this day
    for (i = 0; i < 3; i++) {
      t.pagePlanningEvents(i, 1, function() {
        t.donecounter++;

        if (t.donecounter == t.done) {
          // Stop the loading
          t.stopLoading();
        }
      }, function() {
        t.donecounter++;

        if (t.donecounter == t.done) {
          // TODO: give error
          // Stop the loading
          t.stopLoading();
        }
      });
    }

  }, function() {
    // The templates couldn't be loaded
    // Give an error to the user
    t.showNotification('Could not load the needed templates');
    t.stopLoading();
  });
}
/*----------------------------------------------------------------------------*/
// Method to switch dates
GUI.prototype.pagePlanningMove = function(days_increase = 0, months_increase = 0) {
  // Check if we are still loading
  if (this.loading) {
    // Give an error that the page is still loading
    this.showNotification('Page is still loading');
    return;
  }

  // Start the loading
  this.startLoading();

  // Find out what the date should be (days)
  newdate = new Date(this.planning['date_obj']);
  newdate.setDate(newdate.getDate() + days_increase);

  // Find out what the date should be (months)
  month = newdate.setMonth((newdate.getMonth()) + months_increase);

  // Create a string
  newdate = t.getDateTime(newdate, 'yyyy-mm-dd');

  // Start the page
  this.pagePlanningStart(newdate, true);
}
/*----------------------------------------------------------------------------*/
// Method to get events from the api and place them in the correct card
GUI.prototype.pagePlanningEvents = function(tracked, page, success, fail) {
  // A variable for the callback methods below
  t = this;

  t.apiCall('events.Get', { 'date': t.planning['date'], 'tracked': tracked, 'page': page }, function(data) {
    // Loop through all given items
    $.each(data['data']['data'], function(index, event) {
      // Get the template
      planning_event = tpl_cache['planning_event'];

      // Replace the variables
      planning_event = planning_event.replace(/{{ venue }}/g, event['venue']);
      planning_event = planning_event.replace(/{{ stage }}/g, event['stage']);
      planning_event = planning_event.replace(/{{ title }}/g, event['title']);
      planning_event = planning_event.replace(/{{ support }}/g, event['support']);

      // Convert the template to a DOM object
      planning_event = $($.parseHTML(planning_event));

      // Upgrade the element for MDL
      t.upgradeElement(planning_event);

      // Attach the new element to the card and show the the card
      if (tracked == 0) {
        $('#events').append(planning_event);
      } else if (tracked == 1) {
        $('#events-tracked').append(planning_event);
      } else if (tracked == 2) {
        $('#events-going').append(planning_event);
      }
    });

    // Check if we need to do more pages
    if (data['data']['maxpage'] > page) {
      t.pagePlanningEvents(tracked, page + 1, success, fail);
    } else {
      // Show the card if there are elements
      if (data['data']['data_len'] > 0) {
        if (tracked == 0) {
          $('#events').show();
        } else if (tracked == 1) {
          $('#events-tracked').show();
        } else if (tracked == 2) {
          $('#events-going').show();
        }
      }

      // Call the success callback
      if (success) { success(); }
    }
  }, function() {
    // Call the fail callback
    if (fail) { fail(); }
  });
}
/*----------------------------------------------------------------------------*/
// The method to show the planning
GUI.prototype.pageConcerts = function() {
  // A variable for the callback methods below
  t = this;

  // Preload the templates
  this.preloadTemplates([ 'concerts' ], function () {
    // The feed for the template is loaded. Clear the content div
    $('#content').html('');

    // Get the template
    concerts = tpl_cache['concerts'];

    // Convert the template to a DOM object
    concerts = $($.parseHTML(concerts));

    // Upgrade the element for MDL
    t.upgradeElement(concerts);

    // Attach the new element to the content div
    $('#content').append(concerts);

    // Done! Stop the loading of the page
    t.stopLoading();
  }, function() {
    // The templates couldn't be loaded
    // Give an error to the user
    t.showNotification('Could not load the needed templates');
    t.stopLoading();
  });
}
/*------------------------------------------------------------------------------
- Start of the script
------------------------------------------------------------------------------*/
// Create an object from the Me-class to handle the website
var gui = new GUI();
/*----------------------------------------------------------------------------*/
// Set and event listener for when the page is active so we can do whatever we
// need to do to start up the page
$(document).ready(function() {
  // Add an event listener to every menuitem
  $.each($('.me-navigation').find('a'), function(index, object) {
    $(object).click(function() {
      // When a menuitem is clicked, we have to fire off the correct function
      gui.clickMenuItem($(object).attr('id'))
    });
  });

  // Add an event listener to 'onopopstate' for the window so we can make the
  // return button work
  $(window).bind('popstate', function(page) {
    gui.changePage();
  });

  // Update the badge with the amount of items
  gui.updateFeedCount();

  // Set a timer to update the badge every few minutes
  gui.setTimerUpdate();

  // Start the correct page
  gui.changePage();
});
/*----------------------------------------------------------------------------*/
