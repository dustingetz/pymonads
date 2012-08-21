# ; Continuation monad

# (defmonad cont-m
#   "Monad describing computations in continuation-passing style. The monadic
#    values are functions that are called with a single argument representing
#    the continuation of the computation, to which they pass their result."
#   [m-result   (fn m-result-cont [v]
#                 (fn [c] (c v)))
#    m-bind     (fn m-bind-cont [mv f]
#                 (fn [c]
#                   (mv (fn [v] ((f v) c)))))
#    ])

# (defn run-cont
#   "Execute the computation c in the cont monad and return its result."
#   [c]
#   (c identity))

# (defn call-cc
#   "A computation in the cont monad that calls function f with a single
#    argument representing the current continuation. The function f should
#    return a continuation (which becomes the return value of call-cc),
#    or call the passed-in current continuation to terminate."
#   [f]
#   (fn [c]
#     (let [cc (fn cc [a] (fn [_] (c a)))
#           rc (f cc)]
#       (rc c))))
