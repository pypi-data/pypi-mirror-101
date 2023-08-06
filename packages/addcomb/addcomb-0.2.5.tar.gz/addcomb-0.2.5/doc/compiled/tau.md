The tau function is defined so that tau(G, h) is the maximum size of a zero-H-free sumset. In other words, it's the largest size of a set A such that hA does not contain 0.

ARGUMENTS:

* G - Either an integer n (representing G = Z_n) or a tuple (n1, n2, ..., nm) (representing G = Z_n1 * Z_n2 * ... * Z_nm)

* h - An integer

* (optional) verbose [default: False] - Print a zero-H-free sumset set A of maximum size

This function uses the _unsigned_, _unrestricted_ variation of sumsets. This means that in the sumset, terms are allowed to repeat and are not allowed to be subtracted. For more information, read the (link forthcoming) master page of details on sumsets.