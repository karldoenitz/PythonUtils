from setuptools import setup, Extension

setup(
    name='sum_num_demo',
    version='0.0.1',
    packages=['sum_num_demo'],
    url='',
    license='',
    author='karl',
    author_email='karlvorndoenitz@gmail.com',
    description='test encryption for karlooper',
    ext_modules=[
        Extension(
            'sum_num_demo.demo',
            sources=['sum_num_demo/demo.c'],
            extra_compile_args=["-Wno-char-subscripts"]
        )
    ]
)
