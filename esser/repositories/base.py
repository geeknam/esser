import json
import dateutil.parser


class Event(object):
    """
    Event class to represent a consistent interface across
    all repository implementations
    """

    def __init__(self, aggregate_name, aggregate_id, version,
                 event_type, created_at, event_data):
        self.aggregate_name = aggregate_name
        self.aggregate_id = aggregate_id
        self.version = version
        self.event_type = event_type
        self.created_at = created_at
        self.event_data = event_data

    @property
    def aggregate_key(self):
        return '%s:%s' % (self.aggregate_id, self.version)

    def as_dict(self):
        """Serialise event object to dictionary format

        Returns:
            dict: dict representing event
        """
        return {
            'aggregate_name': self.aggregate_name,
            'aggregate_id': self.aggregate_id,
            'version': self.version,
            'event_type': self.event_type,
            'created_at': self.created_at,
            'event_data': self.event_data,
        }

    def as_json(self):
        """Serialise event object to JSON format

        Returns:
            str: JSON representing event
        """
        return json.dumps(self.as_dict())

    @classmethod
    def from_image(cls, image):
        """Turn dynamodb image from stream event
        into `esser.repositories.base.Event` object

        Args:
            image (dict): Dynamodb Strea NEW_IMAGE key

        Returns:
            esser.repositories.base.Event: Event objet
        """
        aggregate_id, version = image['aggregate_key']['S'].split(':')
        return cls(
            aggregate_name=image['aggregate_name']['S'],
            aggregate_id=aggregate_id,
            version=version,
            event_type=image['event_type']['S'],
            created_at=dateutil.parser.parse(image['created_at']['S']),
            event_data=json.loads(image['event_data']['S']),
        )


class BaseRepository(object):

    def __init__(self, aggregate):
        self.aggregate = aggregate

    def to_event(self, obj):
        """
        :return: Event object
        :rtype: esser.repositories.base.Event
        """
        raise NotImplementedError(
            'Repository interface needs to implement to_event() method'
        )

    def get_events(self, version):
        """
        :param version: version of event from which to start
        :type version: int
        :return: Iterable (list, generator) of Event objects
        :rtype: iterable of esser.repositories.base.Event

        Return an iterable set of Event objects
        Available context: `self.aggregate`
        """
        raise NotImplementedError()

    def get_all_events(self):
        """
        :return: Iterable (list, generator) of Event objects
        :rtype: iterable of esser.repositories.base.Event

        Returns all events of current aggregate
        """
        raise NotImplementedError()

    def get_last_event(self):
        """
        :return: Event object
        :rtype: esser.repositories.base.Event

        Should return an Event object
        """
        raise NotImplementedError()

    def persist(self, aggregate_id, version, event_type, attrs):
        """
        :param aggregate_id: unique id of an aggregate (uuid can be used)
        :type aggregate_id: str
        :param version: version of event from which to start
        :type version: int
        :param event_type: Type of event E.g: CartUpdated
        :type event_type: str
        :param attrs: Attributes or data of the event
        :type attrs: dict
        :return: Event object
        :rtype: esser.repositories.base.Event

        Should return an Event object
        """
        raise NotImplementedError()
