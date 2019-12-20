module PC(
input clk,
input [31:0] pc_in,
output reg [31:0] pc_out
    );
    
    initial begin
        pc_out <= 100;
    end
    
    always @ (posedge clk) begin
        pc_out <= pc_in;
    end
    
endmodule
