/********************************************************************************
** Form generated from reading UI file 'widget.ui'
**
** Created by: Qt User Interface Compiler version 5.11.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_WIDGET_H
#define UI_WIDGET_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QLabel>
#include <QtWidgets/QPlainTextEdit>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_Widget
{
public:
    QPushButton *pushButton;
    QLabel *time;
    QPlainTextEdit *id;
    QLabel *label;
    QLabel *true_2;
    QLabel *boder;
    QPushButton *yes;
    QPushButton *no;

    void setupUi(QWidget *Widget)
    {
        if (Widget->objectName().isEmpty())
            Widget->setObjectName(QStringLiteral("Widget"));
        Widget->resize(430, 575);
        Widget->setStyleSheet(QStringLiteral("background-color: rgb(0, 0, 0);"));
        pushButton = new QPushButton(Widget);
        pushButton->setObjectName(QStringLiteral("pushButton"));
        pushButton->setGeometry(QRect(150, 550, 121, 25));
        time = new QLabel(Widget);
        time->setObjectName(QStringLiteral("time"));
        time->setGeometry(QRect(0, 0, 111, 61));
        time->setStyleSheet(QLatin1String("color: rgb(0, 255, 0);\n"
"font: 26pt \"Quicksand\";"));
        id = new QPlainTextEdit(Widget);
        id->setObjectName(QStringLiteral("id"));
        id->setGeometry(QRect(0, 430, 431, 121));
        id->setStyleSheet(QStringLiteral("font: 75 18pt \"Quicksand\";"));
        label = new QLabel(Widget);
        label->setObjectName(QStringLiteral("label"));
        label->setGeometry(QRect(110, 60, 261, 361));
        true_2 = new QLabel(Widget);
        true_2->setObjectName(QStringLiteral("true_2"));
        true_2->setGeometry(QRect(190, 0, 241, 61));
        true_2->setStyleSheet(QLatin1String("\n"
"color: rgb(0, 255, 0);\n"
"font: 10pt \"Quicksand\";"));
        boder = new QLabel(Widget);
        boder->setObjectName(QStringLiteral("boder"));
        boder->setGeometry(QRect(40, 60, 341, 341));
        boder->setStyleSheet(QLatin1String("\n"
"border:10px solid rgb(0,255,0);"));
        yes = new QPushButton(Widget);
        yes->setObjectName(QStringLiteral("yes"));
        yes->setGeometry(QRect(0, 550, 99, 30));
        no = new QPushButton(Widget);
        no->setObjectName(QStringLiteral("no"));
        no->setGeometry(QRect(330, 550, 99, 30));

        retranslateUi(Widget);

        QMetaObject::connectSlotsByName(Widget);
    } // setupUi

    void retranslateUi(QWidget *Widget)
    {
        Widget->setWindowTitle(QApplication::translate("Widget", "Widget", nullptr));
        pushButton->setText(QApplication::translate("Widget", "Register", nullptr));
        time->setText(QString());
        label->setText(QString());
        true_2->setText(QString());
        boder->setText(QString());
        yes->setText(QApplication::translate("Widget", "YES", nullptr));
        no->setText(QApplication::translate("Widget", "NO", nullptr));
    } // retranslateUi

};

namespace Ui {
    class Widget: public Ui_Widget {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_WIDGET_H
