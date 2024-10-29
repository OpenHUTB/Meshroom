""" Node plugins.
"""
# Types
from typing import Dict
from types import ModuleType

# Internal
from meshroom.core import desc


class NodeDescriptor(object):
    """ Class to describe a Node Plugin.
    """

    def __init__(self, name: str, descriptor: desc.Node, module: ModuleType=None):
        """ Constructor.

        Args:
            name (str): Name of the Node.
            descriptor (desc.Node): The Node descriptor.

        Keyword Args:
            module (ModuleType): Plugin module.
        """
        super().__init__()

        # Node descriptions
        self._name: str = name
        self._descriptor: desc.Node = descriptor

        # Module descriptions
        self._module: ModuleType = module

    # Properties
    descriptor = property(lambda self: self._descriptor)
    category = property(lambda self: self._descriptor.category)


class NodePluginManager(object):
    """ A Singleton class Managing the Node plugins for Meshroom.
    """
    # Static class instance to ensure we have only one created at all times
    _instance = None

    def __new__(cls):
        # Verify that the instance we have is of the current type
        if not isinstance(cls._instance, cls):
            # Create an instance to work with
            cls._instance = object.__new__(cls)

            # Init the class parameters
            # The class parameters need to be initialised outside __init__ as when Cls() gets invoked __init__ gets
            # called as well, so even when we get the same instance back, the params are updated for this and every
            # other instance and that what will affect attrs in all places where the current instance is being used
            cls._instance.init()

        # Return the instantiated instance
        return cls._instance

    def init(self):
        """ Constructor for members.
        """
        self._descriptors: Dict[str: NodeDescriptor] = {}     # pylint: disable=attribute-defined-outside-init

    # Properties
    descriptors = property(lambda self: self._descriptors)

    # Public
    def registered(self, name: str) -> bool:
        """ Returns whether the plugin has been registered already or not.

        Args:
            name (str): Name of the plugin.
        """
        return name in self._descriptors

    def registerNode(self, descriptor: desc.Node) -> bool:
        """ Registers a Node into Meshroom.

        Args:
            descriptor (desc.Node): The Node descriptor.

        Returns:
            bool. Returns True if the node is registered. False if it is already registered.
        """
        # Plugin name
        name = descriptor.__name__

        # Already registered ?
        if self.registered(name):
            return False

        # # Register it
        # self._descriptors[name] = NodeDescriptor(name, descriptor)
        self.register(name, descriptor)

        return True

    def unregisterNode(self, descriptor: desc.Node) -> None:
        """ Unregisters the Node from the Registered Set of Nodes.

        Args:
            descriptor (desc.Node): The Node descriptor.
        """
        # Plugin name
        name = descriptor.__name__

        # Ensure that we have this node already present
        assert name in self._descriptors
        # Delete the instance
        del self._descriptors[name]

    def register(self, name: str, descriptor: desc.Node) -> None:
        """ Registers a Node within meshroom.

        Args:
            descriptor (desc.Node): The Node descriptor.
        """
        self._descriptors[name] = NodeDescriptor(name, descriptor)

    def descriptor(self, name: str) -> desc.Node:
        """ Returns the Node Desc for the provided name.

        Args:
            name (str): Name of the plugin.

        Returns:
            desc.Node. The Node Desc instance.
        """
        # Returns the plugin for the provided name
        plugin = self._descriptors.get(name)

        # Plugin not found with the name
        if not plugin:
            return None

        # Return the Node Descriptor for the plugin
        return plugin.descriptor
