import urwid
import asyncio
import uuid
import logging

log = logging.getLogger('eventloop')


class EventLoopException(Exception):
    """ Problem with eventloop
    """
    pass


class EventLoop:

    """ Abstracts out event loop
    """
    loop = None
    alarms = {}

    @classmethod
    def build_loop(cls, ui, palette, **kwargs):
        """ Builds eventloop
        """
        extra_opts = {
            'screen': urwid.raw_display.Screen(),
            'handle_mouse': True
        }
        extra_opts['screen'].set_terminal_properties(colors=256)
        extra_opts['screen'].reset_default_terminal_palette()
        extra_opts.update(**kwargs)
        evl = asyncio.get_event_loop()
        cls.loop = urwid.MainLoop(ui, palette,
                                  event_loop=urwid.AsyncioEventLoop(loop=evl),
                                  pop_ups=True,
                                  **extra_opts)

    @classmethod
    def exit(cls, err=0):
        log.info("Stopping eventloop")
        raise urwid.ExitMainLoop()

    @classmethod
    def redraw_screen(cls):
        try:
            cls.loop.draw_screen()
        except AssertionError as e:
            log.exception("exception failure in redraw_screen")
            raise e

    @classmethod
    def set_alarm_in(cls, interval, cb):
        return cls.add_alarm(cls.loop.set_alarm_in(interval, cb),
                             str(uuid.uuid1()))

    @classmethod
    def add_alarm(cls, handle, name):
        if name in cls.alarms:
            cls.loop.remove_alarm(cls.alarms[name])
        cls.alarms[name] = handle

    @classmethod
    def remove_alarm(cls, handle):
        return cls.loop.remove_alarm(handle)

    @classmethod
    def remove_alarms(cls):
        for alarm in cls.alarms.values():
            cls.loop.remove_alarm(alarm)
        cls.alarms = {}

    @classmethod
    def run(cls):
        """ Run eventloop
        """
        try:
            cls.loop.run()
        except:
            log.exception("Exception in ev.run():")
            raise
        return
