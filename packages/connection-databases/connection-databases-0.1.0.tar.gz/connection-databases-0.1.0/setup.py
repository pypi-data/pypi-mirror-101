from setuptools import setup, find_packages

# Add install requirements
setup(
    author="Fabio Caffarello",
    description="ackage for querying different databases",
    name="connection-databases",
    version="0.1.0",
    packages=find_packages(include=["connection", "connection.*"]),
    install_requires=[
        'pandas>=1.2',
        'SQLAlchemy>=1.4',
        'dnspython>=2.1',
        'pymongo>=3.11',
        'PyMySQL>=1.0',
        'pybigquery>=0.5',
        'google-cloud-bigquery>=2.13'
        'google-cloud-bigquery-storage>=2.3'
    ],
    python_requires=">=3.6",
)
