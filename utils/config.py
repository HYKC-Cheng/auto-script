import pygetwindow as gw


# 获取窗口大小
def initialize_window_dimensions():
    global window_left, window_top, window_width, window_height
    active_window = gw.getActiveWindow()
    x, y, width, height = active_window.left, active_window.top, active_window.width, active_window.height
    window_left, window_top, window_width, window_height = x, y, width, height


initialize_window_dimensions()
