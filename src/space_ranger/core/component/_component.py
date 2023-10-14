class Component:

    def __init__(self) -> None:
        self._game_object = None
    
    def start(self):
        pass

    def process_event(self, event) -> None:
        pass

    def update(self):
        pass


class Sprite(Component):
    