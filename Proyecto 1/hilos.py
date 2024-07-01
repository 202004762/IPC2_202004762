import threading
import ctypes
from pygame import mixer 


class TPlay(threading.Thread):
    def __init__(self, ruta):
        threading.Thread.__init__(self)
        self.ruta = ruta
        self.estado = ""

    def run(self):
        mixer.init()
        mixer.music.load(self.ruta)
        mixer.music.set_volume(0.8)
        mixer.music.play()  # Añadí los paréntesis aquí
        while True:
            if self.estado == 'p':
                mixer.music.pause()
            elif self.estado == 'r':
                mixer.music.unpause()
            elif self.estado == 'e':
                mixer.music.stop()
                break

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._tread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))

        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')