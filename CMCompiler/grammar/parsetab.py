
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "ANNOTATION EE ELSE GE ID IF INT LE NE NUM RETURN VOID WHILEprogram : declaration_listdeclaration_list : declaration_list declarationdeclaration_list : declarationdeclaration : var_declarationdeclaration : fun_declarationvar_declaration : type_specifier ID ';' var_declaration : type_specifier ID '[' NUM ']' ';' type_specifier : INTtype_specifier : VOIDfun_declaration : type_specifier ID '(' params ')' fun_declaration : compound_stmtparams : param_listparams : VOIDparams : param_list : param_list ',' paramparam_list : paramparam : type_specifier IDparam : type_specifier ID '[' ']' compound_stmt : '{' local_declarations statement_list '}' local_declarations : local_declarations var_declarationlocal_declarations : statement_list : statement_list statementstatement_list : statement : expression_stmtstatement : compound_stmtstatement : selection_stmtstatement : iteration_stmtstatement : return_stmtexpression_stmt : expression ';' expression_stmt : ';' selection_stmt : IF '(' expression ')' statementselection_stmt : IF '(' expression ')' statement ELSE statementiteration_stmt : WHILE '(' expression ')' statementreturn_stmt : RETURN ';' return_stmt : RETURN expression ';' expression : var '=' expressionexpression : simple_expression var : ID var : ID '[' expression ']' simple_expression : additive_expression relop additive_expressionsimple_expression : additive_expressionrelop : LErelop : '<' relop : '>' relop : GErelop : EErelop : NEadditive_expression : additive_expression addop termadditive_expression : termaddop : '+' addop : '-' term : term mulop factorterm : factor mulop : '*'  mulop : '/' factor : '(' expression ')' factor : varfactor : callfactor : NUM call : ID '(' args ')' args : arg_listargs :  arg_list : arg_list ',' expression arg_list : expression"
    
_lr_action_items = {'INT':([0,2,3,4,5,7,10,11,13,14,16,18,26,50,51,74,],[8,8,-3,-4,-5,-11,-21,-2,8,-6,8,-20,-19,-10,8,-7,]),'VOID':([0,2,3,4,5,7,10,11,13,14,16,18,26,50,51,74,],[9,9,-3,-4,-5,-11,-21,-2,9,-6,24,-20,-19,-10,9,-7,]),'{':([0,2,3,4,5,7,10,11,13,14,17,18,26,27,28,29,30,31,32,34,50,52,56,74,80,91,92,96,97,99,100,],[10,10,-3,-4,-5,-11,-21,-2,-23,-6,10,-20,-19,-22,-24,-25,-26,-27,-28,-30,-10,-29,-34,-7,-35,10,10,-31,-33,10,-32,]),'$end':([1,2,3,4,5,7,11,14,26,50,74,],[0,-1,-3,-4,-5,-11,-2,-6,-19,-10,-7,]),'ID':([6,8,9,10,13,14,17,18,19,21,24,26,27,28,29,30,31,32,34,36,38,52,53,55,56,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,80,91,92,95,96,97,99,100,],[12,-8,-9,-21,-23,-6,41,-20,47,49,-9,-19,-22,-24,-25,-26,-27,-28,-30,41,41,-29,41,41,-34,41,41,41,41,41,-42,-43,-44,-45,-46,-47,-50,-51,41,-54,-55,-7,-35,41,41,41,-31,-33,41,-32,]),'}':([10,13,14,17,18,26,27,28,29,30,31,32,34,52,56,74,80,96,97,100,],[-21,-23,-6,26,-20,-19,-22,-24,-25,-26,-27,-28,-30,-29,-34,-7,-35,-31,-33,-32,]),';':([10,12,13,14,17,18,26,27,28,29,30,31,32,33,34,38,39,40,41,42,43,44,45,46,47,48,52,56,57,74,78,80,81,86,87,88,89,91,92,93,94,96,97,99,100,],[-21,14,-23,-6,34,-20,-19,-22,-24,-25,-26,-27,-28,52,-30,56,-57,-37,-38,-41,-49,-53,-58,-59,14,74,-29,-34,80,-7,-56,-35,-36,-40,-57,-48,-52,34,34,-39,-60,-31,-33,34,-32,]),'IF':([10,13,14,17,18,26,27,28,29,30,31,32,34,52,56,74,80,91,92,96,97,99,100,],[-21,-23,-6,35,-20,-19,-22,-24,-25,-26,-27,-28,-30,-29,-34,-7,-35,35,35,-31,-33,35,-32,]),'WHILE':([10,13,14,17,18,26,27,28,29,30,31,32,34,52,56,74,80,91,92,96,97,99,100,],[-21,-23,-6,37,-20,-19,-22,-24,-25,-26,-27,-28,-30,-29,-34,-7,-35,37,37,-31,-33,37,-32,]),'RETURN':([10,13,14,17,18,26,27,28,29,30,31,32,34,52,56,74,80,91,92,96,97,99,100,],[-21,-23,-6,38,-20,-19,-22,-24,-25,-26,-27,-28,-30,-29,-34,-7,-35,38,38,-31,-33,38,-32,]),'(':([10,12,13,14,17,18,26,27,28,29,30,31,32,34,35,36,37,38,41,52,53,55,56,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,80,91,92,95,96,97,99,100,],[-21,16,-23,-6,36,-20,-19,-22,-24,-25,-26,-27,-28,-30,53,36,55,36,60,-29,36,36,-34,36,36,36,36,36,-42,-43,-44,-45,-46,-47,-50,-51,36,-54,-55,-7,-35,36,36,36,-31,-33,36,-32,]),'NUM':([10,13,14,15,17,18,26,27,28,29,30,31,32,34,36,38,52,53,55,56,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,80,91,92,95,96,97,99,100,],[-21,-23,-6,20,46,-20,-19,-22,-24,-25,-26,-27,-28,-30,46,46,-29,46,46,-34,46,46,46,46,46,-42,-43,-44,-45,-46,-47,-50,-51,46,-54,-55,-7,-35,46,46,46,-31,-33,46,-32,]),'[':([12,41,47,49,],[15,59,15,75,]),')':([16,22,23,24,25,39,40,41,42,43,44,45,46,49,54,60,76,77,78,79,81,83,84,85,86,87,88,89,90,93,94,98,],[-14,50,-12,-13,-16,-57,-37,-38,-41,-49,-53,-58,-59,-17,78,-62,-15,91,-56,92,-36,94,-61,-64,-40,-57,-48,-52,-18,-39,-60,-63,]),']':([20,39,40,41,42,43,44,45,46,75,78,81,82,86,87,88,89,93,94,],[48,-57,-37,-38,-41,-49,-53,-58,-59,90,-56,-36,93,-40,-57,-48,-52,-39,-60,]),',':([23,25,39,40,41,42,43,44,45,46,49,76,78,81,84,85,86,87,88,89,90,93,94,98,],[51,-16,-57,-37,-38,-41,-49,-53,-58,-59,-17,-15,-56,-36,95,-64,-40,-57,-48,-52,-18,-39,-60,-63,]),'ELSE':([26,28,29,30,31,32,34,52,56,80,96,97,100,],[-19,-24,-25,-26,-27,-28,-30,-29,-34,-35,99,-33,-32,]),'=':([39,41,93,],[58,-38,-39,]),'*':([39,41,43,44,45,46,78,87,88,89,93,94,],[-57,-38,72,-53,-58,-59,-56,-57,72,-52,-39,-60,]),'/':([39,41,43,44,45,46,78,87,88,89,93,94,],[-57,-38,73,-53,-58,-59,-56,-57,73,-52,-39,-60,]),'LE':([39,41,42,43,44,45,46,78,87,88,89,93,94,],[-57,-38,63,-49,-53,-58,-59,-56,-57,-48,-52,-39,-60,]),'<':([39,41,42,43,44,45,46,78,87,88,89,93,94,],[-57,-38,64,-49,-53,-58,-59,-56,-57,-48,-52,-39,-60,]),'>':([39,41,42,43,44,45,46,78,87,88,89,93,94,],[-57,-38,65,-49,-53,-58,-59,-56,-57,-48,-52,-39,-60,]),'GE':([39,41,42,43,44,45,46,78,87,88,89,93,94,],[-57,-38,66,-49,-53,-58,-59,-56,-57,-48,-52,-39,-60,]),'EE':([39,41,42,43,44,45,46,78,87,88,89,93,94,],[-57,-38,67,-49,-53,-58,-59,-56,-57,-48,-52,-39,-60,]),'NE':([39,41,42,43,44,45,46,78,87,88,89,93,94,],[-57,-38,68,-49,-53,-58,-59,-56,-57,-48,-52,-39,-60,]),'+':([39,41,42,43,44,45,46,78,86,87,88,89,93,94,],[-57,-38,69,-49,-53,-58,-59,-56,69,-57,-48,-52,-39,-60,]),'-':([39,41,42,43,44,45,46,78,86,87,88,89,93,94,],[-57,-38,70,-49,-53,-58,-59,-56,70,-57,-48,-52,-39,-60,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'declaration_list':([0,],[2,]),'declaration':([0,2,],[3,11,]),'var_declaration':([0,2,13,],[4,4,18,]),'fun_declaration':([0,2,],[5,5,]),'type_specifier':([0,2,13,16,51,],[6,6,19,21,21,]),'compound_stmt':([0,2,17,91,92,99,],[7,7,29,29,29,29,]),'local_declarations':([10,],[13,]),'statement_list':([13,],[17,]),'params':([16,],[22,]),'param_list':([16,],[23,]),'param':([16,51,],[25,76,]),'statement':([17,91,92,99,],[27,96,97,100,]),'expression_stmt':([17,91,92,99,],[28,28,28,28,]),'selection_stmt':([17,91,92,99,],[30,30,30,30,]),'iteration_stmt':([17,91,92,99,],[31,31,31,31,]),'return_stmt':([17,91,92,99,],[32,32,32,32,]),'expression':([17,36,38,53,55,58,59,60,91,92,95,99,],[33,54,57,77,79,81,82,85,33,33,98,33,]),'var':([17,36,38,53,55,58,59,60,61,62,71,91,92,95,99,],[39,39,39,39,39,39,39,39,87,87,87,39,39,39,39,]),'simple_expression':([17,36,38,53,55,58,59,60,91,92,95,99,],[40,40,40,40,40,40,40,40,40,40,40,40,]),'additive_expression':([17,36,38,53,55,58,59,60,61,91,92,95,99,],[42,42,42,42,42,42,42,42,86,42,42,42,42,]),'term':([17,36,38,53,55,58,59,60,61,62,91,92,95,99,],[43,43,43,43,43,43,43,43,43,88,43,43,43,43,]),'factor':([17,36,38,53,55,58,59,60,61,62,71,91,92,95,99,],[44,44,44,44,44,44,44,44,44,44,89,44,44,44,44,]),'call':([17,36,38,53,55,58,59,60,61,62,71,91,92,95,99,],[45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,]),'relop':([42,],[61,]),'addop':([42,86,],[62,62,]),'mulop':([43,88,],[71,71,]),'args':([60,],[83,]),'arg_list':([60,],[84,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> declaration_list','program',1,'p_program_1','c_grammar_uiapi.py',103),
  ('declaration_list -> declaration_list declaration','declaration_list',2,'p_declaration_list_1','c_grammar_uiapi.py',106),
  ('declaration_list -> declaration','declaration_list',1,'p_declaration_list_2','c_grammar_uiapi.py',108),
  ('declaration -> var_declaration','declaration',1,'p_declaration_1','c_grammar_uiapi.py',111),
  ('declaration -> fun_declaration','declaration',1,'p_declaration_2','c_grammar_uiapi.py',113),
  ('var_declaration -> type_specifier ID ;','var_declaration',3,'p_var_declaration_1','c_grammar_uiapi.py',116),
  ('var_declaration -> type_specifier ID [ NUM ] ;','var_declaration',6,'p_var_declaration_2','c_grammar_uiapi.py',118),
  ('type_specifier -> INT','type_specifier',1,'p_type_specifier_1','c_grammar_uiapi.py',121),
  ('type_specifier -> VOID','type_specifier',1,'p_type_specifier_2','c_grammar_uiapi.py',123),
  ('fun_declaration -> type_specifier ID ( params )','fun_declaration',5,'p_fun_declaration_1','c_grammar_uiapi.py',126),
  ('fun_declaration -> compound_stmt','fun_declaration',1,'p_fun_declaration_2','c_grammar_uiapi.py',128),
  ('params -> param_list','params',1,'p_params_1','c_grammar_uiapi.py',131),
  ('params -> VOID','params',1,'p_params_2','c_grammar_uiapi.py',133),
  ('params -> <empty>','params',0,'p_params_empty','c_grammar_uiapi.py',135),
  ('param_list -> param_list , param','param_list',3,'p_param_list_1','c_grammar_uiapi.py',138),
  ('param_list -> param','param_list',1,'p_param_list_2','c_grammar_uiapi.py',140),
  ('param -> type_specifier ID','param',2,'p_param_1','c_grammar_uiapi.py',143),
  ('param -> type_specifier ID [ ]','param',4,'p_param_2','c_grammar_uiapi.py',145),
  ('compound_stmt -> { local_declarations statement_list }','compound_stmt',4,'p_compound_stmt_1','c_grammar_uiapi.py',148),
  ('local_declarations -> local_declarations var_declaration','local_declarations',2,'p_local_declarations_1','c_grammar_uiapi.py',151),
  ('local_declarations -> <empty>','local_declarations',0,'p_local_declarations_empty','c_grammar_uiapi.py',153),
  ('statement_list -> statement_list statement','statement_list',2,'p_statement_list_1','c_grammar_uiapi.py',156),
  ('statement_list -> <empty>','statement_list',0,'p_statement_list_empty','c_grammar_uiapi.py',158),
  ('statement -> expression_stmt','statement',1,'p_statement_1','c_grammar_uiapi.py',161),
  ('statement -> compound_stmt','statement',1,'p_statement_2','c_grammar_uiapi.py',163),
  ('statement -> selection_stmt','statement',1,'p_statement_3','c_grammar_uiapi.py',165),
  ('statement -> iteration_stmt','statement',1,'p_statement_4','c_grammar_uiapi.py',167),
  ('statement -> return_stmt','statement',1,'p_statement_5','c_grammar_uiapi.py',169),
  ('expression_stmt -> expression ;','expression_stmt',2,'p_expression_stmt_1','c_grammar_uiapi.py',172),
  ('expression_stmt -> ;','expression_stmt',1,'p_expression_stmt_2','c_grammar_uiapi.py',174),
  ('selection_stmt -> IF ( expression ) statement','selection_stmt',5,'p_selection_stmt_1','c_grammar_uiapi.py',177),
  ('selection_stmt -> IF ( expression ) statement ELSE statement','selection_stmt',7,'p_selection_stmt_2','c_grammar_uiapi.py',179),
  ('iteration_stmt -> WHILE ( expression ) statement','iteration_stmt',5,'p_iteration_stmt_1','c_grammar_uiapi.py',182),
  ('return_stmt -> RETURN ;','return_stmt',2,'p_return_stmt_1','c_grammar_uiapi.py',185),
  ('return_stmt -> RETURN expression ;','return_stmt',3,'p_return_stmt_2','c_grammar_uiapi.py',187),
  ('expression -> var = expression','expression',3,'p_expression_1','c_grammar_uiapi.py',190),
  ('expression -> simple_expression','expression',1,'p_expression_2','c_grammar_uiapi.py',192),
  ('var -> ID','var',1,'p_var_1','c_grammar_uiapi.py',195),
  ('var -> ID [ expression ]','var',4,'p_var_2','c_grammar_uiapi.py',197),
  ('simple_expression -> additive_expression relop additive_expression','simple_expression',3,'p_simple_expression_1','c_grammar_uiapi.py',200),
  ('simple_expression -> additive_expression','simple_expression',1,'p_simple_expression_2','c_grammar_uiapi.py',202),
  ('relop -> LE','relop',1,'p_relop_1','c_grammar_uiapi.py',205),
  ('relop -> <','relop',1,'p_relop_2','c_grammar_uiapi.py',207),
  ('relop -> >','relop',1,'p_relop_3','c_grammar_uiapi.py',209),
  ('relop -> GE','relop',1,'p_relop_4','c_grammar_uiapi.py',211),
  ('relop -> EE','relop',1,'p_relop_5','c_grammar_uiapi.py',213),
  ('relop -> NE','relop',1,'p_relop_6','c_grammar_uiapi.py',215),
  ('additive_expression -> additive_expression addop term','additive_expression',3,'p_additive_expression_1','c_grammar_uiapi.py',218),
  ('additive_expression -> term','additive_expression',1,'p_additive_expression_2','c_grammar_uiapi.py',220),
  ('addop -> +','addop',1,'p_addop_1','c_grammar_uiapi.py',223),
  ('addop -> -','addop',1,'p_addop_2','c_grammar_uiapi.py',225),
  ('term -> term mulop factor','term',3,'p_term_1','c_grammar_uiapi.py',228),
  ('term -> factor','term',1,'p_term_2','c_grammar_uiapi.py',231),
  ('mulop -> *','mulop',1,'p_mulop_1','c_grammar_uiapi.py',234),
  ('mulop -> /','mulop',1,'p_mulop_2','c_grammar_uiapi.py',236),
  ('factor -> ( expression )','factor',3,'p_factor_1','c_grammar_uiapi.py',239),
  ('factor -> var','factor',1,'p_factor_2','c_grammar_uiapi.py',241),
  ('factor -> call','factor',1,'p_factor_3','c_grammar_uiapi.py',243),
  ('factor -> NUM','factor',1,'p_factor_4','c_grammar_uiapi.py',245),
  ('call -> ID ( args )','call',4,'p_call_1','c_grammar_uiapi.py',248),
  ('args -> arg_list','args',1,'p_args_1','c_grammar_uiapi.py',251),
  ('args -> <empty>','args',0,'p_args_empty','c_grammar_uiapi.py',253),
  ('arg_list -> arg_list , expression','arg_list',3,'p_arg_list_1','c_grammar_uiapi.py',256),
  ('arg_list -> expression','arg_list',1,'p_arg_list_2','c_grammar_uiapi.py',258),
]