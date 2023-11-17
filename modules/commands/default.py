from modules import system


# -----------------------------------------------------------------------------
def run(params={}):
    system.force_debug = True

    system.initialize()
    system.build_pages()
    system.start_live_reload()
