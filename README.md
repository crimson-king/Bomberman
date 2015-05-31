# PyBomberman

Bombs, plot twists, torn off limbs, gruesome deaths.
Fun for the whole family.


## Requirements
Project is developed in Python 3.4 and Python 3.5 environments.
File requirements.txt contains all the requirements.
See Installing dependencies below.


### Creating Virtual Environment
Using virtual Python environment is strongly recommended to run PyBomberman.
```
pyvenv-3.5 env
source env/bin/activate
```


### Installing dependencies
Navigate to project root directory and run following line in a shell:
```
pip install -r requirements.txt
```
Hint: you may have to install PyGame not so standard way.
Either try to compile it from sources, or let pip do it.
Please note, you need `mercurial` installed for this to work.
```
pip3 install hg+https://bitbucket.org/pygame/pygame
```


### Running project
PyBomberman may be started by running script from project root: 
```
./main.py
```

## Technical details

* **framework** module contains generic patterns for developing games in Python 3 with PyGame.
  * **core** submodule encapsulates standard game development patterns, such as `Game` which implement game window and invokes `handle_input`, `handle_draw` and `handle_update` methods of provided `GameHandler` object.
  * **state** submodule has `State` interface derived from `GameHandler`, which subclass instances are operated by `StateManager`. To use this feature, you need to pass `StateGameHandler` to `Game`'s initializer.
  * **scene** includes `Node` and `NodeGroup` for managing scene graph. Theese should be `update`d and `draw`n is appropriate `GameHandler` events.
  * **input** allows easy use of pygame key input (although can be easily adapted to handle other input as well). `Action` interface along with straightforward `NormalAction` and almost as trivial `InitialAction` managed by `InputManager` may be used as deadly simple, yet powerfull and extensible input processor.
  * **\__init__** lets you `from framework import state_manager` to make some state pushing and `from framework import input_manager` if you want to make use of **input** submodule.
