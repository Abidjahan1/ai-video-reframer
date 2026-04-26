import importlib
try:
    import gui.controller as gc
    print("import ok: GUIController methods:", hasattr(gc.GUIController, '_on_play_pause'))
except Exception as e:
    print("import failed:", e)
    raise
