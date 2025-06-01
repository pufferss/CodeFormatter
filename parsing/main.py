import pprint
import re

def LoadFile(FileName):
    with open(FileName, "r") as f:
        return f.read()

class CPP:
    def __init__(self, Data):
        self.Data = Data
        self.CleanedData = self.SimplifyData(Data)
        self.Statements = self.GetStatements(self.CleanedData)

    def SimplifyData(self, Data):
        CleanedData = ""
        CleanedData = re.sub(r"//.*", " ", Data)
        CleanedData = re.sub(r"\".*\"", "\"\"", CleanedData)
        CleanedData = re.sub(r"\'.*\'", "\'\'", CleanedData)
        CleanedData = re.sub(r"#.*", "", CleanedData)
        CleanedData = re.sub(r"\n+", " ", CleanedData)
        CleanedData = re.sub(r" +", " ", CleanedData)
        CleanedData = re.sub(r"\) *\{", "){", CleanedData)
        CleanedData = re.sub(r" \{", "{", CleanedData)
        CleanedData = re.sub(r" *= *", "=", CleanedData)
        CleanedData = re.sub(r"; ", ";", CleanedData)
        return CleanedData

    def GetStatements(self, CleanedData):
        Statements = ""
        for line in CleanedData.split(";"):
            Statements += line + ";\n"
        return Statements

    def GetFunctions(self):
        L = re.findall(r"[a-zA-Z_][a-zA-Z0-9_&*<>:]* [a-zA-Z_][a-zA-Z0-9_]+\(.*\)\{", self.Statements)
        L = [re.sub(r"\(.*", "", x.split()[1]) for x in L]  # comment to keep prototype etc
        #L = [x for x in L if x != "main"]
        return list(set(L))

    def GetClasses(self):
        return [x.split()[1][0:-1] for x in re.findall(r"class [a-zA-Z_][a-zA-Z0-9_]+\{", self.Statements)]

    def GetStructs(self):
        return [x.split()[1][0:-1] for x in re.findall(r"struct [a-zA-Z_][a-zA-Z0-9_]+\{", self.Statements)]

    def GetVariables(self):
        L = re.findall(r"[a-zA-Z_][a-zA-Z0-9_&*<>:]* [a-zA-Z_][a-zA-Z0-9_]*[;,=)\[]", self.Statements)
        L = [x for x in L if ("return" not in x)]
        L = [v[0:-1] if (v[-1] in [";", ",", "=", "[", ")"]) else v for v in L]
        L = [x.split()[1] for x in L]    # comment to keep type etc
        return list(set(L))

    def GetAllIdentifiers(self):
        return self.GetClasses() + self.GetStructs() + self.GetFunctions() + self.GetVariables()

    def PrintAnalyzedFileData(self):
        Classes = self.GetClasses()
        print("Found", len(Classes), "classes")
        for Class in Classes:
            print("  -", Class )

        Structs = self.GetStructs()
        print("Found", len(Structs), "structs")
        for Struct in Structs:
            print("  -", Struct )
        
        Functions = self.GetFunctions()
        print("Found", len(Functions), "functions")
        for Func in Functions:
            print("  -", Func )

        Variables = self.GetVariables()
        print("Found", len(Variables), "variables")
        for Var in Variables:
            print("  -", Var )

    def GetNamingInfo(self):
        dico = {
            "lowercase" : [],
            "camelCase" : [],
            "snake_case" : [],
            "PascalCase" : [],
            "Unknown" : []
        }

        for ident in self.GetAllIdentifiers():
            if (re.match(r"[a-z][a-z0-9]*_[a-z0-9_]*", ident)):
                dico["snake_case"].append(ident)
            elif (re.match(r"[A-Z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*", ident)): 
                dico["PascalCase"].append(ident)
            elif (re.match(r"[a-z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*", ident)): 
                dico["camelCase"].append(ident)
            elif (re.match(r"[a-z][a-z0-9]*", ident)): 
                dico["lowercase"].append(ident)
            else:
                dico["Unknown"].append(ident)

        return dico

    def GetIndentationInfo(self):
        dico = {
            "Allman" : len(re.findall(r"^ *\{", self.Data, re.MULTILINE)),
            "K&R" : len(re.findall(r"\) *\{\n", self.Data)),
        }
        return dico

    def GetConventionInfo(self):
        return {
            "Naming conventions" : self.GetNamingInfo(),
            "Indentation style" : self.GetIndentationInfo()
        }

class PY:
    def __init__(self, Data):
        self.Data = Data
        self.CleanedData = self.SimplifyData(Data)

    def SimplifyData(self, Data):
        CleanedData = re.sub(r"#.*", "", Data)
        CleanedData = re.sub(r"^\n", "", CleanedData, flags=re.MULTILINE)
        CleanedData = re.sub(r"^ +", "", CleanedData, flags=re.MULTILINE)

        return CleanedData
    
    def GetClasses(self):
        return re.findall(r"class (.*):", self.CleanedData)
        
    def GetFunctions(self):
        functions = re.findall(r"def .*\(.*\)", self.CleanedData)
        functions = [re.sub(r"\(.*", "", f.split()[1]) for f in functions]

        functions.remove('main')
        return functions
    
    def GetVariables(self):
        vars = re.findall(r"(.*) =[^=]", self.CleanedData)
        vars = [re.sub(r".*\.", "", v) for v in vars]

        for d in re.findall(r"def .*\((.+)\)", self.CleanedData):
            for x in d.split(","):
                vars.append(x.strip())

        vars = list(set(vars))
        vars.remove('self')
        return vars

    def GetAllIdentifiers(self):
        return self.GetClasses() + self.GetFunctions() + self.GetVariables()

    def PrintAnalyzedFileData(self):
        functions = self.GetFunctions()
        print("Found", len(functions), "functions")
        for f in functions:
            print("  -", f)
            
        vars = self.GetVariables()
        print("Found", len(vars), "variables")
        for v in vars:
            print("  -", v)
        
        classes = self.GetClasses()
        print("Found", len(classes), "classes")
        for c in classes:
            print("  -", c)

    def GetNamingInfo(self):
        dico = {
            "lowercase" : [],
            "camelCase" : [],
            "snake_case" : [],
            "PascalCase" : [],
            "Unknown" : []
        }

        for ident in self.GetAllIdentifiers():
            if (re.match(r"[a-z][a-z0-9]*_[a-z0-9_]*", ident)) or (re.match(r"_[a-z0-9]*", ident)):
                dico["snake_case"].append(ident)
            elif (re.match(r"[A-Z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*", ident)) or (re.match(r"[A-Z][a-z0-9]*", ident)): 
                dico["PascalCase"].append(ident)
            elif (re.match(r"[a-z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*", ident)): 
                dico["camelCase"].append(ident)
            elif (re.match(r"[a-z][a-z0-9]*", ident)): 
                dico["lowercase"].append(ident)
            else:
                dico["Unknown"].append(ident)

        return dico
    
    def GetIndentationInfo(self):
        dico = {
            "4_spaces" : len(re.findall(r"^    [a-zA-Z_][a-zA-Z0-9_]*", self.Data, re.MULTILINE)),
            "tabs" : len(re.findall(r"^\t[a-zA-Z_][a-zA-Z0-9_]*", self.Data, re.MULTILINE)),
        }
        return dico

    def GetConventionInfo(self):
        return {
            "Naming conventions" : self.GetNamingInfo(),
            "Indentation style" : self.GetIndentationInfo()
        }

class JS:
    def __init__(self, Data):
        self.Data = Data
        self.CleanedData = self.SimplifyData(Data)
        self.Statements = self.GetStatements(self.CleanedData)

    def SimplifyData(self, Data):
        CleanedData = ""
        CleanedData = re.sub(r"//.*", " ", Data)
        CleanedData = re.sub(r"\".*\"", "\"\"", CleanedData)
        CleanedData = re.sub(r"\'.*\'", "\'\'", CleanedData)
        CleanedData = re.sub(r"#.*", "", CleanedData)
        CleanedData = re.sub(r"\n+", " ", CleanedData)
        CleanedData = re.sub(r" +", " ", CleanedData)
        CleanedData = re.sub(r"\) *\{", "){", CleanedData)
        CleanedData = re.sub(r" \{", "{", CleanedData)
        CleanedData = re.sub(r" *= *", "=", CleanedData)
        CleanedData = re.sub(r"; ", ";", CleanedData)
        return CleanedData

    def GetStatements(self, CleanedData):
        Statements = ""
        for line in CleanedData.split(";"):
            Statements += line + ";\n"
        return Statements
    
    def GetFunctions(self):
        Functions = re.findall(r"(?:function)? ([a-zA-Z_][a-zA-Z0-a]*)\(.*\) *{", self.Statements)
        Functions += re.findall(r"([a-zA-Z_][a-zA-Z0-9_]*) *= *\(\) *=> *{", self.Statements)

        Functions = [f for f in Functions if f != 'constructor']

        return Functions
    
    def GetClasses(self):
        return re.findall(r"class ([a-zA-Z_][a-zA-Z0-9_]*)", self.Statements)
    
    def GetVariables(self):
        vars = re.findall(r"\b(?:let|var|const)\b\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?!\(\s*\)\s*=>).+", self.Statements)
        vars += re.findall(r"this\.(?:.*\.)*(.*) *=", self.Statements)
        params = re.findall(r"(?:function\s+\w+|\bconstructor\b|\b\w+\s*\()\s*\(([^)|(]+)\)", self.Statements)

        for p in params:
            for x in p.split(","):
                vars.append(x.strip())

        return list(set(vars))
    
    def GetAllIdentifiers(self):
        return self.GetClasses() + self.GetFunctions() + self.GetVariables()

    def PrintAnalyzedFileData(self):
        functions = self.GetFunctions()
        print("Found", len(functions), "functions")
        for f in functions:
            print("  -", f)
            
        vars = self.GetVariables()
        print("Found", len(vars), "variables")
        for v in vars:
            print("  -", v)
        
        classes = self.GetClasses()
        print("Found", len(classes), "classes")
        for c in classes:
            print("  -", c)

    def GetNamingInfo(self):
        dico = {
            "lowercase" : [],
            "camelCase" : [],
            "snake_case" : [],
            "PascalCase" : [],
            "Unknown" : []
        }

        for ident in self.GetAllIdentifiers():
            if (re.match(r"[a-z][a-z0-9]*_[a-z0-9_]*", ident)) or (re.match(r"_[a-z0-9]*", ident)):
                dico["snake_case"].append(ident)
            elif (re.match(r"[A-Z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*", ident)) or (re.match(r"[A-Z][a-z0-9]*", ident)): 
                dico["PascalCase"].append(ident)
            elif (re.match(r"[a-z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*", ident)): 
                dico["camelCase"].append(ident)
            elif (re.match(r"[a-z][a-z0-9]*", ident)): 
                dico["lowercase"].append(ident)
            else:
                dico["Unknown"].append(ident)

        return dico
    
    def GetIndentationInfo(self):
        dico = {
            "4_spaces" : len(re.findall(r"^    [a-zA-Z_][a-zA-Z0-9_]*", self.Data, re.MULTILINE)),
            "tabs" : len(re.findall(r"^\t[a-zA-Z_][a-zA-Z0-9_]*", self.Data, re.MULTILINE)),
        }
        return dico

    def GetConventionInfo(self):
        return {
            "Naming conventions" : self.GetNamingInfo(),
            "Indentation style" : self.GetIndentationInfo()
        }

if __name__ == '__main__':
    print("\nC++ part:\n")
    cpp = CPP(LoadFile("example.cpp"))
    cpp.PrintAnalyzedFileData()
    pprint.pprint(cpp.GetConventionInfo())

    print("\nPython Part:\n")
    py = PY(LoadFile("example.py"))
    py.PrintAnalyzedFileData()
    pprint.pprint(py.GetConventionInfo())

    print("\nJS Part:\n")
    js = JS(LoadFile("example.js"))
    print("-------------------")
    js.PrintAnalyzedFileData()
    pprint.pprint(js.GetConventionInfo())


# c pr debug le parsin cpp bref
#with open("test", "w") as f:
#    for l in cpp.CleanedData.split(";"):
#        f.write(l + ";\n")
    #f.write(cpp.CleanedData)