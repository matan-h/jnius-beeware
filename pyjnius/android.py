import sys
import os

from java import (
    jclass,
    cast,
    dynamic_proxy,
)
import toga

org_cast = cast
act = jclass("org.beeware.android.MainActivity")

python_act = act  # yes, plyer can import it with this name
mActivity = act.singletonThis
act.mActivity = mActivity  # used a lot

## modifiy act properties:
DEBUG = False


def _install(debug=False, mod=None):
    global DEBUG
    DEBUG = debug

    os.environ[
        "ANDROID_ARGUMENT"
    ] = "BeeWare"  # make kvdroid stop asking to use android
    if not mod:
        mod = sys.modules[__name__]
    sys.modules["jnius"] = sys.modules["android"] = mod


def _print(*args):
    if DEBUG:
        print("jnius_workaround:", *args)


class AttrDict(dict):
    __slots__ = ()
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


class Config:
    JAVA_NAMESPACE = "org.beeware.android.MainActivity"


config = Config()


def cast(cls, obj):
    if isinstance(cls, str):
        cls = jclass(cls)
    return org_cast(cls, obj)

def toast(activity,msg):
    Toast = jclass("android.widget.Toast")
    Toast.makeText(activity, msg,
                        Toast.LENGTH_SHORT).show()

class IntentActivity:
    def __init__(self):
        pass

    def bind(
        self, on_activity_result
    ):  # FIXME: this method assumes only one intent is happening
        # print(type(toga.App.app))  # plyer_beeware.app.PlyerBeeware
        # print(type(toga.App.app.main_window))  # toga.app.MainWindow
        # the implemention of onActivityResult is in toga. but we can override it if its not found there
        togaApp = toga.App.app._impl._listener
        running_intents = togaApp.running_intents

        super_onActivityResult = togaApp.onActivityResult

        def onActivityResult_ifnot(requestCode, resultCode, resultData):
            if requestCode in running_intents:  # if its set in toga
                super_onActivityResult(requestCode, resultCode, resultData)
            else:  # probably we should take it
                on_activity_result(requestCode, resultCode, resultData)

        togaApp.onActivityResult = onActivityResult_ifnot


def autoclass(className):
    _print("autoclass: ", className)

    if (
        className.startswith(
            "org.beeware.android.MainActivity"
        )  # it looked at the config
        or className
        == "org.renpy.android.PythonActivity"  # it just hardcoded the default
        ):
        return act
        # return AttrDict({"mActivity": mActivity}) # FIXME : there is probably a better way to do it, but i`ve only seen cases of autoclass().mActivity
    return jclass(className)


def java_method(fn):
    # most Classes are alredy PythonJavaClass, and this java_method way is corrently not supported

    def blank_fn(*args, **kwargs):
        return fn

    return blank_fn  # the usage is @java_method(something) so this function -> (function -> fn)


class PythonJavaClass:
    def __init__(self, *args, **kwargs):
        ji = getattr(self, "__javainterfaces__", "")
        if not ji:
            _print(
                "FIXME:PythonJavaClass without __javainterfaces__"
            )  # maybe we I should raise an Exception as this is not support by jnius
            return
        ji = (
            ji[0].replace("/", ".").strip()
        )  # FIXME: better convertion beween actual java name and the domain

        wanted = (dynamic_proxy(jclass(ji)), object)
        self.__class__.__bases__ = (
            wanted  # set the class to be based on the correct dynamic_proxy
        )

## direct convertors
activity = IntentActivity()
JavaException = Exception  # FIXME: only java Exceptions ...
##
act.toastError = toast # support jnius MainActivity.toastError to support kvdroid.tools.toast


# TODO : implement some java converters. e.g.:
# java_method(str,list)->java_method(str,String[])
# this TOOD is about the limitations of chaquopy #1055 #1048.
