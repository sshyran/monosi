class BaseIntegration(object):
    def __init__(self, configuration):
        self.configuration = configuration

    @classmethod
    def name(cls):
        return cls.__name__.lower()

    @classmethod
    def type(cls):
        return cls.__name__

    @classmethod
    def enabled(cls):
        return True

    @classmethod
    def configuration_schema(cls):
        return {}

    @classmethod
    def icon(cls):
        raise NotImplementedError()

    def alert(self, message):
        raise NotImplementedError()

    @classmethod
    def to_dict(cls):
        return {
            "name": cls.name(),
            "type": cls.type(),
            "icon": cls.icon(),
            "configuration_schema": cls.configuration_schema(),
            **({ "deprecated": True } if not cls.enabled else {})
        }


