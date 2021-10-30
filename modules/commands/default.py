from modules import system


# -----------------------------------------------------------------------------
def run(params):
    system.build_pages()
    system.start_live_reload()
