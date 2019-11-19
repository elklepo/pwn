#include "pin.H"
#include <iostream>
#include <fstream>
#include <stack> 
#include <map> 
#include <utility> 
using std::hex;
using std::cerr;
using std::string;
using std::ios;
using std::endl;
using std::pair;

std::ofstream TraceFile;

KNOB<string> KnobOutputFile(KNOB_MODE_WRITEONCE, "pintool",
    "o", "cache_function_calls.log", "specify trace file name");


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


std::stack<pair<pair<ADDRINT, ADDRINT>, ADDRINT>> stack;
std::map<pair<ADDRINT, ADDRINT>, pair<ADDRINT, ADDRINT>> map;
 
VOID foo_entry_hook(CONTEXT *ctx, ADDRINT arg1, ADDRINT arg2_ptr, ADDRINT ret_addr)
{
    // read arg2 value from its reference
    ADDRINT arg2;
    PIN_SafeCopy(&arg2, (void*)arg2_ptr, sizeof(ADDRINT));

    TraceFile << "foo(" << arg1 << ", " << arg2 << ")";

    auto args = std::make_pair(arg1, arg2);

    // if return values are not already cached for given arguments
    if(map.count(args) == 0)
    {
        // push to internal stack both argument values 
        // and reference to second argument (which is also reference to second return value).
        stack.push(std::make_pair(args, arg2_ptr));
        // let the function execute
        return;
    }

    // get cached return values for given arguments
    auto rvals = map[args];
    TraceFile << " = "<< rvals.first << ", " << rvals.second << " [cached]" << endl;

    // override first return value
    PIN_SetContextReg(ctx, REG_RAX, rvals.first);
    // override second return value which was passed as reference
    PIN_SafeCopy((void*)arg2_ptr, &rvals.second, sizeof(ADDRINT));
    // set RIP to function return address
    PIN_SetContextReg(ctx, REG_INST_PTR, ret_addr);
    // pop return address from stack
    ADDRINT r_rsp = PIN_GetContextReg(ctx, LEVEL_BASE::REG_RSP);
    PIN_SetContextReg(ctx, REG_RSP, r_rsp + 8);
    // resume execution with updated context
    PIN_ExecuteAt(ctx);
}

VOID foo_ret_hook(ADDRINT rval1)
{
    // get both argument values and reference to second argument for given call
    auto params = stack.top();
    stack.pop();
    auto args = params.first;

    // read second return value using second argument reference
    ADDRINT rval2;
    PIN_SafeCopy(&rval2, (void*)params.second, sizeof(rval2));

    // cache return values for given arguments
    map[args] = std::make_pair(rval1, rval2);
    
    TraceFile << " = " << rval1 << ", " << rval2 << endl;
}

VOID Image(IMG img, VOID *v)
{
    //  Find the foo() function.
    RTN fooRtn = RTN_FindByName(img, "foo");

    if (RTN_Valid(fooRtn))
    {
        RTN_Open(fooRtn);

        // Instrument foo() at entry.
        RTN_InsertCall(fooRtn, IPOINT_BEFORE, (AFUNPTR)foo_entry_hook,
                        IARG_CONTEXT,
                        IARG_FUNCARG_ENTRYPOINT_VALUE, 0,
                        IARG_FUNCARG_ENTRYPOINT_VALUE, 1,
                        IARG_RETURN_IP,
                        IARG_END);

        // Instrument foo() at returns.
        RTN_InsertCall(fooRtn, IPOINT_AFTER, (AFUNPTR)foo_ret_hook,
                        IARG_FUNCRET_EXITPOINT_VALUE, // same as IARG_REG_VALUE, REG_RAX
                        IARG_END);

        RTN_Close(fooRtn);
    }
}

VOID Fini(INT32 code, VOID *v)
{
    TraceFile.close();
}
   
INT32 Usage()
{
    cerr << "This tool produces a trace of calls to malloc." << endl;
    cerr << endl << KNOB_BASE::StringKnobSummary() << endl;
    return -1;
}

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
    TraceFile.setf(ios::showbase);
    
    // Register Image to be called to instrument functions.
    IMG_AddInstrumentFunction(Image, 0);
    PIN_AddFiniFunction(Fini, 0);

    // Never returns
    PIN_StartProgram();
    
    return 0;
}
