#Compiler for ABS(Angle BracketS) language
import absparser
import absvisitors
import abscodegeneration
import os
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage : abscompiler <sourcefile>"
        sys.exit(1)
    
    source = sys.argv[1]
    output = source.split('.')[0]
    
    f = open(source,'r')
    data = f.read()
    f.close()
    ast = absparser.parse(data)
    
    if absparser.has_errors():
        for error in absparser.errors:
            print error
        sys.exit(1)
    
    #printASTVisitor = absvisitors.PrintASTVisitor();
    #printASTVisitor.visit(ast)
        
    #Symbol table
    symbolTableVisitor = absvisitors.SymbolTableVisitor();
    symbolTableVisitor.visit(ast)
        
    if symbolTableVisitor.has_errors():
        for error in symbolTableVisitor.errors:
            print error
        sys.exit(1)
        
    #print symbol table
    #for method,sTable in absvisitors.symbolTables.iteritems():
        #print method
        #print 'parameters \n %s' % sTable.parameters
        #print 'locals \n %s' % sTable.locals
        
    #type checking
    typeCheckVisitor = absvisitors.TypeCheckVisitor();
    typeCheckVisitor.visit(ast)
    
    if typeCheckVisitor.has_errors():
        for error in typeCheckVisitor.errors:
            print error
        sys.exit(1)
    
    
    
    #Code Generation
    codeGeneratorVisitor = abscodegeneration.ILCodeGenerationVisitor();
    code = codeGeneratorVisitor.visit(ast,output)
    print code
    outputFile = output + '.il'
    f = open(outputFile,'w')
    f.write(code)
    f.close()
    
    #create exe
    result = os.system('ilasm ' + outputFile)
    if result == 1:
        print 'ERROR COMPIILING TO MSIL'
    else:
        if  len(sys.argv) > 2 and sys.argv[2] == '-run':
            os.system(output)
            
