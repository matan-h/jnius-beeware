# Jnius-beeware - a way to run Jnius on beeware

## why

beeware is a great software. it really simplify the build apps and simple graphics process
but it has two big limitations:

1. debug - its a strong reference to my [other library](https://github.com/matan-h/brbug)
2. `PyJNIus`

there are (mainly) two frameworks to make android apps in python: `kivy` and `beeware`.

kivy (`kivy`) has something like `16K` stars, while beeware (`toga`) has about `4k`, so natively there are more "java in python" code written in `kivy`.

the way to write java in `kivy` is using [PyJNIus](https://github.com/kivy/pyjnius) while in beeware its using [Chaquopy](https://github.com/chaquo/chaquopy).
they both provide a similar python API, for example, the function to get java from class name is called `jclass` in chaquopy, and it called `autoclass` in pyjnius, but they do the exact same thing.

but unlike beeware, where it seem the only library written in `Chaquopy` are the `toga` framework itself (plus the awesome `tatogalib` library created by `tomArn` that contains all the basic android things,e.g. filechooser, clipboard that are [m](https://github.com/beeware/toga/pull/1158)[i](https://github.com/beeware/toga/pull/1191)[s](https://github.com/beeware/toga/issues/1192)[s](https://bitbucket.org/TomArn/tatogalib/src/main/src/tatogalib/system/notifications/android.py)[i](https://bitbucket.org/TomArn/tatogalib/src/main/src/tatogalib/uri_io/urioutputstream/android.py)[n](https://bitbucket.org/TomArn/tatogalib/src/main/src/tatogalib/ui/window.py)[g](https://bitbucket.org/TomArn/tatogalib/src/main/src/tatogalib/uri_io/urifilebrowser/android.py) from `toga`), in `PyJNIus` there are two big projects: 

1. `plyer`
2. `kvdroid`

and there both providing very cool utils.

## supported libraries:

* `plyer` - ~60%
* `kvdroid.tools` - ~80%

the main blockers are not this implementation, but base chaquopy limitations: especially [#1055](https://github.com/chaquo/chaquopy/issues/1055) (automatic convert `python list`->`java array`) and [#1048](https://github.com/chaquo/chaquopy/issues/1048) (automatic convert `java ArrayList` -> `python list`)

## installation

to install put it in your `pyproject.toml` requires, before the dependencies that import it:

```toml
[tool.briefcase.app.your-app]
requires = ["brbug","scoop","git+https://github.com/matan-h/jnius-beeware.git","kvdroid"]
```

and if you want the auto-complete you can also install it using pip : `pip install git+https://github.com/matan-h/jnius-beeware.git`.