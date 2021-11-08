# [                              quackery                               ]

import time
import sys
import os
import os.path
try:
    import readline
except:
    pass


class QuackeryError(Exception):
    pass


def quackery(source_string):

    """   Perform a Quackery program. Return the stack as a string.  """

    def failed(message):
        traverse(build("""  stacksize pack
                            decimal unbuild
                            return$
                            nestdepth ]bailby[  """))
        returnstack = string_from_stack()
        thestack = string_from_stack()
        raise QuackeryError('\n       Problem: ' + message +
                            '\nQuackery Stack: ' + str(thestack)[2:-2] +
                            '\n  Return stack: ' + str(returnstack))

    def isNest(item):
        return(isinstance(item, list))

    def isNumber(item):
        return(isinstance(item, int))

    def isOperator(item):
        return(isinstance(item, type(lambda: None)))

    def expect_something():
        nonlocal qstack
        if qstack == []:
            failed('Stack unexpectedly empty.')

    def top_of_stack():
        nonlocal qstack
        return(qstack[-1])

    def expect_nest():
        expect_something()
        if not isNest(top_of_stack()):
            failed('Expected nest on stack.')

    def expect_number():
        expect_something()
        if not isNumber(top_of_stack()):
            failed('Expected number on stack.')

    def to_stack(item):
        nonlocal qstack
        qstack.append(item)

    def from_stack():
        nonlocal qstack
        expect_something()
        return(qstack.pop())

    def string_from_stack():
        expect_nest()
        result = ''
        for ch in from_stack():
            if ch == 13:
                result += '\n'
            elif 31 < ch < 127:
                result += chr(ch)
            else:
                result += '?'
        return(result)

    def string_to_stack(str):
        result = []
        for ch in str:
            if ch == '\n':
                result.append(13)
            elif 31 < ord(ch) < 127:
                result.append(ord(ch))
            else:
                result.append(ord('?'))
        to_stack(result)

    def share_path():
        nonlocal current_nest
        nonlocal program_counter
        nonlocal rstack
        backup_current_nest = current_nest
        backup_program_counter = program_counter
        backup_rstack = rstack
        rstack = []
        traverse(build('file.path share'))
        current_nest = backup_current_nest
        program_counter = backup_program_counter
        rstack = backup_rstack
        return string_from_stack()

    def python():
        nonlocal to_stack
        nonlocal from_stack
        nonlocal string_to_stack
        nonlocal string_from_stack
        try:
            exec(string_from_stack())
        except QuackeryError:
            raise
        except Exception as diagnostics:
            failed('Python reported: "' + str(diagnostics) + '"')

    def qfail():
        message = string_from_stack()
        failed(message)

    def stack_size():
        nonlocal qstack
        to_stack(len(qstack))

    def qreturn():
        nonlocal rstack
        to_stack(rstack)

    def dup():
        a = from_stack()
        to_stack(a)
        to_stack(a)

    def drop():
        from_stack()

    def swap():
        a = from_stack()
        b = from_stack()
        to_stack(a)
        to_stack(b)

    def rot():
        a = from_stack()
        swap()
        to_stack(a)
        swap()

    def over():
        a = from_stack()
        dup()
        to_stack(a)
        swap()

    def nest_depth():
        nonlocal rstack
        to_stack(len(rstack)//2)

    def to_return(item):
        nonlocal rstack
        rstack.append(item)

    def from_return():
        nonlocal rstack
        if rstack == []:
            failed('Return stack unexpectedly empty.')
        return(rstack.pop())

    true = 1

    false = 0

    def bool_to_stack(qbool):
        to_stack(true if qbool else false)

    def nand():
        expect_number()
        a = from_stack()
        expect_number()
        bool_to_stack(from_stack() == false or a == false)

    def equal():
        expect_something()
        a = from_stack()
        expect_something()
        bool_to_stack(a == from_stack())

    def greater():
        expect_number()
        a = from_stack()
        expect_number()
        bool_to_stack(from_stack() > a)

    def inc():
        expect_number()
        to_stack(1 + from_stack())

    def plus():
        expect_number()
        a = from_stack()
        expect_number()
        to_stack(a + from_stack())

    def negate():
        expect_number()
        to_stack(-from_stack())

    def multiply():
        expect_number()
        a = from_stack()
        expect_number()
        to_stack(a * from_stack())

    def qdivmod():
        expect_number()
        a = from_stack()
        if a == 0:
            failed('Cannot divide by zero.')
        expect_number()
        results = divmod(from_stack(), a)
        to_stack(results[0])
        to_stack(results[1])

    def exponentiate():
        expect_number()
        a = from_stack()
        if a < 0:
            failed('Cannot ** by a negative number: ' + str(a))
        expect_number()
        to_stack(from_stack() ** a)

    def shift_left():
        expect_number()
        a = from_stack()
        if a < 0:
            failed('Cannot << by a negative number: ' + str(a))
        expect_number()
        to_stack(from_stack() << a)

    def shift_right():
        expect_number()
        a = from_stack()
        if a < 0:
            failed('Cannot >> by a negative number: ' + str(a))
        expect_number()
        to_stack(from_stack() >> a)

    def bitwise_and():
        expect_number()
        a = from_stack()
        expect_number()
        to_stack(a & from_stack())

    def bitwise_or():
        expect_number()
        a = from_stack()
        expect_number()
        to_stack(a | from_stack())

    def bitwise_xor():
        expect_number()
        a = from_stack()
        expect_number()
        to_stack(a ^ from_stack())

    def bitwise_not():
        expect_number()
        to_stack(~from_stack())

    def qtime():
        to_stack(int(time.time()*1000000))

    def meta_done():
        from_return()
        from_return()

    def meta_again():
        from_return()
        to_return(-1)

    def meta_if():
        expect_number()
        if from_stack() == 0:
            to_return(from_return() + 1)

    def meta_iff():
        expect_number()
        if from_stack() == 0:
            to_return(from_return() + 2)

    def meta_else():
        to_return(from_return() + 1)

    def meta_literal():
        pc = from_return() + 1
        return_nest = from_return()
        if len(return_nest) == pc:
            failed('''Found a "'" at the end of a nest.''')
        to_stack(return_nest[pc])
        to_return(return_nest)
        to_return(pc)

    def meta_this():
        pc = from_return()
        return_nest = from_return()
        to_stack(return_nest)
        to_return(return_nest)
        to_return(pc)

    def meta_do():
        expect_something()
        the_thing = from_stack()
        if not isNest(the_thing):
            the_thing = [the_thing]
        to_return(the_thing)
        to_return(-1)

    def meta_bail_by():
        expect_number()
        a = 2*(from_stack())
        if a <= len(rstack):
            for _ in range(a):
                from_return()
        else:
            failed('Bailed out of Quackery.')

    def qput():
        expect_nest()
        a = from_stack()
        expect_something()
        b = from_stack()
        a.append(b)

    def immovable():
        pass

    def take():
        expect_nest()
        a = from_stack()
        if len(a) == 0:
            failed('Unexpectedly empty nest.')
        if len(a) == 1:
            if isNest(a[0]):
                if len(a[0]) > 0:
                    if a[0][0] == immovable:
                        failed('Cannot remove an immovable item.')
        to_stack(a.pop())

    def create_nest():
        to_stack([])

    def qsplit():
        expect_number()
        a = from_stack()
        expect_nest()
        b = from_stack()
        to_stack(b[:a])
        to_stack(b[a:])

    def join():
        expect_something()
        b = from_stack()
        if not isNest(b):
            b = [b]
        expect_something()
        a = from_stack()
        if not isNest(a):
            a = [a]
        to_stack(a+b)

    def qsize():
        expect_nest()
        to_stack(len(from_stack()))

    def qfind():
        expect_nest()
        nest = from_stack()
        expect_something()
        a = from_stack()
        if a in nest:
            to_stack(nest.index(a))
        else:
            to_stack(len(nest))

    def peek():
        expect_number()
        index = from_stack()
        expect_nest()
        nest = from_stack()
        if index >= len(nest) or (
           index < 0 and len(nest) < abs(index)):
            failed('Cannot access an item outside a nest.')
        else:
            to_stack(nest[index])

    def poke():
        expect_number()
        index = from_stack()
        expect_nest()
        nest = from_stack().copy()
        expect_something()
        value = from_stack()
        if index >= len(nest) or (
           index < 0 and len(nest) < abs(index)):
            failed('Cannot access an item outside a nest.')
        else:
            nest[index] = value
            to_stack(nest)

    def qnest():
        expect_something()
        bool_to_stack(isNest(from_stack()))

    def qnumber():
        expect_something()
        bool_to_stack(isNumber(from_stack()))

    def qoperator():
        expect_something()
        bool_to_stack(isOperator(from_stack()))

    def quid():
        expect_something()
        to_stack(id(from_stack()))

    def qemit():
        expect_number()
        char = from_stack()
        if char == 13:
            print()
        elif 31 < char < 127:
            print(chr(char), end='')
        else:
            print('?', end='')

    def ding():
        print('\a', end='')

    def qinput():
        prompt = string_from_stack()
        string_to_stack(input(prompt))

    def putfile():
        path = share_path()
        filename = string_from_stack()
        filepath = os.path.join(path, filename)
        filetext = string_from_stack()
        try:
            f = open(filepath, 'x')
            f.close()
        except FileExistsError:
            to_stack(false)
        except:
            raise
        else:
            try:
                f = open(filepath, 'w')
                f.write(filetext)
                f.close()
            except:
                raise
            else:
                to_stack(true)

    def releasefile():
        path = share_path()
        filename = string_from_stack()
        filepath = os.path.join(path, filename)
        try:
            os.remove(filepath)
        except FileNotFoundError:
            to_stack(false)
        except:
            raise
        else:
            to_stack(true)

    def sharefile():
        nonlocal rstack
        dup()
        path = share_path()
        filename = string_from_stack()
        filepath = os.path.join(path, filename)
        try:
            f = open(filepath)
            filetext = f.read()
            f.close()
        except FileNotFoundError:
            to_stack(false)
        except:
            raise
        else:
            drop()
            string_to_stack(filetext)
            to_stack(true)

    operators = {
           'python':      python,       # (     $ -->       )
           'fail':        qfail,        # (     $ -->       )
           'nand':        nand,         # (   b b --> b     )
           '=':           equal,        # (   x x --> b     )
           '>':           greater,      # (   n n --> b     )
           '1+':          inc,          # (     n --> n     )
           '+':           plus,         # (   n n --> n     )
           'negate':      negate,       # (     n --> n     )
           '*':           multiply,     # (   n n --> n     )
           '/mod':        qdivmod,      # (   n n --> n n   )
           '**':          exponentiate, # (   n n --> n     )
           '<<':          shift_left,   # (   f n --> f     )
           '>>':          shift_right,  # (   f n --> f     )
           '&':           bitwise_and,  # (   f f --> f     )
           '|':           bitwise_or,   # (   f f --> f     )
           '^':           bitwise_xor,  # (   f f --> f     )
           '~':           bitwise_not,  # (     f --> f     )
           'time':        qtime,        # (       --> n     )
           'stacksize':   stack_size,   # (       --> n     )
           'nestdepth':   nest_depth,   # (       --> n     )
           'return':      qreturn,      # (       --> [     )
           'dup':         dup,          # (     x --> x x   )
           'drop':        drop,         # (     x -->       )
           'swap':        swap,         # (   x x --> x x   )
           'rot':         rot,          # ( x x x --> x x x )
           'over':        over,         # (   x x --> x x x )
           ']done[':      meta_done,    # (       -->       )
           ']again[':     meta_again,   # (       -->       )
           ']if[':        meta_if,      # (     b -->       )
           ']iff[':       meta_iff,     # (     b -->       )
           ']else[':      meta_else,    # (       -->       )
           "]'[":         meta_literal, # (       --> x     )
           ']this[':      meta_this,    # (       --> [     )
           ']do[':        meta_do,      # (     x -->       )
           ']bailby[':    meta_bail_by, # (     n -->       )
           'put':         qput,         # (   x [ -->       )
           'immovable':   immovable,    # (       -->       )
           'take':        take,         # (     [ --> x     )
           '[]':          create_nest,  # (       --> n     )
           'split':       qsplit,       # (   [ n --> [ [   )
           'join':        join,         # (   x x --> [     )
           'find':        qfind,        # (     x --> b     )
           'peek':        peek,         # (   [ n --> x     )
           'poke':        poke,         # ( x [ n -->       )
           'size':        qsize,        # (     [ --> n     )
           'nest?':       qnest,        # (     x --> b     )
           'number?':     qnumber,      # (     x --> b     )
           'operator?':   qoperator,    # (     x --> b     )
           'quid':        quid,         # (     x --> n     )
           'emit':        qemit,        # (     c -->       )
           'ding':        ding,         # (       -->       )
           'input':       qinput,       # (     $ --> $     )
           'putfile':     putfile,      # (     $ --> b     )
           'releasefile': releasefile,  # (     $ --> b     )
           'sharefile':   sharefile}    # (     $ --> $ b   )

    qstack = []

    rstack = []

    current_nest = []

    program_counter = 0

    def traverse(the_nest):
        nonlocal current_nest
        nonlocal program_counter
        nonlocal rstack
        current_nest = the_nest
        program_counter = 0
        while True:
            if program_counter >= len(current_nest):
                if rstack == []:
                    break
                else:
                    program_counter = from_return()
                    current_nest = from_return()
                    program_counter += 1
                    continue
            current_item = current_nest[program_counter]
            if isNest(current_item):
                to_return(current_nest)
                to_return(program_counter)
                current_nest = current_item
                program_counter = 0
            elif isOperator(current_item):
                current_item()
                program_counter += 1
            elif isNumber(current_item):
                to_stack(current_item)
                program_counter += 1
            else:
                failed('Quackery was worried by a python.')

    def isinteger(string):
        numstr = string
        if len(numstr) > 0 and numstr[0] == '-':
            numstr = numstr[1:]
        return numstr.isdigit()

    def next_char():
        nonlocal source
        if len(source) > 0:
            char = source[0]
            source = source[1:]
            return(char)
        else:
            return('')

    def next_word():
        result = ''
        while True:
            char = next_char()
            if char == '':
                return(result)
            if ord(char) < 33:
                if result == '':
                    continue
                return(result)
            result += char

    def one_char():
        while True:
            char = next_char()
            if char == '':
                return(char)
            if ord(char) < 33:
                continue
            return(char)

    def get_name():
        name = next_word()
        if name == '':
            sys.exit('Unexpected end of program text.')
        return(name)

    def check_build():
        nonlocal current_build
        if len(current_build) == 0:
            sys.exit('Unexpected naming.')

    def qis():
        nonlocal operators
        nonlocal current_build
        check_build()
        name = get_name()
        operators[name] = current_build.pop()

    def qcomment():
        word = ''
        while word != ')':
            word = next_word()
            if word == '':
                sys.exit('Unfinished comment.')

    def endcomment():
        sys.exit('Unexpected end of comment.')

    def unresolved():
        sys.exit('Unresolved forward reference.')

    def forward():
        nonlocal current_build
        current_build.append([unresolved])

    def resolves():
        nonlocal current_build
        name = get_name()
        if name in operators:
            if operators[name][0] != unresolved:
                sys.exit(name + ' is not a forward reference.')
            check_build()
            operators[name][0] = current_build.pop()
        else:
            sys.exit(' Unrecognised word: ' + name)

    def char_literal():
        nonlocal current_build
        char = one_char()
        if char == '':
            sys.exit('No character found.')
        current_build.append(ord(char))

    def string_literal():
        nonlocal current_build
        delimiter = ''
        result = []
        while delimiter == '':
            char = next_char()
            if char == '':
                sys.exit('No string found.')
            if ord(char) > 32:
                delimiter = char
                char = ''
        while char != delimiter:
            char = next_char()
            if char == '':
                sys.exit('No end of string found.')
            if char != delimiter:
                result.append(ord(char))
        current_build.append([[meta_literal], result])

    def ishex(string):
        hexstr = string
        if len(hexstr) > 1 and hexstr[0] == '-':
            hexstr = hexstr[1:]
        for char in hexstr:
            if char not in '0123456789abcdefABCDEF':
                return False
        return True

    def hexnum():
        nonlocal current_build
        word = get_name()
        if not ishex(word):
            sys.exit(word + " is not hexadecimal.")
        current_build.append(int(word, 16))

    builders = {'is':       qis,
                '(':        qcomment,
                ')':        endcomment,
                'forward':  forward,
                'resolves': resolves,
                'char':     char_literal,
                '$':        string_literal,
                'hex':      hexnum}

    current_build = []

    source = ''

    the_nest = []

    def build(source_string):
        nonlocal source
        nonlocal the_nest
        source = source_string
        nesting = 0

        def sub_build():
            nonlocal nesting
            nonlocal current_build
            the_nest = []
            while True:
                current_build = the_nest
                word = next_word()
                if word == '':
                    return(the_nest)
                elif word == '[':
                    nesting += 1
                    the_nest.append(sub_build())
                elif word == ']':
                    nesting -= 1
                    if nesting < 0:
                        sys.exit('Unexpected end of nest.')
                    return(the_nest)
                elif word in builders.keys():
                    builders[word]()
                elif word in operators.keys():
                    the_nest.append(operators[word])
                elif isinteger(word):
                    the_nest.append(int(word, 10))
                else:
                    sys.exit('Unrecognised word: ' + word)

        the_nest = sub_build()
        if nesting > 0:
            sys.exit('Unfinished nest.')
        return(the_nest)

    predefined = r"""

  [ 0 ]                         is false        (         --> b       )

  [ 1 ]                         is true         (         --> b       )

  [ dup nand ]                  is not          (       b --> b       )

  [ nand not ]                  is and          (     b b --> b       )

  [ not swap not nand ]         is or           (     b b --> b       )

  [ = not ]                     is !=           (     x x --> b       )

  [ not swap not != ]           is xor          (     b b --> b       )

  [ swap > ]                    is <            (     n n --> b       )

  [ negate + ]                  is -            (       n --> n       )

  [ /mod drop ]                 is /            (     n n --> n       )

  [ swap drop ]                 is nip          (     x x --> x       )

  [ /mod nip ]                  is mod          (     n n --> n       )

  [ 1 swap << ]                 is bit          (       n --> n       )

  [ swap over ]                 is tuck         (     x x --> x x x   )

  [ rot rot ]                   is unrot        (   x x x --> x x x   )

  [ rot tuck >
    unrot > not and ]           is within       (   n n n --> b       )

  [ over over ]                 is 2dup         (     x x --> x x x x )

  [ drop drop ]                 is 2drop        (     x x -->         )

  [ ]again[ ]                   is again        (         -->         )

  [ ]done[ ]                    is done         (         -->         )

  [ ]if[ ]                      is if           (       b -->         )

  [ ]iff[ ]                     is iff          (       b -->         )

  [ ]else[ ]                    is else         (         -->         )

  [ 2dup > if swap drop ]       is min          (   n n n --> n       )

  [ 2dup < if swap drop ]       is max          (   n n n --> n       )

  [ rot min max ]               is clamp        (   n n n --> n       )

  [ dup nest? iff [] join ]     is copy         (       [ --> [       )

  [ ]'[ ]                       is '            (         --> x       )

  [ ]this[ ]                    is this         (         --> [       )

  [ ]do[ ]                      is do           (       x -->         )

  [ ]this[ do ]                 is recurse      (         -->         )

  [ not if ]again[ ]            is until        (       b -->         )

  [ not if ]done[ ]             is while        (       b -->         )

  [ immovable ]this[ ]done[ ]   is stack        (         --> s       )

  [ dup take dup rot put ]      is share        (       s --> x       )

  [ take drop ]                 is release      (       s -->         )

  [ dup release put ]           is replace      (     x s -->         )

  [ dup take rot + swap put ]   is tally        (     n s -->         )

  [ swap take swap put ]        is move         (     s s -->         )

  [ [] tuck put ]               is nested       (       x --> [       )

  [ stack [ ] ]                 is protected    (         --> s       )

  [ protected take
    ]'[ nested join
    protected put ]             is protect      (         -->         )

  [ stack ]                     is dip.hold     (         --> s       )
  protect dip.hold

  [ dip.hold put
    ]'[ do
    dip.hold take ]             is dip          (       x --> x       )

  [ rot dip rot ]               is 2swap        ( x x x x --> x x x x )

  [ dip [ dip 2dup ] 2swap ]    is 2over    ( x x x x --> x x x x x x )

  [ stack ]                     is depth        (         --> s       )
  protect depth

  [ depth share
    0 != while
    -1 depth tally
    ]this[ do
    1 depth tally ]             is decurse      (         -->         )

  [ dup 0 < if negate ]         is abs          (       n --> n       )

  [ stack ]                     is times.start  (         --> s       )
  protect times.start

  [ stack ]                     is times.count  (         --> s       )
  protect times.count

  [ stack ]                     is times.action (         --> s       )
  protect times.action

  [ ]'[ times.action put
    dup times.start put
    [ 1 - dup -1 > while
      times.count put
      times.action share do
      times.count take again ]
    drop
    times.action release
    times.start release ]       is times        (       n -->         )

  [ times.count share ]         is i            (         --> n       )

  [ times.start share i 1+ - ]  is i^           (         --> n       )

  [ 0 times.count replace ]     is conclude     (         -->         )

  [ times.start share
    times.count replace ]       is refresh      (         -->         )

  [ times.count take 1+
    swap - times.count put ]    is step         (         --> s       )

  [ stack ]                     is temp         (         --> s       )
  protect temp

  [ immovable
    dup -1 > +
    ]this[ swap peek
    ]done[ ]                    is table        (       n --> x       )

  [ [] unrot
    dup 1 < iff 2drop done
    [ 2 /mod over while
      if [ dip [ tuck join swap ] ]
      dip [ dup join ]
      again ] 2drop join ]      is of           (     x n --> [       )

  [ split 1 split
    swap dip join
    0 peek ]                    is pluck        (     [ n --> [ x     )

  [ split
    rot nested
    swap join join ]            is stuff        (   x [ n --> [       )

  [ 0 pluck ]                   is behead       (       [ --> [ x     )

  [ over size over size
    dup temp put
    swap - 1+ times
      [ 2dup over size split
        drop = if
          [ i^ temp replace
            conclude ]
        behead drop ]
    2drop temp take ]            is findseq     (     [ [ --> n       )

  [ 13 ]                        is carriage     (         --> c       )

  [ carriage emit ]             is cr           (         -->         )

  [ 32 ]                        is space        (         --> c       )

  [ space emit ]                is sp           (         -->         )

  [ dup char a char { within
    if [ 32 - ] ]               is upper        (       c --> c       )

  [ dup char A char [ within
    if [ 32 + ] ]               is lower        (       c --> c       )

  [ dup 10 <
    iff 48 else 55 + ]          is digit        (       n --> c       )

  [ stack 10 ]                  is base         (         --> s       )
  protect base

  [ 10 base put ]               is decimal      (         -->         )

  [ $ '' over abs
    [ base share /mod digit
      rot join swap
      dup 0 = until ]
      drop
      swap 0 < if
        [ $ '-' swap join ] ]   is number$      (       n --> $       )

  [ stack ]                     is with.hold    (         --> s       )
  protect with.hold

  [ nested
    ' [ dup with.hold put
        size times ]
    ' [ with.hold share
        i^ peek ]
    rot join
    nested join
    ' [ with.hold release ]
    join ]                      is makewith     (      x  --> [       )

  [ ]'[ makewith do ]           is witheach     (       [ -->         )

  [ witheach emit ]             is echo$        (       $ -->         )

  [ stack ]                     is mi.tidyup    (         --> s       )
  protect mi.tidyup

  [ stack ]                     is mi.result    (         --> s       )
  protect mi.result

  [ mi.tidyup put
    over size mi.result put
    nested
    ' [ if
        [ i^ mi.result replace
          conclude ] ]
    join makewith do
    mi.tidyup take do
    mi.result take ]            is matchitem    (   [ x x --> n       )

  [ ]'[ ]'[ matchitem ]         is findwith     (   [     --> n       )

  [ size < ]                    is found        (     n [ --> b       )

  [ space > ]                   is printable    (       c --> b       )

  [ dup findwith
      printable [ ]
    split nip ]                 is trim         (       $ --> $       )

  [ dup findwith
      [ printable not ] [ ]
    split swap ]                is nextword     (       $ --> $ $     )

  [ dup nest? if
      [ [] swap witheach
          [ nested
            swap join ] ] ]     is reverse      (       x --> x       )

                        forward is reflect
  [ dup nest? if
    [ [] swap witheach
        [ reflect
          nested
          swap join ] ] ] resolves reflect      (       x --> x       )

  [ [] swap times
      [ swap nested join ]
    reverse ]                   is pack         (     * n --> [       )

  [ witheach [ ] ]              is unpack       (       [ --> *       )

  [ stack ]                     is to-do        (         --> s       )
  protect to-do

  [ ' done swap put ]           is new-do       (      s -->          )

  [ dip [ 1+ pack ] put ]       is add-to       (   * x n s -->       )

  [ [ dup take
      unpack do again ] drop ]  is now-do       (       s -->         )

  [ 1 split reverse join
    now-do ]                    is do-now       (       s -->         )

  [ [ dup take ' done = until ]
    drop ]                      is not-do       (       s -->         )

  [ stack ]                     is sort.test    (         --> s       )
  protect sort.test

  [ ]'[ sort.test put
    [] swap witheach
      [ swap 2dup findwith
        [ over sort.test share
          do ] [ ]
        nip stuff ]
    sort.test release ]         is sortwith     (       [ --> [       )

  [ sortwith > ]                is sort         (       [ --> [       )

  [ 32 127 clamp 32 -
    [ table
       0 86 88 93 94 90 92 87 63 64 75 73 82 74 81 76
       1  2  3  4  5  6  7  8  9 10 83 84 69 72 70 85
      91 11 13 15 17 19 21 23 25 27 29 31 33 35 37 39
      41 43 45 47 49 51 53 55 57 59 61 65 78 66 77 80
      89 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40
      42 44 46 48 50 52 54 56 58 60 62 67 79 68 71  0 ]
  ]                             is qacsfot      (       c --> n       )

  [ [ dup  $ '' = iff false done
      over $ '' = iff true done
      behead rot behead rot
      2dup = iff [ 2drop swap ] again
      qacsfot swap qacsfot > ]
    unrot 2drop ]               is $<           (     $ $ --> b       )

  [ swap $< ]                   is $>           (     $ $ --> b       )

  [ sortwith $> ]               is sort$        (       [ --> [       )

  [ upper 47 - 0 44 clamp
    [ table
      -1  0  1  2  3  4  5  6  7  8  9 -1 -1 -1 -1
      -1 -1 -1 10 11 12 13 14 15 16 17 18 19 20 21
      22 23 24 25 26 27 28 29 30 31 32 33 34 35 -1 ]
    dup 0 base share
    within not if [ drop -1 ] ] is char->n      (       c --> n       )

  [ dup $ '' = iff [ drop 0 false ] done
    dup 0 peek char - =
    tuck if [ behead drop ]
    dup $ '' = iff [ 2drop 0 false ] done
    true 0 rot witheach
      [ char->n
        dup 0 < iff [ drop nip false swap ]
        else [ swap base share * + ] ]
    rot if negate
    swap ]                      is $->n         (       $ --> n b     )

  (    adapted from 'A small noncryptographic PRNG' by Bob Jenkins    )
  (          https://burtleburtle.net/bob/rand/smallprng.html         )

  [ hex FFFFFFFFFFFFFFFF ]      is 64bitmask    (         --> f       )

  [ 64bitmask & ]               is 64bits       (       f --> f       )

  [ dip 64bits 2dup << 64bits
    unrot 64 swap - >> | ]      is rot64        (     f n --> f       )

  [ stack 0 ]                   is prng.a       (         --> s       )
  [ stack 0 ]                   is prng.b       (         --> s       )
  [ stack 0 ]                   is prng.c       (         --> s       )
  [ stack 0 ]                   is prng.d       (         --> s       )

  [ prng.a share
    prng.b share tuck
    7 rot64 - 64bits swap
    prng.c share tuck
    13 rot64 ^ prng.a replace
    prng.d share tuck
    37 rot64 + 64bits prng.b replace
    over + 64bits prng.c replace
    prng.a share + 64bits
    dup prng.d replace ]        is prng         (         --> n       )

  [ hex F1EA5EAD prng.a replace
    dup prng.b replace
    dup prng.c replace
    prng.d replace
    20 times [ prng drop ] ]    is initrandom   (       n -->         )

  hex DEFACEABADFACADE initrandom

  [ time initrandom ]           is randomise    (         -->         )

  [ 64bitmask 1+
    over / over *
    [ prng 2dup > not while
      drop again ]
      nip swap mod ]            is random       (       n --> n       )

  [ [] swap dup size times
    [ dup size random pluck
      nested rot join swap ]
    drop ]                      is shuffle      (       [ --> [       )

  [ stack ]                     is history      (         --> s       )

  [ protected share
    [ dup [] != while
      -1 split 0 peek
      size history put again ]
    drop
    pack dup history put unpack
    stacksize history put
    nestdepth history put
    false history put ]         is backup       (       n -->         )

  [ history release
    nestdepth
    history take
    - ]bailby[
    true history put ]          is bail         (         -->         )

  [ history take iff
      [ stacksize
        history take
        history share
        size - - times drop
        history take unpack
        protected share
        reverse
        [ dup [] != while
          -1 split 0 peek
          dup size
          history take -
          [ dup 0 > while
            over release
            1 - again ]
          2drop again ]
        drop true ]
      else
        [ protected share
          size 3 + times
            [ history release ]
          false ] ]             is bailed       (         --> b       )

  [ quid swap quid = ]          is oats         (     x x --> b       )

  [ [] swap
    [ trim
      dup size while
      nextword nested
      swap dip join again ]
    drop ]                      is nest$        (       $ --> [       )

  [ stack ]                     is namenest     (         --> s       )

  [ namenest share ]            is names        (         --> [       )

  [ names find names found ]    is name?        (       $ --> b       )

                        forward is actions      (       n --> x       )

  [ ' actions ]                 is actiontable  (         --> x       )

  [ stack ]                     is buildernest  (         --> s       )

  [ buildernest share ]         is builders     (         --> s       )

  [ builders find
    builders found ]            is builder?     (       $ --> b       )

                        forward is jobs         (       n --> x       )

  [ ' jobs ]                    is jobtable     (         --> [       )

  [ stack ]                     is message      (         --> s       )

  [ stack ]                     is b.nesting    (         --> s       )
  protect b.nesting

  [ stack ]                     is b.to-do      (         --> s       )

  [ $ '[' b.nesting put
    [] swap ]                   is b.[          (     [ $ --> [ [ $   )

  [ b.nesting take dup
    $ '' = if
      [ $ 'Unexpected "]".'
        message put
        bail ]
    dup $ '[' = iff drop
    else
      [ $ 'Nest mismatch: '
        swap join $ ' ]' join
        message put
        bail ]
    dip [ nested join ] ]       is b.]          (   [ [ $ --> [ $     )

  [ over [] = if
      [ $ '"is" needs something to name.'
        message put
        bail ]
    dup $ '' = if
      [ $ '"is" needs a name after it.'
        message put
        bail ]
    nextword nested
    namenest take
    join
    namenest put
    dip
      [ -1 pluck
        actiontable take
        1 stuff
        actiontable put ] ]     is b.is         (     [ $ --> [ $     )

  [ over [] = if
      [ $ '"builds" needs something to name.'
        message put
        bail ]
    dup $ '' = if
      [ $ '"builds" needs a name after it.'
        message put
        bail ]
    nextword nested
    buildernest take
    join
    buildernest put
    dip
      [ -1 pluck
        jobtable take
        1 stuff
        jobtable put ] ]        is b.builds     (     [ $ --> [ $     )

  [ trim nextword
    dup $ '' = if
      [ $ 'Unfinished comment.'
        message put
        bail ]
    $ ')' = until ]             is b.(          (     [ $ --> $ [     )

  [ $ 'Unexpected ")".'
    message put
    bail ]                      is b.)          (     [ $ --> $ [     )

  [ $ 'Unresolved reference.'
    fail  ]                     is unresolved   (         -->         )

  [ dip
      [ ' [ unresolved ]
        copy nested join ] ]    is b.forward    (     [ $ --> [ $     )

   [ over [] = if
      [ $ '"resolves" needs something to resolve with.'
        message put
        bail ]
    dup $ '' = if
      [ $ '"resolves" needs a name to resolve.'
        message put
        bail ]
     dip [ -1 split ]
     nextword dup temp put
     names find
     dup names found not if
       [ $ 'Unknown word after "resolves": '
         temp take join
         message put
         bail ]
     actions
     dup ' [ unresolved ] = not if
       [ char " temp take join
         $ '" is not an unresolved forward reference.'
         join
         message put
         bail ]
     rot 0 peek over
     replace
     ' unresolved swap
     ' replace 2 b.to-do add-to
     temp release ]             is b.resolves   (     [ $ --> [ $     )

  [ 1 split
    over $ '' = if
      [ $ '"char" needs a character after it.'
        message put
        bail ]
    dip join ]                  is b.char       (     [ $ --> [ $     )

  [ dup $ '' = if
      [ $ '"$" needs to be followed by a string.'
        message put
        bail ]
    behead over find
    2dup swap found not if
      [ $ 'Endless string discovered.'
        message put
        bail ]
    split behead drop
    ' ' nested
    rot nested join
    nested swap dip join ]      is b.$          (     [ $ --> [ $     )

  [ dup $ '' = if
      [ $ '"say" needs to be followed by a string.'
        message put
        bail ]
    $ '$' builders find jobs do
    dip
      [ -1 pluck
        '  echo$ nested join
        nested join ] ]         is b.say        (     [ $ --> [ $     )

  [ 16 base put
    nextword dup
    $ '' = if
      [ $ '"hex" needs a number after it.'
        message put
        bail ]
    dup $->n iff
      [ nip swap dip join ]
    else
      [ drop
        char " swap join
        $ '" is not hexadecimal.'
        join message put
        bail ]
    base release ]              is b.hex        (     [ $ --> [ $     )

  [ dip [ -1 split ] swap do ]  is b.now!       (     [ $ --> [ $     )

  [ over [] = if
      [ $ '"constant" needs something before it.'
        message put
        bail ]
    dip
      [ -1 pluck do
      dup number? not if
        [ ' ' nested swap
          nested join
          nested ]
      join ] ]                  is b.constant   (     [ $ --> [ $     )

  [ ' [ namenest actiontable
        buildernest jobtable ]
    witheach
      [ do share copy
        history put ] ]         is backupwords  (         -->         )

  [ ' [ jobtable buildernest
        actiontable namenest ]
    witheach
      [ do dup release
        history swap move ] ]   is restorewords (         -->         )

  [ 4 times
    [ history release ] ]       is releasewords (         -->         )

  [ backupwords
    b.to-do new-do
    1 backup
      [ $ '' b.nesting put
        decimal
        [] swap
        [ trim
          dup $ '' = iff drop done
          nextword
          dup builders find
          dup builders found iff
            [ dip [ drop trim ]
              jobs do ] again
          drop
          dup names find
          dup names found iff
            [ actions nested
              nip swap dip join ] again
          drop
          dup $->n iff
            [ nip swap dip join ] again
          drop
          $ 'Unknown word: '
          swap join message put
          bail ]
        base release
        b.nesting take dup
        $ '' = iff drop
        else
          [ $ 'Unfinished nest: '
            swap join message put
            bail ] ]
    bailed iff
      [ drop b.to-do now-do
        restorewords
        ' ' nested
        message take nested join
        ' echo$ nested join ]
    else
      [ b.to-do not-do
        releasewords ] ]        is build        (       $ --> [       )

  [ build do ]                  is quackery     (       $ -->         )

  [ stack -1 ]                  is nesting      (         --> [       )

                        forward is unbuild      (       x --> $       )

  [ nesting share
    0 = iff [ drop $ '...' ] done
    $ '' swap
    dup number? iff
      [ number$ join ] done
    actiontable share
    behead drop
    [ dup [] = iff
        [ drop false ] done
      behead
      rot tuck oats iff
        [ drop size 2 +
          actiontable share
          size swap -
          names swap peek join
        true ] done
      swap again ]
    if done
    dup nest? iff
      [ $ '[ ' rot join swap
        [ dup [] = iff drop done
          behead
          -1 nesting tally
          unbuild
          1 nesting tally
          space join
          swap dip join again ]
      $ ']' join ] 
    else 
       [ drop 
         $ "Quackery was worried by a python."
         fail ] ]         resolves unbuild      (       x --> $       )

  [ unbuild echo$ ]             is echo         (       x -->         )

  [ $ ''
    return -2 split drop
    witheach
      [ dup number? iff
        [ number$ join
          $ '} ' join ]
      else
        [ $ '{' swap dip join
          actiontable share
          findwith
            [ over oats ] drop
          dup actiontable share
          found iff
            [ 1 - names swap
              peek join
              space join ]
          else
            [ drop $ '[...] '
              join ] ] ]
    -1 split drop ]             is return$      (         --> $       )

  [ return$ echo$ ]             is echoreturn   (         -->         )

  [ stacksize dup 0 = iff
      [ $ 'Stack empty.' echo$ drop ]
    else
      [ $ 'Stack: ' echo$
        pack dup
        witheach [ echo sp ]
        unpack ]
    cr ]                        is echostack    (         -->         )

  [ cr $ '' $ '/O> '
    [ input
      dup $ '' != while
      carriage join join
      $ '... ' again ]
    drop
    quackery
    5 nesting put
    cr echostack
    nesting release again ]     is shell        (         -->         )

  [ cr randomise 12 random
    [ table
      $ 'Goodbye.'  $ 'Adieu.' $ 'So long.'
      $ 'Cheerio.'  $ 'Aloha.' $ 'Ciao.'
      $ 'Farewell.' $ 'Be seeing you.'
      $ 'Sayonara.' $ 'Auf wiedersehen.'
      $ 'Toodles.'  $ 'Hasta la vista.' ]
    do echo$ cr cr
    3 ]bailby[ ]                is leave        (         -->         )

  [ stacksize times drop ]      is empty        (     all -->         )

  [ tuck temp put
    witheach
      [ dup size
        rot + dup
        temp share > iff
          [ cr drop dup size ]
        else sp 1+ swap echo$ ]
    drop temp release ]          is wrap$        (     [ n -->         )

  [ names reverse 70 wrap$ cr
    builders reverse
    70 wrap$ cr ]                is words        (         -->         )

  [ stack [ 46 47 ] ]            is file.path    (         --> [       )
  file.path protect

  [ dup name? iff drop
    else
      [ dup sharefile not if
        [ $ |$ 'file not found: "|
          swap join
          $ |"' echo$| join ]
        nip quackery ] ]        is loadfile     (       $ -->         )

  [ dup sharefile iff
      [ swap releasefile ]
    else [ drop false ] ]       is takefile     (       $ --> $ b     )

  [ dup releasefile iff
      putfile
    else [ 2drop false ] ]      is replacefile  (     $ $ --> b       )

  [ nested ' [ ' ]
    swap join
    decimal unbuild
    base release ]              is quackify     (       x --> $       )

  $ "quackify replacefile takefile loadfile words empty wrap$ leave
     shell echostack echoreturn return$ echo unbuild nesting quackery
     build releasewords restorewords backupwords unresolved b.to-do
     b.nesting message jobtable jobs builder? builders buildernest
     actiontable actions name? names namenest nest$ oats bailed bail
     backup history shuffle random randomise initrandom prng prng.d
     prng.c prng.b prng.a rot64 64bits 64bitmask $->n char->n sort$
     $> $< qacsfot sort sortwith sort.test not-do do-now now-do
     add-to new-do to-do unpack pack reflect reverse nextword trim
     printable found findwith matchitem mi.result mi.tidyup echo$
     witheach makewith with.hold number$ decimal base digit lower
     upper sp space cr carriage findseq behead stuff pluck of table
     temp step refresh conclude i^ i times times.action times.count
     times.start abs decurse depth 2over 2swap dip dip.hold protect
     protected nested move tally replace release share stack while
     until recurse do this ' copy clamp max min else iff if done
     again 2drop 2dup within unrot tuck bit mod nip / - < xor != or
     and not true false sharefile releasefile putfile input ding emit
     quid operator? number? nest? size poke peek find join split []
     take immovable put ]bailby[ ]do[ ]this[ ]'[ ]else[ ]iff[ ]if[
     ]again[ ]done[ over rot swap drop dup return nestdepth stacksize
     time ~ ^ | & >> << ** /mod * negate + 1+ > = nand fail python
     file.path"
  nest$ namenest put

  [ table
    quackify replacefile takefile loadfile words empty wrap$ leave
    shell echostack echoreturn return$ echo unbuild nesting quackery
    build releasewords restorewords backupwords unresolved b.to-do
    b.nesting message jobtable jobs builder? builders buildernest
    actiontable actions name? names namenest nest$ oats bailed bail
    backup history shuffle random randomise initrandom prng prng.d
    prng.c prng.b prng.a rot64 64bits 64bitmask $->n char->n sort$
    $> $< qacsfot sort sortwith sort.test not-do do-now now-do
    add-to new-do to-do unpack pack reflect reverse nextword trim
    printable found findwith matchitem mi.result mi.tidyup echo$
    witheach makewith with.hold number$ decimal base digit lower
    upper sp space cr carriage findseq behead stuff pluck of table
    temp step refresh conclude i^ i times times.action times.count
    times.start abs decurse depth 2over 2swap dip dip.hold protect
    protected nested move tally replace release share stack while
    until recurse do this ' copy clamp max min else iff if done
    again 2drop 2dup within unrot tuck bit mod nip / - < xor != or
    and not true false sharefile releasefile putfile input ding emit
    quid operator? number? nest? size poke peek find join split []
    take immovable put ]bailby[ ]do[ ]this[ ]'[ ]else[ ]iff[ ]if[
    ]again[ ]done[ over rot swap drop dup return nestdepth stacksize
    time ~ ^ | & >> << ** /mod * negate + 1+ > = nand fail python
    file.path ]

                          resolves actions      (       n --> x       )

  $ "constant now! hex say $ char resolves forward ) ( builds is ] ["
  nest$ buildernest put

  [ table
    b.constant b.now! b.hex b.say b.$ b.char b.resolves
    b.forward b.) b.( b.builds b.is b.] b.[ ]

                          resolves jobs         (       n --> x       )

                  """

    traverse(build(predefined))
    while(True):
        to_stack([ord(char) for char in source_string])
        try:
            traverse(build('quackery'))
        except QuackeryError as diagnostics:
            if __name__ == '__main__' and len(sys.argv) == 1:
                print(diagnostics)
                continue
            else:
                raise
        except Exception as diagnostics:
            print('Quackery system damage detected.')
            print('Python reported: ' + str(diagnostics))
            sys.exit()
        else:
            traverse(build('stacksize pack decimal unbuild'))
            result = ''
            for ch in (qstack[0][2:-2]):
                result += chr(ch)
            return(result)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            f = open(filename)
            filetext = f.read()
            f.close()
        except FileNotFoundError:
            print('Cannot find file "' + filename + '"')
        else:
            try:
                print(quackery(filetext))
                print()
            except QuackeryError as diagnostics:
                print()
                print('Quackery crashed.')
                print()
                print(diagnostics)
                print()
            except Exception as diagnostics:
                print('Quackery system damage detected.')
                print('Python reported: ' + str(diagnostics))
                sys.exit()
    else:
        print()
        print('Welcome to Quackery.')
        print()
        print('Enter "leave" to leave the shell.')
        quackscript = r"""

          $ 'extensions.qky' dup name? not
          dip sharefile and iff
            [ cr say 'Building extensions.' cr quackery ]
          else drop

          shell """

        try:
            quackery(quackscript)
            print()
        except QuackeryError as diagnostics:
            print()
            print('Quackery crashed.')
            print()
            print(diagnostics)
            print()
