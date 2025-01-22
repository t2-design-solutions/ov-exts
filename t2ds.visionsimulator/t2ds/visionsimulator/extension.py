import carb
import omni.ext
from .main import MainModel
from .views import MainView


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`)
# will be instantiated when extension gets enabled and `on_startup(ext_id)` will be called.
# Later when extension gets disabled on_shutdown() is called
class MyExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.

    def on_startup(self, ext_id):
        carb.log_info(f"[Vision Simulator] Extension startup")
        Model = MainModel()
        self._window = MainView(Model)

    def on_shutdown(self):
        carb.log_info(f"[Vision Simulator] Extension shutdown")
        self._window.destroy()
        self._window = None      