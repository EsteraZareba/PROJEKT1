# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 11:48:51 2019

@author: Estera
"""

import sys
from PyQt5.QtWidgets import QApplication, QColorDialog, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QMessageBox


class AppWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.title = 'Program'       
        self.initInterface()
        self.initWidgets()
        
    def initInterface(self):
        
        self.setWindowTitle(self.title)
        self.setGeometry(600,600,700,600)
        self.show()
        
    def initWidgets(self):
        
        #buttons       
        btnCol=QPushButton("Rysuj/Zmień kolor",self)
        btnOblicz=QPushButton("Oblicz",self)
        btnczysc=QPushButton("Wyczyść dane",self)
    
        #labels
        xLabel=QLabel("X",self)
        yLabel=QLabel("Y",self)
        podajwspLabel=QLabel("Podaj współrzędne końców odcinków [m]:",self)
        aLabel=QLabel("A",self)
        bLabel=QLabel("B",self)
        cLabel=QLabel("C",self)
        dLabel=QLabel("D",self)
        pLabel=QLabel("P",self)
        polLabel=QLabel("Położenie punktu P:",self)
       
       
        #edits
        self.xaEdit=QLineEdit()
        self.yaEdit=QLineEdit()
        self.xbEdit=QLineEdit()
        self.ybEdit=QLineEdit()
        self.xcEdit=QLineEdit()
        self.ycEdit=QLineEdit()
        self.xdEdit=QLineEdit()
        self.ydEdit=QLineEdit()
        self.xpEdit=QLineEdit()
        self.ypEdit=QLineEdit()
        self.polEdit=QLineEdit()
        self.pol2Edit=QLineEdit()
        
        #wykres
        self.figure=plt.figure()
        self.canvas=FigureCanvas(self.figure)
        
        grid=QGridLayout()
        
        #rozmieszczenie widgetów
        grid.addWidget(podajwspLabel,1,1)
        grid.addWidget(aLabel,2,1)
        grid.addWidget(bLabel,2,2)
        grid.addWidget(cLabel,2,3)
        grid.addWidget(dLabel,2,4)
        grid.addWidget(pLabel,2,5)
        
        grid.addWidget(xLabel,3,0)
        grid.addWidget(self.xaEdit,3,1)
        grid.addWidget(self.xbEdit,3,2)
        grid.addWidget(self.xcEdit,3,3)
        grid.addWidget(self.xdEdit,3,4)
        grid.addWidget(self.xpEdit,3,5)
        
        grid.addWidget(yLabel,4,0)
        grid.addWidget(self.yaEdit,4,1)
        grid.addWidget(self.ybEdit,4,2)
        grid.addWidget(self.ycEdit,4,3)
        grid.addWidget(self.ydEdit,4,4)
        grid.addWidget(self.ypEdit,4,5)
        grid.addWidget(polLabel,5,0)
        grid.addWidget(self.polEdit,5,1,1,5)
        grid.addWidget(self.pol2Edit,6,1,1,5)
        

        grid.addWidget(btnCol,8,0)
        grid.addWidget(btnOblicz,9,0)
        grid.addWidget(btnczysc,10,0)
        grid.addWidget(self.canvas,10, 1,10,10)
                

        self.setLayout(grid)
                        
        
        btnczysc.clicked.connect(self.czyszczenie)
        btnCol.clicked.connect(self.zmienKolor)
        btnOblicz.clicked.connect(self.oblicz)

#funkcje

    def sprawdzwartosc(self,element):
        if element.text().lstrip('-').replace('.','',1).isdigit():
            return float(element.text())
        else:
            mb1= QMessageBox()
            mb1.setIcon(QMessageBox.Information)
            mb1.setWindowTitle('Error')
            mb1.setText('Podaj wartosc liczbowa')
            mb1.setStandardButtons(QMessageBox.Ok)
            mb1.show()
            element.setFocus()
            return None
            
        
        
    def oblicz(self):
        #sprawdzenie wartosci
        xa=self.sprawdzwartosc(self.xaEdit)
        ya=self.sprawdzwartosc(self.yaEdit)
        xb=self.sprawdzwartosc(self.xbEdit)
        yb=self.sprawdzwartosc(self.ybEdit)
        xc=self.sprawdzwartosc(self.xcEdit)
        yc=self.sprawdzwartosc(self.ycEdit)
        xd=self.sprawdzwartosc(self.xdEdit)
        yd=self.sprawdzwartosc(self.ydEdit)
        
        #sprawdzenie czy mianownik t1,t2 nie jest równy '0'
        m=((xb-xa)*(yd-yc))-((yb-ya)*(xd-xc))
        if m==0:
            mb = QMessageBox()
            mb.setIcon(QMessageBox.Information)
            mb.setWindowTitle('Error')
            mb.setText('Dzielenie przez zero')
            mb.setStandardButtons(QMessageBox.Ok)
            mb.show()     
               
        else:
            t1=((xc-xa)*(yd-yc)-(yc-ya)*(xd-xc))/m   
            t2=((xc-xa)*(yb-ya)-(yc-ya)*(xb-xa))/m
            Xp=xc+t2*(xd-xc)
            Yp=yc+t2*(yd-yc)
            
        #położenie punktu względem odcinków
        det1=xa*yb+xb*Yp+Xp*ya-Xp*yb-xa*Yp-xb*ya
        det2=xc*yd+xd*Yp+Xp*yc-Xp*yd-xc*Yp-xd*yc
        if det1>0 and det2>0:
            self.pol2Edit.setText("Punkt P leży po prawej stronie odcinka AB/Punkt P leży po prawej stronie odcinka CD")
        elif det1<0 and det2<0:
            self.pol2Edit.setText("Punkt P leży po lewej stronie odcinka AB/Punkt P leży po lewej stronie odcinka CD")
        elif det1>0 and det2<0:
            self.pol2Edit.setText("Punkt P leży po prawej stronie odcinka AB/Punkt P leży po lewej stronie odcinka CD")
        elif det1>0 and det2==0:
            self.pol2Edit.setText("Punkt P leży po prawej stronie odcinka AB/Punkty C,D i P są współliniowe")
        elif det1<0 and det2>0:
            self.pol2Edit.setText("Punkt P leży po lewej stronie odcinka AB/Punkt P leży po prawej stronie odcinka CD")
        elif det1<0 and det2==0:
            self.pol2Edit.setText("Punkt P leży po lewej stronie odcinka AB/Punkty C,D i P są współliniowe")
        elif det1==0 and det2>0:
            self.pol2Edit.setText("Punkty A,B i P są współliniowe/Punkt P leży po prawej stronie odcinka CD")
        elif det1==0 and det2<0:
            self.pol2Edit.setText("Punkty A,B i P są współliniowe/Punkt P leży po lewej stronie odcinka CD")                
        elif det1==0 and det2==0:
            self.pol2Edit.setText("Punkty A,B i P są współliniowe/Punkty C,D i P są współliniowe")
          
            
            
        #badanie przecięcia odcinków            
        if (t1>=0 and t1<=1) and (t2>=0 and t2<=1):       
             self.polEdit.setText("Punkt znajduje sie na przecieciu odcinkow")
        elif (t1>=0 and t1<=1 and (t2<0 or t2>1)) or ((t1<0 or t1>1) and t2>=0 and t2<=1):   
            self.polEdit.setText("Punkt znajduje sie na przecięciu odcinka i przedłużeniu jednego z odcinków")
        elif det1==0 and det2==0 and (t2<0 or t2>1) and (t1<0 or t1>1):
            self.polEdit.setText("Punkt znajduje się na przecięciu przedłużeń odcinków")
        else:
             self.polEdit.setText("Brak punktu przecięcia")         

        self.ypEdit.setText(str(round(Yp,3)))
        self.xpEdit.setText(str(round(Xp,3)))
        
        #zapis do pliku tekstowego
        wyjscie = open("plik.txt", "w")
        wyjscie.write('\n|{:^8}|{:^8}|'.format('Xp','Yp'))
        wyjscie.write('\n|{:8.3f}|{:8.3f}|'.format(Xp,Yp))
        wyjscie.close()


    #funkcja rysująca wykres
    def rysuj(self,col='red'):
        xa=self.sprawdzwartosc(self.xaEdit)
        ya=self.sprawdzwartosc(self.yaEdit)
        xb=self.sprawdzwartosc(self.xbEdit)
        yb=self.sprawdzwartosc(self.ybEdit)
        xc=self.sprawdzwartosc(self.xcEdit)
        yc=self.sprawdzwartosc(self.ycEdit)
        xd=self.sprawdzwartosc(self.xdEdit)
        yd=self.sprawdzwartosc(self.ydEdit)
        
     
        m=((xb-xa)*(yd-yc)-(yb-ya)*(xd-xc))        
        if m==0:
            odp=QMessageBox.text(self,'Komunikat',"Dzielenie przez '0'")              
        else:
            t1=((xc-xa)*(yc-yd)-(yc-ya)*(xd-xc))/m   
            t2=((xc-xa)*(yb-ya)-(yc-ya)*(xb-xa))/m
            Xp=xc+t2*(xd-xc)
            Yp=yc+t2*(yd-yc)        
         
        if (xa is not None) and (ya is not None) and (xb is not None) and (yb is not None) and (xc is not None) and (yc is not None) and (xd is not None) and (yd is not None):            
            self.figure.clear()            
            ax=self.figure.add_subplot(111) 
            a=ax.plot(xa,ya,color="red", marker='o')
            b=ax.plot(xb,yb,color="green", marker='o')
            c=ax.plot(xc,yc,color="blue", marker='o')
            d=ax.plot(xd,yd,color="pink", marker='o')
            p=ax.plot(Xp,Yp,color="black", marker='o')
            ax.plot([xa,xb],[ya,yb],color=col)                
            ax.plot([xc,xd],[yc,yd],color=col)
            
            
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title('Wykres')
            plt.legend(('A','B','C','D','P'))

            self.canvas.draw()  #odswiezenie wykresu
            
            
    #funkcja zmiany koloru wykresu            
    def zmienKolor(self):
        color=QColorDialog.getColor()
        if color.isValid():
            self.rysuj(col=color.name())  


    #funkcja usuwająca wartosci z pól
    def czyszczenie(self):
        self.xaEdit.setText("")
        self.yaEdit.setText("")
        self.xbEdit.setText("")
        self.ybEdit.setText("")
        self.xcEdit.setText("")
        self.ycEdit.setText("")
        self.xdEdit.setText("")
        self.ydEdit.setText("")
        self.xpEdit.setText("")
        self.ypEdit.setText("")
        self.polEdit.setText("")
        self.pol2Edit.setText("")
        
def main():
    app=QApplication(sys.argv)
    window=AppWindow()
    app.exec_()  
    
if __name__=='__main__':
    main()