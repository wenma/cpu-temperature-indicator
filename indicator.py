
import os
import base64
import gi
import time
import sys
import tempfile
from functools import reduce
from datetime import datetime

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GLib

icon = """
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
"""

class CpuTemperatureIndicator(object):
    def __init__(self, icon_path, max_cache_len=3):
        self.indicator = AppIndicator3.Indicator.new(self.__class__.__name__, icon_path,
                                                     AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)

        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_ordering_index(0)

        self.menu = Gtk.Menu()
        self.current_hz_menu = Gtk.MenuItem()
        self.indicator.set_menu(self.menu)

        self._running = True
        self.format = ' {}°C'
        self.hwmon = '/sys/class/hwmon/'

        self.cache = []
        self.max_cache_len = max_cache_len

    def detect(self):
        for _, dirs, _ in os.walk(self.hwmon, False):
            for hwmon in dirs:
                full_name = os.path.join(self.hwmon, hwmon, 'name')
                with open(full_name, 'r') as f:
                    if f.read().strip() == 'coretemp':
                        log('find coretemp hwmon in %s' % os.path.join(self.hwmon, hwmon))
                        return os.path.join(self.hwmon, hwmon, 'temp1_input')

    def token(self):
        with open(self.hwmon, 'r') as f:
            return int(f.read())

    def generate_menu(self):
        quit_menu = Gtk.MenuItem(label='close')
        quit_menu.connect('activate', self.quit)
        self.menu.add(self.current_hz_menu)
        self.menu.add(quit_menu)
        self.menu.show_all()

    def update(self):
        if not self._running:
            return False

        self.cache.append(self.token())
        if len(self.cache) > self.max_cache_len:
            self.cache.pop(0)

        token = reduce(lambda x, y: x + y, self.cache) / len(self.cache)
        label = self.format.format(str(round(token / 1000.0, 1)))
        self.indicator.set_label(label, '')
        return True

    def run(self, refresh_interval=1):
        self.hwmon = self.detect()
        self.generate_menu()
        self.update()
        GLib.timeout_add_seconds(refresh_interval, self.update)
        Gtk.main()

    def quit(self, item=None):
        self._running = False
        Gtk.main_quit()


def log(msg):
    sys.stdout.write(u"[%s] -- %s\n" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg))
    sys.stdout.flush()


def main():
    _, path = tempfile.mkstemp(suffix=".png")
    with open(path, "wb") as f:
        log('temp icon file path: %s' % path)
        content = base64.b64decode(icon)
        f.write(content)

    app = CpuTemperatureIndicator(icon_path=path, max_cache_len=3)
    try:
        app.run(refresh_interval=2)
    except KeyboardInterrupt:
        app.quit()
    finally:
        os.remove(path)


if __name__ == '__main__':
    main()
