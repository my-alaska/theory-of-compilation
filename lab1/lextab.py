# lextab.py. This file automatically created by PLY (version 3.11). Don't edit!
_tabversion   = '3.10'
_lextokens    = set(('ADDASSIGN', 'BREAK', 'COMMENT', 'CONTINUE', 'DIVASSIGN', 'DOTADD', 'DOTDIV', 'DOTMUL', 'DOTSUB', 'EGREATER', 'ELESS', 'ELSE', 'EQUALS', 'EYE', 'FLOATNUM', 'FOR', 'ID', 'IF', 'INTNUM', 'MULASSGIN', 'NEQUALS', 'ONES', 'PRINT', 'RETURN', 'STRING', 'SUBASSIGN', 'WHILE', 'ZEROS'))
_lexreflags   = 64
_lexliterals  = "+-*/()[]{}=<>:',;"
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_ID>[a-zA-Z_][a-zA-Z_0-9]*)|(?P<t_INTNUM>\\d+)|(?P<t_FLOATNUM>(-?\\d+\\.\\d+)(e(\\+|-)?\\d+)?)|(?P<t_STRING>\\".*?")|(?P<t_ignore_COMMENT>\\#.*)|(?P<t_DOTADD>\\.+)|(?P<t_DOTSUB>\\.-)|(?P<t_DOTMUL>\\.*)|(?P<t_DOTDIV>\\./)|(?P<t_ADDASSIGN>\\+=)|(?P<t_MULASSIGN>\\*=)|(?P<t_ELESS><=)|(?P<t_EGREATER>>=)|(?P<t_EQUALS>==)|(?P<t_NEQUALS>!=)|(?P<t_SUBASSIGN>-=)|(?P<t_DIVASSIGN>-=)', [None, ('t_ID', 'ID'), ('t_INTNUM', 'INTNUM'), ('t_FLOATNUM', 'FLOATNUM'), None, None, None, ('t_STRING', 'STRING'), (None, None), (None, 'DOTADD'), (None, 'DOTSUB'), (None, 'DOTMUL'), (None, 'DOTDIV'), (None, 'ADDASSIGN'), (None, 'MULASSIGN'), (None, 'ELESS'), (None, 'EGREATER'), (None, 'EQUALS'), (None, 'NEQUALS'), (None, 'SUBASSIGN'), (None, 'DIVASSIGN')])]}
_lexstateignore = {'INITIAL': ''}
_lexstateerrorf = {'INITIAL': 't_error'}
_lexstateeoff = {}
