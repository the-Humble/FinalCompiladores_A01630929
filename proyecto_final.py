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

def p_statement_inline_dcls(p):
    '''statement : inlineintdcl
                  | inlinefloatdcl
                  | inlinebooldcl '''
    p[0] = p[1]


def p_dcl_declare_int(p):
    '''statement : INTDCL NAME ";"'''
    symbolsTable["table"][p[2]] = {"type": "INT", "value": 0}
    n = Node()
    n.type = "INT_DCL"
    n.val = p[2]
    p[0] = n

def p_dcl_declareinline_int(p):
    '''inlineintdcl : INTDCL NAME "=" numexp ";"'''
    symbolsTable["table"][p[2]] = {"type": "INT", "value": 0}
    n = Node()
    n.type = "INT_DCL"
    n.val = p[2]
    n2 = Node()
    n2.type = 'ASSIGN'
    n3 = Node()
    n3.type = 'ID'
    n3.val = p[2]
    n2.children.append(n3)
    n2.children.append(p[4])
    n.children.append(n2)

    if str(p[4].val).isnumeric(): 
        symbolsTable["table"][p[2]]["value"] = p[4].val
    else:
        print("Invalid Integer Expression")
        exit()
    p[0] = n

def p_statement_declareinline_float(p):
    '''inlinefloatdcl : FLOATDCL NAME "=" numexp ";"'''
    symbolsTable["table"][p[2]] = {"type": "FLOAT", "value": 0}
    n = Node()
    n.type = "FLOAT_DCL"
    n.val = p[2]
    n2 = Node()
    n2.type = 'ASSIGN'
    n3 = Node()
    n3.type = 'ID'
    n3.val = p[2]
    n2.children.append(n3)
    n2.children.append(p[4])
    n.children.append(n2)
    symbolsTable["table"][p[2]]["value"] = p[4].val
    p[0] = n

def p_statement_declare_float(p):
    '''statement : FLOATDCL NAME ";"'''
    symbolsTable["table"][p[2]] = {"type": "FLOAT", "value": 0}
    n = Node()
    n.type = "FLOAT_DCL"
    n.val = p[2]
    p[0] = n


def p_statement_declareinline_bool(p):
    '''inlinebooldcl : BOOLDCL NAME  "="  boolexp ";"'''
    symbolsTable["table"][p[2]] = {"type": "BOOLEAN", "value": False}
    n = Node()
    n.type = "BOOL_DCL"
    n.val = p[2]
    n2 = Node()
    n2.type = 'ASSIGN'
    n3 = Node()
    n3.type = 'ID'
    n3.val = p[2]
    n2.children.append(n3)
    n2.children.append(p[4])
    n.children.append(n2)
    symbolsTable["table"][p[2]]["value"] = p[4].val
    p[0] = n

def p_statement_declare_bool(p):
    '''statement : BOOLDCL NAME ";"'''
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
    "statement : ifblock elifrecursive elseblock"
    n = Node()
    n.children.append(p[1])
    n.children.append(p[2])
    n2 = Node()
    n2.children.append(p[3])
    n.children.append(n2)
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

def p_statement_elifrecursive(p):
    '''elifrecursive : elifrecursive elifblock
                     |'''
    if len(p) >2:
        n = Node()
        if p[1] != None:
            n.children.append(p[1])
        n.children.append(p[2])
        p[0] = n
    else:
        pass
    

def p_statement_elif(p):
    '''elifblock : ELIF "(" boolexp ")" "{" stmts "}"'''
    n = Node()
    n.type = 'ELIF'
    n.children.append(p[3])
    n2 = Node()
    n2.children.extend(p[6])
    n.children.append(n2)
    p[0] = n

def p_statement_while(p):
    'statement : WHILE "(" boolexp ")" "{" stmts "}"'
    n = Node()
    n.type = 'WHILE'
    n.children.append(p[3])
    n2 = Node()
    n2.children.extend(p[6])
    n.children.append(n2)
    p[0] = n


def p_statement_for(p):
    'statement : FOR "(" inlineintdcl boolexp ";" numassign ")" "{" stmts "}"'
    n = Node()
    n.type = 'FOR'
    n.children.append(p[3])
    n.children.append(p[4])
    n.children.append(p[6])
    n2 = Node()
    n2.children.extend(p[9])
    n.children.append(n2)
    p[0] = n

def p_statement_assign(p):
    '''statement : numassign
                 | boolassign'''
    p[0] = p[1]

def p_statement_numassign(p):
    'numassign : NAME "=" numexp ";"'
    if p[1] not in symbolsTable["table"]:
        print("You must declare a variable before using it")
    n = Node()
    n.type = 'ASSIGN'
    
    numberType = ''
    ##n.children.append(p[1])
    if p[1] in symbolsTable["table"]:
        numberType = symbolsTable["table"][p[1]]["type"]
        n1 = Node()
        n1.type = 'ID'
        n1.val = p[1]
        n.children.append(n1)
    else:
        print("Error undeclared variable")
    if numberType == 'FLOAT':
        symbolsTable["table"][p[1]]["value"] = float(p[3].val)
    elif numberType == 'INT':
        if str(p[3].val).isnumeric():
            symbolsTable["table"][p[1]]["value"] = int(p[3].val)
        else:
            print("Invalid Integer Expression")
            exit()
    
    n.children.append(p[3])
    p[0] = n

def p_statement_boolassign(p):
    'boolassign : NAME "=" boolexp ";"'
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

def p_num_expression(p):
    '''numexp : NAME'''
    n = Node()
    if p[1] in symbolsTable["table"]:
        if symbolsTable["table"][p[1]]["type"] == "INT":
            n.type = "INUMBER"
            n.val = p[1]
            p[0] = n

        elif symbolsTable["table"][p[1]]["type"] == "FLOAT":
            n.type = "FNUMBER"
            n.val = p[1]
            p[0] = n
    elif p[1] not in symbolsTable["table"] and not type(p[1]) is int or float:
        print("You must declare a variable before using it")
        exit()
    else:
        p[0] = p[1]

def p_numexp_binop(p):
    '''numexp : numexp '+' numexp
             | numexp '-' numexp
             | numexp '*' numexp
             | numexp '/' numexp
             | numexp '^' numexp'''
    n = Node()
    tempP1 = p[1].val
    tempP3 = p[3].val
    if p[1].val in symbolsTable["table"]:
        tempP1 = symbolsTable["table"][p[1].val]["value"]

    if p[3].val in symbolsTable["table"]:
        tempP3 = symbolsTable["table"][p[3].val]["value"]

    if p[2] == '+':
        n.type = 'PLUS'
        n.val = tempP1 + tempP3
    elif p[2] == '-':
        n.type = 'MINUS'
        n.val = tempP1 - tempP3
    elif p[2] == '*':
        n.type = 'MULT'
        n.val = tempP1 * tempP3
    elif p[2] == '/':
        n.type = 'DIV'
        n.val = tempP1 / tempP3
    elif p[2] == '^':
        n.type = 'EXP'
        n.val = tempP1 ** tempP3
    n.children.append(p[1])
    n.children.append(p[3])
    p[0] = n

def p_numexp_inumber(p):
    '''numexp : INUMBER'''
    n = Node()
    n.type = 'INUMBER'
    n.val = int(p[1])
    p[0] = n



def p_numexp_fnumber(p):
    '''numexp : FNUMBER'''
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
    n = Node()

    tempP1 = p[1].val
    tempP3 = p[3].val
    if p[1].val in symbolsTable["table"]:
        tempP1 = symbolsTable["table"][p[1].val]["value"]

    if p[3].val in symbolsTable["table"]:
        tempP3 = symbolsTable["table"][p[3].val]["value"]

    if p[2] == '==':
        n.type = 'EQ'
        n.val = tempP1 == tempP3
    elif p[2] == '!=':
        n.type = 'NEQ'
        n.val = tempP1 != tempP3
    elif p[2] == '>':
        n.type = 'GT'
        n.val = tempP1 > tempP3
    elif p[2] == '<':
        n.type = 'LT'
        n.val = tempP1 < tempP3
    elif p[2] == '>=':
        n.type = 'GET'
        n.val = tempP1 >= tempP3
    elif p[2] == '<=':
        n.type = 'LET'
        n.val = tempP1 <= tempP3
    elif p[2] == 'and':
        n.type = 'AND'
        n.val = tempP1 and tempP3
    elif p[2] == 'or':
        n.type = 'OR'
        n.val = tempP1 or tempP3
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
        print("Syntax error at '%s' in line '%d'" % (p.value, lexer.lineno))
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()


f = open("code.txt")
content = f.read()
yacc.parse(content)


abstractTree.print()

#TODO: Semantic Ananlysis



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
        return tempVar
    elif (node.type == 'GT'):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter + 1
        print(tempVar + " := " +
              genTAC(node.children[0]) + " > " + genTAC(node.children[1]))
        return tempVar
    elif (node.type == 'LT'):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter + 1
        print(tempVar + " := " +
              genTAC(node.children[0]) + " < " + genTAC(node.children[1]))
        return tempVar
    elif (node.type == 'GET'):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter + 1
        print(tempVar + " := " +
              genTAC(node.children[0]) + " >= " + genTAC(node.children[1]))
        return tempVar
    elif (node.type == 'LET'):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter + 1
        print(tempVar + " := " +
              genTAC(node.children[0]) + " <= " + genTAC(node.children[1]))
        return tempVar
    elif (node.type == 'AND'):
        tempVar = "t" + str(varCounter)
        print(tempVar + " := " +
              genTAC(node.children[0]) + " AND " + genTAC(node.children[1]))
        return tempVar
    elif (node.type == 'OR'):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter + 1
        print(tempVar + " := " +
              genTAC(node.children[0]) + " OR " + genTAC(node.children[1]))
        return tempVar
    elif (node.type == "PRINT"):
        print("PRINT " + genTAC(node.children[0]))
    elif (node.type == "IF" or node.type == "ELIF"):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter + 1
        print(tempVar + " := !" + genTAC(node.children[0]))
        tempLabel = "l" + str(labelCounter)
        labelCounter = labelCounter + 1
        print("gotoLabelIf " + tempVar + " " + tempLabel)
        genTAC(node.children[1])
        print(tempLabel)
    elif (node.type == "ELSE"):
        tempLabel = "l" + str(labelCounter)
        labelCounter = labelCounter
        print("gotoLabel " + tempLabel)
        genTAC(node.children[1])
        print(tempLabel)
    elif (node.type == "WHILE"):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter + 1
        tempLabel = "l" + str(labelCounter)
        print(tempLabel)
        labelCounter = labelCounter + 1
        tempLabel = "l" + str(labelCounter)
        print(tempVar + " := !" + genTAC(node.children[0]))
        print("gotoLabelIf " + tempVar + " " + tempLabel)
        genTAC(node.children[1])
        labelCounter = labelCounter - 1
        tempLabel = "l" + str(labelCounter)
        print("gotoLabel " + tempLabel)
        labelCounter = labelCounter + 1
        tempLabel = "l" + str(labelCounter)
        print(tempLabel)
    elif (node.type == "FOR"):
        genTAC(node.children[0])
        tempVar = "t" + str(varCounter)
        varCounter = varCounter + 1
        tempLabel = "l" + str(labelCounter)
        print(tempLabel)
        labelCounter = labelCounter + 1
        tempLabel = "l" + str(labelCounter)
        print(tempVar + " := !" + str(genTAC(node.children[1])))
        print("gotoLabelIf " + tempVar + " " + tempLabel)
        genTAC(node.children[3])
        genTAC(node.children[2]) 
        labelCounter = labelCounter - 1
        tempLabel = "l" + str(labelCounter)
        print("gotoLabel " + tempLabel)
        labelCounter = labelCounter + 1
        tempLabel = "l" + str(labelCounter)
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
