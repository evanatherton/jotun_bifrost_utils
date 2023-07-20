"""

"""
import maya.cmds as cmds

import jotun.utils.ui_utils

# For Maya debugging
import importlib
importlib.reload(jotun.utils.ui_utils)


from jotun.utils.ui_utils import get_bif_container


def create_compound(bif_shape, container='/', name='expr'):
    """
    Creates a compound in a bifrost graph.

    Parameters
    ----------
    bif_shape : str
        The name of the target bifrost graph shape where the compound node is to be created.
    container : str, optional
        The path to an existing compound that we want to add our new compound to
    name : str, optional
        The name of the compound, by default 'jotun_expr'.

    Returns
    -------
    str
        The path of the created compound in the bifrost graph.
    """
    return cmds.vnnCompound(bif_shape, container, create=name)


def set_value(bif_shape, container, node_name, value):
    """
    Sets the value of a value node

    Parameters
    ----------
    bif_shape : str
        The name of the target bifrost graph shape where the compound node is to be created.
    container : str
        Path of the compound holding the node we want to modify
    node_name : str
        name of the node we want to set the value of
    value : float
        The value we want to set

    Returns
    -------

    """
    return cmds.vnnNode(bif_shape, container + '/{}'.format(node_name), setPortDefaultValues=['value', str(value)])


def delete_node(bif_shape, node_name, container='/'):
    """

    Parameters
    ----------
    bif_shape : str
        The name of the target bifrost graph shape where the compound node is to be created.
    node_name : str
        Name of the node we want to delete
    container : str, optional
        The path to an existing compound that holds the node we want to delete.
        Defaults to the top-level graph

    Returns
    -------

    """
    return cmds.vnnCompound(bif_shape, container, removeNode=node_name)


def create_node(bif_shape, container, node_type):
    """
    Creates a node in a bifrost graph compound.

    Parameters
    ----------
    bif_shape : str
        The name of the target bifrost graph where the node is to be created.
    container : str
        The path of the compound in the bifrost graph where the node is to be added.
    node_type : str
        The type of the node to be created.

    Returns
    -------
    str
        The path of the created node in the bifrost graph.
    """
    return cmds.vnnCompound(bif_shape, container, addNode='BifrostGraph,{}'.format(node_type))[0]


def create_node_input_port(bif_shape, container, node_name, port_name='input', port_type='auto'):
    """
    Creates an input port on the given node and returns the name

    Parameters
    ----------
    bif_shape : str
        The name of the target bifrost graph that holds the node
    container : str
        The path of the compound in the bifrost graph that holds the node
    node_name : str
        The name of the node to add the port to
    port_name : str, optional
        The name of the input port, by default 'input'.
    port_type : str, optional
        The type of the output port, by default 'auto', which means the type will be automatically inferred.

    Returns
    -------
    str
        Name of the input port on the given compound
    """
    # TODO: Stripping the output port and then taking the last input port added to get the actual port name.
    # TODO: replace with output port query when I figure it out
    # Create port
    cmds.vnnNode(bif_shape, container + '/{}'.format(node_name), createInputPort=(port_name, port_type))

    # Query the port for its actual name
    return cmds.vnnNode(bif_shape, container + '/{}'.format(node_name), lp=True)[:-1][-1]


def create_compound_output_port(bif_shape, compound_path, port_name='output', port_type='auto'):
    """
    Creates an output port on the given compound and returns the name

    Parameters
    ----------
    bif_shape : str
        The name of the target bifrost graph where the output port is to be created.
    compound_path : str
        The path of the compound in the bifrost graph where the output port is to be added.
    port_name : str, optional
        The name of the output port, by default 'output'.
    port_type : str, optional
        The type of the output port, by default 'auto', which means the type will be automatically inferred.

    Returns
    -------
    str
        Name of the output port on the given compound
    """
    # Create the port
    cmds.vnnCompound(bif_shape, compound_path, createOutputPort=(port_name, port_type))

    # Get the name of the port we just created. This might differ from the input name if the added port was renamed
    # by Bifrost on creation to avoid a name conflict with another output port
    # TODO: Using [-1] here but replace with output port query when I figure it out
    return cmds.vnnCompound(bif_shape, compound_path, lp=True)[-1]


def create_compound_input_port(bif_shape, compound_path, port_name='input', port_type='auto', skip_existing=False):
    """
    Creates an input port on the given compound and returns the name

    Parameters
    ----------
    bif_shape : str
        The name of the target bifrost graph where the input port is to be created.
    compound_path : str
        The path of the compound in the bifrost graph where the input port is to be added.
    port_name : str, optional
        The name of the input port, by default 'input'.
    port_type : str, optional
        The type of the input port, by default 'auto', which means the type will be automatically inferred.
    skip_existing : bool, optional
        If True, a new port will not be created if one with the input name already exists. If False, it will create a
        new port, which Bifrost will rename to kep its name unique. False by default

    Returns
    -------
    str
        Name of the input port on the given compound
    """
    # If we want to skip existing ports
    ports = cmds.vnnCompound(bif_shape, compound_path, lp=True)
    if ports and skip_existing:
        # And the port does exist
        if port_name in ports:
            # Then return without creating a new port
            return

    # Create the port
    cmds.vnnCompound(bif_shape, compound_path, createInputPort=(port_name, port_type))

    # Get the name of the port we just created. This might differ from the input name if the added port was renamed
    # by Bifrost on creation to avoid a name conflict with another output port
    # TODO: Using [-1] here but replace with output port query when I figure it out
    return cmds.vnnCompound(bif_shape, compound_path, lp=True)[:-1][-1]


def get_node_output_port(bif_shape, container, node_name):
    """
    Gets the name of the output port on the given node

    Note: This is assumes our target only has one output port, which happens to be true for all the math operations
    we're using

    Parameters
    ----------
    bif_shape : str
        The name of the target bifrost graph
    container : str
        The path of the compound in the bifrost graph where the node is
    node_name
        The name of the node that we want to get the output port from

    Returns
    -------
    str
        Path of the output port
    """
    return cmds.vnnNode(bif_shape, container + '/{}'.format(node_name), lp=True)[-1]


def get_or_create_input_port(bif_shape, container, node_name):
    """
    Gets the first available input port with no connection. If no input ports exist, it creates one

    Parameters
    ----------
    bif_shape : str
        The name of the target bifrost graph
    container : str
        The path of the compound in the bifrost graph where the node is
    node_name
        The name of the node that we want to get or create the port on

    Returns
    -------
    str
        Path to existing or created port
    """
    # Find the first one without a connection, or if there are no available ports, create one
    return find_first_unconnected_port(bif_shape, container, node_name) or create_node_input_port(bif_shape, container, node_name)


def find_first_unconnected_port(bif_shape, container, node_name):
    """
    Return the first unconnected port from a list of ports on the input node.

    Parameters
    ----------
    bif_shape : str
        The name of the target bifrost graph
    container : str
        The path of the compound in the bifrost graph where the node is
    node_name
        The name of the node that we want to check

    Returns
    -------
    str
        The first unconnected port, or None if all ports are connected.
    """
    # TODO: replace this with checking explicitly for input ports when I figure it out
    all_input_ports = cmds.vnnNode(bif_shape, container + '/{}'.format(node_name), lp=True)[:-1]
    connected_ports = cmds.vnnNode(bif_shape, container + '/{}'.format(node_name), lp=True, connected=True)

    if connected_ports:
        # Convert connected_ports to a set for efficient lookups
        connected_ports_set = set(connected_ports)

        # Loop over all_ports and return the first port that is not in connected_ports_set
        for port in all_input_ports:
            if port not in connected_ports_set:
                return port

    # If we didn't find an unconnected port, return None
    return None


def connect_output(bif_shape, container, node_name, output_port):
    """
    Connects the output port of the given node to the output port of its compound container

    Parameters
    ----------
    bif_shape : str
        The name of the target bifrost graph
    container : str
        The path of the compound in the bifrost graph where the node is
    node_name : str
        The name of the node that we want to connect
    output_port : str
        Path to the output port of the compound container

    Returns
    -------
    None
    """
    source_port = get_node_output_port(bif_shape, container, node_name)
    cmds.vnnConnect(bif_shape, container + '/{}'.format(source_port), container + '/output.{}'.format(output_port))


def connect_input(bif_shape, container, input_port, node_name):
    """
    Connects the output port of the given node to the output port of its compound container

    Parameters
    ----------
    bif_shape : str
        The name of the target bifrost graph
    container : str
        The path of the compound in the bifrost graph where the node is
    input_port : str
        Path to the input port of the compound container
    node_name : str
        The name of the node that we want to connect to the input

    Returns
    -------
    None
    """
    target_port = get_or_create_input_port(bif_shape, container, node_name)
    cmds.vnnConnect(bif_shape, container + '/input.{}'.format(input_port), container + '/{}'.format(target_port))


def connect(bif_shape, container, source, target, connection_type='node'):
    """
    Connects the output port of source to the first unconnected input port on target.

    When connection_type='node' it connects the output of the source node to the input of the target node
    When connection_type='input' it connects the compound input port to the target input port
    When connection_type='output it connects the source node's output port to the compound's output port

    Parameters
    ----------
    bif_shape : str
        The name of the target bifrost graph
    container : str
        The path of the compound in the bifrost graph where the connection is to be made
    source : str
        The name of the source node.
    target : str
        The name of the target node.
    connection_type : str, optional
        The type of connection to be made. Can be 'node', 'input', or 'output'
        depending on the specific connection needs (default is 'node').

    Returns
    -------
    None
    """

    if connection_type == 'input':
        connect_input(bif_shape, container, source, target)
    elif connection_type == 'output':
        connect_output(bif_shape, container, source, target)
    else:
        source_port = get_node_output_port(bif_shape, container, source)
        target_port = get_or_create_input_port(bif_shape, container, target)

        cmds.vnnConnect(bif_shape, container + '/{}'.format(source_port), container + '/{}'.format(target_port))


def init_board(bif_shape):
    """
    Ensures the Bifrost Graph Editor window is open and the input bif_shape is the active tabe

    Parameters
    ----------
    bif_shape : str
        The name of the target bifrost graph shape

    Returns
    -------
    None
    """
    # If there is no active bifrost graph (i.e. open tab) in the Bifrost Graph Editor window, or the window is closed
    if not get_bif_container():
        cmds.vnnCompoundEditor(edit=bif_shape, name='bifrostGraphEditorControl')


def add_backdrop(bif_shape, compound_name, label, container='/'):
    """
    Adds a bifrost UI backdrop behind the
    
    Parameters
    ----------
    bif_shape : str
        The name of the target bifrost graph shape
    compound_name : str
        Name of the compound to add the backdrop behind
    label : str
        The label to set on the backdrop
    container : str
        Full path to the compound to add the backdrop behind

    Returns
    -------
    str
        Name of the backdrop object
    """
    cmds.refresh()
    # # Select the bifrost board to edit, making it the focused tab in the Bifrost Graph Editor
    # cmds.vnnCompoundEditor(edit=bif_shape, name='bifrostGraphEditorControl')

    # Select the compound to add the backdrop behind
    cmds.vnnCompoundEditor(name='bifrostGraphEditorControl', selectNodes=compound_name)

    # Add a backdrop behind the selected compound and set the title to the input text
    backdrop_name = compound_name + '_backdrop'
    cmds.vnnCompound(bif_shape, container, addBackdrop=backdrop_name)
    cmds.vnnCompound(bif_shape, container, setAnnotationMetaDataValue=[backdrop_name, 'title', label])

    return backdrop_name


def add_sticky_note(bif_shape, container, text, name='sticky_note', color='#ffa58bd7'):
    """
    Adds a sticky note behind inside the input compound with the given text and color

    Parameters
    ----------
    bif_shape : str
        The name of the target bifrost graph shape
    container : str
        Path to the compound that the sticky will be added inside
    text : str
        The text to add to the sticky
    name : str, optional
        The name of the sticky note object
        Default is 'sticky_note'
    color : str, optional
        Hex color code for the sticky note color
        Default is #ffa58bd7, which is purple-ish
        Must be one of Bifrost's default sticky colors:
            #ffb2b2b5 : gray
            #ffd78282 : red
            #ffe0a66c : orange
            #ffe2cc5c : yellow
            #ff53bc88 : green
            #ff7b99d5 : blue
            #ffa58bd7 : purple
            #ffd574a5 : pink

    Returns
    -------
    None
    """
    cmds.refresh()
    cmds.vnnCompound(bif_shape, container, addStickyNote=name)
    cmds.vnnCompound(bif_shape, container, setAnnotationMetaDataValue=[name, 'color', color])
    cmds.vnnCompound(bif_shape, container, setAnnotationMetaDataValue=[name, 'text', text])


def frame_compound(compound_path):
    """
    Send an 'f' keyboard keystroke to the Bifrost Graph Editor window to frame the compound in he window

    Parameters
    ----------
    compound_path : str
        Path to the compound to frame

    Returns
    -------
    None
    """
    cmds.refresh()

    # Select the compound to add the backdrop behind
    cmds.vnnCompoundEditor(name='bifrostGraphEditorControl', selectNodes=compound_path.split('/')[-1])

    cmds.vnnCompoundEditor(name='bifrostGraphEditorControl', sendKey=[70, 0])


def get_selected_bif_shapes():
    """
    Gets any bifrost graph shapes in the user selection of the Maya scene

    Returns
    -------
    list of str
        List of any bifrost graph shapes in the user selection

    """
    all_bif_shapes = cmds.ls(type='bifrostGraphShape')

    selected_bif_graph_shapes = []
    for sel in cmds.ls(sl=True):
        sel_shapes = cmds.listRelatives(sel, shapes=True)
        for sel_shape in sel_shapes:
            if sel_shape in all_bif_shapes:
                selected_bif_graph_shapes.append(sel_shape)
                continue

    return selected_bif_graph_shapes


def get_target_graph_shape():
    """
    Returns the target bifrostGraphShape in the current scene. Creates a new one if none exist.

    First checks to see if there are no Bifrost graphs in the scene and creates one if not. If there is already a graph,
    it checks to see if there's an active graph open in the Bifrost Graph Editor window. If there is at least one graph
    in the scene but none active in the Bifrost Graph Editor window, it returns the first Bifrost graph shape in the
    user selection if there is one, if not it returns the first listed graph in the scene

    Returns
    -------
    str
        Name of the target Bifrost Graph Sahep
    """
    bif_shapes = cmds.ls(type='bifrostGraphShape')

    # No existing bifrost graphs, create a new one.
    if not bif_shapes:
        cmds.CreateNewBifrostGraph()
        new_shape = cmds.ls(type='bifrostGraphShape')[0]
        return new_shape

    # Check for an active bifrost container in the Bifrost Graph Editor.
    bif_shape = get_bif_container() or get_selected_bif_shapes()
    if bif_shape:
        # get_selected_bif_shapes might return a list, so we ensure bif_shape is a single item here.
        return bif_shape[0] if isinstance(bif_shape, list) else bif_shape

    # Fall back to the first graph in the scene.
    return bif_shapes[0]


def get_compound_container():
    """
    Gets the path to the compound that is being edited in the Bifrost Graph Editor window

    Returns
    -------
    str
        Path to the bifrost compound being edited in the Bifrost Graph Editor window
    """
    return cmds.vnnCompoundEditor(query=True, currentCompound=True, name='bifrostGraphEditorControl')

