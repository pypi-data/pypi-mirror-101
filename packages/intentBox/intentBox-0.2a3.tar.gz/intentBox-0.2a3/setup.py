from setuptools import setup

setup(
    name='intentBox',
    version='0.2a3',
    packages=['intentBox'],
    url='https://github.com/HelloChatterbox/intentBox',
    license='',
    author='jarbasai',
    install_requires=["adapt-parser>=0.3.3", "padaos>=0.1.9", "auto_regex",
                      "pronomial>=0.0.2"],
    author_email='jarbasai@mailfence.com',
    extras_require={
        "plugins": ["requests", "padatious>=0.4.6", "fann2>=1.0.7"]
    },
    description='chatterbox intent parser, extract multiple intents from a single utterance '
)
