# Author: Ilja Novickij
# This file describes the rules for the dispatch functions. Will later be used 
# for transition functions

###############################################################################
# Imports

from pyknow import *
import array

###############################################################################
# Microgrid Parameters (Temporary)
BASE = 1e6
RDER_RATING = 220e3/BASE
ESS_RATING = 320e3/BASE
DIESEL_RATING = 400e3/BASE
MLC = 0.2*DIESEL_RATING


###NOTE###
# EVERYTHING enters rules under base power of 1MW

class GridConnectedDispatch(KnowledgeEngine):
    
    # Breaker Status (Default: closed)
    b_pcc = 1;
    b_load = 1;
    b_diesel = 1;
    b_ess = 1;
    
    # Setpoints
    p_ess = 0;
    p_diesel = 0;
    
    # Modes
    m_ess = 1;
    
    # Curtailment (Default: No curtailment)
    c_rder = 1;
    c_load = array.array('d', [1.0, 1.0]);
    
    @DefFacts()
    def _initial_action(self):
        yield Fact(r_ess=ESS_RATING)
        yield Fact(r_diesel=DIESEL_RATING*0.9)
        yield Fact(r_rder=RDER_RATING)
    
    
    @Rule(NOT(Fact(default=True)))
    def default_case(self):
        self.declare(Fact(default=True))
        self.p_diesel = MLC
        self.declare(Fact(p_diesel=self.p_diesel))
    
    
    @Rule(Fact(p_diesel="p_diesel" << W()),
          Fact(p_load="p_load" << W()),
          Fact(p_rder="p_rder" << W()),
          Fact(p_pcc_desired="p_pcc_desired" << W()),
          NOT(Fact(p_ess=W())),
          Fact(default=True))
    def power_balance(self, p_diesel, p_load, p_rder, p_pcc_desired):
        self.p_ess = p_load - p_diesel - p_rder - p_pcc_desired
        self.declare(Fact(p_ess=self.p_ess))
        
        
    @Rule('f_ess' << Fact(p_ess="p_ess" << W()),
          'f_diesel' << Fact(p_diesel="p_diesel" << W()),
          Fact(p_load="p_load" << W()),
          Fact(p_rder="p_rder" << W()),
          Fact(p_pcc_desired="p_pcc_desired" << W()),
          Fact(r_ess="r_ess" << W()),
          TEST(lambda p_ess, r_ess: p_ess > r_ess))
    def ess_power_rating(self, f_ess, f_diesel, p_ess, p_diesel,
                         p_load, p_rder, p_pcc_desired, r_ess):
        self.p_ess = r_ess
        self.modify(f_ess, p_ess=r_ess)
        self.p_diesel = p_load - r_ess - p_rder - p_pcc_desired
        self.modify(f_diesel, p_diesel=self.p_diesel)
      
    
    @Rule('f_diesel' << Fact(p_diesel="p_diesel" << W()),
          Fact(r_diesel="r_diesel" << W()),
          TEST(lambda p_diesel, r_diesel: p_diesel > r_diesel))
    def diesel_power_rating(self, f_diesel, p_diesel, r_diesel):
        self.p_diesel = r_diesel
        self.modify(f_diesel, p_diesel=r_diesel)
        self.declare(Fact(load_curtailment=True))
        
    
    @Rule('f_priority' << Fact(c_load_priority="c_load_priority" << W()),
          'f_load_c' << Fact(p_load_c="p_load_c" << W(), priority="priority" << W()),
          'f_load' << Fact(p_load="p_load" << W()),
          'flag' << Fact(load_curtailment=True),
          'f_ess' << Fact(p_ess=W()),
          'f_default' << Fact(default=True),
          TEST(lambda priority, c_load_priority : priority == c_load_priority),
          TEST(lambda c_load_priority : c_load_priority > 0)
          )
    def load_curtailment(self,f_default, f_ess, f_priority, f_load_c, f_load, c_load_priority,
                         p_load_c, p_load, flag, priority):
        print("Curtailing Load!")
        self.c_load[c_load_priority - 1] = 0;
        self.modify(f_priority, c_load_priority=c_load_priority-1)
        self.modify(f_load, p_load=p_load-p_load_c)
        self.modify(flag, load_curtailment=False)
        self.retract(f_ess)
        self.retract(f_default)
        