#!/bin/csh -f


gentbvlog -in reset_waveforms.v -top reset_waveforms -out tb.v -clk "clk1@8{in1:in2}" -clk clk2 -rst rst1 -rst "rst2{1@5:0@50:1@150}" 

