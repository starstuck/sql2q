from lark import Lark, Transformer

# Subset of postgres SQL select grammar
# (https://www.postgresql.org/docs/current/sql-select.html)
grammar = r"""
query: SELECT  \
    ( ALL | STAR | columns ) \
    FROM table \
    [ WHERE condition ]

columns: column ("," column)* | STAR
column: NAME | "`" QUOTEDNAME "`"

table: NAME DOT (NAME | "`" QUOTEDNAME "`")

condition: condition AND condition
    | column COMP_OP value_expr
value_expr: STR_VALUE 

SELECT: "select"i
FROM: "from"i
WHERE: "where"i
ALL: "all"i
STAR: "*"
DOT: "."
NAME: /[a-z0-9_]+/i
QUOTEDNAME: /\w+/
COMP_OP: "=" | "<>" | "<" | "<=" | ">" | ">="
AND: "and"i
STR_VALUE: "\"" /\w+/ "\""
INT_VALUE: /[0-9]+/

%ignore /[ \t\n\f\r]+/
"""


class QTransformer(Transformer):
    """Transform parsed sql tree to q"""

    def query(self, tokens):
        print("query tokens: ", tokens) 
        _select , columns, _from , table, _where, _condition = tokens
        return f"select {columns} from {table}"

    def columns(self, tokens):
        return ''

    def table(self, tokens):
        print("Table tokens:", tokens)
        ns, _dot, name = tokens
        return f".{ns}.get{name.capitalize()}"

def main():
    parser = Lark(grammar, start='query', parser='lalr')
    tree = parser.parse("select * from cls.positions")
    print ("Parse tree:\n", tree.pretty())
    
    q = QTransformer().transform(tree)
    print ("Q query:", q)
    
main()
