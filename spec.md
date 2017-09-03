
# metadata
```
::documentclass: cocuh_blog_article
::usemodule: CodeInlineModule
::usemodule: [CodeInlineModule, CodeBlockModule]
```

# inline
```
:bold:{text}
:italic:{text}
:underline:{text}
:code:{text}
:code{lang=python,scheme=molokai}:{text}
:link{href="http://dakko.site"}:{text}
```


### 短縮記法
```
*bold*
/italic/
_underline_
`code`
```

# Module
```
.. ModuleName
    .. AttrName: value
    .. AttrName: [value, value, value]
    body
```


# lines
## itemize
```
.. itemize
    .. type: circle
    - hoge
    - hoge
    - hoge
```

### 短縮記法
```
- hoge
- hoge
- hoge
```

## enumeration
```
.. enumerate
    .. type: arabic
    .. renumbering: true
    0. hoge
    0. hoge
    0. hoge
```
```
.. enumerate
    .. type: arabic
    .. renumbering: true
    0. hoge
    0. hoge
    0. hoge
```

### 短縮記法
```
0. hoge
0. hoge
0. hoge
```