from setuptools import setup

setup(
    name='inhouseDemandManager',
    packages=['inhouseDemandManager'],
    include_package_data=True,
    install_requires=[
        'flask',
        'cachelib',
        'click',
        'colorama',
        'dnspython',
        'email-validator',
        'Flask-Session',
        'idna',
        'itsdangerous',
        'Jinja2',
        'mariadb',
        'MarkupSafe',
        'packaging',
        'sqlparse',
        'Werkzeug'
    ],
)