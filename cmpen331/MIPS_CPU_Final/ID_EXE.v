module ID_EXE(
input clk, wreg, m2reg, wmem, aluimm,
input [1:0] aluc,
input [4:0] mux,
input [31:0] regOutA, regOutB, extended,
output reg ewreg, em2reg, ewmem, ealuimm,
output reg [3:0] ealuc,
output reg [4:0] emux,
output reg [31:0] eRegOutA, eRegOutB, eExtended
    );
    
    always @ (posedge clk)
    begin
        ewreg = wreg;
        em2reg = m2reg;
        ewmem = wmem;
        ealuimm = aluimm;
        ealuc = aluc;
        eRegOutA = regOutA;
        eRegOutB = regOutB;
        eExtended = extended;
        emux = mux;
    end
    
endmodule
