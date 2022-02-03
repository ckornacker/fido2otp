# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='fido2otp',
    version='1.0.0',
    description='OTP token store for Fido2 devices',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ckornacker/fido2otp',
    author='Christian Kornacker',
    author_email='christian.kornacker@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='fido2, otp, opensk, development',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.5, <4',
    install_requires=[
        'pyotp',
        'secretstorage',
        'Crypto',
        'fido2>=0.9.0,<1',
        'click'
    ],
    entry_points={
        'console_scripts': [
            'fido2otp=fido2otp:cli',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/ckornacker/fido2otp/issues',
        'Source': 'https://github.com/ckornacker/fido2otp/',
    },
)
