#include "pin.H"
#include <iostream>
#include <fstream>
using std::hex;
using std::cerr;
using std::cout;
using std::string;
using std::ios;
using std::endl;

std::ofstream TraceFile;

KNOB<string> KnobOutputFile(KNOB_MODE_WRITEONCE, "pintool",
    "o", "zwiebel_solver.log", "specify trace file name");

VOID displayCurrentContext(CONTEXT *ctx)
{
  TraceFile << std::hex << std::internal << std::setfill('0') 
    << "RAX = " << std::setw(16) << PIN_GetContextReg(ctx, REG_RAX) << " " 
    << "RBX = " << std::setw(16) << PIN_GetContextReg(ctx, REG_RBX) << " " 
    << "RCX = " << std::setw(16) << PIN_GetContextReg(ctx, REG_RCX) << std::endl
    << "RDX = " << std::setw(16) << PIN_GetContextReg(ctx, REG_RDX) << " " 
    << "RDI = " << std::setw(16) << PIN_GetContextReg(ctx, REG_RDI) << " " 
    << "RSI = " << std::setw(16) << PIN_GetContextReg(ctx, REG_RSI) << std::endl
    << "RBP = " << std::setw(16) << PIN_GetContextReg(ctx, REG_RBP) << " "
    << "RSP = " << std::setw(16) << PIN_GetContextReg(ctx, REG_RSP) << " "
    << "RIP = " << std::setw(16) << PIN_GetContextReg(ctx, REG_RIP) << std::endl << std::endl;
}


UINT8  *shellcode_addr = NULL;
UINT64 shellcode_len  = 0;

char flag[100] = {0};

VOID MmapBefore(VOID *addr, UINT64 length, UINT64 prot, UINT64 flags, UINT64 fd, UINT64 offset)
{
    shellcode_len = length;
    TraceFile << "mmap("    << addr << ", " 
                            << length << ", " 
                            << prot << ", " 
                            << flags << ", " 
                            << fd << ", " 
                            << offset << ")" << endl;
}

VOID MmapAfter(ADDRINT ret)
{
    shellcode_addr = (UINT8*)ret;
    TraceFile << "mmap returns " << ret << endl;
}

UINT64 char_off = -1;
UINT8 char_mask  = -1;

VOID RecordMov(VOID *ip, UINT64 disp)
{
    if(shellcode_addr != NULL &&
        ip >= shellcode_addr && ip <= shellcode_addr + shellcode_len)
    {
        char_off = disp;
        TraceFile << "MOV at " << ip << ": " << disp << endl;
    }
}


// Print a memory read record
VOID RecordAnd(VOID *ip, UINT64 reg_val, UINT64 val)
{
    if(shellcode_addr != NULL &&
        ip >= shellcode_addr && ip <= shellcode_addr + shellcode_len)
    {
        char_mask = (0xFF & val);
        TraceFile << "AND at " << ip << ": " << reg_val << " " << (0xFF & val) << endl;
    }
}

VOID RecordJump(CONTEXT *ctx, VOID *ip, OPCODE opcode, UINT64 target, UINT64 fall)
{
    if(shellcode_addr != NULL &&
        ip >= shellcode_addr && ip <= shellcode_addr + shellcode_len)
    {
        if(opcode == XED_ICLASS_JZ)
        {
            TraceFile << "JZ";
            flag[char_off] |= char_mask;
        }
        else if(opcode == XED_ICLASS_JNZ)
        {
            TraceFile << "JNZ";
            flag[char_off] &= (0xFF | char_mask);
        }
        else
        {
            exit(-1); //should not happen due to check in Instruction()
        }

        TraceFile << " at " << ip << ": " << target << " " << fall << endl;

        PIN_SetContextReg(ctx, REG_INST_PTR, fall);
        PIN_ExecuteAt(ctx);
    }
}


// Is called for every instruction and instruments reads and writes
VOID Instruction(INS ins, VOID *v)
{
    INS next = INS_Next(ins);
    INS n_next = INS_Next(next);

    if( INS_IsMov(ins) &&
        INS_OperandCount(ins) > 1 &&
        INS_MemoryOperandCount(ins) == 1 &&
        INS_OperandReg(ins, 0) == REG_AL &&
        INS_OperandMemoryBaseReg(ins, INS_MemoryOperandIndexToOperandIndex(ins, 0)) == REG_RAX && 
        INS_OperandMemoryIndexReg(ins, INS_MemoryOperandIndexToOperandIndex(ins, 0)) == REG_INVALID_ &&
        // next
        INS_Opcode(next) == XED_ICLASS_AND && 
        INS_OperandCount(next) > 1 &&
        INS_OperandReg(next, 0) == REG_AL &&
        // next->next
        (INS_Opcode(n_next) == XED_ICLASS_JZ || INS_Opcode(n_next) == XED_ICLASS_JNZ)
        )
    {
        INS_InsertPredicatedCall(
            ins, IPOINT_BEFORE, (AFUNPTR)RecordMov,
            IARG_INST_PTR,
            IARG_UINT64, INS_OperandMemoryDisplacement(ins, INS_MemoryOperandIndexToOperandIndex(ins, 0)),
            IARG_END);

        INS_InsertPredicatedCall(
            next, IPOINT_BEFORE, (AFUNPTR)RecordAnd,
            IARG_INST_PTR,
            IARG_REG_VALUE, REG_AL,
            IARG_UINT64, INS_OperandImmediate(next, 1),
            IARG_END);

        INS_InsertPredicatedCall(
            n_next, IPOINT_BEFORE, (AFUNPTR)RecordJump,
            IARG_CONTEXT,
            IARG_INST_PTR,
            IARG_UINT64, INS_Opcode(n_next),
            IARG_BRANCH_TARGET_ADDR,
            IARG_FALLTHROUGH_ADDR,
            IARG_END);
    }
}

VOID Image(IMG img, VOID *v)
{
    // Instrument the malloc() and free() functions.  Print the input argument
    // of each malloc() or free(), and the return value of malloc().
    //
    //  Find the malloc() function.
    RTN mmapRtn = RTN_FindByName(img, "mmap");
    if (RTN_Valid(mmapRtn))
    {
        RTN_Open(mmapRtn);

        // Instrument malloc() to print the input argument value and the return value.
        RTN_InsertCall(mmapRtn, IPOINT_BEFORE, (AFUNPTR)MmapBefore,
                       IARG_FUNCARG_ENTRYPOINT_VALUE, 0,
                       IARG_FUNCARG_ENTRYPOINT_VALUE, 1,
                       IARG_FUNCARG_ENTRYPOINT_VALUE, 2,
                       IARG_FUNCARG_ENTRYPOINT_VALUE, 3,
                       IARG_FUNCARG_ENTRYPOINT_VALUE, 4,
                       IARG_FUNCARG_ENTRYPOINT_VALUE, 5,
                       IARG_END);

        RTN_InsertCall(mmapRtn, IPOINT_AFTER, (AFUNPTR)MmapAfter,
                       IARG_FUNCRET_EXITPOINT_VALUE, 
                       IARG_END);

        RTN_Close(mmapRtn);
    }
}

VOID Fini(INT32 code, VOID *v)
{
    cout << "flag: " << flag << endl;
    TraceFile.close();
}

/* ===================================================================== */
/* Print Help Message                                                    */
/* ===================================================================== */
INT32 Usage()
{
    cerr << "This tool produces a trace of calls to malloc." << endl;
    cerr << endl << KNOB_BASE::StringKnobSummary() << endl;
    return -1;
}

/* ===================================================================== */
/* Main                                                                  */
/* ===================================================================== */

int main(int argc, char *argv[])
{
    // Initialize pin & symbol manager
    PIN_InitSymbols();
    if( PIN_Init(argc,argv) )
    {
        return Usage();
    }
    
    // Write to a file since cout and cerr maybe closed by the application
    TraceFile.open(KnobOutputFile.Value().c_str());
    TraceFile << hex;
    TraceFile.setf(ios::showbase);
    
    IMG_AddInstrumentFunction(Image, 0);
    INS_AddInstrumentFunction(Instruction, 0);
    PIN_AddFiniFunction(Fini, 0);

    // Never returns
    PIN_StartProgram();
    
    return 0;
}