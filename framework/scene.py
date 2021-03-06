"""Includes Node and NodeGroup for managing scene graph. These should be
updated and drawn in appropriate GameHandler events. It's a shame PyGame
hasn't got something like this!"""

# pygame modules are loaded dynamically, thus, supress no name/members errors
# pylint: disable=no-name-in-module
# pylint: disable=no-member
from pygame.math import Vector2
from pygame.surface import Surface


class Node:
    """Class for handling objects' actual display"""

    def __init__(self, pos_x=0, pos_y=0):
        self.position = Vector2()
        self.position.x = pos_x
        self.position.y = pos_y
        self.size = Vector2()

        self.parent = None

    def draw(self, canvas: Surface, offset=(0, 0)):
        """Drawing stuff"""
        raise NotImplementedError

    def update(self, delta_time):
        """Updating stuff"""
        raise NotImplementedError


class NodeGroup(Node):
    """Handles list of nodes"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._nodes = []

    def add_node(self, node: Node):
        """Adds a node to the list of nodes"""
        self._nodes.append(node)
        node.parent = self

    def remove_node(self, node: Node):
        """Removes a node from the list"""
        self._nodes.remove(node)
        node.parent = None

    def draw(self, canvas: Surface, offset=(0, 0)):
        """Draws each node in the list"""
        for node in self._nodes:
            node.draw(canvas, offset=offset + self.position)

    def update(self, delta_time):
        """Updates each node in the list"""
        for node in self._nodes:
            node.update(delta_time)

    def __len__(self):
        """Returns length of node list"""
        return len(self._nodes)

    def __iter__(self):
        """Iterates through the list"""
        return (node for node in self._nodes)

    def __repr__(self):
        """Returns representation of nodes"""
        return '<{name}: position: {position}, nodes: {_nodes}'.format(
            name=self.__class__.__name__, **self.__dict__)
