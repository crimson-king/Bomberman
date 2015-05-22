from pygame.math import Vector2


class Node:
    def __init__(self, x=0, y=0):
        self.position = Vector2()
        self.position.x = x
        self.position.y = y

        self.parent = None

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
        node.parent = self

    def remove_node(self, node: Node):
        self._nodes.remove(node)
        node.parent = None

    def draw(self, canvas, offset=(0, 0)):
        for node in self._nodes:
            node.draw(canvas, offset=offset + self.position)

    def update(self, dt):
        for node in self._nodes:
            node.update(dt)

    def __len__(self):
        return len(self._nodes)

    def __iter__(self):
        return (node for node in self._nodes)

    def __repr__(self):
        return '<{name}: position: {position}, nodes: {_nodes}'.format(
            name=self.__class__.__name__, **self.__dict__)
