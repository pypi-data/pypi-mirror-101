from setuptools import setup, find_packages


setup(
    name='mkdocs-smart-meta-plugin',
    version='0.1.0',
    description='Generates meta tags for MkDocs automatically',
    long_description='',
    keywords='mkdocs',
    url='https://github.com/aprosvetova/mkdocs-smart-meta-plugin',
    author='Anna Prosvetova',
    author_email='anna@prosvetova.me',
    license='MIT',
    python_requires='>=3.7',
    install_requires=[
        'mkdocs>=1.1',
        'beautifulsoup4'
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'smart-meta = mkdocs_smart_meta_plugin.plugin:SmartMetaPlugin'
        ]
    }
)
