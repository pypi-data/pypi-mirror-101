The chi function is defined so that chi(G, h) is the smallest m for which every m size subset of G spans G.

ARGUMENTS:

* G - Either an integer n (representing G = Z_n) or a tuple (n1, n2, ..., nm) (representing G = Z_n1 * Z_n2 * ... * Z_nm)

* h - An integer

* (optional) verbose [default: False] - Print extra computational information

This function uses the _unsigned_, _unrestricted_ variation of sumsets. This means that in the sumset, terms are allowed to repeat and are not allowed to be subtracted. For more information, read the (link forthcoming) master page of details on sumsets.