`timescale 1ns/1ps
 module testbench(
    );
    reg clk;
    
    initial begin
        clk = 0;
    end
    
    wire [31:0] pc_in, pc_out, instruction_in, instruction_out, extended, dataOutA, dataOutB, eRegOutA, eRegOutB, eExtended, aluSelect, aluOut, maluOut, mRegOutB, dataMemOut, waluOut, wdataMemOut, d, twoBitMuxA, twoBitMuxB;
    wire wreg, m2reg, wmem, aluimm, regrt, ewreg, em2reg, ewmem, ealuimm, mwreg, mm2reg, mwmem, wwreg, wm2reg;
    wire [1:0] fwda, fwdb;
    wire [3:0] aluc, ealuc;
    wire [4:0] rdrt, emux, mmux, wmux, wn;

    PC PC(clk, pc_in, pc_out);
    adder adder(pc_out, pc_in);
    IM_reg IM_reg(pc_out, instruction_in);
    IF_ID IF_ID(clk, instruction_in, instruction_out);
    controlunit controlunit(instruction_out, ewreg, em2reg, mwreg, mm2reg, emux, mmux, wreg, m2reg, wmem, aluimm, regrt, aluc, fwda, fwdb);
    TwoBitMux TwoBitMux1(fwda, dataOutA, aluOut, maluOut, dataMemOut, twoBitMuxA); 
    TwoBitMux TwoBitMux2(fwdb, dataOutB, aluOut, maluOut, dataMemOut, twoBitMuxB); 
    mux mux(regrt, instruction_out, rdrt);
    SignExt SignExt(instruction_out[15:0], extended);
    ID_EXE ID_EXE(clk, wreg, m2reg, wmem, aluimm, aluc, rdrt, twoBitMuxA, twoBitMuxB, extended, ewreg, em2reg, ewmem, ealuimm, ealuc, emux, eRegOutA, eRegOutB, eExtended);
    FullMux FullMux(eRegOutB, eExtended, ealuimm, aluSelect);
    alu alu(eRegOutA, aluSelect, ealuc, aluOut);
    ExeMem ExeMem(clk, ewreg, em2reg, ewmem, emux,eRegOutB, aluOut, mwreg, mm2reg, mwmem, mmux, maluOut, mRegOutB);
    DataMem DataMem(clk, mwmem, maluOut, mRegOutB, dataMemOut);
    MemWb MemWb(clk, mwreg, mm2reg, mmux, maluOut, dataMemOut, wwreg, wm2reg, wmux, waluOut, wdataMemOut);
    FullMux FullMux2(waluOut, wdataMemOut, wm2reg, d);
    RegFile RegFile(clk, wwreg, instruction_out[25:21], instruction_out[20:16], wmux, d, dataOutA, dataOutB);
    
    
    always
        #1 clk = ! clk;
    
endmodule
