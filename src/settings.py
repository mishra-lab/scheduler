import json
import os


class SettingsManager:
    """
    Allows to easily read and write to settings file.

    Use inside ```with``` statement
    """

    def __init__(self, settings_file):
        self._settings_file = settings_file
        self._dirname = os.path.dirname(self._settings_file)

        with open(self._settings_file, 'r') as f:
            self._json = json.load(f)

    def get_path_from_key(self, key):
        """
        Returns path assuming same directory as the settings file.

        Useful when retrieveing a setting that stores a relative path
        """
        path = self[key]
        if path:
            return os.path.normpath(
                os.path.join(self._dirname, path)
            )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._write()

    def __getitem__(self, key):
        if key in self._json:
            return self._json[key]
        return None

    def __setitem__(self, key, value):
        self._json[key] = value

    def _write(self):
        with open(self._settings_file, 'w') as f:
            json.dump(self._json, f, sort_keys=True, indent=4)
