"""
Bootstrap compiler for Zebra.

$Id$
"""
import zebra
class Bootstrap:
    """A class to compile zebra reports until zebra can compile itself."""

    def compile(self, zbx):
        """Bootstrap.().compile(zbx) => python version of zbx"""
        
        return zebra.trim(
            """
            def fetch(model=None):
                pass
            """)

