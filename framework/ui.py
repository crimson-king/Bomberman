"""
This module contains Node and NodeGroups used for easy ui creating
"""

# pygame modules are loaded dynamically, thus, supress no name/members errors
# pylint: disable=no-name-in-module
# pylint: disable=no-member

# It is intended to make View another abstraction layer.
# pylint: disable=abstract-method

import pygame
from pygame.surface import Surface

from framework.input import InitialAction
from framework.scene import NodeGroup, Node
from framework.state import State
from framework import input_manager


class View(Node):
    """
    Focusable, clickable Node with appropriate methods. Intended to use with
    Stage NodeGroup
    """

    def __init__(self):
        super().__init__()

        self._on_click = lambda view: None
        self._on_focus = lambda view: None
        self._on_unfocus = lambda view: None

    @property
    def on_click(self):
        """Invoked on click"""
        return self._on_click

    @on_click.setter
    def on_click(self, value):
        """Sets on click value"""
        self._on_click = value

    @property
    def on_focus(self):
        """Invoked on focus"""
        return self._on_focus

    @on_focus.setter
    def on_focus(self, value):
        """Sets on focus value"""
        self._on_focus = value

    @property
    def on_unfocus(self):
        """Invoked on focus lose"""
        return self._on_unfocus

    @on_unfocus.setter
    def on_unfocus(self, value):
        """Sets on unfocus value"""
        self._on_unfocus = value


class Text(View):
    """View that displays text"""

    def __init__(self, text, size=24, color=(0, 0, 0)):
        super().__init__()
        self.font = pygame.font.Font(pygame.font.get_default_font(), size)
        self.surface = self.font.render(text, True, color)
        self.size.x = self.surface.get_width()
        self.size.y = self.surface.get_height()

    def draw(self, canvas: Surface, offset=(0, 0)):
        """Draws text surface"""
        canvas.blit(self.surface, offset + self.position)

    def update(self, delta_time):
        pass


class Button(Text):
    """View that changes its surface on focus and unfocus"""

    def __init__(self, text,
                 normal_color=(0, 0, 0xff),
                 focused_color=(220, 20, 60)):
        super().__init__(text, color=normal_color)

        self._text = text
        self.surface_normal = self.surface
        self.surface_focused = None
        self.normal_color = normal_color
        self.focused_color = focused_color

        self.render()

    def render(self):
        """Renders the button"""
        focused = self.surface is self.surface_focused
        self.surface_normal = self.font.render(
            self._text, True, self.normal_color)
        self.surface_focused = self.font.render(
            self._text, True, self.focused_color)
        self.surface = self.surface_focused if focused else self.surface_normal
        self.size.x = self.surface.get_width()
        self.size.y = self.surface.get_height()
        if self.parent:
            self.parent.layedout = False

    @property
    def text(self):
        """Returns text on a button"""
        return self._text

    @text.setter
    def text(self, value):
        """Sets text on a button"""
        self._text = value
        self.render()

    def on_focus(self):
        """Sets appropriate surface to draw"""
        self.surface = self.surface_focused

    def on_unfocus(self):
        """Sets appropriate surface to draw"""
        self.surface = self.surface_normal


class Stage(NodeGroup):
    """NodeGroup that handles focus of its elements"""

    def __init__(self):
        super().__init__()
        self.focus = 0

        self.next = InitialAction()
        self.previous = InitialAction()
        self.select = InitialAction()

        self.focusables = []
        self.unfocusables = []

        self.layedout = False

    def layout(self, width, height):
        """Lays out views"""
        print('layout')
        node_count = len(self._nodes)
        for i, view in enumerate(self._nodes):
            view.position.x = (width - view.size.x) * .5
            view.position.y = (height - view.size.y) \
                              * (i + 1) / (node_count + 1)

        self.layedout = True

    def add_node(self, view: View):
        """Adds nodes and invalidates current layout"""
        super().add_node(view)
        self.layedout = False

        if isinstance(view, Button):
            self.focusables.append(view)
            if len(self.focusables) - 1 == self.focus:
                view.on_focus()
        else:
            self.unfocusables.append(view)

    def draw(self, canvas: Surface, offset=(0, 0)):
        """Invokes layout method if necessary and draws stage"""
        if not self.layedout:
            self.layout(*canvas.get_size())

        super().draw(canvas=canvas, offset=offset)

    def map_actions(self, input_manager_=input_manager):
        """Maps actions required to handle ui"""
        input_manager_.map_action(pygame.K_DOWN, self.next)
        input_manager_.map_action(pygame.K_UP, self.previous)
        input_manager_.map_action(pygame.K_RETURN, self.select)

    def update(self, delta_time):
        """Updates stage and its focus"""
        if len(self.focusables) == 0:
            return

        old_focus = self.focus

        if self.next:
            self.focus += 1
        if self.previous:
            self.focus -= 1

        self.focus %= len(self.focusables)

        if old_focus != self.focus:
            self.focusables[old_focus].on_unfocus()
            self.focusables[self.focus].on_focus()

        super().update(delta_time)

        if self.select:
            focused_node = self.focusables[self.focus]
            focused_node.on_click(focused_node)


class StageState(State):
    """State that manages stage"""

    def __init__(self):
        self.stage = Stage()

    def resume(self):
        """Remaps input actions"""
        input_manager.clear()
        self.stage.map_actions(input_manager)
        input_manager.reset()

    def pause(self):
        """Clears input actions"""
        input_manager.clear()

    def handle_draw(self, canvas):
        """Draws stage"""
        canvas.fill((36, 36, 36))
        self.stage.draw(canvas)

    def handle_update(self, delta_time):
        """Updates stage"""
        self.stage.update(delta_time)

    def handle_input(self, event):
        """Handles input"""
        input_manager.handle_input(event)


if __name__ == '__main__':
    from framework.core import Game
    from framework.state import StateGameHandler
    from framework import state_manager

    # theese ain't constants, dear pylint!
    # pylint: disable=invalid-name

    # make sure Game is initialized before ui elements are used
    state = StageState()
    game = Game(handler=StateGameHandler())

    text_view = Text('Hello, ui!')
    state.stage.add_node(text_view)

    button = Button('click me (and watch console output)')
    button.on_click = lambda view: print(view, 'clicked!')
    state.stage.add_node(button)

    button = Button('woo-hoo!')
    state.stage.add_node(button)

    state_manager.push(state)
    game.start()
