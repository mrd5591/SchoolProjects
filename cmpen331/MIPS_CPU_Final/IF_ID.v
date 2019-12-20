module IF_ID(
input clk,
input [31:0] do,
output reg [31:0] out
    );
    
    always @ (posedge clk) begin
        out <= do;
    end
    
endmodule
