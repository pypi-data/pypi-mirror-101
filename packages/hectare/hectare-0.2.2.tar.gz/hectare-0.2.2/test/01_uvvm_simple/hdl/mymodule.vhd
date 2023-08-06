-- This file was automatically generated with HECTARE
--
-- DO NOT EDIT
--
--   input_filename = mymodule.rdl


library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

use work.mymodule_pkg.all;

entity mymodule is
  generic(
    G_ADDR_W: integer := 8
  );
  port (
    status_color_sel_rbv_i : in ColorsEnum_t;
    status_ready_o : out std_logic;
    status_ready_i : in std_logic;
    control_color_sel_o : out ColorsEnum_t;
    control_color_sel_swmod : out std_logic;
    control_enable_o : out std_logic;
    coef_a_a_o : out std_logic_vector(15 downto 0);
    coef_b_b_o : out std_logic_vector(15 downto 0);
    result_sum_o : out std_logic_vector(15 downto 0);
    result_sum_i : in std_logic_vector(15 downto 0);
    result_diff_o : out std_logic_vector(15 downto 0);
    result_diff_i : in std_logic_vector(15 downto 0);

    clk           : in std_logic;
    reset         : in std_logic;
    S_AXI_AWADDR  : in std_logic_vector(G_ADDR_W-1 downto 0);
    S_AXI_AWPROT  : in std_logic_vector(2 downto 0);
    S_AXI_AWVALID : in std_logic;
    S_AXI_AWREADY : out std_logic;
    S_AXI_WDATA   : in std_logic_vector(32-1 downto 0);
    S_AXI_WSTRB   : in std_logic_vector(32/8-1 downto 0);
    S_AXI_WVALID  : in std_logic;
    S_AXI_WREADY  : out std_logic;
    S_AXI_BRESP   : out std_logic_vector(1 downto 0);
    S_AXI_BVALID  : out std_logic;
    S_AXI_BREADY  : in std_logic;
    S_AXI_ARADDR  : in std_logic_vector(G_ADDR_W-1 downto 0);
    S_AXI_ARPROT  : in std_logic_vector(2 downto 0);
    S_AXI_ARVALID : in std_logic;
    S_AXI_ARREADY : out std_logic;
    S_AXI_RDATA   : out std_logic_vector(32-1 downto 0);
    S_AXI_RRESP   : out std_logic_vector(1 downto 0);
    S_AXI_RVALID  : out std_logic;
    S_AXI_RREADY  : in std_logic

);
end entity;

architecture arch of mymodule is


  -- address constants
  constant C_ADDR_STATUS : integer := 0;
  constant C_ADDR_CONTROL : integer := 1;
  constant C_ADDR_IDENT : integer := 2;
  constant C_ADDR_COEF_A : integer := 4;
  constant C_ADDR_COEF_B : integer := 5;
  constant C_ADDR_RESULT : integer := 6;

  -- field ranges constants
  constant C_FIELD_STATUS_COLOR_SEL_RBV_MSB : integer := 27;
  constant C_FIELD_STATUS_COLOR_SEL_RBV_LSB : integer := 24;
  constant C_FIELD_STATUS_READY_MSB : integer := 31;
  constant C_FIELD_STATUS_READY_LSB : integer := 31;
  constant C_FIELD_CONTROL_COLOR_SEL_MSB : integer := 27;
  constant C_FIELD_CONTROL_COLOR_SEL_LSB : integer := 24;
  constant C_FIELD_CONTROL_ENABLE_MSB : integer := 31;
  constant C_FIELD_CONTROL_ENABLE_LSB : integer := 31;
  constant C_FIELD_IDENT_IDENT_MSB : integer := 31;
  constant C_FIELD_IDENT_IDENT_LSB : integer := 0;
  constant C_FIELD_COEF_A_A_MSB : integer := 15;
  constant C_FIELD_COEF_A_A_LSB : integer := 0;
  constant C_FIELD_COEF_B_B_MSB : integer := 15;
  constant C_FIELD_COEF_B_B_LSB : integer := 0;
  constant C_FIELD_RESULT_SUM_MSB : integer := 15;
  constant C_FIELD_RESULT_SUM_LSB : integer := 0;
  constant C_FIELD_RESULT_DIFF_MSB : integer := 31;
  constant C_FIELD_RESULT_DIFF_LSB : integer := 16;

  -- registers
  signal reg_status : std_logic_vector(32-1 downto 0);
  signal reg_control : std_logic_vector(32-1 downto 0);
  signal reg_ident : std_logic_vector(32-1 downto 0);
  signal reg_coef_a : std_logic_vector(32-1 downto 0);
  signal reg_coef_b : std_logic_vector(32-1 downto 0);
  signal reg_result : std_logic_vector(32-1 downto 0);
  signal reg_control_swmod : std_logic;


  -- read
  type t_state_read is (sReadIdle, sReadValid);
  signal state_read : t_state_read;
  
  signal rdata_reg : std_logic_vector(31 downto 0);
  signal raddr_word : integer;
  
  signal arready_wire : std_logic;
  signal rvalid_wire : std_logic;
  
  -- write
  type t_state_write is (sWriteIdle, sWriteWaitData, sWriteWaitAddr, sWriteResp);
  signal state_write : t_state_write;
  signal state_write_prev : t_state_write;
  
  signal waddr_reg : std_logic_vector(G_ADDR_W-1 downto 0);
  signal wdata_reg : std_logic_vector(31 downto 0);
  
  signal waddr_word : integer;
  
  signal awready_wire : std_logic;
  signal wready_wire : std_logic;
  signal bvalid_wire : std_logic;


begin

  reg_status(27 downto 24) <= std_logic_vector(to_unsigned(ColorsEnum_t'pos(status_color_sel_rbv_i), 4)) when rising_edge(clk);
  status_ready_o <= reg_status(31);
  reg_status(31) <= status_ready_i when rising_edge(clk);
  control_color_sel_o <= ColorsEnum_t'val(to_integer(unsigned(reg_control(27 downto 24))));
  control_color_sel_swmod <= reg_control_swmod;
  control_enable_o <= reg_control(31);
  coef_a_a_o <= reg_coef_a(15 downto 0);
  coef_b_b_o <= reg_coef_b(15 downto 0);
  result_sum_o <= reg_result(15 downto 0);
  reg_result(15 downto 0) <= result_sum_i when rising_edge(clk);
  result_diff_o <= reg_result(31 downto 16);
  reg_result(31 downto 16) <= result_diff_i when rising_edge(clk);



  proc_state_read: process (clk)
  begin
    if rising_edge(clk) then
      if reset = '1' then
        state_read <= sReadIdle;
      else
        case state_read is
          when sReadIdle =>
            if S_AXI_ARVALID = '1' then
              state_read <= sReadValid;
            end if;
          when sReadValid =>
            if S_AXI_RREADY = '1' then
              state_read <= sReadIdle;
            end if;
        end case;
      end if;
    end if;
  end process;

  raddr_word <= to_integer(unsigned(S_AXI_ARADDR(G_ADDR_W-1 downto 2)));


  -- ### read logic

  proc_rdata_reg: process (clk)
  begin
    if rising_edge(clk) then
      rdata_reg <= (others => '0');
      case raddr_word is
        when C_ADDR_STATUS =>
          rdata_reg(27 downto 24) <= reg_status(27 downto 24);
          rdata_reg(31 downto 31) <= reg_status(31 downto 31);
        when C_ADDR_CONTROL =>
          rdata_reg(27 downto 24) <= reg_control(27 downto 24);
          rdata_reg(31 downto 31) <= reg_control(31 downto 31);
        when C_ADDR_IDENT =>
          rdata_reg(31 downto 0) <= reg_ident(31 downto 0);
        when C_ADDR_COEF_A =>
          rdata_reg(15 downto 0) <= reg_coef_a(15 downto 0);
        when C_ADDR_COEF_B =>
          rdata_reg(15 downto 0) <= reg_coef_b(15 downto 0);
        when C_ADDR_RESULT =>
          rdata_reg(15 downto 0) <= reg_result(15 downto 0);
          rdata_reg(31 downto 16) <= reg_result(31 downto 16);
        when others  =>
          null;
      end case;
    end if;
  end process;

  proc_read_output: process (state_read)
  begin
    case state_read is
      when sReadIdle =>
        arready_wire <= '1';
        rvalid_wire <= '0';
      when sReadValid =>
        arready_wire <= '0';
        rvalid_wire <= '1';
      when others =>
        arready_wire <= '0';
        rvalid_wire <= '0';
    end case;
  end process;

  S_AXI_ARREADY <= arready_wire;
  S_AXI_RVALID <= rvalid_wire;
  S_AXI_RDATA <= rdata_reg;
  S_AXI_RRESP <= "00";

  proc_state_write_prev: process (clk) begin
    if rising_edge(clk) then
      state_write_prev <= state_write;
    end if;
  end process;

  proc_state_write: process (clk) begin
    if rising_edge (clk) then
      if reset = '1' then
        state_write <= sWriteIdle;
      else
        case state_write is
          when sWriteIdle =>
            if S_AXI_AWVALID = '1' and S_AXI_WVALID = '1' then
              state_write <= sWriteResp;
              waddr_reg <= S_AXI_AWADDR;
              wdata_reg <= S_AXI_WDATA;
            elsif S_AXI_AWVALID = '1' and S_AXI_WVALID = '0' then
              state_write <= sWriteWaitData;
              waddr_reg <= S_AXI_AWADDR;
            elsif S_AXI_AWVALID = '0' and S_AXI_WVALID = '1' then
              state_write <= sWriteWaitAddr;
              wdata_reg <= S_AXI_WDATA;
            end if;
          when sWriteWaitData =>
            if S_AXI_WVALID = '1' then
              state_write <= sWriteResp;
              wdata_reg <= S_AXI_WDATA;
            end if;
          when sWriteWaitAddr =>
            if S_AXI_AWVALID = '1' then
              state_write <= sWriteResp;
              waddr_reg <= S_AXI_AWADDR;
            end if;
          when sWriteResp =>
            if S_AXI_BREADY = '1' then
              state_write <= sWriteIdle;
            end if;
        end case;
      end if;
    end if;
  end process;

  waddr_word <= to_integer(unsigned(waddr_reg(G_ADDR_W-1 downto 2)));
  -- ### write logic (use waddr_word and wdata_reg)

proc_write: process (clk) begin
  if rising_edge(clk) then
    if reset = '1' then
      reg_control(31 downto 31) <= "0";
      reg_ident(31 downto 0) <= "10100001101100101100001111010100";
    else

      -- default (pulse)
      -- TODO

      -- default (swmod)
      reg_control_swmod <= '0';

      if state_write = sWriteResp and state_write_prev /= sWriteResp then
        case waddr_word is
          when C_ADDR_STATUS =>
            null;
          when C_ADDR_CONTROL =>
            reg_control(27 downto 24) <= wdata_reg(27 downto 24);
            reg_control_swmod <= '1';
            reg_control(31 downto 31) <= wdata_reg(31 downto 31);
            reg_control_swmod <= '1';
          when C_ADDR_IDENT =>
            null;
          when C_ADDR_COEF_A =>
            reg_coef_a(15 downto 0) <= wdata_reg(15 downto 0);
          when C_ADDR_COEF_B =>
            reg_coef_b(15 downto 0) <= wdata_reg(15 downto 0);
          when C_ADDR_RESULT =>
            null;
          when others  =>
            null;
        end case;
      end if;
    end if;
  end if;
end process;

  proc_write_output: process (state_write) begin
    case state_write is
      when sWriteIdle =>
        awready_wire <= '1';
        wready_wire <= '1';
        bvalid_wire <= '0';
      when sWriteWaitData =>
        awready_wire <= '0';
        wready_wire <= '1';
        bvalid_wire <= '0';
      when sWriteWaitAddr =>
        awready_wire <= '1';
        wready_wire <= '0';
        bvalid_wire <= '0';
      when sWriteResp =>
        awready_wire <= '0';
        wready_wire <= '0';
        bvalid_wire <= '1';
      when others =>
        awready_wire <= '0';
        wready_wire <= '0';
        bvalid_wire <= '0';
    end case;
  end process;

  S_AXI_AWREADY <= awready_wire;
  S_AXI_WREADY <= wready_wire;
  S_AXI_BRESP <= "00";
  S_AXI_BVALID <= bvalid_wire;

end architecture;
