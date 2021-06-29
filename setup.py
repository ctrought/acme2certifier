""" build script for acme2certifier """
from setuptools import setup
from glob import glob
# exec(open('acme_srv/version.py').read())
from acme_srv.version import __version__
setup(name='acme2certifier',
      version=__version__,
      description='ACMEv2 server',
      url='https://github.com/grindsa/acme2certifier',
      author='grindsa',
      author_email='grindelsack@gmail.com',
      license='GPL',
      # packages=['docs', 'acme', 'examples'],
      include_package_data = True,
      data_files=[('/usr/share/doc/acme2certifier/', glob('docs/*')),
                  ('/var/lib/acme2certifier/acme_srv/', glob('acme_srv/*.py')),
                  ('/var/lib/acme2certifier/examples', glob('examples/*.*')),
                  ('/var/lib/acme2certifier/examples/ca_handler', glob('examples/ca_handler/*.py')),
                  ('/var/lib/acme2certifier/examples/db_handler', glob('examples/db_handler/*.py')),
                  ('/var/lib/acme2certifier/examples/django', glob('examples/django/*.py')),
                  ('/var/lib/acme2certifier/examples/django/acme2certifier', glob('examples/django/acme2certifier/*.py')),
                  ('/var/lib/acme2certifier/examples/django/acme', glob('examples/django/acme_srv/*.py')),
                  ('/var/lib/acme2certifier/examples/django/acme_srv/fixture', glob('examples/django/acme_srv/fixture/*')),
                  ('/var/lib/acme2certifier/examples/django/acme_srv/migrations', glob('examples/django/acme_srv/migrations/*.py')),
                  ('/var/lib/acme2certifier/examples/nginx', glob('examples/nginx/*')),
                  ('/var/lib/acme2certifier/examples/trigger', glob('examples/trigger/*')),
                  ('/var/lib/acme2certifier/tools', glob('tools/*.py')),
                  ('/var/lib/acme2certifier/examples/Docker', glob('examples/Docker/*.*')),
                  ('/var/lib/acme2certifier/examples/Docker/wsgi', glob('examples/Docker/wsgi/*')),
                  ('/var/lib/acme2certifier/examples/Docker/django', glob('examples/Docker/django/*')),
                 ],

      platforms='any',
      classifiers=[
          'Programming Language :: Python',
          'Development Status :: 4 - Beta',
          'Natural Language :: German',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Python Modules'
          ],
      zip_safe=False,
      test_suite="test")
