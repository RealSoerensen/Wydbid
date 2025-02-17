import os
import pickle
from PyQt5.QtWidgets import QComboBox, QMessageBox, QWidget
from Data import Company
import Wydbid


def addItems(companylist: QComboBox):
    l = f'{Wydbid.location}Companies/'
    files = []

    for folder in os.listdir(l):
        for file in os.listdir(l + folder):
            if file.endswith('.wbf'):
                files.append(f'{l}{folder}/{file}')

    for n_file in files:
        try:
            n = open(n_file, 'rb')
        except:
            QMessageBox.about(Wydbid.app.parent(), 'Warning',
                              'Something went wrong!')
            return

        try:
            company: Company.Company = pickle.load(n)
        except:
            QMessageBox.about(Wydbid.app.parent(), 'Warning',
                              'Something went wrong!')
            return

        companylist.addItem(company.name, [company, n_file])


def changePasswordFinal(companybox: QComboBox, old_password: str, new_password: str, widget: QWidget):
    if old_password == '' or new_password == '':
        QMessageBox.warning(Wydbid.app.parent(), 'Warning',
                            'All fields must be filled in!')
        return

    company: Company.Company = companybox.currentData()[0]

    if not old_password == company.password:
        QMessageBox.warning(Wydbid.app.parent(), 'Attention',
                            'The password you entered is incorrect!')
        return

    company.password = new_password
    writer = open(companybox.currentData()[1], 'wb')
    pickle.dump(company, writer, pickle.HIGHEST_PROTOCOL)
    writer.close()

    QMessageBox.about(Wydbid.app.parent(), 'Process completed',
                      f'The password of {company.name} was successfully changed.')

    m = QMessageBox.question(Wydbid.app.parent(),
                             'Restart Wydbid',
                             'Attention, you need to restart Wydbid to make the changes! Do you want to restart now?',
                             QMessageBox.Yes,
                             QMessageBox.No)

    if m == QMessageBox.No:
        widget.close()
        return

    elif m == QMessageBox.Yes:
        Wydbid.app.exit(0)
