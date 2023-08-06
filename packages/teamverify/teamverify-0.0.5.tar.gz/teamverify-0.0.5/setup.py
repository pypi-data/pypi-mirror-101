import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='teamverify',
    version='0.0.5',
    author='danielverd',
    description='Automated reasoning tool for competitive Pokemon teambuilding',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/danielverd/teamverify',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=[
        'owlready2>=0.23',
        'selenium',
        'pandas',
        'beautifulsoup4',
        'requests'
    ],
    entry_points={
        'console_scripts':[
            'teamverify = teamverify.teambuilder:main',
            'teamverify-fts = teamverify.prepareOntology:main'
        ]
    }
)