from pygemstones.io import file

from modules import config, system


# -----------------------------------------------------------------------------
def run(params = {}):
    system.force_debug = False

    system.initialize()
    file.recreate_dir(config.build_dir)
    system.build_pages()
