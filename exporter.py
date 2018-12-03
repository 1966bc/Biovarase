#!/usr/bin/env python3
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn 2018                                                           
#-----------------------------------------------------------------------------
import tempfile
import xlwt
from xlwt import easyxf
import math
import sys

class Exporter(object):
    def __init__(self,*args, **kwargs):
        super(Exporter, self).__init__( )

        self.args = args
        self.kwargs = kwargs
        
    def __str__(self):
        return "class: %s\nMRO: %s" % (self.__class__.__name__,  [x.__name__ for x in Exporter.__mro__])


    def rpt_rejections(self,):

        path = tempfile.mktemp (".xls")
        obj = xlwt.Workbook()
        ws = obj.add_sheet('Biovarase',cell_overwrite_ok=True)

        ws.col(0).width = 200 * 20
        #ws.col(1).width = 300 * 20 
        row = 0
        #indexing is zero based, row then column

        ws.write(row,0,'Test',self.xls_style_font(True,False,'Arial'))
        ws.write(row,1,'Sample',self.xls_style_font(True,False,'Arial'))
        ws.write(row,2,'Batch',self.xls_style_font(True,False,'Arial'))
        ws.write(row,3,'Target',self.xls_style_font(True,False,'Arial'))
        ws.write(row,4,'SD',self.xls_style_font(True,False,'Arial'))
        ws.write(row,5,'Result',self.xls_style_font(True,False,'Arial'))
        ws.write(row,6,'Recived',self.xls_style_font(True,False,'Arial'))
        ws.write(row,7,'Action',self.xls_style_font(True,False,'Arial'))
        ws.write(row,8,'Description',self.xls_style_font(True,False,'Arial'))
        ws.write(row,9,'Modify',self.xls_style_font(True,False,'Arial'))
        
        row +=1

        sql = "SELECT * FROM rpt_rejections"
        rs = self.read(True, sql)

        if rs:
            for i in rs:
                ws.write(row,0,i[0])
                ws.write(row,1,i[1])
                ws.write(row,2,i[2])
                ws.write(row,3,i[3])
                ws.write(row,4,i[4])
                ws.write(row,5,i[5])
                ws.write(row,6,i[6])
                ws.write(row,7,i[7])
                ws.write(row,8,i[8])
                ws.write(row,9,i[9])
                
                row +=1
            
        obj.save(path)
        self.launch(path)

    
    def quick_data_analysis(self,):

        path = tempfile.mktemp (".xls")
        obj = xlwt.Workbook()
        ws = obj.add_sheet('Biovarase',cell_overwrite_ok=True)

        ws.col(0).width = 200 * 20
        #ws.col(1).width = 300 * 20 
        row = 0
        #indexing is zero based, row then column

        ws.write(row,0,'Test',self.xls_style_font(True,False,'Arial'))
        ws.write(row,1,'Batch',self.xls_style_font(True,False,'Arial'))
        ws.write(row,2,'Target',self.xls_style_font(True,False,'Arial'))
        ws.write(row,3,'SD',self.xls_style_font(True,False,'Arial'))
        ws.write(row,4,'Result',self.xls_style_font(True,False,'Arial'))
        ws.write(row,5,'Wstg',self.xls_style_font(True,False,'Arial'))
        ws.write(row,6,'Date',self.xls_style_font(True,False,'Arial'))
        
        row +=1

        sql = "SELECT * FROM lst_tests WHERE enable =1"
        rs_tests = self.read(True, sql)
        for test in rs_tests:
            sql2 = "SELECT * FROM batchs WHERE enable =1 AND test_id =?"
            rs_batchs = self.read(True, sql2, (test[0],))
            for batch in rs_batchs:
                sql3 = "SELECT result, recived\
                        FROM results\
                        WHERE batch_id =?\
                        AND enable =1\
                        ORDER BY result_id\
                        DESC LIMIT 1"
                rs_results = self.read(True, sql3, (batch[0],))

                series = self.get_series(batch[0],self.get_elements())
                #reverce series
                x = series[::-1]
                if len(x) > 9:  
                    rule = self.get_violation(batch[4], batch[5], x)
                else:
                    rule = "No data"
                c = None
                try:
                    if len(rs_results) !=0:

                        result = float(rs_results[0][0])
                        date = rs_results[0][1].strftime("%d-%m-%Y")
                        target = float(batch[4])
                        sd = float(batch[5])
                           
                        if result >= target:
                            #result > 3sd
                            if result >= (target + (sd*3)):
                                c = "red"  
                            #if result is > 2sd and < +3sd
                            #elif (target + (sd*2) <= result <= target + (sd*3)):
                            elif result >= (target + (sd*2)) and result <= (target + (sd*3)):
                                c =  "yellow"
                                    
                        elif result <= target:
                            if result <= (target - (sd*3)):
                                c = "red"
                            #if result is > -2sd and < -3sd
                            #elif (target - (sd*2) <= result <= target - (sd*3)):
                            elif result <= (target - (sd*2)) and result >= (target - (sd*3)):
                                c = "yellow"

                        ws.write(row,0,test[1])
                        ws.write(row,1,batch[2])
                        ws.write(row,2,target)
                        ws.write(row,3,sd)
                        ws.write(row,6,date)

                        if rule not in('Accept','No data'):
                            
                            ws.write(row,5,rule,self.xls_bg_colour('blue'))
                        else:
                            ws.write(row,5,rule,)

                        if c :
                            ws.write(row,4,result,self.xls_bg_colour(c))
                            row +=1
                        else:
                            ws.write(row,4,result,)
                            row +=1
                except:
                   
                    print (test,batch,rs_results)
                    print (sys.exc_info()[0])
                    print (sys.exc_info()[1])
                    print (sys.exc_info()[2])
        

        obj.save(path)
        self.launch(path)              


    def get_xls(self,limit,rs):

        
        path = tempfile.mktemp (".xls")
        obj = xlwt.Workbook()
        ws = obj.add_sheet('Biovarase',cell_overwrite_ok=True)

        ws.col(0).width = 32 * 20
        ws.col(1).width = 300 * 20 
        row = 0
        #indexing is zero based, row then column

        ws.write(row,0,'T')
        ws.write(row,1,'analyte',self.xls_style_font(True,False,'Arial'))
        ws.write(row,2,'batch',self.xls_style_font(True,False,'Arial'))
        ws.write(row,3,'expiration',self.xls_style_font(True,False,'Arial'))
        ws.write(row,4,'target',self.xls_style_font(True,False,'Arial'))
        ws.write(row,5,'avg',self.xls_style_font(True,False,'Arial'))
        ws.write(row,6,'CVa',self.xls_style_font(True,False,'Arial'))
        ws.write(row,7,'CVw',self.xls_style_font(True,False,'Arial'))
        ws.write(row,8,'CVb',self.xls_style_font(True,False,'Arial'))
        ws.write(row,9,'Imp%',self.xls_style_font(True,False,'Arial'))
        ws.write(row,10,'Bias%',self.xls_style_font(True,False,'Arial'))
        ws.write(row,11,'ETa',self.xls_style_font(True,False,'Arial'))
        ws.write(row,12,'CVt',self.xls_style_font(True,False,'Arial'))
        ws.write(row,13,'k imp',self.xls_style_font(True,False,'Arial'))
        ws.write(row,14,'k bias',self.xls_style_font(True,False,'Arial'))
        ws.write(row,15,'ETs',self.xls_style_font(True,False,'Arial'))
        ws.write(row,16,'esc',self.xls_style_font(True,False,'Arial'))
        ws.write(row,17,'ecc',self.xls_style_font(True,False,'Arial'))
        ws.write(row,18,'dcr%',self.xls_style_font(True,False,'Arial'))
        ws.write(row,19,'sigma%',self.xls_style_font(True,False,'Arial'))
        ws.write(row,20,'records',self.xls_style_font(True,False,'Arial'))
        
        
        row +=1
        records = len(rs)
        for i in rs:
            
            stat_args = self.get_stat(i[0],limit)
            if stat_args:
                if stat_args[0] > 5:

                    elements = stat_args[0]
                    cva = round(stat_args[1],2)
                    avg = stat_args[2]
                    sd = stat_args[3]
                    
                    cvw = i[6]
                    cvb = i[7]
                    target = float(i[5])

                    ws.write(row,0,i[1])
                    ws.write(row,1,i[2],self.xls_style_font(True,False,'Times New Roman'))
                    ws.write(row,2,str(i[3]))
                    ws.write(row,3,str(i[4]))
                    ws.write(row,4,target)
                    ws.write(row,5,avg)

                    if cva > self.get_imp(cvw):
                        ws.write(row,6,float(cva),self.xls_bg_colour("yellow"))
                    else:
                        ws.write(row,6,float(cva))
                        
                    ws.write(row,7,float(cvw))
                    ws.write(row,8,float(cvb))
                    
                    ws.write(row, 9, xlwt.Formula(self.get_formula_imp(row)),)
                    ws.write(row, 10, xlwt.Formula(self.get_formula_bias(row)),)
                    ws.write(row, 11, xlwt.Formula(self.get_formula_eta(row)),)
                    ws.write(row, 12, xlwt.Formula(self.get_formula_cvt(row)),)

                    x = self.get_formula_k_imp(cva, cvw, row)
                    if x is not None:
                        if x[1] is not None:
                            ws.write(row,13,xlwt.Formula(x[0]),self.xls_bg_colour(x[1]))
                        else:
                            ws.write(row,13,xlwt.Formula(x[0]))

                    x = self.get_formula_k_bias(avg, target, cvw, cvb, row)
                    if x[1] is not None:
                         ws.write(row, 14, xlwt.Formula(x[0]),self.xls_bg_colour(x[1]))
                    else:
                        ws.write(row, 14, xlwt.Formula(x[0]))


                    x = self.get_formula_ets(avg, target, cvw, cvb, cva, row)
                    ws.write(row,15,xlwt.Formula(x[0]),self.xls_bg_colour(x[1]))
                    
                    #max bias variation 
                    x = self.get_delta_esc(cvw,cvb,sd)
                    if x[1] is not None:
                        ws.write(row, 16, x[0], self.xls_bg_colour(x[1]))
                    else:
                        ws.write(row, 16, x[0], self.xls_bg_colour(x[1]))
                        
                    #max variation of random error 
                    ws.write(row, 17, self.get_delta_ecc(cvw,cvb,sd),)
                    
                    #critical difference
                    ws.write(row,18,xlwt.Formula(self.get_formula_drc(row)),)
                    #metrica sigma
                    #"(L%s-K%s)/(H%s*0,5)"
                     
                    #s = "ROUND((L%s - K%s)/J%s;2)"%(row+1,row+1,row+1)
                    x = self.get_sigma(avg, target, cva, cvw, cvb)
                    if x[1] is not None:
                        ws.write(row, 19, x[0], self.xls_bg_colour(x[1]))
                    else:
                        ws.write(row, 19, x[0])
                    
                    #records
                    ws.write(row, 20, elements,)

                    row +=1

        obj.save(path)
        self.launch(path)                    
        

    def get_sigma(self,avg, target, cva, cvw, cvb):
        
        x = self.get_imp(cvw)
        y = self.get_bias_xls(cvw,cvb)
        eta = round((1.65*x)+y,2)
        bias = self.get_relative_error(avg, target)
        
        s = round((eta - bias)/ cva,2)

        if s <= 2:
            c = "red"
        elif s >= 6:
            c = "green"
        else:
            c = None
        return s,c
        
    def get_formula_imp(self, row):
        return "ROUND((H%s * 0.5);2)"%(row+1,)

    def get_formula_bias(self, row):
        return "ROUND(SQRT(POWER(H%s;2)+POWER(I%s;2))*0.25;2)"%(row+1,row+1,)

    def get_formula_eta(self, row):
        return "ROUND((1.65*J%s)+ K%s;2)"%(row+1,row+1,)

    def get_formula_cvt(self, row):
        return "ROUND(SQRT(POWER(G%s;2)+POWER(H%s;2));2)"%(row+1,row+1,)

    def get_formula_k_imp(self, cva, cvw, row):

        try:

            k = round((cva/cvw),2)
            
            if 0.25 <= k <= 0.50:
                c ="green"
            elif 0.50 <= k <= 0.75:
                c = "yellow"
            elif  k > 0.75:
                c = "red"
            else:
                c = None
          
            f = "ROUND(G%s/H%s;2)"%(row+1,row+1)
            return f,c
        except:
            return None

    def get_formula_k_bias(self,avg, target, cvw, cvb, row):

        """return bias k 0.125,0.25,0.375"""
        
        k = round(self.get_relative_error(avg, target)/self.get_cvt(cvw,cvb),2)
     
        if 0.125 <= k <= 0.25:
            c ="green"
        elif 0.25 <= k <= 0.375:
            c = "yellow"
        elif  k > 0.375:
            c = "red"
        else:
            c = None
       
        f = "ROUND((((F%s-E%s)/E%s)*100)/SQRT(POWER(H%s;2)+POWER(I%s;2));2)"%(row+1,row+1,
                                                                             row+1,row+1,
                                                                              row+1,)             
        return f,c

    def get_relative_error(self, avg, target):
        """compute bias"""
        try:
            x = avg - target
            return round((x/target)*100,2)
        except ZeroDivisionError:
            return None
        

    def get_formula_ets(self, avg, target, cvw, cvb, cva, row):

        """return instrumental total error"""

        try:
            x = round(self.get_bias_xls(cvw,cvb) + (1.65 * self.get_imp(cvw)),2)
            y = round(self.get_relative_error(avg, target) + (1.65 * cva),2)

            if y < x:
                c = "green"
            elif y == x:
                c = "yellow"
            elif y > x:
                c = "red"

            f = "ROUND(O%s+(1.65*G%s);2)"%(row+1,row+1)
            return f,c
        except ZeroDivisionError:
            return None

    def get_formula_drc(self,row):
        """compute critical difference"""
        return "ROUND(SQRT(POWER(G%s;2)+POWER(H%s;2))*2.77;2)"%(row+1,row+1,)

    def get_cvt(self,cvw,cva):
        x = cvw**2
        y = cva*2
        z = x+y
        return round(math.sqrt(z),2)

    def get_bias_xls(self,cvw,cvb):
        return round(math.sqrt((math.pow(cvw,2) + math.pow(cvb,2)))*0.25,2)

    def get_imp(self,cvw):
        return round(cvw*0.5,2)

    def get_delta_esc(self,cvw,cvb,sd):
        """compute delta sistematic criticalerror"""
        
        bias = self.get_bias_xls(cvw,cvb)
        eta = round((1.65 * self.get_imp(cvw)) + (self.get_cvt(cvw,cvb)*0.25),2)
        x = (eta-bias)/sd
        y = round(x-1.65,2)
        if y > 3:
            c = "green"
        elif y > 2 and y <= 3:
            c = "yellow"
        elif y < 2:
            c = "red"
        else:
            c = None
        return y,c
    
    def get_delta_ecc(self,cvw,cvb,sd):
        
        bias = self.get_bias_xls(cvw,cvb)
        eta = round((1.65 * self.get_imp(cvw)) + (self.get_cvt(cvw,cvb)*0.25),2)
        x = eta-bias
        y = sd * 1.65
        return round(x/y,2)

    def xls_bg_colour(self,colour):

        dict_colour = {"green":3,
                       "red":2,
                       "white":1,
                       "yellow":5,
                       "gray":22,
                       "blue":4,"magenta":6,"cyan":7}
        bg_colour = xlwt.XFStyle()
        p = xlwt.Pattern()
        p.pattern = xlwt.Pattern.SOLID_PATTERN
        p.pattern_fore_colour = dict_colour[colour]
        bg_colour.pattern = p
        return bg_colour

    def xls_style_font(self,is_bold,is_underline,font_name):

        style = xlwt.XFStyle()
        # Create a font to use with the style
        font = xlwt.Font()
        font.name = font_name
        font.bold = is_bold
        font.underline = is_underline
        # Set the style's font to this new one you set up
        style.font = font
        return style
  
            
def main():
    
    foo = Exporter()
    print(foo)
    input('end')
       
if __name__ == "__main__":
    main()
