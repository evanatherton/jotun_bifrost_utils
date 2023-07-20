"""
Main module that runs the Jotun plugin
"""
from sympy import sympify, SympifyError, srepr

import maya.cmds as cmds

# For debugging in Maya
import importlib
import jotun.utils.bif_utils
import jotun.expr_to_compound.compound_builder
importlib.reload(jotun.utils.bif_utils)
importlib.reload(jotun.expr_to_compound.compound_builder)

from jotun.utils.bif_utils import init_board, add_backdrop, add_sticky_note, frame_compound, get_target_graph_shape
from jotun.expr_to_compound.compound_builder import CompoundBuilder


def get_user_input():
    """
    Creates a promptDialog for the user to input an expression

    Returns
    -------
    string
        User input expression
    """
    # Show the prompt dialog.
    result = cmds.promptDialog(
        title='',
        message='Enter Equation:',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel')

    # If the user clicked 'OK', return the input text
    if result == 'OK':
        expr = cmds.promptDialog(query=True, text=True)

        return expr


def validate_expr(expr):
    """
    Takes an expression as a string and check if it's valid

    Parameters
    ----------
    expr : str
        Mathematical expression represented as a string

    Returns
    -------
    bool
        True if the expression is valid
        False otherwise
    """
    try:
        sympify(expr)
        return True
    except SympifyError:
        return False


def main():
    """
    This is where the magic happens. It launches the UI for user input, then takes the input, builds the compound
    and adds it to the bifrost graph.

    This is typicalled called from the exprToCompound.py Maya command plugin found in jotun/plug-ins

    Returns
    -------

    """
    expr = get_user_input()

    if expr is None:
        return

    if not validate_expr(expr):
        cmds.inViewMessage(amg='Invalid expr: <hl>' + expr + '</hl>', pos='midCenter', fade=True)
        return

    # We have a valid expr
    parsed_expr = sympify(expr)

    # Find the target bifrost graph to add the compound too and make sure the Bifrost Graph Editor is open
    bif_shape = get_target_graph_shape()
    init_board(bif_shape)

    # Build the compound from the parsed expression
    builder = CompoundBuilder(parsed_expr, bif_shape)

    # Add a backdrop to the compound with the expression as the label
    add_backdrop(bif_shape, builder.compound_path.split('/')[-1], expr, builder.compound_container)

    # Add a sticky not inside the compound which shows the parsed representation of the expression
    # This is helpful to show how sympy might have simplified an expression. For example, if the user inputs 'x - y'
    # the sympy representation becomes `Add(Symbol('x'), Mul(Integer(-1), Symbol('y')))`
    sticky_text = expr + ' --> ' + str(srepr(parsed_expr))
    add_sticky_note(bif_shape, builder.compound_path, sticky_text)

    # Frame the compound in the Bifrost Graph Editor
    frame_compound(builder.compound_path)

    # TODO Add HUD message saying node created successfully and give node name
    return builder
