class DataStore(object):
    """Data store class that will be passed to the subsequent commands in the CLI."""

    def __init__(self):
        self.name = "empty"
        """The name of the current graph imported into the database."""

        self.backend = None
        """Neo4j docker container instance."""

        self.graph = None
        """py4neo Graph object."""
