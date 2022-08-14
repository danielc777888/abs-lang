import absparser

#Base class for all visitors
class Visitor:

    def __init__(self):
        self.errors = []    
    
    def visit(self,node):
        node.accept(self)
        
    def has_errors(self):
        if len(self.errors) > 0:
            return True
        return False

#Traverses Parse Tree, and prints out information        
class PrintASTVisitor(Visitor):
   
    def visit_program(self,node):
        print 'program'
        #accept start node
        node.nonTerminals[0].accept(self)
        if node.nonTerminals[1] != None:
            #accept method list
            node.nonTerminals[1].accept(self)
            
    def visit_method_list(self,node):
        print 'method_list %s' % node.lineNo
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        return
        
    def visit_method(self,node):
        print 'method %s gives %s' % (node.terminals[0],node.terminals[1])
        if node.nonTerminals[0] != None:
            node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        return
        
    def visit_parameter_list(self,node):
        print 'parameter_list'
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        return
        
    def visit_parameter(self,node):
        print 'parameter %s %s' % (node.terminals[0],node.terminals[1])
        return
        
    
    def visit_start(self, node):
        print 'start'
        node.nonTerminals[0].accept(self)
    
    def visit_statement_list(self,node):
        print 'statement list' 
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        return
            
    def visit_gives_stmt(self,node):
        print 'gives stmt'
        node.nonTerminals[0].accept(self)
        
    def visit_assignment_stmt(self,node):
        node.nonTerminals[0].accept(self)
        print 'assignment_statement'
        
    def visit_method_call(self,node):
        print 'method_call %s' % node.terminals[0]
        if node.nonTerminals[0] != None:
            node.nonTerminals[0].accept(self)
            
    def visit_expression_list(self,node):
        print 'expression_list'
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
    
                
    def visit_output_stmt(self,node):
        print 'output_stmt'
        node.nonTerminals[0].accept(self)
        return
        
    def visit_input_stmt(self,node):
        print 'input_stmt'
        return
        
    def visit_if_stmt(self,node):
        print 'if_stmt'
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        return
        
    def visit_else_stmt(self,node):
        print 'else_stmt'
        if len(node.nonTerminals) > 0:
            node.nonTerminals[0].accept(self)
        return
        
    def visit_loop_stmt(self,node):
        print 'loop_stmt'
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        
    def visit_array_define(self,node):
        print 'array_define'
        node.nonTerminals[0].accept(self)
        return
        
    def visit_array_assign(self,node):
        print 'array_assign'
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        return
            
        
    def visit_equality(self,node):
        print 'equality %s' % (node.terminals[0])
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        return

   
    def visit_binop(self,node):
        print 'binop %s' % (node.terminals[0])
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        return
        
         
    def visit_integer(self,node):
        print 'integer %s' % (node.terminals[0])
        return node.terminals[0]
        
    def visit_text(self,node):
        print 'text %s' % (node.terminals[0])
        return node.terminals[0]
        
    def visit_identifier(self,node):
        print 'identifier %s' % (node.terminals[0])
        return node.terminals[0]
        
    def visit_array(self,node):
        print 'array'
        node.nonTerminals[0].accept(self)
        return



#SymbolTable containing method information
class SymbolTable:
    def __init__(self):
        self.parameters = {}
        self.locals = {}
        self.returnType = ''
 
symbolTables = {}

#Initializes symbol tables. Also checks for duplicate identifiers
#and uninitialized identifiers.
class SymbolTableVisitor(Visitor):
    
    def __init__(self):
        Visitor.__init__(self)
        self.currentSymbolTable = SymbolTable()
    
    def checkDuplicateIdentifier(self,identifier,node):
        if self.currentSymbolTable.locals.has_key(identifier) == True:
            self.errors.append("Identifier %s already defined : line %d" % (identifier,node.lineNo))
            return True
            
        else:
            return False
            
    def checkDefinedIdentifier(self,identifier,node):
        if self.currentSymbolTable.locals.has_key(identifier) == False and self.currentSymbolTable.parameters.has_key(identifier) == False:
            self.errors.append("Identifier %s not defined : line %d" % (identifier,node.lineNo))
            return False
        else:
            return True
            
    def visit_program(self,node):
        #accept start node
        node.nonTerminals[0].accept(self)
        if node.nonTerminals[1] != None:
            #accept method list
            node.nonTerminals[1].accept(self)
            
    def visit_method_list(self,node):
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        return
        
    def visit_method(self,node):
        #initialize new symbol table for new method
        self.currentSymbolTable = SymbolTable()
        self.methodId = ''
        #method name, return type
        self.methodId = '%s' % (node.terminals[0])
        self.currentSymbolTable.returnType = node.terminals[1]
        if node.nonTerminals[0] != None:
            node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        symbolTables[self.methodId] = self.currentSymbolTable;
        return
        
    def visit_parameter_list(self,node):
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        return
        
    def visit_parameter(self,node):
        #add parameter to symbol table
        self.currentSymbolTable.parameters[node.terminals[1]] = node.terminals[0]
        return
        
    
    def visit_start(self, node):
        #initialize new symbol table for start method
        self.currentSymbolTable = SymbolTable()
        symbolTables['start'] = self.currentSymbolTable
        node.nonTerminals[0].accept(self)
    
    def visit_statement_list(self,node):
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        return
            
    def visit_assignment_stmt(self,node):
        #declare & assign stmt
        if node.terminals[0] != None:
            type = node.terminals[0]
            identifier = node.terminals[1]
            if self.checkDuplicateIdentifier(identifier,node) == False:
                self.currentSymbolTable.locals[identifier] = type
        #only assign stmnt
        else:
            identifier = node.terminals[1]
            self.checkDefinedIdentifier(identifier,node)
      
        node.nonTerminals[0].accept(self)
        return
        
    def visit_method_call(self,node):
        if node.nonTerminals[0] != None:
            node.nonTerminals[0].accept(self)
            
    def visit_expression_list(self,node):
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        
    def visit_array_define(self,node):
        arraytype = node.terminals[1]
        identifier = node.terminals[0]
        if self.checkDuplicateIdentifier(identifier,node) == False:
            self.currentSymbolTable.locals[identifier] = arraytype + '[]' 
            
    def visit_array_assign(self,node):
        identifier = node.terminals[0]
        self.checkDefinedIdentifier(identifier,node)
        
           
    def visit_output_stmt(self,node):
        node.nonTerminals[0].accept(self)
        return
        
    def visit_gives_stmt(self,node):
        node.nonTerminals[0].accept(self)
        return
        
        
    def visit_input_stmt(self,node):
        if len(node.terminals) == 2:
            type = node.terminals[0]
            identifier = node.terminals[1]
            if self.checkDuplicateIdentifier(identifier,node) == False:
                self.currentSymbolTable.locals[identifier] = type
        #only assign
        elif len(node.terminals) == 1:
            identifier = node.terminals[0]
            self.checkDefinedIdentifier(identifier,node)
        return
        
    def visit_if_stmt(self,node):
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        if node.nonTerminals[2] != None:
            node.nonTerminals[2].accept(self)
        
    def visit_else_stmt(self,node):
        if len(node.nonTerminals) > 0:
            node.nonTerminals[0].accept(self)
    
    def visit_loop_stmt(self,node):
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
    
    def visit_equality(self,node):
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        return

           
   
    def visit_binop(self,node):
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        return
               
    def visit_integer(self,node):
        return node.terminals[0]
        
    def visit_text(self,node):
        return node.terminals[0]
        
    def visit_identifier(self,node):
        identifier = node.terminals[0]
        #if identifier not defined add error
        self.checkDefinedIdentifier(identifier,node)
        return node.terminals[0]
        
    def visit_array(self,node):
        identifier = node.terminals[0]
        #if identifier not defined add error
        self.checkDefinedIdentifier(identifier,node)
        node.nonTerminals[0].accept(self)
        return node.terminals[0]
        
#Visitor for checking correct type usage.
#Assumes that symbolTables properly initialized. 
class TypeCheckVisitor(Visitor):
    
    def __init__(self):
        Visitor.__init__(self)
        self.currentSymbolTable = None
        self.currentType = None
    
    #Checks literals type with current type scope.
    def checkLiteralType(self,type,node):
        #if current type not set, then set it with literal's type
        if self.currentType == None:
            self.currentType = type
        if self.currentType.find(type) == -1:
            self.errors.append("Cannot use type '%s' when type '%s' is required : line %d" % (type,self.currentType,node.lineNo))
    
    #Checks identifier type with current type scope.
    def checkIdentifierType(self,identifier,type,node):
        #if current type not set, then set it with identifiers type
        if self.currentType == None:
            self.currentType = type
        if self.currentType.find(type) == -1:
            self.errors.append("Identifier '%s' is not of type '%s' : line %d" % (identifier,self.currentType,node.lineNo))
               
    def visit_program(self,node):
        #accept start node
        node.nonTerminals[0].accept(self)
        if node.nonTerminals[1] != None:
            #accept method list
            node.nonTerminals[1].accept(self)
            
    def visit_method_list(self,node):
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        return
        
    def visit_method(self,node):
         #method name, return type
        self.currentSymbolTable = symbolTables[node.terminals[0]]
        if node.nonTerminals[0] != None:
            node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        return
        
    def visit_parameter_list(self,node):
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        return
        
    def visit_parameter(self,node):
        return
        
    
    def visit_start(self, node):
        self.currentSymbolTable = symbolTables['start']
        node.nonTerminals[0].accept(self)
    
    def visit_statement_list(self,node):
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        return
            
    def visit_assignment_stmt(self,node):
        identifier = node.terminals[1]
        self.currentType = self.currentSymbolTable.locals[identifier] 
        node.nonTerminals[0].accept(self)
        #after assignment stmn set current type scope to None
        self.currentType = None
        return
        
    def visit_method_call(self,node):
        if node.nonTerminals[0] != None:
            node.nonTerminals[0].accept(self)
        self.currentType = None
            
    def visit_expression_list(self,node):
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        
    def visit_array_define(self,node):
        #when defining an array , ints used to specify size
        self.currentType = 'int'
        node.nonTerminals[0].accept(self)
        self.currentType = None
                   
    def visit_array_assign(self,node):
       
        self.currentType = 'int'
         #evaluate index expression,must be of type int
        node.nonTerminals[0].accept(self)
        #evaluate expression, must of of array type
        identifier = node.terminals[0]
        self.currentType = self.currentSymbolTable.locals[identifier].strip('[]')
        node.nonTerminals[1].accept(self)
        self.currentType = None
              
           
    def visit_output_stmt(self,node):
        node.nonTerminals[0].accept(self)
        self.currentType = None
        return
        
    def visit_gives_stmt(self,node):
        node.nonTerminals[0].accept(self)
        return
        
        
    def visit_input_stmt(self,node):
        identifier = ''
        if len(node.terminals) == 2:
            type = node.terminals[0]
            identifier = node.terminals[1]
        #only assign
        elif len(node.terminals) == 1:
            identifier = node.terminals[0]
        self.currentType = None
        return
        
    def visit_if_stmt(self,node):
        node.nonTerminals[0].accept(self)
        self.currentType = None
        node.nonTerminals[1].accept(self)
        if node.nonTerminals[2] != None:
            node.nonTerminals[2].accept(self)
        
        
    def visit_else_stmt(self,node):
        if len(node.nonTerminals) > 0:
            node.nonTerminals[0].accept(self)
        self.currentType = None
    
    def visit_loop_stmt(self,node):
        node.nonTerminals[0].accept(self)
        self.currentType = None
        node.nonTerminals[1].accept(self)
        
    
    def visit_equality(self,node):
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        return

    
    def visit_binop(self,node):
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        return
               
    def visit_integer(self,node):
        self.checkLiteralType('int',node)
        return node.terminals[0]
        
    def visit_text(self,node):
        self.checkLiteralType('text',node)
        return node.terminals[0]
        
    def visit_identifier(self,node):
        identifier = node.terminals[0]
        if (self.currentSymbolTable.locals.has_key(identifier)):
            type = self.currentSymbolTable.locals[identifier]
            self.checkIdentifierType(identifier,type,node)
        return node.terminals[0]
        
    def visit_array(self,node):
        identifier = node.terminals[0]
        type = self.currentSymbolTable.locals[identifier].strip('[]')
        self.checkIdentifierType(identifier,type,node)
        node.nonTerminals[0].accept(self)
        return node.terminals[0]   
        
    
        