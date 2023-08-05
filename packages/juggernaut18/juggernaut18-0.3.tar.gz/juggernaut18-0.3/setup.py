from distutils.core import setup
setup(
  name = 'juggernaut18',         # How you named your package folder (MyLib)
  packages = ['juggernaut18'],   # Chose the same as "name"
  version = '0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Test Package',   # Give a short description about your library
  author = 'Bilal Latif',                   # Type in your name
  author_email = 'bilal.latif18@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/BilalLatif',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/BilalLatif/juggernaut-package/archive/refs/tags/0.3.tar.gz',    # I explain this later on
  # download_url = 'https://dev.azure.com/AWSInstitut/7f09eebc-5108-45b9-84a8-9e2083ad3aab/_git/8389d47b-055c-4101-8f26-f7c4dc1cde91/commit/33bbda8457e3a791d88e23f07a3dacc08c00d571',
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  # install_requires=[            # I get to this in a second
  #         'validators',
  #         'beautifulsoup4',
  #     ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)