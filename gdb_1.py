#        gdb_Value = gdb.newest_frame().read_register('rip')


call_stack = [['DUMMY_FRAME', '']]
is_running = True

def exit_handler(event):
    merged_stack = [[]]

    for call in call_stack[2:]:
        if call not in merged_stack:
            merged_stack.append(call)

    counter = 1
    print('digraph {')
    for call in merged_stack[1:]:
        print(call[1] + ' -> ' + call[0] + '[label="' + str(counter) + '"];')
        counter = counter + 1

    print('}')


gdb.execute("br *_start")
gdb.execute("run")

gdb.events.exited.connect(exit_handler)

while is_running:
    gdb.execute("stepi")

    frame_name = str(gdb.newest_frame().name())
    rip_reg = str(gdb.newest_frame().read_register('rip'))

    lib_name = str(gdb.solib_name(int(rip_reg.split()[0], 16)))

    caller_name = ''

    if gdb.newest_frame().older() is not None:
        caller_name = str(gdb.newest_frame().older().name())
        if caller_name == 'None':
            continue
    else:
        caller_name = ''

    if call_stack[-1][0] != frame_name:
        call_stack.append([frame_name, caller_name])

