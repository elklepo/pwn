
call_stack = [['DUMMY_FRAME', '']]


def exit_handler(event):
    merged_stack = [[]]
    graph = []

    for call in call_stack[2:]:
        if call not in merged_stack:
            merged_stack.append(call)

    counter = 1
    graph.append("digraph {")
    for call in merged_stack[1:]:
        graph.append(call[1] + ' -> ' + call[0] + '[label="' + str(counter) + '"];')
        counter = counter + 1
    graph.append('}')

    with open(graph_path, "w") as file:
        file.write("\n".join(graph))

    print("graph written to: " + graph_path)

def stop_handler(event):

    frame_name = str(gdb.newest_frame().name())
    rip_reg = str(gdb.newest_frame().read_register('rip'))

    lib_name = str(gdb.solib_name(int(rip_reg.split()[0], 16)))
    caller_name = ''

    if gdb.newest_frame().older() is not None:
        caller_name = str(gdb.newest_frame().older().name())
        if caller_name == 'None':
            return
    else:
        caller_name = ''

    if call_stack[-1][0] != frame_name:
        call_stack.append([frame_name, caller_name, lib_name])


gdb.events.exited.connect(exit_handler)
gdb.events.stop.connect(stop_handler)

"""
gdb.execute("set pagination off")
gdb.execute("set logging off")
gdb.execute("set logging file /dev/null")
gdb.execute("set logging redirect on")
gdb.execute("set logging on")
"""

gdb.execute("br _start")
gdb.execute('run')

while True:
    gdb.execute("stepi")

