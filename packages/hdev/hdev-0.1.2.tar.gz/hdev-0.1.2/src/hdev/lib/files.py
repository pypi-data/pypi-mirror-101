"""Collection of functions dealing with files."""
import os


def project_file_abspath(relative_path):
    """Return the absolute path of a file within the project."""
    here = os.path.abspath(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(here, "..", relative_path))
