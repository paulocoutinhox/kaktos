from modules import config, file, system


# -----------------------------------------------------------------------------
def run(params):
    file.recreate_dir(config.build_dir)
    system.build_pages()
