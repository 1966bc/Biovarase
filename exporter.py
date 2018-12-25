#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" This is the exporter module of Biovarase. It set data to export datase in xls file format."""
import tempfile
import xlwt
import sys


SQL_BATCHES = "SELECT *\
               FROM batchs\
               WHERE enable =1\
               AND test_id =?"

SQL_RESULTS = "SELECT result, recived\
               FROM results\
               WHERE batch_id =?\
               AND enable =1\
               ORDER BY result_id\
               DESC LIMIT 1"

__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "4.2"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2018-12-25"
__status__ = "Production"

class Exporter(object):
    def __init__(self,*args, **kwargs):
        super(Exporter, self).__init__( )

        self.args = args
        self.kwargs = kwargs
        
    def __str__(self):
        return "class: %s\nMRO: %s" % (self.__class__.__name__,  [x.__name__ for x in Exporter.__mro__])


    def get_rejections(self, args):

        path = tempfile.mktemp (".xls")
        obj = xlwt.Workbook()
        ws = obj.add_sheet('Biovarase', cell_overwrite_ok=True)

        row = 0
        #indexing is zero based, row then column
        cols = ('Test', 'Sample', 'Batch', 'Target', 'SD', 'Result',
                 'Recived', 'Action', 'Description', 'Modify')

        for c,t in enumerate(cols):
            ws.write(row,c, t,self.xls_style_font(True, False, 'Arial'))

        row +=1

        sql = "SELECT * FROM rpt_rejections WHERE modified >=?"

        rs = self.read(True, sql, args)

        if rs:
            for i in rs:
                ws.write(row, 0, i[0])
                ws.write(row, 1, i[1])
                ws.write(row, 2, i[2])
                ws.write(row, 3, i[3])
                ws.write(row, 4, i[4])
                ws.write(row, 5, i[5])
                ws.write(row, 6, i[6])
                ws.write(row, 7, i[7])
                ws.write(row, 8, i[8])
                ws.write(row, 9, i[9])
                
                row +=1
            
        obj.save(path)
        self.launch(path)


  
    def get_quick_data_analysis(self,):

        path = tempfile.mktemp (".xls")
        obj = xlwt.Workbook()
        ws = obj.add_sheet('Biovarase', cell_overwrite_ok=True)

        ws.col(0).width = 200 * 20
        row = 0
        cols = ('Test', 'Batch', 'Target', 'Result', 'avg',
                 'bias', 'SD', 'sd', 'cv', 'Wstg', 'Date',)
        #cols = ('Test','Batch','Target','SD','Result','Wstg','Date',)
        
        for c,t in enumerate(cols):
            ws.write(row, c, t, self.xls_style_font(True, False, 'Arial'))
        
        row += 1
        
        sql_tests = "SELECT * FROM lst_tests WHERE enable =1"
        rs_tests = self.read(True, sql_tests)
        
        for test in rs_tests:

            rs_batchs = self.read(True, SQL_BATCHES, (test[0],))

            for batch in rs_batchs:
                
                rs_results = self.read(False, SQL_RESULTS, (batch[0],))
                
                series = self.get_series(batch[0])
                
                if len(series) > 9:
                    rule = self.get_westgard_violation_rule(batch[4], batch[5], series, batch, test)
                else:
                    rule = "No data"

                c = None

                try:
                    if rs_results:

                        args = self.get_series_stat(series)

          

                        compute_avg = args[0]
                        compute_sd = args[1]
                        compute_cv = args[2]

                        target = float(batch[4])
                        sd = float(batch[5])
                        bias = self.get_bias(compute_avg, target)

    
                        result = float(rs_results[0])
                        date = rs_results[1].strftime("%d-%m-%Y")

                                        
                        if result > target:
                            #result > 3sd
                            if result > (target + (sd*3)):
                                c = "red"   
                            #if result is > 2sd and < +3sd
                            #elif (target + (sd*2) <= result <= target + (sd*3)):
                            elif result > (target + (sd*2)) and result < (target + (sd*3)):
                                c =  "yellow"
                                    
                        elif result < target:
                            if result < (target - (sd*3)):
                                c = "red"
                            #if result is > -2sd and < -3sd
                            #elif (target - (sd*2) <= result <= target - (sd*3)):
                            elif result < (target - (sd*2)) and result > (target - (sd*3)):
                                c = "yellow"


          
                                                        
                        ws.write(row,0,test[1])
                        ws.write(row,1,batch[2])
                        ws.write(row,2,target)
                        ws.write(row,3,result)
                        ws.write(row,4,compute_avg)
                        ws.write(row,5,bias)
                        ws.write(row,6,sd)
                        ws.write(row,7,compute_sd)
                        ws.write(row,8,compute_cv)
                        ws.write(row,10,date)
                        
                
                        
                    
                        if rule not in('Accept','No data'):
                            
                            ws.write(row,9,rule,self.xls_bg_colour('blue'))
                        else:
                            ws.write(row,9,rule,)

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

    def get_analitical_goals(self,limit,rs):

        path = tempfile.mktemp (".xls")
        obj = xlwt.Workbook()
        ws = obj.add_sheet('Biovarase', cell_overwrite_ok=True)
        row = 0
        #indexing is zero based, row then column
        cols =('T','analyte','batch','expiration','target','avg',
               'CVa','CVw','CVb','Imp%','Bias%','ETa','CVt','k imp',
               'k bias','ETs','records',)
        for c,t in enumerate(cols):
            ws.write(row,c, t, self.xls_style_font(True, False, 'Arial'))

        row +=1
        
        for i in rs:
            
            args = self.get_stat(i[0], limit)
            
            if args:
                if args[0] > 5:

                    elements = args[0]
                    cva = round(args[1],2)
                    sd = round(args[3],2)
                    avg = args[2]
                    cvw = i[6]
                    cvb = i[7]
                    target = float(i[5])
                   
                    ws.write(row, 0, i[1])
                    ws.write(row, 1, i[2], self.xls_style_font(True, False, 'Times New Roman'))
                    ws.write(row, 2, str(i[3]))
                    ws.write(row, 3, str(i[4]))
                    ws.write(row, 4, target)
                    ws.write(row, 5, avg)

                    #if cva is > cvw*0.50 
                    if cva > self.get_imp(cvw):
                        ws.write(row, 6, float(cva), self.xls_bg_colour("blue"))
                    else:
                        ws.write(row, 6, float(cva))
                        
                    ws.write(row, 7, float(cvw))
                    ws.write(row, 8, float(cvb))
                    ws.write(row, 9, xlwt.Formula(self.get_formula_imp(row)),)
                    ws.write(row, 10, xlwt.Formula(self.get_formula_bias(row,)),)
                    ws.write(row, 11, xlwt.Formula(self.get_formula_eta(row)),)
                    ws.write(row, 12, xlwt.Formula(self.get_formula_cvt(row)),)

                    x = self.get_formula_k_imp(cva, cvw, row)
                    if x is not None:
                        if x[1] is not None:
                            ws.write(row, 13, xlwt.Formula(x[0]), self.xls_bg_colour(x[1]))
                        else:
                            ws.write(row, 13, xlwt.Formula(x[0]))

                    x = self.get_formula_k_bias(avg, target, cva, cvw, row)
                    if x[1] is not None:
                        ws.write(row, 14, xlwt.Formula(x[0]), self.xls_bg_colour(x[1]))
                    else:
                        ws.write(row, 14, xlwt.Formula(x[0]))

                    x = self.get_ets(avg, target, cvw, cvb, sd)
                    ws.write(row,15,x[0],self.xls_bg_colour(x[1]))
                    #records
                    ws.write(row, 16, elements,)
                    row +=1

        obj.save(path)
        self.launch(path)

    def xls_bg_colour(self,colour):

        dict_colour = {"green":3,
                       "red":2,
                       "white":1,
                       "yellow":5,
                       "gray":22,
                       "blue":4,
                       "magenta":6,
                       "cyan":7,}
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
