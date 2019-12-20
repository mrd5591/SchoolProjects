module IM_reg(
input [31:0] pc,
output [31:0] out
    );
    
    wire [31:0] IM [0:511];
    
    assign IM[100] = 32'h34040050; // (00) main: ori $4, $zero, 0x50 no stall $4 = 0x0 | 0x50 = 0x50
    assign IM[104] = 32'h8c880000; // (04) lw $8, 0($4) no stall $8 = ram[$4] = ram[0x50] = 0xa3
    assign IM[108] = 32'h20840004; // (08) addi $4, $4, 4 no stall $4 = $4 + 4 = 0x54
    assign IM[112] = 32'h8c890000; // (0c) lw $9, 0($4) no stall $9 = ram[$4] = ram[0x54] = 0x27
    assign IM[116] = 32'h01094020; // (10) add $8, $8, $9 stall $8 = $8 + $9 = 0xa3 + 0x27 = 0xca
    assign IM[120] = 32'h20840004; // (14) addi $4, $4, 4 no stall $4 = $4 + 4 = 0x58
    assign IM[124] = 32'hac880000; // (18) sw $8, 0($4) no stall ram[$4] = $8 -> ram[0x58] = 0xca
    
    assign out = IM[pc];
    
endmodule
