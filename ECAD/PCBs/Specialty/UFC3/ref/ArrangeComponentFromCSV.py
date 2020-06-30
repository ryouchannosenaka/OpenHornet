import csv
import pcbnew
import Tkinter
from tkFileDialog import askopenfilename
import tkMessageBox


class ArrangeComponentFromCSV(pcbnew.ActionPlugin):
    def defaults( self ):
        self.name = "Arrange components from CSV"
        self.category = "Modify PCB"
        self.description = "Arrange components based on CSV. contain header with following fields ref, x, y\n Requirements:\n  -Placement coordinates are in mm\n  -Requires a single component on the board named rel_origin, this component will be used as reference."

     def get_filename():
        filename = askopenfilename(
            initialdir = ".",
            title = "Select file",
            filetypes = (("csv files","*.csv"),("all files","*.*")),
        )
        return filename

    def csv_to_dictionary(self):
        file = get_filename()
        d = {}
        if len(file) == 0:
            return None
        with open(file) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            header=True
            for row in csv_reader:
                if header:
                    #skip header
                    header = False
                    continue
                d[row['ref']] = row
        return d

    def Arrange(self):
        pcb = pcbnew.GetBoard()
        components = pcb.GetModules()
        positions = csv_to_dictionary()
        if positions is None:
            tkMessageBox.showinfo("Operation aborted", "CSV file invalid")
            return
        if not "ref" in positions or not "x" in positions or not "y" in positions:
            tkMessageBox.showinfo("Operation aborted", "csv file MUST contain ref, x, and y headers, rotation is optional")
            return
        origin = board.FindModuleByReference("rel_origin")
        if origin is None:
            tkMessageBox.showinfo("Operation aborted", "rel_origin component not found")
            return
        for c in components:
            ref = c.GetReference()
            if ref in positions:
                x = positions[ref]['x']*1000000
                y = 0 - positions[ref]['y']*1000000
                c.SetPosition(pcbnew.wxPointMM(x, y))
                if "rotation" in positions[ref]:
                    c.SetOrientationDegrees(positions[ref]['rotation'])
                c.SetLocked(True)

    def Run( self ):
        root = Tkinter.Tk()
        root.update()
        Arrange()
        
        root.update()
        root.destroy()
        root.mainloop()

ArrangeComponentFromCSV().register()