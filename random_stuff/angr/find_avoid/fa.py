import angr
import claripy

# angr uses 0x400000 as base address for PIE executables
START = 0x4006da
AVOID = [0x400724, 0x400742, 0x400760, 0x40077e, 0x40079c, 0x4007ba, 0x4007d8, 0x4007f6, 0x400814, 0x400832, 0x400850, 0x40086e, 0x40088c, 0x4008aa, 0x4008c8, 0x4008e6, 0x400901, 0x40091c, 0x400937, 0x400952]
FIND = [0x400959]
BUF_LEN = 20

def char(state, c):
    return state.solver.And(c <= '~', c >= ' ')

def main():
    p = angr.Project("./fa") 

    print('---START---')
    b = p.factory.block(START)
    b.pp()                
    
    print('---FIND---')
    for f in FIND:
        b = p.factory.block(f)
        b.pp()
        print('------')

    print('---AVOID---')
    for a in AVOID:
        b = p.factory.block(a)
        b.pp()
        print('------')

    flag = claripy.BVS('flag', BUF_LEN * 8)
    state = p.factory.blank_state(addr=START, stdin=flag)
   
    for c in flag.chop(8):
        state.solver.add(char(state, c))

    ex = p.factory.simulation_manager(state)
    ex.use_technique(angr.exploration_techniques.Explorer(find=FIND, avoid=AVOID))

    ex.run()

    return ex.found[0].posix.dumps(0).decode("utf-8")


if __name__ == '__main__':
    print("flag: {}".format(main()))
