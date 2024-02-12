module reset_waveforms ( clk1, clk2, rst1, rst2, in1, in2, out1, out2 );
input clk1, rst1;
input clk2, rst2;
input in1, in2;
output out1;
output out2;
reg out1;
reg out2;

always @(posedge clk1)
begin
	if ( 1'b0 == rst1 )
		out1 = 1'b0;
	else
		out1 = in1 & in2;
end

always @(posedge clk2)
begin
	if ( 1'b0 == rst2 )
		out2 = 1'b0;
	else
		out2 = in1 | in2;
end

endmodule
