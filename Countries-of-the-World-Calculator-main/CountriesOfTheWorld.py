import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
#ADD IMPORT STATEMENT FOR YOUR GENERATED UI.PY FILE HERE
import Ui_Phase_3
import csv
_translate = QtCore.QCoreApplication.translate

#CHANGE THE SECOND PARAMETER (Ui_ChangeMe) TO MATCH YOUR GENERATED UI.PY FILE
class MyForm(QMainWindow, Ui_Phase_3.Ui_MainWindow):

    #globally scoped list
    ListCountries = []
    #global variable
    Filename_ = "Files\countries.txt"

    # DO NOT MODIFY THIS CODE
    def __init__(self, parent=None):
        super(MyForm, self).__init__(parent)
        self.setupUi(self)
    # END DO NOT MODIFY

        # ADD SLOTS HERE, indented to this level (ie. inside def __init__)
        self.frameMain.hide()
        self.frameSecondary.hide()
        self.Load_countries_button.triggered.connect(self.LoadCountriesFromFile)
        self.countriesListBox.currentRowChanged.connect(self.DisplayCountryData)
        self.totalareaToggle.currentIndexChanged.connect(self.toggle_Convert)
        self.densityButtonSQMile.clicked.connect(self.PDensity_in_SQ_Miles)
        self.densityButtonSQKM.clicked.connect(self.PDensity_in_SQ_KM)
        self.Update_Population_button.clicked.connect(self.Population_Updated)
        self.Save_File_button.triggered.connect(self.SaveCountriesToFile)
        self.Exit_button.triggered.connect(self.exitProtocol)


    # ADD SLOT FUNCTIONS HERE
    def LoadCountriesFromFile(self): #reads the file and appends to a list of countries (i.e. countiresList)
        Country_File = open(self.Filename_,"r")
        list_of_countries_from_file = csv.reader(Country_File)
        for country in list_of_countries_from_file:
            self.ListCountries.append(country)
        Country_File.close()
        self.LoadCountriesListBox()


    def LoadCountriesListBox(self):  #loads the country list on to the dialogue box
        for country in self.ListCountries:
            country_name = country[0]
            self.countriesListBox.addItem(country_name)


    def DisplayCountryData(self, list_row):  #Displays all the desired country data onto frame
        self.frameMain.show()
        self.frameSecondary.show()
        Name_of_Country = self.ListCountries[list_row][0]
        self.labelCountryName.setText(Name_of_Country)
        flag = QPixmap("Flags\\"+ Name_of_Country.replace(" ","_")+".png")
        self.labelImages.setPixmap(flag)
        Current_population = self.ListCountries[list_row][1]
        self.userEntry.setText(str(Current_population))
        SQ_miles = self.ListCountries[list_row][2]
        self.totalArea.setText(str(SQ_miles))
        self.CalculateTotalWorldPopulation()
        self.PDensity_in_SQ_Miles()


    def CalculateTotalWorldPopulation(self): #calculates the total world population percentage using the data stored in 2D list
        totalpopulation = 0
        for country in range(201):
            totalpopulation = totalpopulation + float(self.ListCountries[country][1])
        population_percentage = (float(self.userEntry.text())/totalpopulation) * 100
        self.labelPOPPercentage.setText(str("{0:.4f}%".format(population_percentage)))


    def SaveCountriesToFile(self):  #Saves the data stored in 2D list to text file
        Country_File = open(self.Filename_, "w")
        for country in self.ListCountries:
            Country_File.write(",".join(country) + "\n")
        Country_File.close()
        QMessageBox.information(self, "Save Changes", "File saved successfully", QMessageBox.Ok)
        self.Save_File_button.triggered = 0 #save button is checked as true since successful save task
        self.Load_countries_button.setEnabled(True)


    def exitProtocol(self):   #Follows exit protocol, if data is not saved then save dialogue box is displayed
        if self.Save_File_button.triggered == 0:
            quit()
        else:
            query = QMessageBox.question(self, "Save?",
                                         "Save changes to file before closing?", QMessageBox.Yes, QMessageBox.No)
            if query == QMessageBox.Yes:
                self.SaveCountriesToFile()
                quit()
            elif query == QMessageBox.No:
                quit()


    def PDensity_in_SQ_Miles(self):  #displays population density in square miles
       Population = self.userEntry.text()
       if self.totalareaToggle.currentText() == "Sq. KM":
           self.totalareaToggle.setCurrentText(_translate("MainWindow", "Sq. Miles"))
           self.Convert_to_SQ_Miles()
       Square_Miles = float(Population) / float(self.totalArea.text())
       self.pDensitylabel.setText(str("{0:.2f}".format(Square_Miles)))


    def PDensity_in_SQ_KM(self):  #displays population density in square km
        Population = self.userEntry.text()
        if self.totalareaToggle.currentText() == "Sq. Miles":
            self.totalareaToggle.setCurrentText(_translate("MainWindow", "Sq. KM"))
            self.Convert_to_SQ_KM()
        Square_KM = float(Population) / float(self.totalArea.text())
        self.pDensitylabel.setText(str("{0:.2f}".format(Square_KM)))


    def toggle_Convert(self):  #toggling/changing the area between square km and square miles converts the value
        if self.totalareaToggle.currentText() == "Sq. Miles":
            self.Convert_to_SQ_Miles()
        else:
            self.Convert_to_SQ_KM()


####################################### HELPER FUNCTIONS START #########################################################


    def Convert_to_SQ_Miles(self):  #converts square km to square miles
        Square_Miles = (float(self.totalArea.text()) / 2.58999)
        self.totalArea.setText(str("{0:.1f}".format(Square_Miles)))
        self.PDensity_in_SQ_Miles()


    def Convert_to_SQ_KM(self):  #converts square miles to square km
        Square_KM = (float(self.totalArea.text()) * 2.58999)
        self.totalArea.setText(str("{0:.1f}".format(Square_KM)))
        self.PDensity_in_SQ_KM()


    def Population_Updated(self):  #Updates valid population data in the two dimensional list
        pos = 1
        Updated_Population = self.userEntry.text()
        check_type = Updated_Population.isnumeric()
        originalPopulation = self.ListCountries[self.countriesListBox.currentRow()][pos]
        if check_type == False or int(Updated_Population) <= 500:
            QMessageBox.information(self, "Invalid",
                                    "Data is invalid so not updated in memory",
                                    QMessageBox.Ok)
            self.userEntry.setText(str(originalPopulation))
        else:
            self.ListCountries[self.countriesListBox.currentRow()][pos] = Updated_Population
            self.Load_countries_button.setEnabled(False)
            self.Save_File_button.setEnabled(True)
            QMessageBox.information(self, "Updated",
                                    "Data has been updated in memory, but hasn't been updated in the file yet",
                                    QMessageBox.Ok)

############################################# Helper Functions END ####################################################



# DO NOT MODIFY THIS CODE
if __name__ == "__main__":
    app = QApplication(sys.argv)
    the_form = MyForm()
    the_form.show()
    sys.exit(app.exec_())
# END DO NOT MODIFY