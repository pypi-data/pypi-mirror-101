import configparser                                                                                                                                              
config = configparser.ConfigParser()

config['flavors'] = dict(
    use_hdf5 = True,
    use_hdf5_qe = False,
    flavor_complex = True,
    dft_flavor = 'espresso',
    )

config['MPI'] = dict(
    mpirun = 'mpirun',
    nproc = 1,
    nproc_flag = '-n',
    nproc_per_node = 1,
    nproc_per_node_flag = '--npernode',
    nodes = '',
    nodes_flag = '',
    )

config['runscript'] = dict(
    first_line = '#!/bin/bash',
    header = """
# Lines before execution
# can be multiple lines
# but they must be indented.
; This is a real comment.
; Lines starting with ";" will be ignored
; and lines starting with "#" will be used.
""",
    footer = """
# Lines after execution
# can also be multiple lines.
""",
    )


if __name__ == '__main__':
    import os
    import argparse
    
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f', metavar='force', type=bool,  default=True,
                        help='Overwrite existing file')
    fname = os.path.join(os.environ['HOME'], '.BGWpyrc')
    force = True
    args = parser.parse_args()
    if os.path.exists(fname):
        if not args.force:
            import warnings
            warnings.warn('Cannot overwrite existing file ~/.BGWpyrc. Use -f to overwrite')
            sys.exit(1)

    with open(fname, 'w') as cf:
      config.write(cf)


