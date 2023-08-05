from setuptools import setup

django_extras = ['dj-email-url==1.0.2', 'dj-database-url==0.5.0']
test_extras = ['pytest-cov']
with open('README.rst', 'r') as f:
    long_description = f.read()


setup(
    name='castaway',
    version='0.4.1',
    description='Simple wrapper for dotenv, with casting',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='http://github.com/dakrauth/castaway',
    author='David Krauth',
    author_email='dakrauth@gmail.com',
    license='MIT',
    zip_safe=False,
    platforms=['any'],
    py_modules=['castaway'],
    python_requires='>=3.7',
    install_requires=['python-dotenv[cli]==0.16.0'],
    extras_require={
        'django': django_extras,
        'test': test_extras,
        'all': django_extras + test_extras
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
