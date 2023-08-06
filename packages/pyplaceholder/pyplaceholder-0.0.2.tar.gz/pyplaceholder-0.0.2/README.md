# pyplaceholder
A placeholder detector in text or in text files. For example, if you have a text like the following: 

```python
s = 'Some example of {term} \\{UN\\}'
```

If you want to detect the {terms} but not {UN} because it is escaped with \\, then you need to execute:

```python
from placeholder import parse_placeholders
s = 'Some example of {term} \\{UN\\}'
parse_placeholders(s)
```

Therefore, it will return the following results:

```text
('Some example of {term} {UM}', [(16, 22)])
```

Where, here, the placeholder is {terms}. The placeholder has to be delimited by just one character, but not more.
The placeholder delimiters can be changed by using the parameters **open_ch** and **close_ch**:

```python
from placeholder import parse_placeholders
s = 'Some example of <term> {UM}'
parse_placeholders(s, '<', '>')
```

The result will be similar, and now we do not need to escape the characters {} for {UN} because we have changed the
default delimiters:


```text
('Some example of <term> {UM}', [(16, 22)])
```

In this case the placeholder is &lt;term&gt;.

Finally, you can detect the placeholders from a text without parse the escape characters changing the parameter 
**escapes**. 

```python
from placeholder import parse_placeholders
s = 'Some example of {term} {UM}'
parse_placeholders(s)
```

The output will be:

```text
('Some example of {term} {UM}', [(16, 22), (23, 27)])
```

In this case, it detects both placeholders because the second one was not escaped with \\.

With this module you can replace the placeholders using **replace_placeholders()**:

```python
from placeholder import replace_placeholders
s = 'Some example of {term} \\{UM\\}'
print(replace_placeholders(s, term='Union Nations'))
```

The result will be:

```text
Some example of Union Nations {UM}
```

Finally, with this module you have also functions to know when a text contain a placehodler (**has_placeholder()**),
count them (**num_placeholders()**), and replace then in a text file (**replace_file_placeholders()**).


