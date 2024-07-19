#import "@preview/wrap-it:0.1.0": wrap-content  // https://github.com/ntjess/wrap-it/blob/main/docs/manual.pdf
#import "./doc_templates/src/note.typ": *
#import "./doc_templates/src/style.typ": set_style


#show: doc => set_style(
    topic: "file_renamer",
    author: "구FS",
    language: "EN",
    doc
)
#set text(size: 3.5mm)


#align(center, text(size: 2em, weight: "bold")[file_renamer])
#line(length: 100%, stroke: 0.3mm)
\
\
= Introduction

This program is intended to change the date format of file names. It renames according to the `./config/format_conversion.csv`.

= Table of Contents

#outline()

#pagebreak(weak: true)

= Usage

+ Execute the program once. This will create a default `./config/format_conversion.csv`.
+ Fill your lines out like this:
    ```CSV
    {input datetime format}\t{input timezone offset}\t{output datetime format}\t{output timezone offset}
    ```

    Example:
    ```CSV
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
+ Execute either `main_outer.py` with python or an executable directly.