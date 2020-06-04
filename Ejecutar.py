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
        new_error = TokenError(descripcion,line,column)
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
                    new_simbol = Simbolo(sentencia.id, None, result, sentencia.tipo,self.ambiente, sentencia.etiqueta,sentencia.line,sentencia.column)
                    self.ts.actualizar(new_simbol)
        else:

            self.agregarError("La variable {0} invalida".format(sentencia.id),sentencia.line, sentencia.column)

    

    def procesar_operacion(self,operacion):
        if isinstance(operacion,OperacionBinaria): return self.procesar_operacionBinaria(operacion)
        elif isinstance(operacion, OperacionNumero): return self.procesar_valor(operacion)

    def procesar_operacionBinaria(self, operacion):
        if operacion.operacion == OPERACION_NUMERICA.SUMA: return self.procesar_valor(operacion.operadorIzq) + self.procesar_valor(operacion.operadorDer)
        elif operacion.operacion == OPERACION_NUMERICA.RESTA: return self.procesar_valor(operacion.operadorIzq) - self.procesar_valor(operacion.operadorDer)
        elif operacion.operacion == OPERACION_NUMERICA.MULTIPLICACION: return self.procesar_valor(operacion.operadorIzq) * self.procesar_valor(operacion.operadorDer)
        elif operacion.operacion == OPERACION_NUMERICA.DIVISION: return self.procesar_valor(operacion.operadorIzq) / self.procesar_valor(operacion.operadorDer)
        elif operacion.operacion == OPERACION_NUMERICA.MODULAR: return self.procesar_valor(operacion.operadorIzq) % self.procesar_valor(operacion.operadorDer)

    def procesar_valor(self,expresion):
        if isinstance(expresion,OperacionNumero):
            if isinstance(expresion.val,int): return int(expresion.val)
            elif isinstance(expresion.val, float): return float(expresion.val)
            else: 
                self.agregarError("No existe tipo",expresion.line,expresion.column)
                return None
            


