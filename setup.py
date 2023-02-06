from setuptools import setup  
setup(
        name='blobs_tools',
        package_dir = {
            'blobs_tools': 'blobs_tools',
            'blobs_tools.crypto': 'blobs_tools/crypto',
            'blobs_tools.misc': 'blobs_tools/misc',
            'blobs_tools.net': 'blobs_tools/net',
            'blobs_tools.payloads': 'blobs_tools/payloads',
            'blobs_tools.utils': 'blobs_tools/utils'},
        packages=['blobs_tools', 'blobs_tools.crypto',
                  'blobs_tools.misc', 'blobs_tools.net',
                  'blobs_tools.payloads', 'blobs_tools.utils']
    )
