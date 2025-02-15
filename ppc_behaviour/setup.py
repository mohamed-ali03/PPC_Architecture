from setuptools import setup

package_name = 'ppc_behaviour'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mo',
    maintainer_email='mohamedalif163@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "behaviour = ppc_behaviour.behaviour:main",
            "idle_state = ppc_behaviour.Idle_state:main",
            "create_plan = ppc_behaviour.create_plan:main",
            "navigate = ppc_behaviour.navigate:main"
        ],
    },
)
