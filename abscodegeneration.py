import absvisitors
from absvisitors import Visitor

#Visitor used to generate MSIL code.
class ILCodeGenerationVisitor(Visitor):
    
    def __init__(self):
        Visitor.__init__(self)
        self.code = ''
        self.currentType = ''
        self.labelCounter = 0
        self.currentSymbolTable = None
        self.bufferCode = ''
        self.maxStack = 0
        self.ldCall = False
        self.useBuffer = False
       
    #emits il code
    def emit(self,str):
        if (self.useBuffer == False):
            self.code += str + '\n'
        else:
        #if using buffer add emited code to temp. string before
        #making it part of the final src. ie.using self.code
            self.bufferCode += str + '\n'
        self.ldPrevious = False

    
    #Code that loads data on stack. Needed to
    #track what the maxstack size should be.
    def emitLd(self,str):
        #maxstack increases with consecutive loads.
        if self.ldPrevious == True:
            self.currentMax += 1
        else:
            self.currentMax = 1
        if self.currentMax > self.maxStack:
            self.maxStack = self.currentMax
        if (self.useBuffer == False):
            self.code += str + '\n'
        else:
            self.bufferCode += str + '\n'
        self.ldPrevious = True
   
    #increment label values, to ensure uniqueness    
    def nextLabel(self):
        self.labelCounter += 1
        return self.labelCounter
    
    #get IL specific type.
    def getType(self,returnType):
        if returnType == None:
            return 'void'
        elif returnType == 'int':
            return 'int32'
        elif returnType == 'int[]':
            return  'int32[]'
        elif returnType == 'text':
            return 'string'
        elif returnType == 'text[]':
            return 'string[]'
        return returnType
        
    #Generated method mody
    def generateMethodBody(self,node):
        self.bufferCode = ''
        self.useBuffer = True
        self.maxStack = 0
        self.initLocals()
        #add method to code buffer
        node.accept(self)
        self.useBuffer = False
        return self.bufferCode
        
    #First method called
    def visit(self,node,outputName):
        self.emit('.assembly extern mscorlib {}\n')
        self.emit('.assembly %s\n' % outputName)
        self.emit('{')
        self.emit('\t.ver 1:0:0:0')
        self.emit('}')
        self.emit('.module %s.exe\n' % outputName)
        #start node traversal
        node.accept(self)
       
        return self.code 
    
    #Initialize local variables at the beginning of the method.
    def initLocals(self):
        if len(self.currentSymbolTable.locals) > 0:
            i = 0
            locals = '\t.locals init('
            #iterate through locals
            for identifier,type in self.currentSymbolTable.locals.iteritems():
                type = self.getType(type)
                                   
                if i > 0:
                    locals += ',[%d] %s %s' % (i,type,identifier)
                else:
                    locals += '[%d] %s %s' % (i,type,identifier)
                i += 1
            locals += ')'
            self.emit(locals)
        
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
        method = node.terminals[0]
        returnType = node.terminals[1]
        key = '%s' % (method)
        self.currentSymbolTable = absvisitors.symbolTables[key]
        paramList = ''
        #TODO: Gets back parameters in wrong order, must fix
        for id,type in self.currentSymbolTable.parameters.iteritems():
            type = self.getType(type)
            paramList = paramList + '%s %s,' % (type,id)
            
        #remove last comma
        if len(paramList) > 0:
            paramList = paramList.rstrip(',')           
        returnType = self.getType(returnType)
        
        #create method body string, use to determine max stack size
        methodBody = self.generateMethodBody(node.nonTerminals[1])
        self.emit('.method public static %s %s( %s ) cil managed' % (returnType,method,paramList))
        self.emit('{')
        #set maxStack size depending on the method body.
        self.emit('\t.maxstack %d' % self.maxStack)
        self.emit(methodBody)
        self.emit('\tret')
        self.emit('}')
        return
        
    def visit_parameter_list(self,node):
        self.parameterList = ''
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        return
        
    def visit_parameter(self,node):
        self.parameterList = self.parameterList + node.terminals[0] + ','
        self.currentSymbolTable.parameters[node.terminals[1]] = node.terminals[0]
        return
        
    def visit_start(self,node):
        self.currentSymbolTable = absvisitors.symbolTables['start']
               
        #create method body string
        methodBody = self.generateMethodBody(node.nonTerminals[0])
               
        #create method
        self.emit('.method static void main() cil managed')
        self.emit('{')
        self.emit('\t.maxstack %d' % self.maxStack)
        self.emit('\t.entrypoint\n')
        self.emit(methodBody);
        self.emit('\tret')
        self.emit('}')
                   
       
    def visit_statement_list(self,node):
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
       
            
    def visit_assignment_stmt(self,node):
        node.nonTerminals[0].accept(self)
        #stores data on stack
        if self.currentSymbolTable.locals.has_key(node.terminals[1]):
            self.emit('\tstloc %s' % node.terminals[1])
        elif self.currentSymbolTable.parameters.has_key(node.terminals[1]):
            self.emit('\tstarg %s' % node.terminals[1])
            
    def visit_array_define(self,node):
        #evaluate expression
        node.nonTerminals[0].accept(self)
        identifier = node.terminals[0]
        type = self.getType(node.terminals[1])
        #new array
        self.emit('\tnewarr %s' % type)
        self.emit('\tstloc %s' % identifier)
        
    def visit_array_assign(self,node):
        #load local variable
        identifier = node.terminals[0]
        type = self.currentSymbolTable.locals[identifier]
        self.emitLd('\tldloc %s' % identifier)
        #evaluate index expression
        node.nonTerminals[0].accept(self)
        #evaluate expression
        node.nonTerminals[1].accept(self)
        suffix = 'ref'
        if type == 'int[]':
            suffix = 'i4'
                    
        self.emit('\tstelem.%s' % suffix)
    
    def visit_gives_stmt(self,node):
        node.nonTerminals[0].accept(self)
        
        
    def visit_output_stmt(self,node):
        node.nonTerminals[0].accept(self)
        self.emit('\tcall void [mscorlib]System.Console::Write(%s)'% (self.currentType))
        
    def visit_input_stmt(self,node):
        self.emit('\tcall string [mscorlib]System.Console::ReadLine()')
        if len(node.terminals) == 2:
            identifier = node.terminals[1]
        else:
            identifier = node.terminals[0]
            
        type = self.currentSymbolTable.locals[identifier]
        if type == 'int':
            self.emit('\tcall int32 [mscorlib]System.Int32::Parse(string)')
        self.emit('\tstloc %s' % identifier)
    
    def visit_if_stmt(self,node):
        #handle equality node
        node.nonTerminals[0].accept(self)
        trueLabel = self.nextLabel()
        falseLabel = self.nextLabel()
        exitBlockLabel = self.nextLabel()
        if self.currentType == 'int32':
            self.emitLd('\tldc.i4.0')
            self.emitLd('\tcgt')
        self.emit('\tbrtrue.s LABEL%d' % trueLabel)
        self.emit('\tbr LABEL%d' % falseLabel)
        self.emit('\tLABEL%d:' % trueLabel)
        node.nonTerminals[1].accept(self)
        self.emit('\tbr LABEL%d' % exitBlockLabel)
        self.emit('\tLABEL%d:' % falseLabel)
        #check for else
        if node.nonTerminals[2] != None:
            node.nonTerminals[2].accept(self)
        self.emit('\tbr LABEL%d' % exitBlockLabel)
        self.emit('\tLABEL%d:' % exitBlockLabel)
        
        
            
    def visit_else_stmt(self,node):
        node.nonTerminals[0].accept(self)
        
    def visit_loop_stmt(self,node):
        startLabel = self.nextLabel()
        exitLabel = self.nextLabel()
        self.emit('\tLABEL%d:' % startLabel)
        node.nonTerminals[0].accept(self)
        self.emitLd('\tldc.i4.0')
        self.emitLd('\tbeq LABEL%d' % exitLabel)
        node.nonTerminals[1].accept(self)
        self.emit('\tbr LABEL%d' % startLabel)        
        self.emit('\tLABEL%d:' % exitLabel)       
        
        
        
    def visit_equality(self,node):
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
        equality = node.terminals[0]
        label = self.nextLabel()
        breakLabel = self.nextLabel()
        if equality == 'is<':
            self.emitLd('\tclt');
        elif equality == 'is<=':
            self.emitLd('\tble LABEL%d' % label)
            self.emitLd('\tldc.i4 0');
            self.emit('\tbr LABEL%d' % breakLabel)
            self.emit('\tLABEL%d:' % label)
            self.emitLd('\tldc.i4 1');
            self.emit('\tLABEL%d:' % breakLabel)
            
        elif equality == 'is>':
            self.emitLd('\tcgt')
        elif equality == 'is>=':
            self.emitLd('\tbgt LABEL%d' % label)
            self.emitLd('\tldc.i4 0');
            self.emit('\tbr LABEL%d' % breakLabel)
            self.emit('\tLABEL%d:' % label)
            self.emitLd('\tldc.i4 1');
            self.emit('\tLABEL%d:' % breakLabel)
        elif equality == 'is=':
            if self.currentType == 'int32':
                self.emitLd('\tceq');
            elif self.currentType == 'string':
                self.emitLd('\tcall bool [mscorlib]System.String::op_Equality(string,string)')
        elif equality == 'isnot=':
            if self.currentType == 'int32':
                self.emitLd('\tbne.un LABEL%d' % label)
                self.emitLd('\tldc.i4 0');
                self.emit('\tbr LABEL%d' % breakLabel)
                self.emit('\tLABEL%d:' % label)
                self.emitLd('\tldc.i4 1');
                self.emit('\tLABEL%d:' % breakLabel)
            elif self.currentType == 'string':
                self.emitLd('\tcall bool [mscorlib]System.String::op_Inequality(string,string)')
        elif equality == 'and':
            self.emitLd('\tand')
        elif equality == 'or':
            self.emitLd('\tor')
        
        
   
    def visit_binop(self,node):
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)
       
        if node.terminals[0] == '+':
            self.emit('\tadd')
        elif node.terminals[0] == '-':
            self.emit('\tsub')
        elif node.terminals[0] == '*':
            self.emit('\tmul')
        elif node.terminals[0] == '/':
            self.emit('\tdiv')
        
        
       
         
    def visit_integer(self,node):
        self.emitLd('\tldc.i4 %d' % node.terminals[0])
        self.currentType = 'int32'
        
    def visit_text(self,node):
        self.emitLd('\tldstr "%s"' % node.terminals[0])  
        self.currentType = 'string'     
    
             
    def visit_identifier(self,node):
        
        if self.currentSymbolTable.locals.has_key(node.terminals[0]):
            self.emitLd('\tldloc %s' % node.terminals[0])
            type = self.currentSymbolTable.locals[node.terminals[0]]
        elif self.currentSymbolTable.parameters.has_key(node.terminals[0]):
            self.emitLd('\tldarg %s' % node.terminals[0])
            type = self.currentSymbolTable.parameters[node.terminals[0]]
        self.currentType = self.getType(type)    
        
            
    def visit_array(self,node):
         #load local variable
        identifier = node.terminals[0]
        if self.currentSymbolTable.locals.has_key(identifier):
            self.emit('\tldloc %s' % identifier)
            type = self.currentSymbolTable.locals[identifier]
        elif self.currentSymbolTable.parameters.has_key(identifier):
            self.emit('\tldarg %s' % identifier)
            type = self.currentSymbolTable.parameters[identifier]

        #evaluate index expression
        node.nonTerminals[0].accept(self)
        #load elements
        suffix = 'ref'
        if type == 'int[]':
            suffix = 'i4'
            self.currentType = 'int32'
        elif type == 'text[]':
            self.currentType = 'text'
        self.emitLd('\tldelem.%s' % suffix)
        
      
    def visit_method_call(self,node):
        #evaluate expression list
        if node.nonTerminals[0] != None:
                node.nonTerminals[0].accept(self)
        #call method
        method = node.terminals[0]
        methodSymbolTable = absvisitors.symbolTables[method]
        returnType = self.getType(methodSymbolTable.returnType)
        paramList = ''
        
        for id,type in methodSymbolTable.parameters.iteritems():
            paramList = paramList + self.getType(type) + ','
        #remove last comma
        if len(paramList) > 0:
                paramList = paramList.rstrip(',')
        self.emit('\tcall %s %s(%s)' % (returnType,method,paramList))
        
        
        
    def visit_expression_list(self,node):
        node.nonTerminals[0].accept(self)
        node.nonTerminals[1].accept(self)