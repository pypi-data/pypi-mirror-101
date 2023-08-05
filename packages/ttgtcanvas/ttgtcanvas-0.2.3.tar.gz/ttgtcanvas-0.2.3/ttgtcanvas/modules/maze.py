import ipywidgets as widgets
from traitlets import Unicode, Bool, validate, TraitError, Int, List, Dict, Float
import asyncio
import re as _re
import os
import time as _time
import copy
from datetime import datetime
import json


def pause(delay = 1.0):
  """Pause for delay seconds."""
  _time.sleep(delay)

_directions = [ (0, 1), (-1, 0), (0, -1), (1, 0) ]
_orient_dict = { 'E': 3, 'S': 2, 'W': 1, 'N': 0}


class _Beeper(object):
    """One ore more beepers at a crossing in the world."""
    def __init__(self, world, radius, av, st, num = 1):
        self.av = av
        self.st = st
        self.num = num
        self.world = world

    def set_number(self, num):
        self.num = num
        self.world.set_number(self)


class Robot(object):
    def init(self, world, avenue = 1, street = 1, orientation = 'E', beepers = 0, index = 0):
        self._dir = _orient_dict[orientation]
        self._x = avenue
        self._y = street
        self._beeper_bag = beepers
        self._trace = True
        self._delay = 0
        self._steps = 0
        self.my_index = index
        self.world = world
        self._update_pos()
    
    def _update_pos(self):
        x, y  = self.world.cr2xy(2 * self._x - 1, 2 * self._y - 1)
        self.world.move_to(self.my_index, x,y)

    def _trace_pos(self):
        x, y  = self.world.cr2xy(2 * self._x - 1, 2 * self._y - 1)
        xr, yr =  _directions[(self._dir - 1) % 4]
        xb, yb =  _directions[(self._dir - 2) % 4]
        return x + 5 * (xr + xb), y - 5 * (yr + yb)
    
    def _update_trace(self):
        if self._trace:
            x, y = self._trace_pos()
            self.world.add_point(self.my_index, x,y)
        
    def set_trace(self, color = None):
        """Without color argument, turn off tracing.
        With color argument, start a new trace in that color."""
        if not color:
            if self._trace:
                self.world.remove_trace(self.my_index)
            self._trace = None
        else:
            self._trace = True
            x, y  = self._trace_pos()
            self.world.set_trace(self.my_index, x, y, color)
    #   self._trace = _g.Path([_g.Point(x, y)])
    #   self._trace.setBorderColor(color)
    #   _scene.add(self._trace)

    def set_pause(self, delay = 0):
        """Set a pause to be made after each move."""
        self._delay = delay
        self.world.set_pause(self.my_index, delay)

    def get_pos(self):
        """Returns current robot position."""
        return self._x, self._y
    
    def turn_left(self):
        """Rotate left by 90 degrees."""
        # self._image[self._dir].moveTo(-100, -100)
        self._dir = (self._dir + 1) % 4
        self._update_pos()
        self._update_trace()

    def move(self):
        """Move one street/avenue in direction where robot is facing."""
        if self.front_is_clear():
            xx, yy = _directions[self._dir]
            self._x += xx
            self._y += yy
        self._update_pos()
        self._update_trace()

    

    def front_is_clear(self):
        """Returns True if no wall or border in front of robot."""
        col = 2 * self._x - 1
        row = 2 * self._y - 1
        xx, yy = _directions[self._dir]
        return self.world.is_clear(col + xx, row + yy)

    def left_is_clear(self):
        """Returns True if no walls or borders are to the immediate left
        of the robot."""
        col = 2 * self._x - 1
        row = 2 * self._y - 1
        xx, yy = _directions[(self._dir + 1) % 4]
        return self.world.is_clear(col + xx, row + yy)

    def right_is_clear(self):
        """Returns True if no walls or borders are to the immediate right
        of the robot."""
        col = 2 * self._x - 1
        row = 2 * self._y - 1
        xx, yy = _directions[(self._dir - 1) % 4]
        return self.world.is_clear(col + xx, row + yy)

    def facing_north(self):
        """Returns True if Robot is facing north."""
        return (self._dir == 0)

    def carries_beepers(self):
        """Returns True if some beepers are left in Robot's bag."""
        return (self._beeper_bag > 0)
    
    def on_beeper(self):
        """Returns True if beepers are present at current robot position."""
        return ((self._x, self._y) in self.world.beepers)

    def pick_beeper(self):
        """Robot picks one beeper up at current location."""
        if self.on_beeper():
            self.world.remove_beeper(self._x, self._y)
            self._beeper_bag += 1

    def drop_beeper(self):
        """Robot drops one beeper down at current location."""
        if self.carries_beepers():
            self._beeper_bag -= 1
            self.world.add_beeper(self._x, self._y)

def _check_world(contents):
    # safety check
    safe = contents[:]
    # only allow known keywords
    keywords = ["avenues", "streets", "walls", "beepers", "robot",
                "'s'", "'S'", '"s"', '"S"',
                "'e'", "'E'", '"e"', '"E"',
                "'w'", "'W'", '"w"', '"W"',
                "'n'", "'N'", '"n"', '"N"', ]
    for word in keywords:
        safe = safe.replace(word, '')
    safe = list(safe)
    for char in safe:
        if char.isalpha():
            raise ValueError("Invalid word or character in world file")


def load_world(filename):
    txt = open(filename, 'r').read()
    txt = _re.sub('\r\n', '\n', str(txt))
    txt = _re.sub('\r', '\n', str(txt))
    _check_world(txt)
    try:
        robot =  None
        wd = locals()
        exec(txt, globals(), wd)

        w = Maze(
                avenues= wd["avenues"], 
                walls= wd["walls"], 
                beepers= wd["beepers"], 
                streets= wd["streets"],
                robot=wd["robot"])
        return w
    except:
        raise ValueError("Error interpreting world file.")


@widgets.register
class Maze(widgets.DOMWidget):

    # Name of the widget view class in front-end
    _view_name = Unicode('MazeView').tag(sync=True)
    # Name of the widget model class in front-end
    _model_name = Unicode('MazeModel').tag(sync=True)
    _view_module = Unicode('ttgtcanvas').tag(sync=True)

    # Name of the front-end module containing widget model
    _model_module = Unicode('ttgtcanvas').tag(sync=True)

    _view_module_version = Unicode('^0.2.3').tag(sync=True)
    # Version of the front-end module containing widget model
    _model_module_version = Unicode('^0.2.3').tag(sync=True)

    current_call  = Unicode('{}').tag(sync=True)
    method_return = Unicode('{}').tag(sync=True)


    def js_call(self, method_name, params): 
        # print("calling method: " + method_name)
        cb = datetime.now().strftime('%f')
        self.current_call = json.dumps({'method_name': method_name, 'params': params, 'cb': cb})

    
    def __init__(self, **kwargs):
        super(Maze, self).__init__(**kwargs)
        options = {"avenues": 10, "streets": 10, "beepers": {}, "walls": [], "robot": (8, 1, 'E', 0)}
        options.update(kwargs)

        self._beepers = options["beepers"]
        self.av = options["avenues"]
        self.st = options["streets"]
        self.robot = options["robot"] 
        self.width = self.av * 50
        self.height = self.st * 50
        self.num_cols = 2*self.av + 1
        self.num_rows = 2*self.st + 1
        self.walls = options["walls"]
        self._bot = None
        for (col, row) in self.walls:
            if not (col+row) % 2:
                raise RuntimeError("Wall in impossible position (%d, %d)." % (col,row))
        self.borders = []
        self.set_borders()
        
        display(self)
        _time.sleep(1)

        self.init()

    def set_borders(self):
        """The world is surrounded by a continuous wall.  This function
            sets the corresponding "wall" or "border" based on the world's
            dimensions."""
        for col in range(1, self.num_cols-1, 2):
            if (col, 0) not in self.borders:
                self.borders.append( (col, 0) )
            if (col, self.num_rows) not in self.borders:
                self.borders.append( (col, self.num_rows-1) )
            for row in range(1, self.num_rows-1, 2):
                if (0, row) not in self.borders:
                    self.borders.append( (0, row) )
                if (self.num_cols, row) not in self.borders:
                    self.borders.append( (self.num_cols-1, row) )
    
    def cr2xy(self, col, row):
        x = self.left + self.ts * col
        y = self.bottom - self.ts * row
        return x, y
    
    def toggle_wall(self, col, row):
        """This function is intended for adding or removing a
            wall from a GUI world editor."""
        if (col+row) % 2 :  # safety check
            if (col, row) in self.walls: # toggle value
                self.walls.remove((col, row))
            else:
                self.walls.append((col, row))
        else:
            raise RuntimeError("Wall in impossible position (%d, %d)." % (col,row))

    def is_clear(self, col, row):
        """Returns True if there is no wall or border here."""
        return not ((col, row) in self.walls or (col, row) in self.borders)
    
    def _create_beeper(self, av, st):
        num = self.beepers[(av, st)]
        bp = _Beeper(self, 0.6 * self.ts, av, st, num)
        self.beeper_icons[(av, st)] = bp
        return bp
        


    def init(self):
        self.beepers = self._beepers.copy()
        self.beeper_icons = {}
        tsx =  self.width / (self.num_cols + 2)
        tsy =  self.height / (self.num_rows + 2)
        self.ts = min(tsx, tsy)
        self.left = 2 * self.ts
        self.right = self.left + 2 * self.ts * self.av
        self.bottom = self.height - 2 * self.ts
        self.top = self.bottom - 2 * self.ts * self.st


        #UI Add layer
        ##Add Beepers
        _beepers = []
        for (av, st) in self.beepers:
            _beeper = self._create_beeper(av, st)
            _beepers.append({'key':[av, st], 'value': _beeper.num})

        self.js_call('draw_grid', [self.width, self.height, self.av, self.st,  self.ts, self.walls, _beepers, self.robot])

        self.init_robot('./robot-design.svg')
        # add_robot
        return self

    def move_to(self, rindex , x, y):
        self.js_call('move_to', [rindex, x,y])

    def add_point(self, rindex ,  x, y):
        self.js_call('add_point', [rindex, x,y])
    
    ##init robot
    def init_robot(self, src):
        avenue, street, orientation, beepers = self.robot
        self.js_call('add_robot', [0, src, avenue, street,orientation, beepers])
        self._bot  =  self._bot or Robot()
        self._bot.init(self, avenue, street, orientation, beepers, 0)
        self.js_call('init_robot', [0])
        return self._bot

    def bot(self):
        return self._bot

    def remove_trace(self, rindex):
        self.js_call("remove_trace", [rindex])
    
    def set_pause(self, rindex,  delay):
        self.js_call('set_pause', [rindex, delay])
    
    def set_trace(self, rindex, x,y, color):
        self.js_call('set_trace', [rindex, x, y, color])
    
    def set_number(self, beeper):
        self.js_call('set_beeper_number', [beeper.av, beeper.st, beeper.number])

    def add_beeper(self, av, st):
        x, y = self.cr2xy(2 * av - 1, 2 * st - 1)
        """Add a single beeper."""
        if (av, st) in self.beepers:
            self.beepers[(av, st)] += 1
            bp = self.beeper_icons[(av,st)]
            bp.set_number(self.beepers[(av, st)])
            self.js_call('update_beeper', [av, st, self.beepers[(av, st)]])
        else:
            self.beepers[(av, st)] = 1
            self._create_beeper(av, st)
            self.js_call('add_beeper', [av, st, x, y, self.beepers[(av, st)]])

    def remove_beeper(self, av, st):
        """Remove a beeper (does nothing if no beeper here)."""
        x, y = self.cr2xy(2 * av - 1, 2 * st - 1)
        
        if (av, st) in self.beepers:
            self.beepers[(av, st)] -= 1
        if self.beepers[(av, st)] == 0:
            del self.beepers[(av, st)]
            del self.beeper_icons[(av,st)]
            self.js_call('remove_beeper', [av, st])
        else:
            bp = self.beeper_icons[(av,st)]
            bp.set_number(self.beepers[(av, st)])
            self.js_call('update_beeper', [av, st, self.beepers[(av, st)]])
    