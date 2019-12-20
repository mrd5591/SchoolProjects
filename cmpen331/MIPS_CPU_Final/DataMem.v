module DataMem(
    input clk, enableWrite,
	input [31:0] Addr, dataIn,
	output [31:0] dataOut
	);

reg [31:0] mem [255:0];
assign dataOut = mem[Addr[6:2]];

always @ (posedge clk)
begin
    if (enableWrite)
        mem[Addr[6:2]] = dataIn;
end

integer i;
initial begin
    for(i = 0; i<32; i=i+1)
        mem[i] = 0;
	mem[5'h14] = 32'h000000a3;
	mem[5'h15] = 32'h00000027;
	mem[5'h16] = 32'h00000079;
	mem[5'h17] = 32'h00000115;
end
	
endmodule
