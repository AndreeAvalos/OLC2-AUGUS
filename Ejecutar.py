from Instruccion import *
from Operacion import *
from TablaSimbolos import Simbolo, TablaSimbolos
from Recolectar import TokenError, Recolectar 


class Ejecutor:
    def __init__(self, instrucciones, ts, lst):
        self.instrucciones = instrucciones
        self.ts = ts
        self.ambiente ="global"
        self.lst_errores = lst


    def agregarError(self,descripcion,line,column):
        new_error = TokenError("Semantico",descripcion,line,column)
        self.lst_errores.append(new_error)

    def graficarErrores(self):
        try:
            file = open("ESemanticos.dot", "w")
            file.write("digraph tablaErrores{\n")
            file.write("graph [ratio=fill];node [label=\"\\N\", fontsize=15, shape=plaintext];\n")
            file.write("graph [bb=\"0,0,352,154\"];\n")
            file.write("arset [label=<")
            file.write("<TABLE ALIGN=\"LEFT\">\n")
            file.write("<TR><TD>TIPO</TD><TD>DESCRIPCION</TD><TD>LINEA</TD><TD>COLUMNA</TD></TR>\n")
            for token in self.lst_errores:
                file.write("<TR>")
                file.write("<TD>")
                file.write(token.tipo)
                file.write("</TD>")
                file.write("<TD>")
                file.write(token.descripcion)
                file.write("</TD>")
                file.write("<TD>")
                file.write(str(token.line))
                file.write("</TD>")
                file.write("<TD>")
                file.write(str(token.column))
                file.write("</TD>")
                file.write("</TR>\n")
            file.write("</TABLE>")
            file.write("\n>, ];\n")
            file.write("}")
        except:
            print("ERROR AL ESCRIBIR TABLA")
        finally:
            file.close()
            self.ts.cmd("dot -Tpng ESemanticos.dot -o ESemanticos.png")

    def procesar(self):
        encontro = False
        exit = False
        for instruccion in self.instrucciones:
            if isinstance(instruccion, Main): encontro = True
            if encontro:
                if isinstance(instruccion,Main): 
                    exit = self.procesar_main(instruccion)
                elif isinstance(instruccion, Etiqueta):
                    exit = self.procesar_etiqueta(instruccion)

                if exit:
                    return

    def procesar_main(self,main):
        self.ambiente = "main"
        exit = False
        for sentencia in main.sentencias:
            if isinstance(sentencia, Asignacion): self.procesar_asignacion(sentencia)
            if isinstance(sentencia, Referencia): self.procesar_referencia(sentencia)
            
            if exit:
                return True
        
        return False

    def procesar_etiqueta(self, etiqueta):
        self.ambiente = etiqueta.id
        exit = False
        for sentencia in etiqueta.sentencias:
            if isinstance(sentencia, Asignacion): self.procesar_asignacion(sentencia)
            
            if exit:
                return True
        
        return False

    def procesar_asignacion(self, sentencia):
        if sentencia.tipo != Tipo_Simbolo.INVALIDO:
            result = self.procesar_operacion(sentencia.valor)
            if result != None:
                if not self.ts.existe(sentencia.id):
                    new_simbol = Simbolo(sentencia.id, None, result, sentencia.tipo,self.ambiente, sentencia.etiqueta,sentencia.line,sentencia.column)
                    self.ts.add(new_simbol)
                else:
                    old_simbol = self.ts.get(sentencia.id)
                    new_simbol = Simbolo(sentencia.id, None, result, sentencia.tipo,old_simbol.ambiente, sentencia.etiqueta,old_simbol.line,old_simbol.column)
                    self.ts.actualizar(new_simbol)
        else:

            self.agregarError("La variable {0} invalida".format(sentencia.id),sentencia.line, sentencia.column)

    def procesar_referencia(self, sentencia):
        print("ENTRO")
        if sentencia.tipo != Tipo_Simbolo.INVALIDO:
            result = self.procesar_valor(sentencia.valor)
            if result != None:
                if not self.ts.existe(sentencia.id):
                    new_simbol = Simbolo(sentencia.id, None, None, sentencia.tipo,self.ambiente, sentencia.etiqueta,sentencia.line,sentencia.column)
                    self.ts.add(new_simbol)
                    self.ts.referenciar(sentencia.id, result.valor)
                else:
                    self.ts.referenciar(sentencia.id, result.valor)
        else:

            self.agregarError("La variable {0} invalida".format(sentencia.id),sentencia.line, sentencia.column)       


    def procesar_operacion(self,operacion):
        if isinstance(operacion,OperacionNumerica): return self.procesar_operacionNumerica(operacion)
        elif isinstance(operacion, OperacionNumero): return self.procesar_valor(operacion)
        elif isinstance(operacion, OperacionCopiaVariable): return self.procesar_valor(operacion)
        elif isinstance(operacion, OperacionLogica): return self.procesar_operacionLogica(operacion)
        elif isinstance(operacion, OperacionUnaria): return self.procesar_operacionUnaria(operacion)
        elif isinstance(operacion,OperacionRelacional): return self.procesar_operacionRelacional(operacion)

    def procesar_operacionNumerica(self, operacion):
        try:
            if operacion.operacion == OPERACION_NUMERICA.SUMA: return self.procesar_valor(operacion.operadorIzq) + self.procesar_valor(operacion.operadorDer)
            elif operacion.operacion == OPERACION_NUMERICA.RESTA: return self.procesar_valor(operacion.operadorIzq) - self.procesar_valor(operacion.operadorDer)
            elif operacion.operacion == OPERACION_NUMERICA.MULTIPLICACION: return self.procesar_valor(operacion.operadorIzq) * self.procesar_valor(operacion.operadorDer)
            elif operacion.operacion == OPERACION_NUMERICA.DIVISION: return self.procesar_valor(operacion.operadorIzq) / self.procesar_valor(operacion.operadorDer)
            elif operacion.operacion == OPERACION_NUMERICA.MODULAR: return self.procesar_valor(operacion.operadorIzq) % self.procesar_valor(operacion.operadorDer)
        except:
            self.agregarError("No es posible operar",operacion.line,operacion.column)

    def procesar_operacionLogica(self, operacion):
        if operacion.operacion == OPERACION_LOGICA.AND: 
            if self.procesar_valor(operacion.operadorIzq) and self.procesar_valor(operacion.operadorDer): return 1  
            else: return 0
        elif operacion.operacion == OPERACION_LOGICA.OR: 
            if self.procesar_valor(operacion.operadorIzq) or self.procesar_valor(operacion.operadorDer): return 1  
            else: return 0
        elif operacion.operacion == OPERACION_LOGICA.XOR:
            op1 = self.procesar_valor(operacion.operadorIzq) 
            op2 = self.procesar_valor(operacion.operadorDer)
            r_notand = not( op1 and op2)
            r_or =   op1 or op2
            r_xor = r_notand and r_or
            if r_xor: return 1
            else: return 0

    def procesar_operacionRelacional(self, operacion):
        try:
            if operacion.operacion == OPERACION_RELACIONAL.IGUAL: return 1 if(self.procesar_valor(operacion.operadorIzq) == self.procesar_valor(operacion.operadorDer)) else 0
            elif operacion.operacion == OPERACION_RELACIONAL.DIFERENTE: return 1 if(self.procesar_valor(operacion.operadorIzq) != self.procesar_valor(operacion.operadorDer)) else 0
            elif operacion.operacion == OPERACION_RELACIONAL.MAYORQUE: return 1 if(self.procesar_valor(operacion.operadorIzq) >= self.procesar_valor(operacion.operadorDer)) else 0
            elif operacion.operacion == OPERACION_RELACIONAL.MENORQUE: return 1 if(self.procesar_valor(operacion.operadorIzq) <= self.procesar_valor(operacion.operadorDer)) else 0
            elif operacion.operacion == OPERACION_RELACIONAL.MAYOR: return 1 if(self.procesar_valor(operacion.operadorIzq) > self.procesar_valor(operacion.operadorDer)) else 0
            elif operacion.operacion == OPERACION_RELACIONAL.MENOR: return 1 if(self.procesar_valor(operacion.operadorIzq) < self.procesar_valor(operacion.operadorDer)) else 0
        except:
            self.agregarError("No es posible operar",operacion.line,operacion.column)

    def procesar_operacionUnaria(self,operacion):
        op1 = self.procesar_valor(operacion.operadorIzq) 
        if operacion.operacion == OPERACION_BIT.NOT:
            return 0
        elif operacion.operacion == OPERACION_LOGICA.NOT:
            if op1==1:
                return 0
            elif op1 == 0:
                return 1
            else:
                self.agregarError("El Numero {0} no puede ser negado".format(op1),operacion.line, operacion.column)
                return 0
        elif operacion.operacion == OPERACION_NUMERICA.RESTA:
            if isinstance(op1, int) or isinstance(op1,float):
                return -1*op1
            else:
                self.agregarError("{0} no es un valor numerico".format(op1),operacion.line,operacion.column)
                return op1

    def procesar_valor(self,expresion):
        if isinstance(expresion,OperacionNumero):
            if isinstance(expresion.val,int): return int(expresion.val)
            elif isinstance(expresion.val, float): return float(expresion.val)
            else: 
                self.agregarError("No existe tipo",expresion.line,expresion.column)
                return None
        elif isinstance(expresion, OperacionVariable):
            if self.ts.existe(expresion.id):
                return self.ts.get(expresion.id)
            else:
                self.agregarError("No existe variable {0}".format(expresion.id),expresion.line,expresion.column)
                return None
        elif isinstance(expresion, OperacionCopiaVariable):
            if self.ts.existe(expresion.id):
                return self.ts.get(expresion.id).valor.get()
            else:
                self.agregarError("No existe variable {0}".format(expresion.id),expresion.line,expresion.column)
                return None


