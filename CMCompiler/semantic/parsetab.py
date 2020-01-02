
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "INT VOID IF ELSE WHILE RETURN NUM ID GE LE EE NE ANNOTATIONprogram : declaration_listdeclaration_list : declaration_list declarationdeclaration_list : declarationdeclaration : var_declarationdeclaration : fun_declarationvar_declaration : type_specifier ID ';' var_declaration : type_specifier ID '[' NUM ']' ';' type_specifier : INTtype_specifier : VOIDfun_declaration : type_specifier ID '(' params ')' compound_stmtparams : param_listparams : VOIDparams : param_list : param_list ',' paramparam_list : paramparam : type_specifier IDparam : type_specifier ID '[' ']' compound_stmt : '{' local_declarations statement_list '}' local_declarations : local_declarations var_declarationlocal_declarations : statement_list : statement_list statementstatement_list : statement : expression_stmtstatement : compound_stmtstatement : selection_stmtstatement : iteration_stmtstatement : return_stmtexpression_stmt : expression ';' expression_stmt : ';' selection_stmt : IF '(' expression ')' M statement Nselection_stmt : IF '(' expression ')' M statement N ELSE M statement MM :N :iteration_stmt : WHILE M '(' expression ')' M statement Mreturn_stmt : RETURN ';' return_stmt : RETURN expression ';' expression : var '=' expressionexpression : simple_expression var : ID var : ID '[' expression ']' simple_expression : additive_expression relop additive_expressionsimple_expression : additive_expressionrelop : LErelop : '<' relop : '>' relop : GErelop : EErelop : NEadditive_expression : additive_expression addop termadditive_expression : termaddop : '+' addop : '-' term : term mulop factorterm : factor mulop : '*'  mulop : '/' factor : '(' expression ')' factor : varfactor : callfactor : NUM call : ID '(' args ')' args : arg_listargs :  arg_list : arg_list ',' expression arg_list : expression"
    
_lr_action_items = {'INT':([0,2,3,4,5,9,11,13,23,24,26,27,30,32,34,],[7,7,-3,-4,-5,-2,-6,7,7,-7,-10,-20,7,-19,-18,]),'VOID':([0,2,3,4,5,9,11,13,23,24,26,27,30,32,34,],[8,8,-3,-4,-5,-2,-6,18,8,-7,-10,-20,8,-19,-18,]),'$end':([1,2,3,4,5,9,11,24,26,34,],[0,-1,-3,-4,-5,-2,-6,-7,-10,-18,]),'ID':([6,7,8,11,15,18,24,27,30,31,32,33,34,35,36,37,38,39,40,42,44,46,56,57,60,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,80,81,91,95,96,97,99,100,101,102,103,104,105,106,107,],[10,-8,-9,-6,21,-9,-7,-20,-22,49,-19,55,-18,-21,-23,-24,-25,-26,-27,-29,49,49,-28,49,-35,49,49,49,49,49,-43,-44,-45,-46,-47,-48,-51,-52,49,-55,-56,49,-36,-32,49,49,-32,-33,49,-30,-32,-32,-34,49,-32,-31,]),';':([10,11,20,24,27,30,31,32,34,35,36,37,38,39,40,41,42,46,47,48,49,50,51,52,53,54,55,56,60,61,79,81,82,87,88,89,90,91,93,94,96,97,99,100,101,102,103,104,105,106,107,],[11,-6,24,-7,-20,-22,42,-19,-18,-21,-23,-24,-25,-26,-27,56,-29,60,-58,-38,-39,-42,-50,-54,-59,-60,11,-28,-35,81,-57,-36,-37,-41,-58,-49,-53,-32,-40,-61,42,-32,-33,42,-30,-32,-32,-34,42,-32,-31,]),'[':([10,21,49,55,],[12,25,63,12,]),'(':([10,11,24,27,30,31,32,34,35,36,37,38,39,40,42,43,44,45,46,49,56,57,59,60,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,80,81,91,95,96,97,99,100,101,102,103,104,105,106,107,],[13,-6,-7,-20,-22,44,-19,-18,-21,-23,-24,-25,-26,-27,-29,57,44,-32,44,64,-28,44,80,-35,44,44,44,44,44,-43,-44,-45,-46,-47,-48,-51,-52,44,-55,-56,44,-36,-32,44,44,-32,-33,44,-30,-32,-32,-34,44,-32,-31,]),'}':([11,24,27,30,31,32,34,35,36,37,38,39,40,42,56,60,81,99,101,102,104,106,107,],[-6,-7,-20,-22,34,-19,-18,-21,-23,-24,-25,-26,-27,-29,-28,-35,-36,-33,-30,-32,-34,-32,-31,]),'{':([11,22,24,27,30,31,32,34,35,36,37,38,39,40,42,56,60,81,91,96,97,99,100,101,102,103,104,105,106,107,],[-6,27,-7,-20,-22,27,-19,-18,-21,-23,-24,-25,-26,-27,-29,-28,-35,-36,-32,27,-32,-33,27,-30,-32,-32,-34,27,-32,-31,]),'IF':([11,24,27,30,31,32,34,35,36,37,38,39,40,42,56,60,81,91,96,97,99,100,101,102,103,104,105,106,107,],[-6,-7,-20,-22,43,-19,-18,-21,-23,-24,-25,-26,-27,-29,-28,-35,-36,-32,43,-32,-33,43,-30,-32,-32,-34,43,-32,-31,]),'WHILE':([11,24,27,30,31,32,34,35,36,37,38,39,40,42,56,60,81,91,96,97,99,100,101,102,103,104,105,106,107,],[-6,-7,-20,-22,45,-19,-18,-21,-23,-24,-25,-26,-27,-29,-28,-35,-36,-32,45,-32,-33,45,-30,-32,-32,-34,45,-32,-31,]),'RETURN':([11,24,27,30,31,32,34,35,36,37,38,39,40,42,56,60,81,91,96,97,99,100,101,102,103,104,105,106,107,],[-6,-7,-20,-22,46,-19,-18,-21,-23,-24,-25,-26,-27,-29,-28,-35,-36,-32,46,-32,-33,46,-30,-32,-32,-34,46,-32,-31,]),'NUM':([11,12,24,27,30,31,32,34,35,36,37,38,39,40,42,44,46,56,57,60,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,80,81,91,95,96,97,99,100,101,102,103,104,105,106,107,],[-6,14,-7,-20,-22,54,-19,-18,-21,-23,-24,-25,-26,-27,-29,54,54,-28,54,-35,54,54,54,54,54,-43,-44,-45,-46,-47,-48,-51,-52,54,-55,-56,54,-36,-32,54,54,-32,-33,54,-30,-32,-32,-34,54,-32,-31,]),')':([13,16,17,18,19,21,28,29,47,48,49,50,51,52,53,54,58,64,78,79,82,84,85,86,87,88,89,90,92,93,94,98,],[-13,22,-11,-12,-15,-16,-14,-17,-58,-38,-39,-42,-50,-54,-59,-60,79,-63,91,-57,-37,94,-62,-65,-41,-58,-49,-53,97,-40,-61,-64,]),']':([14,25,47,48,49,50,51,52,53,54,79,82,83,87,88,89,90,93,94,],[20,29,-58,-38,-39,-42,-50,-54,-59,-60,-57,-37,93,-41,-58,-49,-53,-40,-61,]),',':([17,19,21,28,29,47,48,49,50,51,52,53,54,79,82,85,86,87,88,89,90,93,94,98,],[23,-15,-16,-14,-17,-58,-38,-39,-42,-50,-54,-59,-60,-57,-37,95,-65,-41,-58,-49,-53,-40,-61,-64,]),'ELSE':([34,36,37,38,39,40,42,56,60,81,99,101,102,104,106,107,],[-18,-23,-24,-25,-26,-27,-29,-28,-35,-36,-33,103,-32,-34,-32,-31,]),'=':([47,49,93,],[62,-39,-40,]),'*':([47,49,51,52,53,54,79,88,89,90,93,94,],[-58,-39,76,-54,-59,-60,-57,-58,76,-53,-40,-61,]),'/':([47,49,51,52,53,54,79,88,89,90,93,94,],[-58,-39,77,-54,-59,-60,-57,-58,77,-53,-40,-61,]),'LE':([47,49,50,51,52,53,54,79,88,89,90,93,94,],[-58,-39,67,-50,-54,-59,-60,-57,-58,-49,-53,-40,-61,]),'<':([47,49,50,51,52,53,54,79,88,89,90,93,94,],[-58,-39,68,-50,-54,-59,-60,-57,-58,-49,-53,-40,-61,]),'>':([47,49,50,51,52,53,54,79,88,89,90,93,94,],[-58,-39,69,-50,-54,-59,-60,-57,-58,-49,-53,-40,-61,]),'GE':([47,49,50,51,52,53,54,79,88,89,90,93,94,],[-58,-39,70,-50,-54,-59,-60,-57,-58,-49,-53,-40,-61,]),'EE':([47,49,50,51,52,53,54,79,88,89,90,93,94,],[-58,-39,71,-50,-54,-59,-60,-57,-58,-49,-53,-40,-61,]),'NE':([47,49,50,51,52,53,54,79,88,89,90,93,94,],[-58,-39,72,-50,-54,-59,-60,-57,-58,-49,-53,-40,-61,]),'+':([47,49,50,51,52,53,54,79,87,88,89,90,93,94,],[-58,-39,73,-50,-54,-59,-60,-57,73,-58,-49,-53,-40,-61,]),'-':([47,49,50,51,52,53,54,79,87,88,89,90,93,94,],[-58,-39,74,-50,-54,-59,-60,-57,74,-58,-49,-53,-40,-61,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'declaration_list':([0,],[2,]),'declaration':([0,2,],[3,9,]),'var_declaration':([0,2,30,],[4,4,32,]),'fun_declaration':([0,2,],[5,5,]),'type_specifier':([0,2,13,23,30,],[6,6,15,15,33,]),'params':([13,],[16,]),'param_list':([13,],[17,]),'param':([13,23,],[19,28,]),'compound_stmt':([22,31,96,100,105,],[26,37,37,37,37,]),'local_declarations':([27,],[30,]),'statement_list':([30,],[31,]),'statement':([31,96,100,105,],[35,99,102,106,]),'expression_stmt':([31,96,100,105,],[36,36,36,36,]),'selection_stmt':([31,96,100,105,],[38,38,38,38,]),'iteration_stmt':([31,96,100,105,],[39,39,39,39,]),'return_stmt':([31,96,100,105,],[40,40,40,40,]),'expression':([31,44,46,57,62,63,64,80,95,96,100,105,],[41,58,61,78,82,83,86,92,98,41,41,41,]),'var':([31,44,46,57,62,63,64,65,66,75,80,95,96,100,105,],[47,47,47,47,47,47,47,88,88,88,47,47,47,47,47,]),'simple_expression':([31,44,46,57,62,63,64,80,95,96,100,105,],[48,48,48,48,48,48,48,48,48,48,48,48,]),'additive_expression':([31,44,46,57,62,63,64,65,80,95,96,100,105,],[50,50,50,50,50,50,50,87,50,50,50,50,50,]),'term':([31,44,46,57,62,63,64,65,66,80,95,96,100,105,],[51,51,51,51,51,51,51,51,89,51,51,51,51,51,]),'factor':([31,44,46,57,62,63,64,65,66,75,80,95,96,100,105,],[52,52,52,52,52,52,52,52,52,90,52,52,52,52,52,]),'call':([31,44,46,57,62,63,64,65,66,75,80,95,96,100,105,],[53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,]),'M':([45,91,97,102,103,106,],[59,96,100,104,105,107,]),'relop':([50,],[65,]),'addop':([50,87,],[66,66,]),'mulop':([51,89,],[75,75,]),'args':([64,],[84,]),'arg_list':([64,],[85,]),'N':([99,],[101,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> declaration_list','program',1,'p_program_1','sematic.py',113),
  ('declaration_list -> declaration_list declaration','declaration_list',2,'p_declaration_list_1','sematic.py',117),
  ('declaration_list -> declaration','declaration_list',1,'p_declaration_list_2','sematic.py',119),
  ('declaration -> var_declaration','declaration',1,'p_declaration_1','sematic.py',123),
  ('declaration -> fun_declaration','declaration',1,'p_declaration_2','sematic.py',125),
  ('var_declaration -> type_specifier ID ;','var_declaration',3,'p_var_declaration_1','sematic.py',129),
  ('var_declaration -> type_specifier ID [ NUM ] ;','var_declaration',6,'p_var_declaration_2','sematic.py',133),
  ('type_specifier -> INT','type_specifier',1,'p_type_specifier_1','sematic.py',137),
  ('type_specifier -> VOID','type_specifier',1,'p_type_specifier_2','sematic.py',140),
  ('fun_declaration -> type_specifier ID ( params ) compound_stmt','fun_declaration',6,'p_fun_declaration_1','sematic.py',145),
  ('params -> param_list','params',1,'p_params_1','sematic.py',151),
  ('params -> VOID','params',1,'p_params_2','sematic.py',154),
  ('params -> <empty>','params',0,'p_params_empty','sematic.py',157),
  ('param_list -> param_list , param','param_list',3,'p_param_list_1','sematic.py',160),
  ('param_list -> param','param_list',1,'p_param_list_2','sematic.py',162),
  ('param -> type_specifier ID','param',2,'p_param_1','sematic.py',166),
  ('param -> type_specifier ID [ ]','param',4,'p_param_2','sematic.py',169),
  ('compound_stmt -> { local_declarations statement_list }','compound_stmt',4,'p_compound_stmt_1','sematic.py',174),
  ('local_declarations -> local_declarations var_declaration','local_declarations',2,'p_local_declarations_1','sematic.py',178),
  ('local_declarations -> <empty>','local_declarations',0,'p_local_declarations_empty','sematic.py',180),
  ('statement_list -> statement_list statement','statement_list',2,'p_statement_list_1','sematic.py',183),
  ('statement_list -> <empty>','statement_list',0,'p_statement_list_empty','sematic.py',187),
  ('statement -> expression_stmt','statement',1,'p_statement_1','sematic.py',191),
  ('statement -> compound_stmt','statement',1,'p_statement_2','sematic.py',195),
  ('statement -> selection_stmt','statement',1,'p_statement_3','sematic.py',199),
  ('statement -> iteration_stmt','statement',1,'p_statement_4','sematic.py',203),
  ('statement -> return_stmt','statement',1,'p_statement_5','sematic.py',207),
  ('expression_stmt -> expression ;','expression_stmt',2,'p_expression_stmt_1','sematic.py',218),
  ('expression_stmt -> ;','expression_stmt',1,'p_expression_stmt_2','sematic.py',222),
  ('selection_stmt -> IF ( expression ) M statement N','selection_stmt',7,'p_selection_stmt_1','sematic.py',226),
  ('selection_stmt -> IF ( expression ) M statement N ELSE M statement M','selection_stmt',11,'p_selection_stmt_2','sematic.py',236),
  ('M -> <empty>','M',0,'p_M','sematic.py',245),
  ('N -> <empty>','N',0,'p_N','sematic.py',249),
  ('iteration_stmt -> WHILE M ( expression ) M statement M','iteration_stmt',8,'p_iteration_stmt_1','sematic.py',255),
  ('return_stmt -> RETURN ;','return_stmt',2,'p_return_stmt_1','sematic.py',267),
  ('return_stmt -> RETURN expression ;','return_stmt',3,'p_return_stmt_2','sematic.py',270),
  ('expression -> var = expression','expression',3,'p_expression_1','sematic.py',275),
  ('expression -> simple_expression','expression',1,'p_expression_2','sematic.py',281),
  ('var -> ID','var',1,'p_var_1','sematic.py',287),
  ('var -> ID [ expression ]','var',4,'p_var_2','sematic.py',294),
  ('simple_expression -> additive_expression relop additive_expression','simple_expression',3,'p_simple_expression_1','sematic.py',306),
  ('simple_expression -> additive_expression','simple_expression',1,'p_simple_expression_2','sematic.py',315),
  ('relop -> LE','relop',1,'p_relop_1','sematic.py',323),
  ('relop -> <','relop',1,'p_relop_2','sematic.py',326),
  ('relop -> >','relop',1,'p_relop_3','sematic.py',329),
  ('relop -> GE','relop',1,'p_relop_4','sematic.py',332),
  ('relop -> EE','relop',1,'p_relop_5','sematic.py',335),
  ('relop -> NE','relop',1,'p_relop_6','sematic.py',338),
  ('additive_expression -> additive_expression addop term','additive_expression',3,'p_additive_expression_1','sematic.py',343),
  ('additive_expression -> term','additive_expression',1,'p_additive_expression_2','sematic.py',348),
  ('addop -> +','addop',1,'p_addop_1','sematic.py',353),
  ('addop -> -','addop',1,'p_addop_2','sematic.py',357),
  ('term -> term mulop factor','term',3,'p_term_1','sematic.py',363),
  ('term -> factor','term',1,'p_term_2','sematic.py',369),
  ('mulop -> *','mulop',1,'p_mulop_1','sematic.py',374),
  ('mulop -> /','mulop',1,'p_mulop_2','sematic.py',378),
  ('factor -> ( expression )','factor',3,'p_factor_1','sematic.py',384),
  ('factor -> var','factor',1,'p_factor_2','sematic.py',389),
  ('factor -> call','factor',1,'p_factor_3','sematic.py',394),
  ('factor -> NUM','factor',1,'p_factor_4','sematic.py',398),
  ('call -> ID ( args )','call',4,'p_call_1','sematic.py',405),
  ('args -> arg_list','args',1,'p_args_1','sematic.py',414),
  ('args -> <empty>','args',0,'p_args_empty','sematic.py',417),
  ('arg_list -> arg_list , expression','arg_list',3,'p_arg_list_1','sematic.py',420),
  ('arg_list -> expression','arg_list',1,'p_arg_list_2','sematic.py',428),
]