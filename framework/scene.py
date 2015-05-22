from pygame.math import Vector2


class Node:
    def __init__(self, x=0, y=0):
        self.position = Vector2()
        self.position.x = x
        self.position.y = y

    def draw(self, canvas, offset=(0, 0)):
        raise NotImplementedError

    def update(self, dt):
        raise NotImplementedError


class NodeGroup(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._nodes = []

    def add_node(self, node: Node):
        self._nodes.append(node)

    def draw(self, canvas, offset=(0, 0)):
        for node in self._nodes:
            node.draw(canvas, offset=offset + self.position)

    def update(self, dt):
        for node in self._nodes:
            node.update(dt)

    def __iter__(self):
        return (node for node in self._nodes)
