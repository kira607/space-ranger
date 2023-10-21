"""Built-in library of systems.

Available systems:
  * `RenderingSystem` - A system for rendering sprites.
  * `ScriptingSystem` - A system for handling :class:`space_ranger.core.component.Script` components.
"""

from ._system import System as System
from .debug_system import DebugSystem as DebugSystem
from .rendering_system import RenderingSystem as RenderingSystem
from .scripting_system import ScriptingSystem as ScriptingSystem
from .sprite_rotation_system import SpriteRotationSystem as SpriteRotationSystem
