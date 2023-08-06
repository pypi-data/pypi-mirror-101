import pkg_resources
import os.path as op
from file_tree.parse_tree import available_subtrees


def load():
    for filename in pkg_resources.resource_listdir(__name__, "trees"):
        with pkg_resources.resource_stream(__name__, op.join("trees", filename)) as f:
            available_subtrees[filename] = f.read().decode()

    # allows different capitalisation for backwards compatibility
    available_subtrees['BedpostX.tree'] = available_subtrees['bedpostx.tree']
    available_subtrees['ProbtrackX.tree'] = available_subtrees['probtrackx.tree']
    available_subtrees['Diffusion.tree'] = available_subtrees['diffusion.tree']
