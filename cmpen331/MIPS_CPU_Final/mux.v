module mux(
input select,
input [31:0] do,
output [4:0] out
    );
        assign out = select ? do[20:16] : do[15:11];
    
endmodule
