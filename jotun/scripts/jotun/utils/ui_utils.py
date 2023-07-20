from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui


BIF_TAB_WIDGET_NAME = 'VNN_Node_Tab_Widget'


def get_qt_widget_by_name(name, widget_type):
    """
    Fetches a Qt widget pointer by its name and wraps it in the input type using shiboken2.

    Parameters
    ----------
    name : str
        The name of the widget.
    widget_type : QObject
        The type of the widget.

    Returns
    -------
    widget : widget or None
        The found widget of the specified type and name. If no widget is found, returns None.
    """
    # Get the pointer to the widget
    ptr = omui.MQtUtil.findControl(name)

    if ptr is not None:
        # Wrap the pointer to get the QWidget
        widget = wrapInstance(int(ptr), widget_type)
        return widget
    else:
        return None


def get_qt_widgets_by_type(parent, widget_type):
    """
    Recursively fetches all Qt widgets of a specific type from a given parent widget.

    Parameters
    ----------
    parent : QObject
        The parent widget from which to search for child widgets.
    widget_type : QObject
        The type of the widgets to search for.

    Returns
    -------
    widgets : list
        The list of widgets of the specified type.
    """
    # If the parent is of widget_type, add it to the list
    widgets = []
    if isinstance(parent, widget_type):
        widgets.append(parent)

    # Otherwise, recursively check all children
    for child in parent.children():
        widgets += get_qt_widgets_by_type(child, widget_type)

    # Return the list of widgets
    return widgets


def get_tab_names(tab_widget):
    """
    Retrieves the names of all tabs within a given tab widget.

    Parameters
    ----------
    tab_widget : QTabWidget
        The widget containing the tabs.

    Returns
    -------
    names : list
        A list of names of all tabs in the given tab widget.
    """
    # List to store the names
    names = []

    # Loop over all tabs in all tab_widgets
    for i in range(tab_widget.count()):
        names.append(tab_widget.tabText(i))

    return names


def get_tab_widget_names(tab_widgets):
    """
    Retrieves the names of all tab widgets in a list of QTabWidgets.

    Parameters
    ----------
    tab_widgets : list
        The list of QTabWidgets.

    Returns
    -------
    names : list
        A list of names of all tab widgets in the given list.
    """
    return [tw.objectName() for tw in tab_widgets]


def get_focused_tab(tab_widget_name):
    """
    Returns the name of the currently focused tab within a given tab widget.

    Parameters
    ----------
    tab_widget_name : str
        The name of the tab widget.

    Returns
    -------
    tab_name : str or None
        The name of the currently focused tab, or None if no tab is focused.
    """
    tab_widget = get_qt_widget_by_name(tab_widget_name, QtWidgets.QTabWidget)

    if not tab_widget:
        return None

    if isinstance(tab_widget, QtWidgets.QTabWidget):
        current_index = tab_widget.currentIndex()
        return tab_widget.tabText(current_index)
    else:
        return None


def get_bif_container():
    """
    Retrieves the name of the active graph in the Bifrost Graph editor.

    Returns
    -------
    name : str or None
        The name of the active graph, or None if no graph is active.
    """
    # Check if the Bifrost Graph Editor is open and that there is an active graph

    tab_widget = get_qt_widget_by_name(BIF_TAB_WIDGET_NAME, QtWidgets.QTabWidget)

    # If the Bifrost Graph Editor is closed, there will be no tab widget.
    # Or if it's open but there is no active graph, the tab_widget will have no currentWidget.
    if not tab_widget or not tab_widget.currentWidget():
        return None

    # If the Bifrost Graph editor is open and there is an active graph, get the name of the active graph shape
    # This is somewhat of a hack but is unfortunately the only way to get the bifrost shape name for the active tab
    # as the active tab name and the bifrost shape might be different, but the name of this button always corresponds
    # to the bifrost graph shape name
    btn = tab_widget.currentWidget().children()[1].children()[1].children()[4]

    return btn.text()
