#  import from omniverse
import omni.ui as ui
from omni.ui.workspace_utils import TOP
#  import from other extension py
from .main import MainModel


class MainView():
    def __init__(self, cbmodel: MainModel):
        self._window = ui.Window("Vision Simulator", width=800, height=600, dockPreference=ui.DockPreference.RIGHT_TOP)
        self._window.visible = True
        cbmodel.csv_field_model = None

        with self._window.frame:
            with ui.VStack(alignment=TOP, style={"margin":5}):
                # 2 - parameters to be set, in case not default values
                with ui.VStack():
                    with ui.HStack(height=20):
                        ui.Label("Vision Impairment Mode:", height=0)
                        mode_combo = ui.ComboBox(0, "Disabled", "Deuteranopia (Green)", "Protanopia (Red)", "Tritanopia (Blue)")
                        mode_combo.model.add_item_changed_fn(
                            lambda m, 
                            f=mode_combo: cbmodel.mode_changed(m.get_item_value_model().get_value_as_int()))
                    
                ui.Line(style={"color": 0xff00b976}, height=20)
                # 3 - button to populate the 3D scene
                ui.Button( "Activate", height=50, clicked_fn=lambda: cbmodel.activate())
    
    def destroy(self):
        self._window.destroy()
        self._window = None