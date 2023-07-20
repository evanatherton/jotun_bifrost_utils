import sys
import maya.api.OpenMaya as OpenMaya
from jotun.expr_to_compound import expr_to_compound

import importlib

importlib.reload(expr_to_compound)


def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass


class exprToCompound(OpenMaya.MPxCommand):
    kPluginCmdName = 'exprToCompound'

    def __init__(self):
        super(exprToCompound, self).__init__()

        self.builder = None

    # Creator
    @staticmethod
    def cmdCreator():
        return exprToCompound()

    def doIt(self, args):
        self.builder = expr_to_compound.main()
        # self.result = expr_to_compound.main()
        # self.setResult(self.result)

    def undoIt(self):
        # The undoIt method should implement the logic to reverse
        # the operations performed in the doIt method. This would depend
        # on the specifics of what expr_to_compound.main() is doing.
        pass

    def isUndoable(self):
        return True


def initializePlugin(mobject):
    """
    Initialize the plug-in when Maya loads it.
    """
    mplugin = OpenMaya.MFnPlugin(mobject)
    try:
        mplugin.registerCommand(exprToCompound.kPluginCmdName, exprToCompound.cmdCreator)
    except:
        sys.stderr.write('Failed to register command: ' + exprToCompound.kPluginCmdName)


def uninitializePlugin(mobject):
    """
    Uninitialize the plug-in when Maya un-loads it.
    """
    mplugin = OpenMaya.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(exprToCompound.kPluginCmdName)
    except:
        sys.stderr.write('Failed to unregister command: ' + exprToCompound.kPluginCmdName)
