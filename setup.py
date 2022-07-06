from setuptools import setup, find_packages

setup(
    name='twitter_scraper',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'matplotlib',
        'nltk',
        'google-cloud-speech'
        'mysql_connector_repackaged',
        'numpy',
        'pandas',
        'Pillow',
        'protobuf',
        'PyMySQL',
        'seaborn',
        'SQLAlchemy',
        'tweepy',
        'typing_extensions',
        'wordcloud',
        'mysql-connector-python'

    ],
    entry_points={
        'console_scripts': [
            'main = twitter_scraper.main:cli',
        ],
    },
)