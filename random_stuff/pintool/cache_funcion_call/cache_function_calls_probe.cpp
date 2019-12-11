#include "pin.H"
#include <iostream>
#include <fstream>
#include <stack> 
#include <map> 
#include <utility> 
using std::hex;
using std::dec;
using std::cerr;
using std::cout;
using std::string;
using std::ios;
using std::endl;
using std::pair;

std::ofstream TraceFile;

KNOB<string> KnobOutputFile(KNOB_MODE_WRITEONCE, "pintool",
    "o", "cache_function_calls_probe.log", "specify trace file name");


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


std::map<pair<UINT64, UINT64>, pair<UINT64, UINT64>> map;
 
typedef UINT64 ( *FP_foo )( UINT64, UINT64 * );
UINT64 new_foo(FP_foo orgFuncptr, UINT64 arg1, UINT64 * arg2_ptr)
{
    // read arg2 value from its reference
    UINT64 arg2;
    PIN_SafeCopy(&arg2, (void*)arg2_ptr, sizeof(arg2));

    auto args = std::make_pair(arg1, arg2);

    if(map.count(args) == 0)
    {
        // execute original function
        UINT64 rval1 = orgFuncptr( arg1, arg2_ptr );
        // read rval2 value from its reference
        UINT64 rval2;
        PIN_SafeCopy(&rval2, (void*)arg2_ptr, sizeof(rval2));

        TraceFile << "foo(" << arg1 << ", " << arg2 << ") = " << rval1 << ", " << rval2 << endl;
        // cache return values
        map[args] = std::make_pair(rval1, rval2);
        return rval1;
    }

    // get cached return values for given arguments
    auto rvals = map[args];
    TraceFile << "foo(" << arg1 << ", " << arg2 << ") = " << rvals.first << ", " << rvals.second << " [cached]" << endl;

    // override second return value which was passed as reference
    PIN_SafeCopy((void*)arg2_ptr, &rvals.second, sizeof(rvals.second));

    return rvals.first;
}


VOID Image(IMG img, VOID *v)
{
    // Find the foo() function.
    RTN fooRtn = RTN_FindByName(img, "foo");

    if (RTN_Valid(fooRtn))
    {
        if (RTN_IsSafeForProbedReplacement(fooRtn))
        {
            // create function prototype
            PROTO proto_foo= PROTO_Allocate(
                PIN_PARG(UINT64), 
                CALLINGSTD_DEFAULT, 
                "foo",
                PIN_PARG(UINT64), 
                PIN_PARG(UINT64 *), 
                PIN_PARG_END());
            // replace function with wrapper
            RTN_ReplaceSignatureProbed(
                fooRtn, 
                AFUNPTR(new_foo),
                IARG_PROTOTYPE, proto_foo,
                IARG_ORIG_FUNCPTR,
                IARG_FUNCARG_ENTRYPOINT_VALUE, 0,
                IARG_FUNCARG_ENTRYPOINT_VALUE, 1,
                IARG_END);

            PROTO_Free(proto_foo);
        }
        else
        {
            cout << "Skip replacing foo() in " << IMG_Name(img) << " since it is not safe." << endl;
            exit(-1);
        }
    }
}

VOID Fini(INT32 code, VOID *v)
{
    TraceFile.close();
}
   
INT32 Usage()
{
    cerr << "This tool shows a way to cache function return values using probe mode." << endl;
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

    // Start the program in probe mode, never returns
    PIN_StartProgramProbed();
    
    return 0;
}
