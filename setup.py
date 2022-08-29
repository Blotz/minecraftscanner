from setuptools import setup

if __name__=="__main__":
    setup(
        name="minecraftscanner",
        version="0.1",
        description="Scan for Minecraft servers",
        author="Ferdinand Theil",
        url="https://git.blotz.dev/cgit.cgi/minecraftscanner.git/",
        author_email="f.p.theil@gmail.com",
        license='MIT',
        packages=['minecraftscanner'],
        package_data={'minecraftscanner': ['migrations/*.sql']},
        install_requires=[
            "mcstatus",
            "python-masscan"
        ],
        classifiers=[
            "Environment :: Console",
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3 :: Only',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Utilities',
        ],
        zip_safe=False
        )