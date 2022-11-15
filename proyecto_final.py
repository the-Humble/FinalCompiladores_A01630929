import ply.yacc as yacc
import ply.lex as lex
import sys
sys.path.insert(0, "..")

reserved = {
    "int": "INTDCL",
    "float": "FLOATDCL",
    "print": "PRINT",
    "boolean": "BOOLDCL",
    "true": "BOOLVAL",
    "false": "BOOLVAL",
    "if": "IF",
    "else": "ELSE",
    "elif": "ELIF",
    "while": "WHILE",
    "for": "FOR",
    "and": "AND",
    "or": "OR"
}


tokens = [
    'NAME', 'INUMBER', 'FNUMBER', 'EQ', 'NEQ', 'GT', 'LT', 'GET', 'LET'
]
tokens.extend(reserved.values())

literals = ['=', '+', '-', '*', '/', '^', ';', '(', ')', '{', '}']

# Tokens
t_EQ = r'=='
t_NEQ = r'!='
t_GT = r'>'
t_LT = r'<'
t_GET = r'>='
t_LET = r'<='


def t_NAME(t):
    r'[a-zA-Z_]+[a-zA-Z0-9]*'  # r'[a-eg-hj-oq-z]'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_FNUMBER(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

# Parsing rules


class Node:

    # children = None
    # type = None

    def __init__(self):
        self.children = []
        self.type = ''
        self.val = ''

    def print(self, lvl=0):
        r = (' ' * lvl) + self.type + ":" + str(self.val)
        print(r)
        #print(self.children)
        for c in self.children:
            if():
                pass
            c.print(lvl+1)


# dictionary of names
symbolsTable = {
    "table": {},
    "parent": None,
}
abstractTree = None


def p_prog(p):
    'prog : stmts'
    global abstractTree
    abstractTree = Node()
    abstractTree.type = 'root'
    abstractTree.children.extend(p[1])


def p_statements_recursion(p):
    '''stmts : statement stmts
             | statement '''
    stmt = p[1]
    if len(p) == 3:
        stmts = [stmt]
        stmts.extend(p[2])
        p[0] = stmts
    else:
        p[0] = [stmt]


def p_dcl_declare_int(p):
    'statement : INTDCL NAME ";"'
    symbolsTable["table"][p[2]] = {"type": "INT", "value": 0}
    n = Node()
    n.type = "INT_DCL"
    n.val = p[2]
    p[0] = n


def p_statement_declare_float(p):
    'statement : FLOATDCL NAME ";"'
    symbolsTable["table"][p[2]] = {"type": "FLOAT", "value": 0}
    n = Node()
    n.type = "FLOAT_DCL"
    n.val = p[2]
    p[0] = n


def p_statement_declare_bool(p):
    'statement : BOOLDCL NAME ";"'
    symbolsTable["table"][p[2]] = {"type": "BOOLEAN", "value": False}
    n = Node()
    n.type = "BOOL_DCL"
    n.val = p[2]
    p[0] = n


def p_statement_print(p):
    'statement : PRINT expression ";"'
    n = Node()
    n.type = 'PRINT'
    n.children.append(p[2])
    p[0] = n


def p_statement_if_block(p):
    "statement : ifblock elifblock elseblock"
    n = Node()
    n.children.append(p[1])
    n.children.append(p[2])
    n.children.append(p[3])
    p[0] = n

def p_statement_if(p):
    'ifblock : IF "(" boolexp ")" "{" stmts "}"'
    n = Node()
    n.type = 'IF'
    n.children.append(p[3])
    n2 = Node()
    n2.children.extend(p[6])
    n.children.append(n2)
    p[0] = n

def p_statement_else(p):
    '''elseblock : ELSE "{" stmts "}"
                 | '''
    if len(p) >= 4:
        n = Node()
        n.type = 'ELSE'
        n.children.extend(p[3])
        p[0] = n
    else:
        pass
    

def p_statement_elif(p):
    '''elifblock : ELIF "(" boolexp ")" "{" stmts "}"
                | '''

    if len(p) >= 8:
        n = Node()
        n.type = 'ELIF'
        n.children.append(p[3])
        n2 = Node()
        n2.children.extend(p[6])
        n.children.append(n2)
        p[0] = n
    else:
        pass

def p_statement_assign(p):
    'statement : NAME "=" expression ";"'
    if p[1] not in symbolsTable["table"]:
        print("You must declare a variable before using it")
    n = Node()
    n.type = 'ASSIGN'
    ##n.children.append(p[1])
    if p[1] in symbolsTable["table"]:
        n1 = Node()
        n1.type = 'ID'
        n1.val = p[1]
        n.children.append(n1)
    else:
        print("Error undeclared variable")

    n.children.append(p[3])
    p[0] = n

def p_expression_group(p):
    '''expression : '(' expression ')'
                  | '{' expression '}' '''
    p[0] = p[2]

def p_num_expression(p):
    "expression : numexp"
    p[0] = p[1]

def p_numexp_binop(p):
    '''numexp : numexp '+' numexp
             | numexp '-' numexp
             | numexp '*' numexp
             | numexp '/' numexp
             | numexp '^' numexp'''
    if p[2] == '+':
        n = Node()
        n.type = 'PLUS'
        n.children.append(p[1])
        n.children.append(p[3])
        p[0] = n
    elif p[2] == '-':
        n = Node()
        n.type = 'MINUS'
        n.children.append(p[1])
        n.children.append(p[3])
        p[0] = n
    elif p[2] == '*':
        n = Node()
        n.type = 'MULT'
        n.children.append(p[1])
        n.children.append(p[3])
        p[0] = n
    elif p[2] == '/':
        n = Node()
        n.type = 'DIV'
        n.children.append(p[1])
        n.children.append(p[3])
        p[0] = n
    elif p[2] == '^':
        n = Node()
        n.type = 'EXP'
        n.children.append(p[1])
        n.children.append(p[3])
        p[0] = n

def p_numexp_inumber(p):
    "numexp : INUMBER"
    n = Node()
    n.type = 'INUMBER'
    n.val = int(p[1])
    p[0] = n


def p_numexp_number(p):
    "numexp : FNUMBER"
    n = Node()
    n.type = 'FNUMBER'
    n.val = float(p[1])
    p[0] = n


def p_expression_boolval(p):
    "expression : boolexp"
    p[0] = p[1]

def p_bool_expression(p):
    "boolexp : BOOLVAL"
    n = Node()
    n.type = 'BOOLVAL'
    n.val = (p[1] == 'true')
    p[0] = n

def p_bool_comp(p):
    '''boolexp : numexp EQ numexp
                | boolexp EQ boolexp
                | numexp NEQ numexp
                | boolexp NEQ boolexp
                | numexp GT numexp
                | numexp LT numexp
                | numexp GET numexp
                | numexp LET numexp
                | boolexp AND boolexp
                | boolexp OR boolexp'''
    if p[2] == '==':
        n = Node()
        n.type = 'EQ'
        n.children.append(p[1])
        n.children.append(p[3])
        p[0] = n
    elif p[2] == '!=':
        n = Node()
        n.type = 'NEQ'
        n.children.append(p[1])
        n.children.append(p[3])
        p[0] = n
    elif p[2] == '>':
        n = Node()
        n.type = 'GT'
        n.children.append(p[1])
        n.children.append(p[3])
        p[0] = n
    elif p[2] == '<':
        n = Node()
        n.type = 'LT'
        n.children.append(p[1])
        n.children.append(p[3])
        p[0] = n
    elif p[2] == '>=':
        n = Node()
        n.type = 'GET'
        n.children.append(p[1])
        n.children.append(p[3])
        p[0] = n
    elif p[2] == '<=':
        n = Node()
        n.type = 'LET'
        n.children.append(p[1])
        n.children.append(p[3])
        p[0] = n
    elif p[2] == 'and':
        n = Node()
        n.type = 'AND'
        n.children.append(p[1])
        n.children.append(p[3])
        p[0] = n
    elif p[2] == 'or':
        n = Node()
        n.type = 'OR'
        n.children.append(p[1])
        n.children.append(p[3])
        p[0] = n


def p_expression_name(p):
    "expression : NAME"
    if p[1] in symbolsTable["table"]:
        n = Node()
        n.type = 'ID'
        n.val = p[1]
        p[0] = n


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()


f = open("code.txt")
content = f.read()
yacc.parse(content)


abstractTree.print()
varCounter = 0
labelCounter = 0


def genTAC(node):
    global varCounter
    global labelCounter
    if (node.type == "ASSIGN"):
        print(node.children[0].val + " := " + str(genTAC(node.children[1])))
    elif (node.type == "INUMBER"):
        return str(node.val)
    elif (node.type == "FNUMBER"):
        return str(node.val)
    elif (node.type == "BOOLVAL"):
        return str(node.val)
    elif (node.type == "PLUS"):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter + 1
        print(tempVar + " := " +
              genTAC(node.children[0]) + " + " + genTAC(node.children[1]))
        return tempVar
    elif (node.type == "MINUS"):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter + 1
        print(tempVar + " := " +
              genTAC(node.children[0]) + " - " + genTAC(node.children[1]))
        return tempVar
    elif (node.type == "MULT"):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter + 1
        print(tempVar + " := " +
              genTAC(node.children[0]) + " * " + genTAC(node.children[1]))
        return tempVar
    elif (node.type == "DIV"):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter + 1
        print(tempVar + " := " +
              genTAC(node.children[0]) + " / " + genTAC(node.children[1]))
        return tempVar
    elif (node.type == "EXP"):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter + 1
        print(tempVar + " := " +
              genTAC(node.children[0]) + " ^ " + genTAC(node.children[1]))
        return tempVar
    elif (node.type == "EQ"):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter + 1
        print(tempVar + " := " +
              genTAC(node.children[0]) + " == " + genTAC(node.children[1]))
    elif (node.type == "NEQ"):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter + 1
        print(tempVar + " := " +
              genTAC(node.children[0]) + " != " + genTAC(node.children[1]))
    elif (node.type == 'GT'):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter + 1
        print(tempVar + " := " +
              genTAC(node.children[0]) + " > " + genTAC(node.children[1]))
    elif (node.type == 'LT'):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter + 1
        print(tempVar + " := " +
              genTAC(node.children[0]) + " < " + genTAC(node.children[1]))
    elif (node.type == 'GET'):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter + 1
        print(tempVar + " := " +
              genTAC(node.children[0]) + " >= " + genTAC(node.children[1]))
    elif (node.type == 'LET'):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter + 1
        print(tempVar + " := " +
              genTAC(node.children[0]) + " <= " + genTAC(node.children[1]))
    elif (node.type == 'AND'):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter + 1
        print(tempVar + " := " +
              genTAC(node.children[0]) + " AND " + genTAC(node.children[1]))
    elif (node.type == 'OR'):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter + 1
        print(tempVar + " := " +
              genTAC(node.children[0]) + " OR " + genTAC(node.children[1]))
    elif (node.type == "PRINT"):
        print("PRINT " + genTAC(node.children[0]))
    elif (node.type == "IF"):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter + 1
        print(tempVar + " := " + 
            str(genTAC((node.children[0]))))
        tempLabel = "l" + str(labelCounter)
        labelCounter = labelCounter + 1
        print("gotoLabelIf " + tempVar + " " + tempLabel)
        genTAC(node.children[1])
        print(tempLabel)
    elif (node.type == "ELSE"):
        tempLabel = "l" + str(labelCounter)
        labelCounter = labelCounter + 1
        print("gotoLabelElse " + tempLabel)
        genTAC(node.children[1])
        print(tempLabel)
    elif (node.type == "ELIF"):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter + 1
        print(tempVar + " := " +
              str(genTAC((node.children[0]))))
        tempLabel = "l" + str(labelCounter)
        labelCounter = labelCounter + 1
        print("gotoLabelElif " + tempVar + " " + tempLabel)
        genTAC(node.children[1])
        print(tempLabel)
    else:
        for child in node.children:
            if child.type != None:
                genTAC(child)


print("\ntac:\n")
genTAC(abstractTree)


#Some examples
# for ( i = 0; i < 3; i++){
#     stamentes
# }
# i := 0
# t1 = i < 3
# t0 = !t1
# gotoLabelif t0 Label1

# staments
# i = i + 1
# Label1


# while ( condicion ) {
#     staments
# }
# WHILE
# t1 = condicion
# t0 = !t1
# gotoLabelif t0 Label1

# staments

# Label1
