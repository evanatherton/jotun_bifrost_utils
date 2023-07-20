"""

"""
from queue import Queue

from sympy import preorder_traversal, Symbol

# For debugging in Maya
import importlib
import jotun.utils.bif_utils
import jotun.expr_to_compound.node_mapper
importlib.reload(jotun.utils.bif_utils)
importlib.reload(jotun.expr_to_compound.node_mapper)

from jotun.utils.bif_utils import create_compound, create_node, create_compound_output_port, connect,\
    create_compound_input_port, set_value, delete_node, get_compound_container
from jotun.expr_to_compound.node_mapper import NodeMapper


class CompoundBuilder:
    """
    A class used to build a bifrost compound from a SymPy expression.

    Attributes
    ----------
    sympy_expr : sympy expression
        A sympy expression to be converted to Bifrost graph.
    bif_shape : str
        The name of the Bifrost graph shape the compound will be added to.
    compound_path : str
        The path to the Bifrost compound created for the given Bifrost graph shape.
    output_port : str
        The path to the output port of the compound.
    nodes : dict
        A dictionary to store the nodes of the compound.
    queue : Queue
        A Queue object to manage the process flow for connecting the nodes.
    mapper : NodeMapper
        A NodeMapper object to map the sympy operators to bifrost nodes.

    Methods
    -------
    compound_container:
        Property method to get the current compound container.
    """

    def __init__(self, sympy_expr, bif_shape='bifrostGraphShape1'):
        """
        Constructs all the necessary attributes for the CompoundBuilder object.

        Parameters
        ----------
        sympy_expr : sympy expression
            A sympy expression to be converted to Bifrost graph.
        bif_shape : str, optional
            The name of the Bifrost graph shape (default is 'bifrostGraphShape1').
        """
        self.sympy_expr = sympy_expr
        self.bif_shape = bif_shape
        self.compound_path = create_compound(self.bif_shape, self.compound_container)
        self.output_port = create_compound_output_port(self.bif_shape, self.compound_path)
        self.nodes = {}
        self.queue = Queue()
        self.mapper = NodeMapper()

        try:
            self._build_graph()
            self._connect_nodes()
        except Exception as e:
            # Return the exception
            raise e

    @property
    def compound_container(self):
        return get_compound_container()

    def _create_node_mapping(self, sympy_obj):
        """
        Maps the input sumpy_obj to a corresponding bifrost node and adds it to the self.nodes dict

        Parameters
        ----------
        sympy_obj : sympy.core.basic.Basic
            The SymPy object that we want to get or create a node for.

        Returns
        -------
        None
            Creates a bifrost node for the input sympy object, if necessary, and stores the relationship in self.nodes
        """
        # If the node already exists, return it.
        if sympy_obj in self.nodes:
            return

        # Otherwise, create a new node
        # If the SymPy object is a Symbol, mark it as an input
        if isinstance(sympy_obj, Symbol):
            node = 'input'
            create_compound_input_port(self.bif_shape, self.compound_path, port_name=sympy_obj.name, skip_existing=True)
        # If the SymPy object is an operation, create a bifrost node
        else:
            # Get node type mapping
            bif_node_type = self.mapper.get_mapping(sympy_obj.func)

            # If there is no matching bif type, raise an exception and delete the in-progress compound
            if not bif_node_type:
                node_name = self.compound_path.split('/')[-1]
                delete_node(self.bif_shape, node_name, self.compound_container)
                raise Exception(
                    'expression_to_compound::CompoundBuilder -- No bifrost node for sympy object {}'.format(sympy_obj))

            node = create_node(self.bif_shape, self.compound_path, bif_node_type)

            # If the bifrost node is a value node, set the value
            if bif_node_type == 'Core::Constants,float':
                set_value(self.bif_shape, self.compound_path, node, sympy_obj.evalf())

        # Add the newly create bifrost node to the self.nodes dict
        self.nodes[sympy_obj] = node
        return

    def _build_graph(self):
        """
        Build a queue with paired target-source nodes to be connected from the given SymPy expression
        using Breadth First Search
        """
        for obj in preorder_traversal(self.sympy_expr):
            self._create_node_mapping(obj)

            # If the SymPy object is an operation, connect its arguments
            if not isinstance(obj, Symbol):
                for arg in obj.args:
                    self._create_node_mapping(arg)
                    self.queue.put((arg, obj))

    def _connect_nodes(self):
        """
        Process the queue and build the connections between the nodes.
        """
        if self.queue.empty():
            return

        # Connect output port to the head of the queue, which is the final operation before the output
        head = self.queue.queue[0][1]
        source = self.nodes[head]
        connect(self.bif_shape, self.compound_path, source, self.output_port, connection_type='output')

        while not self.queue.empty():
            source, target = self.queue.get()
            target_node = self.nodes[target]

            if isinstance(source, Symbol):
                source_port = source.name
                connect(self.bif_shape, self.compound_path, source_port, target_node, connection_type='input')
            else:
                source_node = self.nodes[source]
                connect(self.bif_shape, self.compound_path, source_node, target_node)
