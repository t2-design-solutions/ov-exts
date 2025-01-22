import omni.kit.commands
import omni.ext
import carb
import os

class MainModel:
    def __init__(self):
        # Default mode is Disabled (0)
        self._selected_mode = 0  # 0: Disabled, 1: Deuteranopia, 2: Protanopia, 3: Tritanopia
        self._preset_files = {
            1: "Deuteranopia.ini",
            2: "Protanopia.ini",
            3: "Tritanopia.ini",
        }
        self._extension_root = self._get_extension_root()

    def _get_extension_root(self):
        """Retrieve the extension root directory and append the correct subdirectory."""
        ext_manager = omni.kit.app.get_app().get_extension_manager()
        ext_id = ext_manager.get_extension_id_by_module(__name__)
        ext_path = ext_manager.get_extension_path(ext_id)

        # Append the subfolder t2ds/visionsimulator
        return os.path.join(ext_path, "t2ds", "visionsimulator")

    def mode_changed(self, mode_index: int):
        """
        Update the selected vision mode.

        Args:
            mode_index (int): Index of the selected mode.
        """
        self._selected_mode = mode_index
        mode_name = ["Disabled", "Deuteranopia", "Protanopia", "Tritanopia"][mode_index]
        carb.log_info(f"Vision mode updated to: {mode_name}")

    def activate(self):
        """
        Activate reshade with the selected vision mode.
        If Disabled is selected, turn reshade off.
        """
        if self._selected_mode == 0:  # Disabled mode
            omni.kit.commands.execute(
                "ChangeSetting",
                path="/rtx/reshade/enable",
                value=False
            )
            carb.log_info("Reshade disabled.")
            return

        # Define asset and preset paths based on extension root
        effect_search_path = os.path.join(self._extension_root, "assets")
        texture_search_path = os.path.join(self._extension_root, "assets")
        preset_file_path = os.path.join(
            self._extension_root, "presets", self._preset_files[self._selected_mode]
        )

        # Convert paths to consistent format
        effect_search_path = effect_search_path.replace("\\", "/")
        texture_search_path = texture_search_path.replace("\\", "/")
        preset_file_path = preset_file_path.replace("\\", "/")

        # Log paths for debugging
        carb.log_info(f"Effect Search Path: {effect_search_path}")
        carb.log_info(f"Texture Search Path: {texture_search_path}")
        carb.log_info(f"Preset File Path: {preset_file_path}")

        # 1. Set Effect Search Directory
        omni.kit.commands.execute(
            "ChangeSetting",
            path="/rtx/reshade/effectSearchDirPath",
            value=effect_search_path
        )

        # 2. Set Texture Search Directory
        omni.kit.commands.execute(
            "ChangeSetting",
            path="/rtx/reshade/textureSearchDirPath",
            value=texture_search_path
        )

        # 3. Set Preset File Path
        omni.kit.commands.execute(
            "ChangeSetting",
            path="/rtx/reshade/presetFilePath",
            value=preset_file_path
        )

        # 4. Enable Reshade
        omni.kit.commands.execute(
            "ChangeSetting",
            path="/rtx/reshade/enable",
            value=True
        )
