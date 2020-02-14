import json

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from easyaudit.models import CRUDEvent

from accounts.models import User
from db.models import Hub
from db.utils.audit import Event


content_types = {
    'user': ContentType.objects.get(
        app_label='accounts',
        model='user'
    ),
}

event_types = {
    'create': CRUDEvent.CREATE
}


def get_user_audit_log(user):
    """Get all the CRUDevents which relate to a user and return a nice list.
    """
    # get things done by user
    user_activity = Q(user=user)
    # and things done to user
    user_modified = Q(content_type=content_types['user'], object_id=user.id)
    crud_events = CRUDEvent.objects.filter(user_activity | user_modified)
    events = process_crud_events(crud_events)
    return events


def process_crud_events(crud_events):
    events = []
    for event in crud_events:
        events_from_crud = process_crud(event, crud_events)
        events.extend(events_from_crud)

    # some return none if non-interesting, eg. last login updates.
    return [event for event in events if event]

def process_crud(crud, user_events):
    """Process a CRUD event from db into a form which can be displayed in HTML
    """
    events = []
    if crud.content_type == content_types['user']:
        user = User.objects.get(id=crud.object_id)
        if crud.event_type == CRUDEvent.CREATE:
            event = Event(datetime=crud.datetime, icon='user plus')
            event.add_text('User ')
            event.add_link(
                Event.URLRef(
                    name='profile',
                    reference=user.username,
                    display=user.username
                )
            )
            event.add_text(' was created.')
            events.append(event)
        elif crud.event_type == CRUDEvent.M2M_CHANGE:
            events.extend(join_or_leave_hubs_event(crud, user_events))
    return events


def join_or_leave_hubs_event(crud, user_events):
    events = []
    new_json = json.loads(crud.object_json_repr)
    found_previous = False
    while not found_previous:
        previous_crud = crud.get_previous_by_datetime()
        if previous_crud in user_events:
            found_previous = True
    old_json = json.loads(previous_crud.object_json_repr)

    new_hubs = set(new_json[0]['fields']['hubs'])
    old_hubs = set(old_json[0]['fields']['hubs'])

    hubs_joined = new_hubs - old_hubs
    hubs_left = old_hubs - new_hubs

    if hubs_joined:
        events.append(
            change_hubs_event(
                change_type='join',
                hubs=hubs_joined,
                datetime=crud.datetime
            )
        )
    if hubs_left:
        events.append(
            change_hubs_event(
                change_type='leave',
                hubs=hubs_left,
                datetime=crud.datetime
            )
        )

    return events


def change_hubs_event(change_type, hubs, datetime):
    change_text = 'Joined' if change_type == 'join' else 'Left'
    hub_text = 'hub' if len(hubs) == 1 else 'hubs'
    hubs = list(hubs)
    event = Event(datetime=datetime, icon='users')
    event.add_text(f"{change_text} ")

    for i in range(len(hubs)):
        last = True if i+1 == len(hubs) else False
        penultimate = True if i+1 == len(hubs)-1 else False
        hub = Hub.objects.get(id=hubs[i])
        event.add_link(
            Event.URLRef(
                name='hub',
                reference=hub.name,
                display=hub.name
            )
        )
        if last:
            pass
        elif penultimate:
            event.add_text(' and ')
        else:
            event.add_text(', ')

    event.add_text(f" {hub_text}.")
    return event

