from django.urls import reverse


class Event():
    """
    Event which can be interpreted easily by a django template tag.

    Has a list of strings to make up a message, and list of url refs which can
    be included in the message. The message should always come first, and the
    two lists must be of equal length - so there may be padding required.
    """
    def __init__(self, datetime, icon):
        self.text = []
        self.links = []
        self.datetime = datetime
        self.icon = icon

    def add_text(self, text):
        self.add_item(text, to_list=self.text, other_list=self.links)

    def add_link(self, link):
        if self.last_link == '' and self.last_text != '':
            self.links.pop()
            self.links.append(link)
        else:
            self.add_item(link, to_list=self.links, other_list=self.text)

    def add_item(self, item, to_list, other_list):
        to_list.append(item)
        other_list.append('')

    @property
    def last_text(self):
        return self.text[-1] if self.text else None

    @property
    def last_link(self):
        return self.text[-1] if self.text else None

    @property
    def zipped_message(self):
        return list(zip(self.text, self.links))

    def __str__(self):
        message = []
        for i in range(len(self.text)):
            message.append(self.text[i])
            message.append(str(self.links[i]))

        return ''.join(message)

    def __repr__(self):
        return self.__str__()

    class URLRef():
        """
        Reference to another page with a given name and ref, eg. pk.
        """
        def __init__(self, name, reference, display):
            self.name = name
            self.reference = reference
            self.display = display

        @property
        def url(self):
            return reverse(self.name, args=(self.reference,))

        def __str__(self):
            return f"url@{self.name}:{self.reference}"
