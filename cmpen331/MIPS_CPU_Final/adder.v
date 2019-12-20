module adder(
inpc,
outpc
    );
    input [31:0] inpc;
    output wire [31:0] outpc;
    
    assign outpc = inpc + 4;
    
endmodule
