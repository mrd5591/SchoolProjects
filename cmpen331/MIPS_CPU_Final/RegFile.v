module RegFile(
input clk, we,
input [4:0] rna, rnb, wn,
input [31:0] d,
output [31:0] dataOutA, dataOutB
    );
    
    reg [31:0] regs [31:0];
    integer i;
    
    initial begin
        for (i = 0; i<32; i=i+1) begin
            regs[i] <= 0;
        end
    end
    
    assign dataOutA = regs[rna];
    assign dataOutB = regs[rnb];
    
    always @ (posedge clk) begin
        if(we)
            regs[wn] <= d;
    end
    
endmodule
