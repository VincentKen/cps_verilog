
`define width1 3

module test_with_param ( in1, in2, out1 );
    
parameter width2=2;
    
input [`width1-width2 : 0 ] in1;
    
input [`width1+width2 : 0 ] in2;
    
output [`width1:0] out1;

    
assign out1 = in1 & in2;


endmodule
