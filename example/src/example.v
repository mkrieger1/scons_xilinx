module example
(
    input CLK_200MHZ_P,
    input CLK_200MHZ_N,
    input RES_N,
    input PB1,
    input PB2,
    output LED_GREEN_RIGHT,
    output LED_GREEN_LEFT,
    output LED_RED_RIGHT
);

// input clock
wire clk;
(* DIFF_TERM = "TRUE" *)
IBUFGDS ibuf (
  .I(CLK_200MHZ_P), 
  .IB(CLK_200MHZ_N), 
  .O(clk)
);

// clock divider
wire clk_slow;
reg [23:0] count;
always @(posedge clk) begin
    count <= count + 24'd1;
end
assign clk_slow = count[23];

// FIFO from coregen
wire [3:0] Q;
fifo fifo_inst (
  .clk(clk),
  .rst(~RES_N),
  .din({Q[2:0], PB1}),
  .wr_en(PB2),
  .rd_en(PB2),
  .dout(Q),
  .full(),
  .empty()
);

// LED blink
assign LED_RED_RIGHT = clk_slow;
assign LED_GREEN_RIGHT = Q[2];
assign LED_GREEN_LEFT = Q[3];

endmodule

