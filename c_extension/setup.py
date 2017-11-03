from setuptools import setup, Extension

setup(
    name='c_embedding',
    version='0.0.1',
    packages=['c_embedding'],
    url='',
    license='',
    author='karl',
    author_email='karlvorndoenitz@gmail.com',
    description='test encryption for karlooper',
    ext_modules=[
        Extension(
            'c_embedding.demo',
            sources=['c_embedding/demo.c'],
            extra_compile_args=["-Wno-char-subscripts"]
        )
    ]
)
