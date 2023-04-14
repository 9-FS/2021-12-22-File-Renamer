---
Topic: "Filename Dateformat Changer"
Author: "구FS"
---
<link href="./src/KFS/md_style.css" rel="stylesheet"></link>
<body>

# <p style="text-align: center">Filename Dateformat Changer</p>
<br>
<br>

- [1. General](#1-general)
- [2. How to Use](#2-how-to-use)

## 1. General

This program is intended to change the date format of file names. It renames according to the `Filename Dateformat Changer.csv`.

## 2. How to Use

1. Execute the program once. This will create a default `Filename Dateformat Changer.csv`.
1. Fill your lines out like this:
    ```csv
    {input datetime format}\t{input timezone offset}\t{output datetime format}\t{output timezone offset}
    ```

    Example:
    ```csv
    input datetime format	input timezone offset	output datetime format	output timezone offset
    
    # samsung camera
    %Y%m%d_%H%M%S		%Y-%m-%d %H_%M_%S	
    %Y%m%d_%H%M%S(%f)		%Y-%m-%d %H_%M_%S	
    
    # dropbox
    %Y-%m-%d %H.%M.%S		%Y-%m-%d %H_%M_%S	
    %Y-%m-%d %H.%M.%S(%f)		%Y-%m-%d %H_%M_%S	

    # apple
    Foto %d.%m.%y, %H %M %S	+02:00	%Y-%m-%d %H_%M_%S	+00:00
    ```
1. Use the datetime expressions from the python [datetime](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior) library.
1. Execute either `main_outer.py` with python or a `Filename Dateformat Changer.exe` directly.

<div class="img_centre_30">
    <a href="https://www.paypal.com/paypalme/KooFelixSangmo">
        <img alt="Error: Could not load image source."
        src="https://i.pinimg.com/originals/60/fd/e8/60fde811b6be57094e0abc69d9c2622a.jpg"/>
    </a>
    <p class=img_caption>Click to buy me a beer!</p>
</div>

</body