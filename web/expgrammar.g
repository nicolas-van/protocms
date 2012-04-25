
parser AlchemyExp:

ignore: "\\s+"
token identifier: "[a-zA-Z_][a-zA-Z0-9_]*"
token boolean_litteral: "true|false"
token float_litteral: "[0-9]+\.[0-9]*"
token integer_litteral: "[0-9]+"
token string_litteral: "(\"[^\"\n]*(\\\"[^\"\n]*)*\")|('[^'\n]*(\\'[^'\n]*)*')"
token null_litteral: "null"

token logical_or: "or"
token logical_and: "and"
token equality: "==|!="
token relational: "<|>|<=|>="
token additive: "\\+|-"
token mult: "\\*|/|%"
token non: "not"

rule litteral: boolean_litteral {{ return boolean_litteral == "true" }} |
    string_litteral {{ return eval(string_litteral) }} |
    integer_litteral {{ return int(integer_litteral) }} |
    float_litteral {{ return float(float_litteral) }} |
    null_litteral {{ return None }}

rule program: expression "$" {{ return expression }}

rule expression : logical_or_expr {{return logical_or_expr}}
rule logical_or_expr : logical_and_expr {{res = logical_and_expr}}
    (logical_or logical_and_expr {{res = [logical_or, res, logical_and_expr]}})* {{return res}}
rule logical_and_expr : equality_expr {{res = equality_expr}}
    (logical_and equality_expr {{res = [logical_and, res, equality_expr]}})* {{return res}}
rule equality_expr : relational_expr {{res = relational_expr}}
    (equality relational_expr {{res = [equality, res, relational_expr]}})* {{return res}}
rule relational_expr : additive_expr {{res = additive_expr}} 
    (relational additive_expr {{res = [relational, res, additive_expr]}})* {{return res}}
rule additive_expr : mult_expr {{res = mult_expr}}
    (additive mult_expr {{res = [additive, res, mult_expr]}})* {{return res}}
rule mult_expr : unary_expr {{res = unary_expr}}
    (mult unary_expr {{res = [mult, res, unary_expr]}})* {{return res}}
rule unary_expr : {{tmp = None}}(additive {{tmp = additive}} | non {{tmp=non}})
    unary_expr {{return [tmp, unary_expr] if tmp is not None else unary_expr}} | postfix_expr {{return postfix_expr}}
rule postfix_expr : rvalue {{return rvalue}} | "\\(" expression "\\)" {{return expression}}
rule rvalue : litteral {{return ('litteral',litteral)}}| identifier {{return ('identifier',identifier)}}
    | list {{return ('list',list)}}
rule list : "\\[" [( expression ( "," expression  )* [","]  )]  "\\]"


 

