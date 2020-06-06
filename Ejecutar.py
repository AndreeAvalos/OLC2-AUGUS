from Instruccion import *
from Operacion import *
from TablaSimbolos import Simbolo, TablaSimbolos
from Recolectar import TokenError, Recolectar 
import threading
import time
from QCodeEditor import *
class Ejecutor(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name,
                         daemon=daemon)
        self.instrucciones = args[0]
        self.ts = args[1]
        self.ambiente ="global"
        self.lst_errores = args[2]
        self.entrada = args[3]
        self.leido = False
        self.area = args[4]
        self.consola = args[5]


    def run(self):
        temp =  self.area.currentLineColor
        try:      
            #self.area.currentLineColor = QColor("#FF0000")
            self.procesar()
        except:
            print("ERROR DE EJECUCION")
        finally:
            print("__________________________FIN______________________________")
            self.ts.graficarSimbolos()
            self.graficarErrores()
            self.area.currentLineColor = temp

    def setText(self,in_):
        self.entrada= in_
    def setState(self, state):
        self.leido= state

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
        #cursor = self.area.textCursor()
        #cursor.setPosition(0)
        for sentencia in main.sentencias:
            #time.sleep(0.5)
            #cursor.setPosition(0)
            #cursor.movePosition(cursor.Down, cursor.KeepAnchor,  sentencia.line)
            #self.area.setTextCursor(cursor)
            if isinstance(sentencia, Asignacion): self.procesar_asignacion(sentencia)
            elif isinstance(sentencia, Referencia): self.procesar_referencia(sentencia)
            elif isinstance(sentencia, Goto): exit = self.procesar_goto(sentencia)
            elif isinstance(sentencia, Exit): return True
            elif isinstance(sentencia, UnSet): self.procesar_unset(sentencia)
            elif isinstance(sentencia, If_): exit = self.procesar_if(sentencia)
            elif isinstance(sentencia, Print_): self.procesar_print(sentencia)
            #self.ts.graficarSimbolos()
            if exit:
                return True
        
        return False

    def procesar_etiqueta(self, etiqueta):
        self.ambiente = etiqueta.id
        exit = False
        #cursor = self.area.textCursor()
        #cursor.setPosition(0)
        for sentencia in etiqueta.sentencias:
            #time.sleep(0.5)
            #cursor.setPosition(0)
            #cursor.movePosition(cursor.Down, cursor.KeepAnchor,  sentencia.line)
            #self.area.setTextCursor(cursor)
            if isinstance(sentencia, Asignacion): self.procesar_asignacion(sentencia)
            elif isinstance(sentencia, Referencia): self.procesar_referencia(sentencia)
            elif isinstance(sentencia, Goto): exit = self.procesar_goto(sentencia)
            elif isinstance(sentencia, Exit): return True
            elif isinstance(sentencia, If_): exit = self.procesar_if(sentencia)
            elif isinstance(sentencia, Print_): self.procesar_print(sentencia)
            #self.ts.graficarSimbolos()
            
            if exit:
                return True
        
        return False
    
    def procesar_goto(self,sentencia):
        if self.ts.existe(sentencia.id):
            simbol = self.ts.get(sentencia.id)
            if simbol.tipo == Tipo_Simbolo.ETIQUETA:
                ambiente_ant = self.ambiente
                existe = self.procesar_etiqueta(simbol)
                self.ambiente = ambiente_ant
                return existe
            else:
                self.agregarError("{0} no es una etiqueta".format(sentencia.id),sentencia.line, sentencia.column)
        else:
            self.agregarError("{0} no esta declarad".format(sentencia.id),sentencia.line,sentencia.column)

        return False
    
    def procesar_unset(self, sentencia):
        try:
            if self.ts.existe(sentencia.id):
                self.ts.delete(sentencia.id)
            else:
                self.agregarError("{0} no esta declarado".format(sentencia.id),sentencia.line,sentencia.column)     
        except:
            self.agregarError("Error al eliminar",sentencia.line,sentencia.column)

    def procesar_if(self, sentencia):
        operacion = sentencia.operacion
        if isinstance(operacion,OperacionRelacional) or isinstance(operacion,OperacionLogica) or isinstance(operacion, OperacionNumero) or isinstance(operacion,OperacionVariable) or isinstance(operacion,OperacionCopiaVariable):
            result = self.procesar_operacion(operacion)
            operando = False
            
            if result == 1:
                operando = True
            elif result == 0:
                operando = False
            else:
                self.agregarError("{0} valor invalido".format(result))
                return False
            if operando:
                return self.procesar_goto(sentencia.goto)
        elif isinstance(operacion, OperacionUnaria):
            result = self.procesar_operacion(operacion)
            if sentencia.operacion.operacion == OPERACION_LOGICA.NOT:
                operando = False
                if result == 1:
                    operando = True
                elif result == 0:
                    operando = False
                else:
                    self.agregarError("{0} valor invalido".format(result))
                    return False
                if operando:
                    return self.procesar_goto(sentencia.goto)
        else:
            self.agregarError("Operacion no valida",sentencia.line,sentencia.column)
        return False

    def procesar_print(self, sentencia):
        print("ENTRO A PRINT")
        if isinstance(sentencia.val, OperacionCopiaVariable):
            print("ENTRO A VAR")
            result = self.procesar_valor(sentencia.val)
            self.consola.append(str(result))
        else:
            self.consola.append("")
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
        op1 = self.procesar_valor(operacion.operadorIzq)
        op2 = self.procesar_valor(operacion.operadorDer)
        izq = False
        der = False
        if op1 == 1: 
            izq = True
        elif op1 ==0:
            izq = False
        else:
            self.agregarError("{0} invalido para operacion logica".format(op1),operacion.line, operacion.column)
            return 0

        if op2 == 1: 
            der = True
        elif op2 == 0:
            der = False
        else:
            self.agregarError("{0} invalido para operacion logica".format(op2),operacion.line, operacion.column)
            return 0

        if operacion.operacion == OPERACION_LOGICA.AND: 
            return 1 if(izq and der) else 0
        elif operacion.operacion == OPERACION_LOGICA.OR: 
            return 1 if(izq or der) else 0
        elif operacion.operacion == OPERACION_LOGICA.XOR:
            op1 = izq
            op2 = der
            r_notand = not( op1 and op2)
            r_or =   op1 or op2
            r_xor = r_notand and r_or
            return 1 if(r_xor) else 0

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
    def stop(self):
        self.stopped = True

