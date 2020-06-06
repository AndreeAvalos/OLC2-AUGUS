from QCodeEditor import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QInputDialog, QLineEdit,QMainWindow
import Gramatica as gramatica 
from Recolectar import Recolectar
from TablaSimbolos import TablaSimbolos
from Ejecutar import Ejecutor
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

        

class Ui_MainWindow(object):
        

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(735, 600)
        self.lineas = True
        self.metodo =None
        self.cambio = False
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.nuevo = QtWidgets.QPushButton(self.centralwidget)
        self.nuevo.setGeometry(QtCore.QRect(0, 0, 51, 41))
        icon = QtGui.QIcon.fromTheme("new")
        self.nuevo.setIcon(icon)
        self.nuevo.setObjectName("nuevo")
        self.nuevo.clicked.connect(self.agregar_tab)

        self.abrir = QtWidgets.QPushButton(self.centralwidget)
        self.abrir.setGeometry(QtCore.QRect(50, 0, 51, 41))
        icon = QtGui.QIcon.fromTheme("new")
        self.abrir.setIcon(icon)
        self.abrir.setObjectName("abrir")
        self.save = QtWidgets.QPushButton(self.centralwidget)
        self.save.setGeometry(QtCore.QRect(100, 0, 51, 41))
        icon = QtGui.QIcon.fromTheme("new")
        self.save.setIcon(icon)
        self.save.setObjectName("save")
        self.saveas = QtWidgets.QPushButton(self.centralwidget)
        self.saveas.setGeometry(QtCore.QRect(150, 0, 51, 41))
        icon = QtGui.QIcon.fromTheme("new")
        self.saveas.setIcon(icon)
        self.saveas.setObjectName("saveas")
        self.ejecutar = QtWidgets.QPushButton(self.centralwidget)
        self.ejecutar.setGeometry(QtCore.QRect(250, 0, 51, 41))
        icon = QtGui.QIcon.fromTheme("new")
        self.ejecutar.setIcon(icon)
        self.ejecutar.setObjectName("ejecutar")

        self.ejecutar.clicked.connect(self.ejecutar_analisis)

        self.depurar = QtWidgets.QPushButton(self.centralwidget)
        self.depurar.setGeometry(QtCore.QRect(300, 0, 51, 41))
        icon = QtGui.QIcon.fromTheme("new")
        self.depurar.setIcon(icon)
        self.depurar.setObjectName("depurar")
        self.parar = QtWidgets.QPushButton(self.centralwidget)
        self.parar.setGeometry(QtCore.QRect(350, 0, 51, 41))
        icon = QtGui.QIcon.fromTheme("new")
        self.parar.setIcon(icon)
        self.parar.setObjectName("parar")
        self.step = QtWidgets.QPushButton(self.centralwidget)
        self.step.setGeometry(QtCore.QRect(400, 0, 51, 41))
        icon = QtGui.QIcon.fromTheme("new")
        self.step.setIcon(icon)
        self.step.setObjectName("step")
        self.color = QtWidgets.QPushButton(self.centralwidget)
        self.color.setGeometry(QtCore.QRect(530, 0, 51, 41))
        self.continuar = QtWidgets.QPushButton(self.centralwidget)
        self.continuar.setGeometry(QtCore.QRect(450, 0, 51, 41))
        icon = QtGui.QIcon.fromTheme("new")
        self.continuar.setIcon(icon)
        self.continuar.setObjectName("continuar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 735, 21))
        icon = QtGui.QIcon.fromTheme("new")
        self.color.setIcon(icon)
        self.color.setObjectName("color")
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

    def ejecutar_analisis(self):

        self.consola.setText("****** Preparando Analisis ******")
        indextab = self.editores.tabText(self.editores.currentIndex())
        self.consola.setText("Archivo a analizar: "+indextab)
        tab = self.editores.widget(self.editores.currentIndex())
        items = self.tab.children()
        codigo = items[0].toPlainText()
        #print(codigo)
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
        
        in_console = Ejecutor(args=(ast.instruccion if (ast!=None) else ast,ts,lst,"",items[0],self.consola),daemon=False)
        if ast!=None:
            print("___________INICIA PROCESO DE ANALISIS SEMANTICO_______________")
            try:
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
        #in_console.lst_errores = in_console.lst_errores+ gramatica.lst_errores
        #in_console.graficarErrores()
        ts.graficarSimbolos()
        #in_console.stop()
                
        
        
        
        

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

    def closeTab(self, index):
        tab = self.editores.widget(index)
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
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.continuar.setText(_translate("MainWindow", "|>"))
        self.menuProject.setTitle(_translate("MainWindow", "Project"))
        self.menuedit.setTitle(_translate("MainWindow", "Edit"))
        self.menuProgram.setTitle(_translate("MainWindow", "Program"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))

        format = self.area.document().rootFrame().frameFormat()
        format.setBottomMargin(10)
        self.area.document().rootFrame().setFrameFormat(format)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    

    MainWindow.show()
    sys.exit(app.exec_())
