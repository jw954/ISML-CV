`timescale 1ns / 1ps
`default_nettype none

module BTPipe(
	input  wire [4:0]   okUH,
	output wire [2:0]   okHU,
	inout wire  [31:0]  okUHU,
	inout  wire         okAA,

	output wire [7:0]   led
	);


// Interface bus
wire         okClk;
wire [112:0] okHE;
wire [64:0]  okEH;
wire [31:0]	 ep00wire;
wire [31:0]  ep01wire;

// FIFO connections
wire [31:0]  din, dout; // pipes
wire         full, empty; // connect to pipes as triggers
wire		 wr_en, rd_en;
wire         rst;
wire         almost_full, almost_empty;


assign rst = ep00wire[0];

// FIFO
fifo_generator_0 fifo_inst (
  .clk(okClk),                    // input wire clk
  .srst(rst),                  // input wire srst
  .din(din),                    // input wire [63 : 0] din
  .wr_en(wr_en),                // input wire wr_en
  .rd_en(rd_en),                // input wire rd_en
  .dout(dout),                  // output wire [63 : 0] dout
  .full(full),                  // output wire full
  .empty(empty),                // output wire empty
  
  .almost_full(almost_full),    // output wire almost_full
  .almost_empty(almost_empty)  // output wire almost_empty
);

// select
wire sel;
wire [31:0] inv_out;
assign sel = ep01wire[0];

assign inv_out = (sel)? ~dout: dout;



// Instantiate the okHost and connect endpoints.
wire [65*2-1:0]  okEHx;

okHost okHI(
	.okUH(okUH),
	.okHU(okHU),
	.okUHU(okUHU),
	.okAA(okAA),
	.okClk(okClk),
	.okHE(okHE), 
	.okEH(okEH)
);

okWireOR # (.N(2)) wireOR (okEH, okEHx);


okWireIn  	 wi00(.okHE(okHE),                             .ep_addr(8'h00), .ep_dataout(ep00wire));
okWireIn     wi01(.okHE(okHE),                             .ep_addr(8'h00), .ep_dataout(ep01wire));
okBTPipeIn   pi80(.okHE(okHE), .okEH(okEHx[ 0*65 +: 65 ]), .ep_addr(8'h80), .ep_dataout(din), .ep_write(wr_en), .ep_ready(~full), .ep_blockstrobe());
okBTPipeOut  poA0(.okHE(okHE), .okEH(okEHx[ 1*65 +: 65 ]), .ep_addr(8'hA0), .ep_datain(inv_out), .ep_read(rd_en), .ep_ready(~empty), .ep_blockstrobe());

endmodule