from modules import system

# setup
system.setup()

# routes
from modules.routes import *

# entrypoint
if __name__ == "__main__":
    system.process_command()
