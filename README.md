# Quackery
Quackery is lightweight, open-source language for recreational and 
educational programming, inspired by Forth and Lisp.

Sample Quackery shell dialogue; defining and testing an insertion sort.

<pre>/O>   [ [] swap witheach
...       [ swap 2dup 
...         findwith [ over > ] [ ] 
...         nip stuff ] ]           is i-sort ( [ --> [ )
... 

Stack empty.

/O> [] 10 times [ i join ]
... shuffle dup echo 
... say " --> "
... i-sort echo
... 
[ 6 7 5 8 3 4 2 1 0 9 ] --> [ 0 1 2 3 4 5 6 7 8 9 ]
Stack empty.

/O> 
</pre>

The Quackery language is an extensible assembler for a Quackery
Engine. The Quackery Engine has a memory model based on dynamic arrays
and bignums, so presumes comprehensive hardware support for these
features.

Program execution consists of the Quackery Processor traversing
directed tree-like graphs built from dynamic arrays ("Nests" in the
Quackery nomenclature" containing Operators (op-codes), Numbers
(pointers to bignums) and pointers to Nests. The Quackery processor is
stack-based rather than register-based.

Programming in Quackery consists of extending the predefined graphs
that constitute the Quackery environment.

This implementation of a virtual Quackery Engine uses Python lists as
Nests, Python functions as Operators and Python ints as Numbers.

The Quackery processor and a basic Quackery compiler are coded in
Python 3, and the Python Quackery compiler is used to compile the
Quackery environment, which is written in Quackery and includes a more
fully featured (and extensible) Quackery compiler, which is available
to the Quackery programmer.

That the Quackery language has similarities to Forth (also an
extensible assembler for a stack processor), that it leans on Python
for support for dynamic arrays and bignums, and that the majority of
Quackery is written in Quackery all make for a very compact
implementation, under 48k of source code. The downsides are that it is
rather slow by modern standards, and that it is by no means "fully
featured".

In its defence it is possible to understand the entirety of Quackery
in short order, and, once the hurdle of Reverse Polish Notation has
been passed, program development with the interactive environment (the
Quackery Shell) is quick and rewarding. Quackery is intended primarily
for recreational and educational programming, and is a relatively
painless introduction to the concatenative programming paradigm.
