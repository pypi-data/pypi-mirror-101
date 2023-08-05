import setuptools
import glob
import os.path as op

trees = glob.glob("trees/*.tree")
tree_dict = {
    f'{op.basename(tree)[:-5]}={tree}'
    for tree in glob.glob("trees/*.tree")
}


setuptools.setup(
    name="file-tree-fsl",
    version="0.1.3",
    url="https://git.fmrib.ox.ac.uk/ndcn0236/file-tree-fsl",

    author="Michiel Cottaar",
    author_email="MichielCottaar@protonmail.com",

    description="Filetree definitions for the FSL neuroimaging library",
    long_description=open('README.md').read(),

    packages=('file_tree_fsl', ),

    package_data={'file_tree_fsl': ['trees/*.tree']},

    zip_safe=False,

    install_requires=[
        "file-tree"
    ],

    entry_points={'file_tree.trees': ['fsl=file_tree_fsl.load:load']},

    project_urls = {
        "Documentation": "https://open.win.ox.ac.uk/pages/ndcn0236/file-tree/",
    },

    include_package_data=True,

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
