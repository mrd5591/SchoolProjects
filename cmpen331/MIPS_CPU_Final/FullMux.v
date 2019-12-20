module FullMux(
    input [31:0] a, b,
	input select,
	output [31:0] out
    );
    

    assign out = (select == 0) ?  a : b;

    
endmodule
