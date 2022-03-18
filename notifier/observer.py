from __future__ import annotations
from abc import ABC, abstractmethod
from copy import deepcopy


class Subject(ABC):
    """
    The Subject interface declares a set of methods for managing the subscriber.
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from the subject.
        """
        pass

    @abstractmethod
    def notify(self, entity_obj: Subject | None, original_entity_obj: Subject | None, msg: str) -> None:
        """
        Notify observer about an event.
        """
        pass


class ConcreteSubject(Subject):

    _observer: Observer | None

    _config: dict = {}

    _notify_on_creation = False

    _internal = False

    def attach(self, observer: Observer) -> None:
        self._observer = observer
        if self._notify_on_creation:
            observer.update(self, None, f"{self.__class__.__name__}", msg="Attach observer")

    def detach(self, observer: Observer) -> None:
        self._observer = None

    def notify(self, entity_obj: Subject | None, original_entity_obj: Subject | None, msg: str) -> None:
        if hasattr(self, '_observer'):
            self._observer.update(entity_obj, original_entity_obj, self.__class__.__name__, msg)

    def __setattr__(self, key, value):
        if self._config and not self._internal:
            attributes = self._config[self.__class__.__name__]
            if key in attributes['fields']:
                if not hasattr(self, key):
                    msg = f"{key} Created"
                else:
                    self._internal = True
                    original_entity_object = deepcopy(self)
                    msg = f"{key} Updated from {getattr(self, key)} to {value}"
                    super(ConcreteSubject, self).__setattr__(key, value)
                    entity_obj = self
                    for notification_object in attributes['notify_on']:
                        if notification_object == 'self':
                            self.notify(entity_obj, original_entity_object, msg)
                        else:
                            notification_object = getattr(self, notification_object)
                            notification_object.notify(entity_obj, original_entity_object, msg)
                    self._internal = False
                    return
        super(ConcreteSubject, self).__setattr__(key, value)

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        if cls._config and not cls._internal:
            attributes = cls._config[cls.__name__]
            if "new" in attributes["actions"]:
                cls._notify_on_creation = True
        return instance

    def __del__(self):
        # FIXME: We are getting notification on cleaning local stack of the functions.
        if self._config and not self._internal:
            attributes = self._config[self.__class__.__name__]
            if "del" in attributes["actions"]:
                msg = f"{self.__class__.__name__} is deleted"
                for notification_object in attributes['notify_on']:
                    if notification_object == 'self':
                        self.notify(None, self, msg)
                    else:
                        notification_object = getattr(self, notification_object)
                        notification_object.notify(None, self, msg)


class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, entity_obj: Subject | None, original_entity_obj: Subject | None, typ: str, msg: str) -> None:
        """
        Receive update from subject.
        """
        pass
