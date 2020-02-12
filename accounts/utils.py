from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from easyaudit.models import CRUDEvent

from accounts.models import User


content_types = {
    'user': ContentType.objects.get(
        app_label='accounts',
        model='user'
    ),
}


class Event():
    """
    Event which can be interpreted easily by a django template tag.

    Has a list of strings to make up a message, and list of url refs which can
    be included in the message. The message should always come first, and the
    two lists must be of equal length - so there may be padding required.
    """
    def __init__(self):
        self.text = []
        self.links = []

    def add_text(self, text):
        if len(self.text) == 0:
            # first item
            self.text.append(text)
            self.links.append('')
        else:
            self.add_item(text, to_list=self.text, other_list=self.links)


    def add_link(self, link):
        if len(self.links) == 0:
            # first item
            self.text.append('')
            self.links.append(link)
        else:
            self.add_item(link, to_list=self.links, other_list=self.text)

    def add_item(self, item, to_list, other_list):
        if to_list[-1] == '':
            # adding an item to message preceded by a link
            to_list.pop()
        else:
            other_list.append('')
        to_list.append(item)

    def __str__(self):
        message = []
        for i in range(len(self.text)):
            message.append(self.text[i])
            message.append(str(self.links[i]))

        return ''.join(message)

    class URLRef():
        """
        Reference to another page with a given name and ref, eg. pk.
        """
        def __init__(self, name, reference):
            self.name = name
            self.reference = reference

        def __str__(self):
            return f"url@{self.name}:{self.reference}"


def get_user_audit_log(user):
    """Get all the CRUDevents which relate to a user and return a nice list.
    """

    # get things done by user
    user_activity = Q(user=user)
    # and things done to user
    user_modified = Q(content_type=content_types['user'], object_id=user.id)
    crud_events = CRUDEvent.objects.filter(user_activity | user_modified)
    events = [process_crud(x) for x in crud_events]

    return events


def process_crud(crud):
    """Process a CRUD event from db into a form which can be displayed in HTML
    """
    event = Event()
    if crud.content_type == content_types['user']:
        event.text.append('User ')
        event.links.append(
            Event.URLRef(
                name='profile',
                reference=User.objects.get(id=crud.object_id).username
            )
        )
        event.text.append(' was created.')
    else:
        pass
    return event




