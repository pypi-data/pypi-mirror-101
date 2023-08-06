The nu function is defined so that nu(G, m, h) is the largest size of hA, where |A| = m. In other words, nu(G, m, h) is the largest the h-fold sumset of a size m subset of G can be.

ARGUMENTS:

* G - Either an integer n (representing G = Z_n) or a tuple (n1, n2, ..., nm) (representing G = Z_n1 * Z_n2 * ... * Z_nm)

* m - An integer representing the size of the subset A

* h - An integer

* (optional) verbose [default: False] - Print a subset A which maximizes |hA|

This function uses the _unsigned_, _unrestricted_ variation of sumsets. This means that in the sumset, terms are allowed to repeat and are not allowed to be subtracted. For more information, read the (link forthcoming) master page of details on sumsets.