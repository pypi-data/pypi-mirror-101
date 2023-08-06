# NetLogoDOE
NetLogoDOE is a graphical user interface that allows for easy design, execution and analysis of NetLogo experiments. 
## Features

- Design NetLogo experiments
- Run NetLogo models with specified configurations
- Save and import experiments configurations
- Visualise results with 8 different graph types
- Save and import experiment results

## Installation

```
pip install NetLogoDOE
```

## Usage
Make a Python file (.py), copy the following code into it and then run it. This will launch the GUI and allow you to use all functionalities.

#### Windows
```
from NetLogoDOE.NetLogoDOE import Gui
Gui()
```

#### Linux
IMPORTANT: If your operating system is Linux, the Gui() call requires two parameters with your NetLogo version and location.

The netlogo_version parameter has to be one of: '5', '6.0', '6.1', '6.2'.  
The netlogo_home parameter needs to be a valid file path to wherever on your PC your NetLogo installation is located.

```
from NetLogoDOE.NetLogoDOE import Gui
Gui(netlogo_version=??, netlogo_home=path_to_your_netlogo_installation)
```

## License
MIT License

Copyright (c) 2021 Robin Faber

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
