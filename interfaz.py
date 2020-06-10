from QCodeEditor import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QInputDialog, QLineEdit,QMainWindow
import Gramatica as gramatica 
from Recolectar import Recolectar
from TablaSimbolos import TablaSimbolos
from Ejecutar import Ejecutor
from Debuger import Debuger
#variable global donde se almacerana la instancia, ya se de ejecucion o debug para paserlos los valores de read
in_console = None

class PlainTextEdit(QtWidgets.QTextEdit):
    

    def keyPressEvent(self, event):
        global in_console

        if event.key() == QtCore.Qt.Key_Return:
            salida = self.toPlainText()
            lineas = salida.split("\n")
            #print (lineas[len(lineas)-1])
            in_console.setText(lineas[len(lineas)-1])
            in_console.setState(True)

        super(PlainTextEdit, self).keyPressEvent(event)

        

class Interfaz(QMainWindow):
        

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(735, 611)
        self.mw = MainWindow
        #area para declarar variables globales
        self.pestañas = {}
        self.lineas = True
        self.metodo =None
        self.cambio = False
        self.nombre = ""
        self.gc = False
        self.rutaTemp = ""
        self.debug_mode = False#variable que nos va a indicar si es modo debuger
        self.cambiado = False
        self.analizador_cambiado = False
        #Aqui inician los componentes
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.nuevo = QtWidgets.QPushButton(self.centralwidget)
        self.nuevo.setGeometry(QtCore.QRect(0, 0, 51, 41))
        icon = QtGui.QIcon.fromTheme("new")
        self.nuevo.setIcon(icon)
        self.nuevo.setObjectName("nuevo")
        self.nuevo.clicked.connect(self.agregar_tab)
        #Declaracion de boton abrir
        self.abrir = QtWidgets.QPushButton(self.centralwidget)
        self.abrir.setGeometry(QtCore.QRect(50, 0, 51, 41))
        icon = QtGui.QIcon.fromTheme("new")
        self.abrir.setIcon(icon)
        self.abrir.setObjectName("abrir")
        self.abrir.clicked.connect(self.abrir_archivo)
        #Declaracion de boton save
        self.save = QtWidgets.QPushButton(self.centralwidget)
        self.save.setGeometry(QtCore.QRect(100, 0, 51, 41))
        icon = QtGui.QIcon.fromTheme("new")
        self.save.setIcon(icon)
        self.save.setObjectName("save")
        self.save.clicked.connect(self.guardar)
        #Declaracion de boton save as..
        self.saveas = QtWidgets.QPushButton(self.centralwidget)
        self.saveas.setGeometry(QtCore.QRect(150, 0, 51, 41))
        icon = QtGui.QIcon.fromTheme("new")
        self.saveas.setIcon(icon)
        self.saveas.setObjectName("saveas")
        self.saveas.clicked.connect(self.guardar_como)
        #Declaracion de boton ejecutar
        self.ejecutar = QtWidgets.QPushButton(self.centralwidget)
        self.ejecutar.setGeometry(QtCore.QRect(250, 0, 51, 41))
        icon = QtGui.QIcon.fromTheme("new")
        self.ejecutar.setIcon(icon)
        self.ejecutar.setObjectName("ejecutar")
        self.ejecutar.clicked.connect(self.ejecutar_analisis)
        #Declaracion de boton depurar
        self.depurar = QtWidgets.QPushButton(self.centralwidget)
        self.depurar.setGeometry(QtCore.QRect(300, 0, 51, 41))
        icon = QtGui.QIcon.fromTheme("new")
        self.depurar.setIcon(icon)
        self.depurar.setObjectName("depurar")
        self.depurar.clicked.connect(self.debugear)
        #Declaracion de boton parar
        self.parar = QtWidgets.QPushButton(self.centralwidget)
        self.parar.setGeometry(QtCore.QRect(350, 0, 51, 41))
        icon = QtGui.QIcon.fromTheme("new")
        self.parar.setIcon(icon)
        self.parar.setObjectName("parar")
        self.parar.clicked.connect(self.detenerEjecucion)
        #Declaracion de boton paso a paso
        self.step = QtWidgets.QPushButton(self.centralwidget)
        self.step.setGeometry(QtCore.QRect(400, 0, 51, 41))
        icon = QtGui.QIcon.fromTheme("new")
        self.step.setIcon(icon)
        self.step.setObjectName("step")
        self.step.clicked.connect(self.setStep)
        self.color = QtWidgets.QPushButton(self.centralwidget)
        self.color.setGeometry(QtCore.QRect(530, 0, 51, 41))
        #Declaracion de boton continuar y ejecucion solo
        self.continuar = QtWidgets.QPushButton(self.centralwidget)
        self.continuar.setGeometry(QtCore.QRect(450, 0, 51, 41))
        icon = QtGui.QIcon.fromTheme("new")
        self.continuar.setIcon(icon)
        self.continuar.setObjectName("continuar")
        self.continuar.clicked.connect(self.setContinuar)
        #Tabla para mostrar los simbolos
        self.GTS = QtWidgets.QTableWidget(self.centralwidget)
        self.GTS.setGeometry(QtCore.QRect(500, 80, 221, 461))
        self.GTS.setObjectName("GTS")
        self.GTS.setColumnCount(2)
        self.GTS.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.GTS.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.GTS.setHorizontalHeaderItem(1, item)
        #Boton para cambiar tipo de analizador
        self.cambiaTipoAnalizador = QtWidgets.QPushButton(self.centralwidget)
        self.cambiaTipoAnalizador.setGeometry(QtCore.QRect(500, 50, 221, 23))
        self.cambiaTipoAnalizador.setObjectName("cambiaTipoAnalizador")
        self.cambiaTipoAnalizador.clicked.connect(self.cambiarAnalizador)
        #etiqueta tipo:
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 550, 21, 16))
        self.label.setObjectName("label")
        #etiqueta que cambiara dependiendo el tipo de analizador
        self.etiqueta_analizador = QtWidgets.QLabel(self.centralwidget)
        self.etiqueta_analizador.setGeometry(QtCore.QRect(50, 550, 71, 16))
        self.etiqueta_analizador.setObjectName("etiqueta_analizador")
        #Declaracion No los he usado
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 735, 21))
        icon = QtGui.QIcon.fromTheme("new")
        #Declaracion de boton para cambiar color de ide
        self.color.setIcon(icon)
        self.color.setObjectName("color")
        self.color.clicked.connect(self.changeColor)
        self.lineas = QtWidgets.QPushButton(self.centralwidget)
        self.lineas.setGeometry(QtCore.QRect(580, 0, 51, 41))
        self.lineas.clicked.connect(self.cambiarLineas)
        icon = QtGui.QIcon.fromTheme("new")
        self.lineas.setIcon(icon)
        self.lineas.setObjectName("lineas")
        self.ayuda = QtWidgets.QPushButton(self.centralwidget)
        self.ayuda.setGeometry(QtCore.QRect(680, 0, 51, 41))
        icon = QtGui.QIcon.fromTheme("new")
        self.ayuda.setIcon(icon)
        self.ayuda.setObjectName("ayuda")
        
        self.editores = QtWidgets.QTabWidget(self.centralwidget)
        self.editores.setGeometry(QtCore.QRect(10, 60, 481, 321))
        self.editores.setObjectName("editores")
        self.editores.setTabsClosable(True)
        self.editores.tabCloseRequested.connect(self.closeTab)
        #DECLARA TABS
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        #DECLARA AREA
        self.area = QCodeEditor(DISPLAY_LINE_NUMBERS=True, 
                             HIGHLIGHT_CURRENT_LINE=True,
                             SyntaxHighlighter=XMLHighlighter)
        self.area.setGeometry(QtCore.QRect(0, 0, 471, 291))
        self.area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.area.setPlainText("#OLC2 AUGUS \nmain:\n\t")
        self.area.setObjectName("area")
        self.area.setParent(self.tab)
        self.editores.addTab(self.tab, "")
        #EDITAR EN CONSOLA EXTERNA
        #BOTON INTERNO PARA CAMBIAR DE MODO
        self.consola = PlainTextEdit(self.centralwidget)
        self.consola.setGeometry(QtCore.QRect(10, 390, 481, 151))


        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 255, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 255, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.consola.setPalette(palette)
        self.consola.setObjectName("consola")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 735, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuProject = QtWidgets.QMenu(self.menubar)
        self.menuProject.setObjectName("menuProject")
        self.menuedit = QtWidgets.QMenu(self.menubar)
        self.menuedit.setObjectName("menuedit")
        self.menuProgram = QtWidgets.QMenu(self.menubar)
        self.menuProgram.setObjectName("menuProgram")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuProject.menuAction())
        self.menubar.addAction(self.menuedit.menuAction())
        self.menubar.addAction(self.menuProgram.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.editores.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def cambiarAnalizador(self):
        if self.analizador_cambiado:
            self.etiqueta_analizador.setText("Ascendente")
            self.analizador_cambiado = False
        else:
            self.etiqueta_analizador.setText("Descendente")
            self.analizador_cambiado = True
        

    def setStep(self):
        in_console.step = True
    def setContinuar(self):
        in_console.continuar = True
        in_console.step = True
    
    def detenerEjecucion(self):
        in_console.stop()
    
    def debugear(self):
        self.debug_mode =True
        self.ejecutar_analisis()
        self.debug_mode =False

    def ejecutar_analisis(self):

        self.consola.setText("****** Preparando Analisis ******")
        
        indextab = self.editores.tabText(self.editores.currentIndex())
        self.consola.setText("Archivo a analizar: "+indextab)
        tab = self.editores.widget(self.editores.currentIndex())
        items = tab.children()
        codigo = items[0].toPlainText()
        ast = None
        analisis_semantico = False
        print("___________INICIA PROCESO DE ANALISIS LEXICO Y SINTACTICO_______________")
        try:
            gramatica.lst_errores=[]
            ast = gramatica.parse(codigo)
            gramatica.construirAST(ast.nodo)
        except:
            self.consola.append("/\\/\\/\\/\\/\\ERROR DE LEXICO, SINTACTICO/\\/\\/\\/\\")
            self.consola.append("REVISAR REPORTE DE ERRORES")
        finally:
            gramatica.graficarErrores()
        ts = TablaSimbolos()
        lst = []
        global in_console
        if self.debug_mode:
            in_console = Debuger(args=(ast.instruccion if (ast!=None) else ast,ts,lst,"",items[0],self.consola,self.GTS),daemon=False)
        else:
            in_console = Ejecutor(args=(ast.instruccion if (ast!=None) else ast,ts,lst,"",items[0],self.consola,self.GTS),daemon=False)
        if ast!=None:
            try:
                print("___________INICIA PROCESO DE ANALISIS SEMANTICO_______________")
                recolector = Recolectar(ast.instruccion,ts, lst)
                print("******FIN CONSTRUCTOR**********")
                recolector.procesar()
                recolector.getErrores()
                print("******FIN RECOLECCION*******")
                print("********** FIN DE CONSTRUCTOR ********")
                in_console.start()
            except:
                self.consola.append("/\\/\\/\\/\\/\\ERROR DE EJECUCION/\\/\\/\\/\\")
                self.consola.append("REVISAR REPORTE DE ERRORES")
        ts.graficarSimbolos() 

        


    def agregar_tab(self):
        text, okPressed = QInputDialog.getText(self.centralwidget, "Nuevo archivo","Nombre:", QLineEdit.Normal, "")
        if okPressed and text != '':

            tab = QtWidgets.QWidget()
            area = QCodeEditor(DISPLAY_LINE_NUMBERS=True, 
                                HIGHLIGHT_CURRENT_LINE=True,
                                SyntaxHighlighter=XMLHighlighter)
            area.setGeometry(QtCore.QRect(0, 0, 471, 291))
            area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
            area.setPlainText("#OLC2 AUGUS \nmain:\n\t")
            area.setObjectName("area")
            area.setParent(tab)
            self.editores.addTab(tab, text+".ags")

    def guardar(self):
        indextab = self.editores.tabText(self.editores.currentIndex())
        if indextab.split(".")[0] in self.pestañas:
            ruta = self.pestañas[indextab.split(".")[0]]
            trozos = ruta.split("/")
            name = indextab
            try:
                file = open(ruta,"w")
                tab = self.editores.widget(self.editores.currentIndex())
                items = tab.children()
                codigo = items[0].toPlainText()
                file.write(codigo)
            except:
                em = Qt.QErrorMessage(self.main_window)
                em.showMessage("No fue posible guardar {0}".format(name))
            finally:
                file.close()
        else:
            self.gc = True
            self.nombre = indextab
            self.guardar_como()
            self.pestañas[self.nombre]=self.rutaTemp
            self.nombre = ""
            self.gc = False

    def guardar_como(self):
        
        if not self.gc:
            self.nombre, okPressed = QInputDialog.getText(self.centralwidget, "Nuevo archivo","Nombre:", QLineEdit.Normal, "")
        carpeta = QtWidgets.QFileDialog().getExistingDirectory(self.centralwidget, "Seleccione carpeta")
        tname = self.nombre.split(".")
        name = tname[0]
        ruta = "{0}/{1}.ags".format(carpeta,name)
        self.nombre=name
        self.rutaTemp = ruta
        try:
            file = open(ruta,"w+")
            tab = self.editores.widget(self.editores.currentIndex())
            items = tab.children()
            codigo = items[0].toPlainText()
            file.write(codigo)
        except:
            em = Qt.QErrorMessage(self.main_window)
            em.showMessage("No fue posible guardar {0}".format(name))
        finally:
            file.close()
        
    
    def abrir_archivo(self):
        try:
            dialog = QtWidgets.QFileDialog().getOpenFileName(None,' Open document',r"C:\Users\\","All Files (*)")
            ruta = dialog[0]
            trozos = ruta.split("/")
            name = trozos[len(trozos)-1]
            self.pestañas[name] = ruta
            file = open(ruta,'r')
            codigo = file.read()
            tab = QtWidgets.QWidget()
            area = QCodeEditor(DISPLAY_LINE_NUMBERS=True, 
                                HIGHLIGHT_CURRENT_LINE=True,
                                SyntaxHighlighter=XMLHighlighter)
            area.setGeometry(QtCore.QRect(0, 0, 471, 291))
            area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
            area.setPlainText(codigo)
            area.setObjectName("area")
            area.setParent(tab)
            self.editores.addTab(tab, name)
        except:
            em = Qt.QErrorMessage(self.main_window)
            em.showMessage("Error al abrir {0}".format(name))
        finally:
            file.close()

    def cambiarLineas(self):
        if self.lineas: self.lineas =False
        else: self.lineas = True

        indextab = self.editores.tabText(self.editores.currentIndex())
        tab = self.editores.widget(self.editores.currentIndex())
        items = tab.children()
        tab = QtWidgets.QWidget()
        area = items[0]
        cod = items[0].toPlainText()
        area = QCodeEditor(DISPLAY_LINE_NUMBERS=self.lineas, 
                             HIGHLIGHT_CURRENT_LINE=True,
                             SyntaxHighlighter=XMLHighlighter)
        area.setGeometry(QtCore.QRect(0, 0, 471, 291))
        area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        area.setPlainText(cod)
        area.setObjectName("area")
        area.setParent(tab)
        self.editores.removeTab(self.editores.currentIndex())
        self.editores.addTab(tab, indextab)
    
    def changeColor(self):
        p = self.mw.palette()
        if self.cambiado:
            p.setColor(self.mw.backgroundRole(), Qt.white)
            self.cambiado=False
        else:
            p.setColor(self.mw.backgroundRole(), Qt.black)
            self.cambiado=True
        self.mw.setPalette(p)
        

    def closeTab(self, index):
        tab = self.editores.widget(index)
        name = self.editores.tabText(self.editores.currentIndex())
        print(name)
        tab.deleteLater()
        self.editores.removeTab(index)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Augus"))
        self.nuevo.setText(_translate("MainWindow", "Nuevo"))
        self.abrir.setText(_translate("MainWindow", "Abrir"))
        self.save.setText(_translate("MainWindow", "Save"))
        self.saveas.setText(_translate("MainWindow", "Save as."))
        self.ejecutar.setText(_translate("MainWindow", "Ejecutar"))
        self.depurar.setText(_translate("MainWindow", "Depurar"))
        self.parar.setText(_translate("MainWindow", "Parar"))
        self.step.setText(_translate("MainWindow", "-->"))
        self.color.setText(_translate("MainWindow", "Color"))
        self.lineas.setText(_translate("MainWindow", "Lineas"))
        self.ayuda.setText(_translate("MainWindow", "(?)"))
        self.editores.setTabText(self.editores.indexOf(self.tab), _translate("MainWindow", "main.ags"))
        self.consola.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\';\"><br /></p></body></html>"))
        self.continuar.setText(_translate("MainWindow", "|>"))
        self.cambiaTipoAnalizador.setText(_translate("MainWindow", "Cambiar Tipo"))
        self.label.setText(_translate("MainWindow", "Tipo:"))
        self.etiqueta_analizador.setText(_translate("MainWindow", "Ascendente"))
        item = self.GTS.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Variable"))
        item = self.GTS.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Valor"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuProject.setTitle(_translate("MainWindow", "Project"))
        self.menuedit.setTitle(_translate("MainWindow", "Edit"))
        self.menuProgram.setTitle(_translate("MainWindow", "Program"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))

        format = self.area.document().rootFrame().frameFormat()
        format.setBottomMargin(10)
        self.area.document().rootFrame().setFrameFormat(format)
