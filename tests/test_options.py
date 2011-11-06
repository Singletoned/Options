import options

def test_optdict():
    d = options.OptDict()
    d['x'] = 5
    d['y'] = 4
    d['z'] = 99
    d['no_other_thing'] = 5
    assert d.x == 5
    assert d.y == 4
    assert d.z == 99
    assert d.no_z == False
    assert d.no_other_thing == True
    try:
        d.p
    except KeyError:
        pass
    else:
        assert False


optspec = """
prog <optionset> [stuff...]
prog [-t] <boggle>
--
t       test
q,quiet   quiet
l,longoption=   long option with parameters and a really really long description that will require wrapping
p= short option with parameters
onlylong  long option with no short
neveropt never called options
deftest1=  a default option with default [1]
deftest2=  a default option with [1] default [2]
deftest3=  a default option with [3] no actual default
deftest4=  a default option with [[square]]
deftest5=  a default option with "correct" [[square]
no-stupid  disable stupidity
#,compress=  set compression level [5]
"""


def test_options():
    o = options.Options(optspec)
    (opt,flags,extra) = o.parse(['-tttqp', 7, '--longoption', '19',
                                 'hanky', '--onlylong', '-7'])
    assert flags[0] == ('-t', '')
    assert flags[1] == ('-t', '')
    assert flags[2] == ('-t', '')
    assert flags[3] == ('-q', '')
    assert flags[4] == ('-p', 7)
    assert flags[5] == ('--longoption', '19')
    assert extra == ['hanky']
    assert (opt.t, opt.q, opt.p, opt.l, opt.onlylong,
              opt.neveropt) == (3,1,7,19,1,None)
    assert (opt.deftest1, opt.deftest2, opt.deftest3, opt.deftest4,
              opt.deftest5) == (1,2,None,None,'[square')
    assert (opt.stupid, opt.no_stupid) == (True, False)
    assert opt['#'] == 7
    assert opt.compress == 7

    (opt,flags,extra) = o.parse(['--onlylong', '-t', '--no-onlylong'])
    assert (opt.t, opt.q, opt.onlylong) == (1, None, 0)
