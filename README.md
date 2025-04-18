# THIS PROJECT WAS ABANDONED and has been revived 
## by Krzysztof Sobolewski <krzysztof.sobolewski@gmail.com> in 2025

- the action of revival has been done just for compatibility issues with Python 3.12, ie. getting rid of errors like "ImportError: cannot import name 'Mapping' from 'collections' (/usr/lib/python3.12/collections/__init__.py)
"
- Grako is being used in another project I am reviving (Cubes), which has been abandoned years ago as well.
- Remember, that you need to have Graphviz devel headers as well. 
  - In Ubuntu, you can install it with:
  ```sudo apt install graphviz libgraphviz-dev```
    - See more about the implementation for Ubuntu at:  https://packages.ubuntu.com/search?keywords=graphviz&searchon=names
  - for Mac, take a look here: https://ports.macports.org/port/graphviz-devel/
  - Graphviz project homepage: https://graphviz.org/
  - Graphviz download page: https://graphviz.org/download/

  - After installing the requirements (```pip3 install -r requirements.txt```), please call the following from the project root directory to setup the project:
  ```python3 setup.py install```
 


- For other grammar-related needs, please take a look at [竜 TatSu](https://github.com/neogeny/TatSu) for the follow-up.
- Tatsu repo is here: https://github.com/neogeny/TatSu
