module TwoBitMux(
input [1:0] select,
input [31:0] regFileOut, ealuOut, maluOut, dataMemOut,
output [31:0] out
    );
    
    assign out = select[1] ? (select[0] ? dataMemOut : maluOut) : (select[0] ? ealuOut : regFileOut);
    
endmodule
