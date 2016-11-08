from setuptools import setup, find_packages

setup(
    name='text2img',
    version='0.0.1',
    url='https://github.com/tuaplicacionpropia/text2img',
    download_url='https://github.com/tuaplicacionpropia/text2img/archive/master.zip',
    author=u'Tu aplicación propia',
    author_email='tuaplicacionpropia@gmail.com',
    description='Python library for generate images from text.',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    license='MIT',
    install_requires=[
        'lxml==3.3.3',
        'hjson==2.0.2',
    ],
)
