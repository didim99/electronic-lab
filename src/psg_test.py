import os
import time
from datetime import datetime
from io import BytesIO
from pathlib import Path

from PIL import Image

from psg9080 import PSG9080
from ds1054z import DS1054Z


def start():
    wd = Path(os.getcwd())
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    data_path = wd / "data" / now
    data_path.mkdir(parents=True)

    dds = PSG9080('/dev/ttyUSB0')
    dds.connect()
    scope = DS1054Z('rigol.home.loc')
    scope.open()
    time.sleep(3)

    dds.on(channel=1)
    for freq in range(100, 1000, 100):
        print(f'Frequency: {freq} Hz')
        dds.frequency(channel=1, frequency=freq)
        time.sleep(0.5)
        print(f'Taking screenshot...')
        im = Image.open(BytesIO(scope.display_data))
        filename = data_path / f'image-{freq}.png'
        im.save(filename, 'PNG')
        print(f'Screenshot saved to {filename}')
        time.sleep(0.5)
    dds.off(channel=1)

    dds.disconnect()
    scope.close()

if __name__ == '__main__':
    start()
