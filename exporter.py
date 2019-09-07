#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" This is the exporter module of Biovarase. It set data to export dataset in xls file format."""
import sys
import inspect
import tempfile
import xlwt


__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "4.2"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2018-12-25"
__status__ = "Production"



class Exporter:
    def __init__(self, *args, **kwargs):
        
        self.args = args
        self.kwargs = kwargs
        
    def __str__(self):
        return "class: %s" % (self.__class__.__name__, )

    def get_counts(self, args):

        try:

            sql = "SELECT tests.test_id,\
                          tests.test,\
                          samples.sample,\
                          COUNT(results.batch_id)\
                   FROM tests\
                   INNER JOIN batches ON tests.test_id = batches.test_id\
                   INNER JOIN samples ON tests.sample_id = samples.sample_id\
                   INNER JOIN results ON batches.batch_id = results.batch_id\
                   WHERE tests.enable=1\
                   AND results.recived >=?\
                   GROUP BY batches.test_id\
                   ORDER BY tests.test"
            
            
            rs = self.read(True, sql, args)

            path = tempfile.mktemp (".xls")
            obj = xlwt.Workbook()
            ws = obj.add_sheet('Biovarase', cell_overwrite_ok=True)

            #ws.col(0).width = 200 * 20
            #ws.col(1).width = 300 * 20 
            row = 0

            #indexing is zero based, row then column
            cols =('Test','Sample','Count',)
            for c,t in enumerate(cols):
                ws.write(row,c, t,)

            row +=1

            if rs:
                for i in rs:
                    ws.write(row, 0, i[1])
                    ws.write(row, 1, i[2],)
                    ws.write(row, 2, i[3])
                    row +=1

            obj.save(path)
            self.launch(path)

        except:
            self.engine.on_log(self,
                               inspect.stack()[0][3],
                               sys.exc_info()[1],
                               sys.exc_info()[0],
                               sys.modules[__name__])


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

        sql = "SELECT * FROM rejections_to_export WHERE modified >=?"

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


    def get_quick_data_analysis(self, selected_data):

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

            sql_batches = "SELECT * FROM batches WHERE enable =1 AND test_id =?"

            rs_batchs = self.read(True, sql_batches, (test[0],))

            if rs_batchs:

                for batch in rs_batchs:

                    sql_results = "SELECT result_id, result, recived\
                                   FROM results\
                                   WHERE batch_id =?\
                                   AND enable =1\
                                   AND date(recived)=?\
                                   ORDER BY recived DESC"

                    rs_results = self.read(True, sql_results, (batch[0], selected_data[0]))

                    if rs_results is not None:

                        for i in rs_results:
                            
                            series = self.get_series(batch[0], int(self.get_elements()), i[0])

                            if len(series) > 9:
                                rule = self.get_westgard_violation_rule(batch[4], batch[5], series, batch, test)
                            else:
                                rule = "No data"

                            c = None

                            try:
                                if i:
                                    
                                    compute_cv = self.get_cv(series)
                                    compute_sd = self.get_sd(series)
                                    compute_avg = self.get_mean(series)
                                    target = float(batch[4])
                                    sd = float(batch[5])
                                    bias = self.get_bias(compute_avg, target)
                                    result = float(i[1])
                                    date = i[2].strftime("%d-%m-%Y")
                                    

                                                    
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
                                        ws.write(row,3,result,self.xls_bg_colour(c))
                                        row +=1
                                    else:
                                        ws.write(row,3,result,)
                                        row +=1
                                                                       
                            except:
                               
                                self.on_log(self,
                                                   inspect.stack()[0][3],
                                                   sys.exc_info()[1],
                                                   sys.exc_info()[0],
                                                   sys.modules[__name__])
                    
        obj.save(path)
        self.launch(path)                     

    def get_analitical_goals(self,limit,rs):

        path = tempfile.mktemp (".xls")
        obj = xlwt.Workbook()
        ws = obj.add_sheet('Biovarase', cell_overwrite_ok=True)
        ws.col(0).width = 50 * 20
        for f in range(4,19):
            ws.col(f).width = 80 * 25
        row = 0
        #indexing is zero based, row then column
        cols =('T','analyte','batch','expiration','target','avg',
               'CVa','CVw','CVb','Imp%','Bias%','TEa%','CVt','k imp',
               'k bias','TE%','Sigma','Sce','Drc%','records',)
        for c,t in enumerate(cols):
            ws.write(row,c, t, self.xls_style_font(True, False, 'Arial'))

        row +=1
        
        for i in rs:
            
            series = self.get_series(i[0], limit)

            if len(series) > 5:

                cva = self.get_cv(series)
                sd = self.get_sd(series)
                avg = self.get_mean(series)
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

                x = self.get_tea_tes_comparision(avg, target, cvw, cvb, cva)
                ws.write(row,15,x[0],self.xls_bg_colour(x[1]))

                #compute sigma
                x = self.get_sigma(cvw, cvb, target, series)
                ws.write(row, 16, x)

                #compute sistematic critical error
                x = self.get_sce(cvw, cvb, target, series)
                ws.write(row,17,x[0],self.xls_bg_colour(x[1]))

                #compute critical difference
                x = self.get_formula_drc(row)
                ws.write(row, 18, xlwt.Formula(x))
                
                #records
                ws.write(row, 19, len(series),)
                row +=1

        obj.save(path)
        self.launch(path)


    def get_formula_drc(self,row):
        """compute critical difference"""
        #=ROUND((ROUND(SQRT(POWER(G30,2)+POWER(H30,2))*2.77,2))*F30/100,2)
        #return "ROUND((ROUND(SQRT(POWER(G%s;2)+POWER(H%s;2))*2.77;2))*F%s/100,2)"%(row+1,row+1,row+1,)
        return "(ROUND(SQRT(POWER(G%s;2)+POWER(H%s;2))*2.77;2))"%(row+1,row+1,)


    def get_formula_imp(self, row):
        return "ROUND((H%s * 0.5);2)"%(row+1,)

    def get_formula_bias(self, row):
        return "ROUND(SQRT(POWER(H%s;2)+POWER(I%s;2))*0.25;2)"%(row+1,row+1,)

    def get_formula_eta(self, row):
        return "ROUND((1.65*J%s)+ K%s;2)"%(row+1, row+1,)

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
                c = "green"
          
            f = "ROUND(G%s/H%s;2)"%(row+1,row+1)
            return f,c

        except (ZeroDivisionError,ValueError):
            return None

    def get_formula_k_bias(self,avg, target, cvw, cva, row):

        """return bias k 0.125,0.25,0.375"""
        
        k = round(self.get_bias(avg, target)/self.get_cvt(cva,cvw),2)
     
        if 0.125 <= k <= 0.25:
            c ="green"
        elif 0.25 <= k <= 0.375:
            c = "yellow"
        elif  k > 0.375:
            c = "red"
        else:
            c = "green"
       
        f = "ROUND((((F%s-E%s)/E%s)*100)/SQRT(POWER(H%s;2)+POWER(I%s;2));2)"%(row+1,row+1,
                                                                              row+1,row+1,
                                                                              row+1,)             
        return f,c
        

    def xls_bg_colour(self,colour):

        """ Colour index
        8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta,
        7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown),
        20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, """


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
