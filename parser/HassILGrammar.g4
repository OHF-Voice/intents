grammar HassILGrammar;

document
   : (sentence)+
   ;

sentence
   : expression EOL
   ;

expression
   : (group | optional | word | list | rule) ((WS | alt) expression)*
   ;

// One or more words in a sequence
group
   : '(' expression ')'
   ;

optional
   : '[' expression ']'
   ;

alt
   : WS? '|' WS?
   ;

word
   : STRING
   ;

prefix
   : STRING
   ;

suffix
   : STRING
   ;

list
   : (prefix)? '{' list_name '}' (suffix)?
   ;

list_name
   : STRING
   ;

rule
   : '<' rule_name '>'
   ;

rule_name
   : STRING
   ;

STRING
   : UNQUOTED_STRING | QUOTED_STRING
   ;

QUOTED_STRING
   : '"' (QUOTED_ESC | ~["])* '"'
   ;

QUOTED_ESC
   : '\\' ["]
   ;

UNQUOTED_STRING
   : (UNQUOTED_ESC | CHARACTER)+
   ;

UNQUOTED_ESC
   : '\\' ["<>()[\]{}]
   ;

CHARACTER
   : ~ ["<>()[\]{} \t\n\r]
   ;

EOL
   : [\n\r] +
   ;

WS
   : [ \t] +
   ;
