##Introduction
**smikan**, a simple module grabbing bangumi information from http://mikanani.me

The API is kindof messing for the time being but using it is quiet simple.

##Example
```python
    import smikan

    # Starting from a homepage
    homepage = smikan.get_homepage()

    # Finding bangumis by broadcasting date
    print(hp.fri)

    # Grabing details from a particular bangumi
    bangumi = hp.fri[0]
    bangumi.get()
    print(bangumi.subtitles)
    
    # Check which season the homepage is currently in
    print(homepage.period)

    # Navigate to another season
    homepage.change_period(homepage.periods[1])
    print(homepage.fri)
```
##License

This module is distributed under the MIT license (https://opensource.org/licenses/MIT).

Copyright (c) 2016 Dasein Phaos

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
