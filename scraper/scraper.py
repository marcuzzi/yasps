from .checks import *
from datetime import datetime
import time
import winsound
import curses
import pynput
from pynput.keyboard import Key, Listener
from urllib.parse import urlsplit

def in_stock(ia):
    return (ia == ItemAvailability.InStock or ia ==ItemAvailability.Reseller)

def in_price(price, target):
    if price is None or target is None:
        return False
    else:
        return price<target

# --------------------------------------------------------------------------------------------------
# CURSES

COL_WHITE = 1
COL_BLACK_RED = 2
COL_BLACK_GREEN = 3
COL_RED = 4
COL_GREEN = 5
COL_CYAN =6
COL_YELLOW = 7

def run_monitor_curses(monitor, stdscr, row):
    stdscr.addstr(row, 1, monitor.item + " <<< " + str(monitor.targetPrice) + " EUR", curses.color_pair(7))
    itemrow = row + 1
    statuses = []
    anyInStock = False
    minPrice = None
    for check in monitor.checks:
        now = datetime.now()
        stdscr.addstr(itemrow, 2, "[" + now.strftime("%H:%M:%S") + "]", curses.color_pair(1))
        display_str = check.item if monitor.differentItems else check.shop
        stdscr.addstr(itemrow, 14, display_str, curses.color_pair(COL_WHITE))
        stdscr.addstr(itemrow, 70, " Chequeando", curses.color_pair(COL_WHITE))
        stdscr.refresh()
        status = check.run()
        statuses.append(status)
        price_color = COL_YELLOW
        if in_stock(status.availability):
            anyInStock = True
            if status.availability == ItemAvailability.InStock:
                stdscr.addstr(itemrow, 70, " En Stock  ", curses.color_pair(COL_BLACK_GREEN))
            else:
                stdscr.addstr(itemrow, 70, " Reseller  ", curses.color_pair(COL_BLACK_GREEN))
            if in_price(status.price, monitor.targetPrice):
                minPrice = status.price if minPrice is None else min(minPrice, status.price)
                price_color = COL_GREEN
        elif status.availability == ItemAvailability.OutOfStock:
            stdscr.addstr(itemrow, 70, " Sin Stock ", curses.color_pair(COL_BLACK_RED))
        else:
            stdscr.addstr(itemrow, 70, "Desconocido", curses.color_pair(COL_BLACK_RED))
        if (status.price is not None):
            stdscr.addstr(itemrow, 55, "{:8.2f} ".format(status.price), curses.color_pair(price_color))
        else:
            stdscr.addstr(itemrow, 55, "--------", curses.color_pair(price_color))
        itemrow = itemrow + 1
        stdscr.refresh()
    title_color = COL_GREEN if minPrice is not None else COL_YELLOW
    stdscr.addstr(row, 1, monitor.item + " <<< " + str(monitor.targetPrice) + " EUR", curses.color_pair(title_color))
    stdscr.refresh()
    return anyInStock, minPrice is not None

class logger_curses():
    def __init__(self, screen):
        screen.box()
        screen.refresh()
        y, x = screen.getmaxyx()
        self.screen = screen.derwin(y-2, x-2, 1, 1)
        self.screen.nodelay(True)
        self.screen.scrollok(True)
        self.screen.idlok(True)
        self.screen.leaveok(True)
        self.screen.refresh()
        self.first = True
    def info(self, msg):
        try:
            screen = self.screen
            fs = "\n"
            line = "[" + datetime.now().strftime("%H:%M:%S") + "] "+ msg
            if not self.first:
                line = fs + line
            screen.addstr(line)
            screen.refresh()
            self.first = False
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            raise    
    def emit(self, item, status):
        try:
            screen = self.screen
            fs = "\n"
            line = "[" + datetime.now().strftime("%H:%M:%S") + "] "+ item + ": " + status
            if not self.first:
                line = fs + line
            screen.addstr(line)
            screen.refresh()
            self.first = False
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            raise

def beep_curses(repeats, window):
    # Alerta sonora
    while repeats > 0:
        frequency = 2500
        duration = 1000
        winsound.Beep(frequency, duration)
        time.sleep(2)
        repeats = repeats - 1
        if escape_pressed_curses(window):
            repeats = 0

def escape_pressed_curses(window):
    c = window.getch()
    if c == ord('q'):
        return True
    elif c == 27:
        return True
    return False

def main_curses(stdscr, monitors, interval_min, interval_max, beep):
    global log
    curses.start_color()
	
    curses.init_pair(COL_WHITE, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(COL_BLACK_RED, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(COL_BLACK_GREEN, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(COL_RED, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(COL_GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(COL_CYAN, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(COL_YELLOW, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    curses.noecho()
    curses.curs_set(0)
    curses.cbreak()
	
    rows, cols = stdscr.getmaxyx()
	
    mainwin = curses.newwin(rows-10, cols, 0, 0)
    mainwin.nodelay(True)
    mainwin.clear()

    mainwin.addstr(0, 0, "Monitorizando stock online ("+ str(interval_max) +"s)", curses.color_pair(COL_CYAN))
    
    logbox = curses.newwin(10, cols, rows-10, 0)
    log = logger_curses(logbox)   

    anyInPrice = False
    while True:
        startTime = time.time()
        row = 1
        for monitor in monitors:
            inStock, inPrice = run_monitor_curses(monitor, mainwin, row)
            log.emit(monitor.item, "En stock" if inStock else "Sin stock")
            anyInPrice = anyInPrice or inPrice
            row = row + monitor.get_count() + 1
            if escape_pressed_curses(mainwin):
                return
        mainwin.refresh()
        endTime = time.time()
        elapsedTime = int(endTime - startTime)
        waitTime = max((interval_max - elapsedTime), interval_min)
        if anyInPrice and beep:
            beep_curses(5, mainwin)
        for i in range(0, waitTime):
            time.sleep(1)
            if escape_pressed_curses(mainwin):
                return