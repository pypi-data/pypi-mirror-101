import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'mentat_misp_connector',
  package_dir={"": "src"},
  packages=setuptools.find_packages(where="src"),
  python_requires=">=3.6",
  version = '0.1',
  license='MIT',
  description = "Basic proprietary module used for integration of MISP platform into Cesnet's Mentat system.",
  author = 'Pavel Eis',
  author_email = 'eis@cesnet.cz',
  url = 'https://github.com/Aisik00/mentat-misp-connector',
  download_url = 'https://github.com/Aisik00/mentat-misp-connector/archive/refs/tags/v_01.tar.gz',
  keywords = ['Mentat', 'MISP', 'integration'],
  install_requires=[
          'pyzenkit',
          'mentat',
          'pymisp'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.8',
  ],
)