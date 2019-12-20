module controlunit(
input [31:0] do,
input ewreg, em2reg, mwreg, mm2reg,
input [4:0] ern, mrn,
output reg wreg, m2reg, wmem, aluimm, regrt,
output reg [1:0] forwardA, forwardB,
output reg [3:0] aluc
    );
    
    reg [5:0] op;
    reg [5:0] func;
    
    always @ (*) begin
        op <= do[31:26];
        func <= do[5:0];
        
        //EX Hazard
        if(ewreg && em2reg != 0 && em2reg==do[25:21])
            forwardA = 2'b10;
        if(ewreg && em2reg != 0 && em2reg==do[20:16])
            forwardB = 2'b10;
        
        //MEM Hazard
        if(mwreg && mm2reg != 0 && mm2reg ==do[25:21])
            forwardA = 2'b01;
        if(mwreg && mm2reg != 0 && mm2reg==do[20:16])
            forwardB = 2'b01;
        
        case(op)
        
            6'b000000: begin

		// Deriving r-format control signals from the function codes
            case(func)
    
            // ADD
            6'b100000: begin
                aluc = 4'b0010;
                wreg = 1;
                m2reg = 0;
                aluimm = 0;
                regrt = 0;
                wmem = 0;
            end
    
            // SUB
            6'b100010: begin
                aluc = 4'b0110;
                wreg = 1;
                m2reg = 0;
                aluimm = 0;
                regrt = 0;
                wmem = 0;
            end
    
            // AND
            6'b100100: begin
                aluc = 4'b0000;
                wreg = 1;
                m2reg = 0;
                aluimm = 0;
                regrt = 0;
                wmem = 0;
            end
    
            // OR
            6'b100101: begin
                aluc = 4'b0001;
                wreg = 1;
                m2reg = 0;
                aluimm = 0;
                regrt = 0;
                wmem = 0;
            end
    
            // XOR
            6'b100110: begin
                aluc = 4'b0010;
                wreg = 1;
                m2reg = 0;
                aluimm = 0;
                regrt = 0;
                wmem = 0;
            end
    
            // SLL
            // SRL
            // SRA
            // JR
            
            endcase
        end
        //LW
        6'b100011: begin
            aluc = 4'b0010;
            wreg = 1;
            m2reg = 1;
            aluimm = 1;
            regrt = 1;
            wmem = 0;
        end
        
        //SW
        6'b101011: begin
            aluc = 4'b0010;
            wreg = 0;
            m2reg = 0;
            aluimm = 1;
            regrt = 1;
            wmem = 1;
	    end
        
        default: begin
            aluc = 4'b0000;
		    wreg = 0;
		    m2reg = 0;
		    aluimm = 0;
		    regrt = 0;
		    wmem = 0;
	    end
        endcase
    end
    
endmodule
