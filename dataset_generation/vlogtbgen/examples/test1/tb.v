//////////////////////////////////////////////////////////////
//                                                          //
// This testbench has been generated by the Verilog         //
// testbench generator                .                     //
// Copyright (c) 2012-2022 EDAUtils LLP                 //
// Contact help@edautils.com  for support/info.//
//                                                          //
//                                                          //
//////////////////////////////////////////////////////////////
//
//
// Generated by : Vincent on 18/01/24 13:58
//
//
module testbench;
	reg [0:1] indata_array;
	wire bench_a;
	wire bench_b;
	wire bench_c;



	assign bench_a = indata_array[0:0];
	assign bench_b = indata_array[1:1];

	always
	begin
		#5  indata_array = $random;
	end

	test inst(
        .a(bench_a), 
        .b(bench_b), 
        .c(bench_c)
    );

	initial
	begin
		$monitor($time, " a = %b , b = %b , c = %b  ",
			bench_a, bench_b, bench_c);
	end

	initial
	begin
		#500 $finish;
	end

endmodule