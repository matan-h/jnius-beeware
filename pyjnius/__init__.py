import sys
from .android import (
    # methods
    cast,
    autoclass,
    java_method,
    # MainActivity:
    python_act,
    act,
    mActivity,
    # heavy workarounds
    activity,
    config,
    PythonJavaClass,
    JavaException,_install
)
from .runnable import run_on_ui_thread

def install(debug=False):
    mod = sys.modules[__name__]
    _install(debug,mod)

install() # just install my default
__all__ = [
    "cast",
    "python_act",
    "act",
    "mActivity",
    "config",
    "autoclass",
    "java_method",
    "PythonJavaClass",
    "activity",
    "JavaException",
    "run_on_ui_thread",
]
