# Force IDE to use Wayland

Add this to custom VM options to force the IDE to use Wayland.

```
-Dawt.toolkit.name=WLToolkit
```


# (X11) Force UI scale

Useful if IDE windows randomly decide to use a different scale factor when moving it to a different monitor.
This also goes into custom VM options of your IDE.

```
-Dsun.java2d.uiScale=2.0 # Replace with whatever scale you need
-Dsun.java2d.uiScale.enabled=true
```


