# =============================================================================
# 文件名：ui.py
# 功能：基于PyQt5的Cmini语法分析图形界面
# 作者： 武起龙
# 时间：2020/1/1
#==============================================================================
# 
# *如何使用*
#   - 运行ui.py后将分析文件拖入即可
#
# *所需文件*
#   - 语法分析器接口:c_grammar_uiapi.py
#   - c_grammar_uiapi.py所引用的特殊yacc文件:yacc_ui.py
#
# *功能*
#   - 语法正确，则显示词法分析结果，语法分析过程和三地址代码
#   - 语法错误，则显示出错类型和位置
#   - 文件错误，则提示文件不匹配
# 
# =============================================================================
# *实现思路*
#   1.构建主界面,出错界面和结果界面
#   2.在主界面中接受文件后将调用c_grammar_uiapi进行语法分析
#   3.根据分析结果调用相应界面
# =============================================================================
import sematic_uiapi as Gram
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import*

openfile = None

#主界面
class MainWidget(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    #界面设置
    def initUI(self):
        #规定大小和标题
        self.resize(600,400)
        self.setMinimumSize(600,400)
        self.setMaximumSize(600,400)
        self.setWindowTitle('CMCompiler演示程序')

        #允许拖入文件
        self.setAcceptDrops(1)

        #提示信息
        la = QLabel(self)
        la.setGeometry(0,100,600,200)
        la.setContentsMargins(120,0,0,0)
        ft = QFont()
        ft.setPointSize(20)
        la.setFont(ft)
        la.setText("请将要分析的C语言文件拖入")
        self.la = la

        #拖入文件不符合标准时的提示信息
        lae = QLabel(self)
        lae.setGeometry(0,100,600,200)
        lae.setContentsMargins(120,0,0,0)
        ft = QFont()
        ft.setPointSize(20)
        lae.setFont(ft)
        lae.setText("该文件无效，请拖入有效文件")
        self.lae = lae
        lae.hide()
        
    #重写拖入文件事件
    def dragEnterEvent(self,event):
        if(event.mimeData().hasUrls()):
            event.acceptProposedAction()
        else: event.ignore()

    #重写文件放下事件
    def dropEvent(self,event):
        mimedata = event.mimeData()
        urllist = mimedata.urls()
        filename = urllist[0].toLocalFile()
        global openfile
        #判断文件是否为C语言文件
        isC = filename.endswith(".c")
        if(isC):
            openfile = filename
            res = Gram.Analysis(filename)
            #文件打开失败
            if(res==2):
                self.la.hide()
                self.lae.show()
            #文件分析出错，调出出错界面
            elif(res==1):
                e = ErrorWidget()
                self.hide()
                self.la.show()
                self.lae.hide()
                e.exec()
                self.show()
            #文件分析成功，调出结果界面
            else:
                r = ResultWidget()
                self.hide()
                self.la.show()
                self.lae.hide()
                r.exec()
                self.show()
        else:
            self.la.hide()
            self.lae.show()
        
#出错界面
class ErrorWidget(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        #规定大小和标题
        self.resize(900,400)
        self.setMinimumSize(900,400)
        self.setMaximumSize(900,400)

        #
        global openfile
        txt = QTextEdit(self)
        txt.setGeometry(590,20,290,360)
        f = open(openfile,'r',encoding='UTF-8')
        lines = f.readlines()
        strline = ''
        i=0
        for line in lines:
            strline+=(('{:<3}'.format(str(i+1)))+':  '+line)
            i+=1
        txt.setText(strline)
        #设为只读模式
        txt.setReadOnly(1)
        self.setWindowTitle('文件语句错误')
        #错误信息显示
        te = QTextEdit(self)
        te.setGeometry(20, 20, 480, 360)
        f = open("error.out",'r',encoding='UTF-8')
        lines = f.readlines()
        strline = ''
        for line in lines:
            strline+=(line)
        te.setText(strline)
        #设为只读模式
        te.setReadOnly(1)
        #右下返回按钮
        btn = QPushButton("分析其他文件",self)
        btn.setGeometry(500,360,90,20)
        #建立按钮被点击和btnClicked函数的连接
        btn.clicked.connect(self.btnClicked)

    def btnClicked(self):
        self.close()
        

#结果界面
class ResultWidget(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    #界面设置
    def initUI(self):
        #规定大小和标题
        self.resize(900,400)
        self.setMinimumSize(900,400)
        self.setMaximumSize(900,400)
        self.setWindowTitle('代码分析结果')

        #
        global openfile
        txt = QTextEdit(self)
        txt.setGeometry(590,20,290,360)
        f = open(openfile,'r', encoding='utf-8')
        lines = f.readlines()
        strline = ''
        i=0
        for line in lines:
            strline+=(('{:<3}'.format(str(i+1)))+':  '+line)
            i+=1
        txt.setText(strline)
        #设为只读模式
        txt.setReadOnly(1)
        #左侧列表信息
        leftlist = QListWidget(self)
        leftlist.insertItem(0, '词法分析结果')
        leftlist.insertItem(1, '语法分析流程')
        leftlist.insertItem(2, '四元式结果')
        leftlist.setGeometry(20, 20, 90, 70)
        leftlist.setCurrentRow(0)
        
        #左下返回按钮
        btn = QPushButton("分析其他文件",self)
        btn.setGeometry(20,360,90,20)
        
        #右侧窗口信息
        Stack = QStackedWidget(self)
        Stack.setGeometry(110, 20, 470, 360)
        stack1 = QWidget()
        stack2 = QWidget()
        stack3 = QWidget()
        Stack.addWidget(stack1)
        Stack.addWidget(stack2)
        Stack.addWidget(stack3)
        
        #窗口stack1显示
        tes1 = QTextEdit(stack1)
        tes1.resize(470,360)
        f = open("tokensanalysis.out",'r')
        lines = f.readlines()
        strline = ''
        for line in lines:
            strline+=(line)
        tes1.setText(strline)
        #设为只读模式
        tes1.setReadOnly(1)
        
        #窗口stack2显示
        tes2 = QTextEdit(stack2)
        tes2.resize(470,360)
        f = open("grammaranalysis.out",'r')
        lines = f.readlines()
        strline = ''
        for line in lines:
            strline+=(line)
        tes2.setText(strline)
        #设为只读模式
        tes2.setReadOnly(1)
        #窗口stack3显示
        f = open("code.out",'r')
        lines = f.readlines()
        tws3 = QTableWidget(int(lines[0]),4,stack3)
        tws3.resize(470,360)
        tws3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tws3.setHorizontalHeaderLabels(['Op','arg1','arg2','result'])
        tws3.setEditTriggers(QAbstractItemView.NoEditTriggers)
        i=1
        while i < int(lines[0]):
            temp = lines[i].split()
            tws3.setItem(i-1,0,QTableWidgetItem(temp[0]))
            tws3.setItem(i-1,1,QTableWidgetItem(temp[1]))
            tws3.setItem(i-1,2,QTableWidgetItem(temp[2]))
            tws3.setItem(i-1,3,QTableWidgetItem(temp[3]))
            i+=1
        #建立按钮被点击和btnClicked函数的连接
        btn.clicked.connect(self.btnClicked)
        #建立leftlist和Stack连接
        leftlist.currentRowChanged.connect(Stack.setCurrentIndex)
        
    #按钮被点击事件
    def btnClicked(self):
        self.close()
       

if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = MainWidget()
    m.exec()
    sys.exit(app.exec_())
