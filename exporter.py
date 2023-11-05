# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn MMXXIII
#-----------------------------------------------------------------------------
""" This is the exporter module of Biovarase."""
import tempfile
import xlwt
import sys
import inspect
import datetime

class Exporter:
     
    def __str__(self):
        return "class: %s\nMRO: %s" % (self.__class__.__name__,  [x.__name__ for x in Exporter.__mro__])

    def get_controls(self,):
        
        today = datetime.datetime.now()

        sql = "SELECT samples.sample,\
                      tests.test,\
                      tests_methods.code,\
                      batches.lot_number,\
                      strftime('%d-%m-%Y', expiration),\
                      controls.description,\
                      controls.reference,\
                      suppliers.supplier,\
                      batches.expiration,\
                      batches.description,\
                      batches.target\
               FROM tests\
               INNER JOIN tests_methods ON tests.test_id = tests_methods.test_id\
               INNER JOIN samples ON tests_methods.sample_id  = samples.sample_id\
               INNER JOIN batches ON tests_methods.test_method_id = batches.test_method_id\
               INNER JOIN controls ON batches.control_id = controls.control_id\
               INNER JOIN suppliers ON controls.supplier_id = suppliers.supplier_id\
               WHERE tests.status =1\
               AND tests_methods.status =1\
               AND batches.status =1\
               ORDER BY tests.test ASC;"

        rs = self.read(True, sql, ())
            

        path = tempfile.mktemp (".xls")
        obj = xlwt.Workbook()
        ws = obj.add_sheet('Biovarase', cell_overwrite_ok=True)

        ws.col(0).width = 50 * 25

        #ws.col(0).width = 200 * 20
        ws.col(1).width = 300 * 20
        ws.col(5).width = 250 * 20
        ws.col(7).width = 300 * 20
        ws.col(8).width = 300 * 20
        row = 0

        #indexing is zero based, row then column
        cols =("Sample", "Test", "Code", "Batch",
               "Expiration", "Description", "Target",
               "Control", "Reference", "Supplier")
        
        for c,t in enumerate(cols):
            ws.write(row,c, t,self.xls_style_font(True, False, 'Arial'))            

        row +=1

        if rs:
            for i in rs:
                expiration = i[4]
                #i[8].strftime("%d %b %Y")
                #sample
                ws.write(row, 0, i[0])
                #ws.write(row, 1, i[1], self.xls_bg_colour("blue"))
                #test
                ws.write(row, 1, i[1],)
                #test method code
                ws.write(row, 2, i[2])
                #lot_number
                ws.write(row, 3, i[3])
                #compute expiration date
                
                formatted_expiration = datetime.datetime.strptime(i[8], "%Y-%m-%d")
                diff_date = formatted_expiration - today
                x = diff_date.days
                if x <= 0:
                    ws.write(row,4,expiration, self.xls_bg_colour('red'))
                elif x <= 15:
                    ws.write(row,4,expiration, self.xls_bg_colour('yellow'))
                else:
                    ws.write(row,4,expiration)
                #ws.write(row, 4, i[4])
                ws.write(row, 5, i[9])
                ws.write(row, 6, i[10])
                ws.write(row, 7, i[5])
                ws.write(row, 8, i[6])
                ws.write(row, 9, i[7])
                row +=1

        obj.save(path)
        self.launch(path)


    def get_counts(self, selected_date):

        try:

            sql = "SELECT tests_methods.test_method_id,\
                          tests_methods.code,\
                          tests.test,\
                          samples.sample,\
                          specialities.description,\
                          COUNT(results.batch_id)\
                   FROM tests\
                   INNER JOIN tests_methods ON tests.test_id = tests_methods.test_id\
                   INNER JOIN batches ON tests_methods.test_method_id = batches.test_method_id\
                   INNER JOIN specialities ON tests.speciality_id = specialities.speciality_id\
                   INNER JOIN samples ON tests_methods.sample_id = samples.sample_id\
                   INNER JOIN sections ON tests_methods.section_id = sections.section_id\
                   INNER JOIN wards ON sections.ward_id = wards.ward_id\
                   INNER JOIN results ON batches.batch_id = results.batch_id\
                   WHERE tests.status=1\
                   AND tests_methods.status=1\
                   AND sections.section_id =?\
                   AND DATE(results.recived) >=?\
                   AND results.is_delete=0\
                   GROUP BY tests_methods.test_method_id\
                   ORDER BY tests.test;"

            args = (self.get_section_id(), selected_date[0])
        
            rs = self.read(True, sql, args)
            
            path = tempfile.mktemp (".xls")
            obj = xlwt.Workbook()
            ws = obj.add_sheet('Biovarase', cell_overwrite_ok=True)
            row = 0

            #indexing is zero based, row then column
            cols =('Code','Test','Sample','Specialities','Count',)
            for c,t in enumerate(cols):
                ws.write(row,c, t,)

            row +=1

            if rs:
                for i in rs:
                    ws.write(row, 0, i[1])
                    ws.write(row, 1, i[2])
                    ws.write(row, 2, i[3])
                    ws.write(row, 3, i[4])
                    ws.write(row, 4, i[5])
                    row +=1

            obj.save(path)
            self.launch(path)

        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0])
            
        

    def get_notes(self, args):

        sql = "SELECT tests.test,\
                      batches.lot_number,\
                      batches.target,\
                      batches.sd,\
                      results.result,\
                      results.recived,\
                      actions.action,\
                      notes.description,\
                      notes.modified,\
                      equipments.description,\
                      workstations.description,\
                      workstations.serial,\
                      wards.ward,\
                      sections.section\
               FROM tests\
               INNER JOIN tests_methods ON tests.test_id = tests_methods.test_id\
               INNER JOIN batches ON tests_methods.test_method_id = batches.test_method_id\
               INNER JOIN results ON batches.batch_id = results.batch_id\
               INNER JOIN workstations ON results.workstation_id = workstations.workstation_id\
               INNER JOIN equipments ON workstations.equipment_id = equipments.equipment_id\
               INNER JOIN sections ON workstations.section_id = sections.section_id\
               INNER JOIN wards ON sections.ward_id = wards.ward_id\
               INNER JOIN notes ON results.result_id = notes.result_id\
               INNER JOIN actions ON notes.action_id = actions.action_id\
               WHERE DATE(results.recived) >=?\
               AND sections.section_id =?\
               AND tests.status = 1\
               AND batches.status = 1\
               AND results.is_delete=0\
               ORDER BY notes.modified DESC;"

        path = tempfile.mktemp (".xls")
        obj = xlwt.Workbook()
        ws = obj.add_sheet('Biovarase', cell_overwrite_ok=True)
        row = 0
        #indexing is zero based, row then column
        cols = ("Test", "Batch", "Target", "SD", "Result",
                 "Recived", "Action", "Description", "Modify", "Instrument", "Workstation", "Serial", "Ward", "Section")

        for c,t in enumerate(cols):
            ws.write(row,c, t,self.xls_style_font(True, False, 'Arial'))

        row +=1

        rs = self.read(True, sql, args)

        if rs:
            for i in rs:
                ws.write(row, 0, i[0])
                ws.write(row, 1, i[1])
                ws.write(row, 2, i[2])
                ws.write(row, 3, round(i[3],3))
                ws.write(row, 4, round(i[4],2))
                x = i[5].strftime("%d-%m-%Y")
                ws.write(row, 5, x)
                ws.write(row, 6, i[6])
                ws.write(row, 7, i[7])
                ws.write(row, 8, i[8])
                ws.write(row, 9, i[9])
                ws.write(row, 10, i[10])
                ws.write(row, 11, i[11])
                ws.write(row, 12, i[12])
                ws.write(row, 13, i[13])
                
                row +=1
            
        obj.save(path)
        self.launch(path)
    
    def quick_data_analysis(self, selected_date):

        checked_tests = []
        mandatory_tests = self.get_mandatory()
        today = datetime.date.today()

        path = tempfile.mktemp (".xls")
        obj = xlwt.Workbook(style_compression=2)
        ws = obj.add_sheet('Biovarase', cell_overwrite_ok=True)

        ws.col(0).width = 50 * 25
        ws.col(1).width = 200 * 20
        ws.col(4).width = 300 * 20
        ws.col(17).width = 300 * 20
        for f in range(5,15):
            ws.col(f).width = 80 * 25
        row = 0
        #indexing is zero based, row then column
        cols = ('Type','Test', 'Batch','Expiration','Instrument', 'Target', 'Result', 'avg',
                 'bias', 'SD', 'sd', 'cv', 'Wstg', 'Date','Speciality','Workstation','Control','Supplier','Mandatory')

        for c,t in enumerate(cols):
            ws.write(row, c, t, self.xls_style_font(True, False, 'Arial'))
        
        row +=1

        sql_tests = "SELECT tests_methods.test_method_id,\
                            samples.sample,\
                            tests.test,\
                            specialities.description\
                       FROM tests\
                       INNER JOIN tests_methods ON tests.test_id = tests_methods.test_id\
                       INNER JOIN specialities ON tests.speciality_id = specialities.speciality_id\
                       INNER JOIN samples ON tests_methods.sample_id = samples.sample_id\
                       INNER JOIN sections ON tests_methods.section_id = sections.section_id\
                       INNER JOIN wards ON sections.ward_id = wards.ward_id\
                       INNER JOIN sites ON wards.site_id = sites.site_id\
                       WHERE wards.ward_id =?\
                       AND tests.status=1\
                       AND tests_methods.status=1\
                       ORDER BY tests.test;"
        
        rs_idd = self.get_idd_by_section_id(self.get_section_id())
        
        args = (rs_idd[3],)

        rs_tests_methods = self.read(True, sql_tests, args)
        
        for test_method in rs_tests_methods:

            sql_batches = "SELECT batches.*,\
                                  strftime('%d-%m-%Y', expiration),\
                                  workstations.description,\
                                  equipments.description\
                           FROM batches\
                           INNER JOIN workstations ON batches.workstation_id = workstations.workstation_id\
                           INNER JOIN equipments ON workstations.equipment_id = equipments.equipment_id\
                           INNER JOIN sections ON workstations.section_id = sections.section_id\
                           INNER JOIN wards ON wards.ward_id = sections.ward_id\
                           WHERE batches.status =1\
                           AND batches.test_method_id =?\
                           AND wards.ward_id =?;"

            rs_batches = self.read(True, sql_batches, (test_method[0], rs_idd[3]))

            for batch in rs_batches:

                expiration_date =  batch[5]
                workstation = batch[16]
                instrument = batch[17]

                sql_results = "SELECT results.result_id,\
                                      ROUND(results.result,2),\
                                      recived,\
                                      workstations.description,\
                                      workstations.workstation_id,\
                                      results.recived\
                               FROM results\
                               INNER JOIN workstations ON results.workstation_id = workstations.workstation_id\
                               WHERE results.batch_id =?\
                               AND DATE(results.recived) =?\
                               AND workstations.workstation_id =?\
                               AND results.status = 1\
                               AND results.is_delete=0\
                               ORDER BY results.recived DESC;"

                args =  (batch[0], selected_date[0], batch[3],)

                rs_results = self.read(True, sql_results, args)

                
                sql_controls = "SELECT controls.description, suppliers.supplier\
                                FROM controls\
                                INNER JOIN suppliers ON controls.supplier_id = suppliers.supplier_id\
                                WHERE control_id =?"
                
                rs_controls = self.read(False, sql_controls, (batch[1],))
                

                if rs_results is not None:

                    for result in rs_results:

                        series = self.get_series(batch[0], result[4], int(self.get_elements()), result[0])

                        if len(series) > 9:
                            rule = self.get_westgard_violation_rule(batch[6], batch[7], series, batch, test_method)
                        else:
                            rule = "NED"

                        result_color = None

                        try:
                            if result:
                                
                                compute_cv = self.get_cv(series)
                                #print("compute_cv {0}".format(compute_cv))
                                compute_sd = self.get_sd(series)
                                compute_avg = self.get_mean(series)
                                #print(compute_cv, compute_sd,compute_avg)
                                target = float(batch[6])
                                sd = float(batch[7])
                                bias = self.get_bias(compute_avg, target)
                                #print(target,sd,bias)
                                res = float(result[1])
                                date = result[2].strftime("%d-%m-%Y %H:%M:%S")
                                workstation = result[3]
                                
                                if res > target:
                                    #result > 3sd
                                    if res > (target + (sd*3)):
                                        result_color = "red"   
                                    #if result is > 2sd and < +3sd
                                    #elif (target + (sd*2) <= result <= target + (sd*3)):
                                    elif res > (target + (sd*2)) and res < (target + (sd*3)):
                                        result_color =  "yellow"
                                        
                                elif res < target:
                                    if res < (target - (sd*3)):
                                        result_color = "red"
                                    #if result is > -2sd and < -3sd
                                    #elif (target - (sd*2) <= result <= target - (sd*3)):
                                    elif res < (target - (sd*2)) and res > (target - (sd*3)):
                                        result_color = "yellow"
                                                            
                                #s = '{0}-{1}'.format(test[2],test[13])
                                ws.write(row,0,test_method[1])
                                ws.write(row,1,test_method[2])
                                ws.write(row,2,batch[4])

                                #compute expiration date
                                formatted_expiration = datetime.datetime.strptime(batch[5], "%Y-%m-%d")
                                diff_date = formatted_expiration-result[5]
                                x = diff_date.days
                                
                                if x <= 0:
                                    ws.write(row,3,expiration_date, self.xls_bg_colour('red'))
                                elif x <= 15:
                                    ws.write(row,3,expiration_date, self.xls_bg_colour('yellow'))
                                else:
                                    ws.write(row,3,expiration_date)
                                     
                                ws.write(row,4,instrument)
                                
                                ws.write(row,5,target)
                                ws.write(row,7,compute_avg)
                                ws.write(row,8,bias)
                                ws.write(row,9,sd)
                                ws.write(row,10,compute_sd)
                                ws.write(row,11,compute_cv)
                                ws.write(row,13,date)
                                ws.write(row,14,test_method[3])
                                ws.write(row,15,workstation)
                                checked_tests.append(test_method[1])
                                ws.write(row,16,rs_controls[0])
                                ws.write(row,17,rs_controls[1])
                            
                        
                                if rule not in('Accept','No data'):
                                    ws.write(row, 12, rule, self.xls_bg_colour('blue'))
                                else:
                                    ws.write(row, 12, rule,)

                                if result_color :
                                    ws.write(row, 6, res, self.xls_bg_colour(result_color))
                                    row +=1
                                else:
                                    ws.write(row, 6, res,)
                                    row +=1

                        except:
                             self.on_log(inspect.stack()[0][3], sys.exc_info()[1],
                                         sys.exc_info()[0], sys.modules[__name__])
                
                   
        for test in checked_tests:
            if test in mandatory_tests:
                     mandatory_tests.remove(test)

        row = 1
        for x in mandatory_tests:
            ws.write(row, 18, x, self.xls_bg_colour('red'))
            row +=1
                          
        obj.save(path)
        self.launch(path)

    def get_analitical_goals(self, limit, rs):

        #print(limit,rs)

        path = tempfile.mktemp (".xls")
        obj = xlwt.Workbook(style_compression=2)
        ws = obj.add_sheet('Biovarase', cell_overwrite_ok=True)
        ws.col(0).width = 50 * 20
        for f in range(4,19):
            ws.col(f).width = 80 * 25
     
        row = 0
        #indexing is zero based, row then column
        cols =('T','analyte','batch','expiration','target','avg',
               'CVa','CVw','CVb','Imp%','Bias%','TEa%','CVt','k imp',
               'k bias','TE%','Drc%','records','wst')
        for c,t in enumerate(cols):
            ws.write(row,c, t, self.xls_style_font(True, False, 'Arial'))

        row +=1
        
        for i in rs:

            series = self.get_series(i[0], i[12], limit)
  
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

                #print(cva,cvw,cvb)

                try:

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

                    x = self.get_tea_tes_comparision(avg, target, cvw, cvb, sd, cva)
                    ws.write(row,15,x[0],self.xls_bg_colour(x[1]))

                  
                    #compute critical difference
                    x = self.get_formula_drc(row)
                    ws.write(row, 16, xlwt.Formula(x))
                    
                    #records
                    ws.write(row, 17, len(series),)
                    
                    sql = "SELECT description FROM workstations WHERE workstation_id =?;"
                    workstation = self.read(False, sql, (i[12],))
                    #workstations
                    ws.write(row, 18, workstation[0],)
                    row +=1
                except:
                    print(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0])
                

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
        return "ROUND((%s*J%s)+ K%s;2)"%(self.get_zscore(),row+1, row+1,)

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

    def get_formula_k_bias(self, avg, target, cvw, cva, row):

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
