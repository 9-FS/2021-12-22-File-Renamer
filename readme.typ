#import "@preview/wrap-it:0.1.0": wrap-content  // https://github.com/ntjess/wrap-it/blob/main/docs/manual.pdf
#import "./doc_templates/src/style.typ": set_style
#import "./doc_templates/src/note.typ": *


#show: doc => set_style(
    topic: "Filename Dateformat Changer",
    author: "구FS",
    language: "EN",
    doc
)


#align(center, text(size: 8mm, weight: "bold")[Filename Dateformat Changer])
#line(length: 100%, stroke: 0.3mm)
\
\
= Introduction

This program is intended to change the date format of file names. It renames according to the `Filename Dateformat Changer.csv`.

= Table of Contents

#outline()

#pagebreak(weak: true)

= Usage

+ Execute the program once. This will create a default `Filename Dateformat Changer.csv`.
+ Fill your lines out like this:
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
+ Use the datetime expressions from the python #link("https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior")[datetime] library.
+ Execute either `main_outer.py` with python or a `Filename Dateformat Changer.exe` directly.