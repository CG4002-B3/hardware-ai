#include "core.h"

void dense_relu_1(const fixpt (&input)[INPUT_SIZE], fixpt &output, const ap_uint<8> index) {
	fixpt result = l1_bias[index];
	for (ap_uint<8> i = 0; i < INPUT_SIZE; i++) {
#pragma HLS PIPELINE
#pragma HLS UNROLL factor=2
		result += (input[i] * l1_weights[index][i]);
	}

	if (result > 0) {
		output = result;
	} else {
		output = 0;
	}
}

void dense_2(const fixpt (&input)[HIDDEN_SIZE], fixpt &output, const ap_uint<8> index) {
	fixpt result = l2_bias[index];
	for (ap_uint<8> i = 0; i < HIDDEN_SIZE; i++) {
#pragma HLS PIPELINE
#pragma HLS UNROLL factor=2
		result += (input[i] * l2_weights[index][i]);
	}
	output = result;
}

void inference_ap_fixed(stream_io& s_axis, stream_io& m_axis) {
#pragma HLS INTERFACE ap_ctrl_none port=return
#pragma HLS INTERFACE axis port=s_axis
#pragma HLS INTERFACE axis port=m_axis

	fixpt input[INPUT_SIZE];
	fixpt out_1[HIDDEN_SIZE];
	fixpt percept[NUM_CLASSES] = {0,0,0,0};

	AXIS_IO in;
	AXIS_IO out;

	load_input:for (ap_uint<8> i = 0; i < INPUT_SIZE; i++) {
#pragma HLS PIPELINE
#pragma HLS UNROLL factor=2
		in = s_axis.read();
		input[i] = in.data;
	}

	mul_1:for (ap_uint<8> i = 0; i < HIDDEN_SIZE; i++) {
		dense_relu_1(input, out_1[i], i);
	}

	mul_2:for (ap_uint<8> i = 0; i < NUM_CLASSES; i++) {
		dense_2(out_1, percept[i], i);
	}

	ap_uint<8> action = 0;
	fixpt max_val = percept[0];
	for (ap_uint<8> i = 0; i < NUM_CLASSES; i++) {
		if (percept[i] > max_val) {
			max_val = percept[i];
			action = i;
		}
	}

	out.last = 1;
	out.data = action;
	m_axis.write(out);

//	for (ap_uint<8> i = 0; i < NUM_CLASSES; i++) {
//		out.data = percept[i];
//		out.last = (i == NUM_CLASSES - 1) ? 1 : 0;
//		m_axis.write(out);
//	}
}
