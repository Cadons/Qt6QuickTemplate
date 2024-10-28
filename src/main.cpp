// QmlProjectTemplateVCPGK.cpp : Defines the entry point for the application.
//

#include "main.h"
#include <QGuiApplication>
#include <QQMLApplicationEngine>
#include <QLoggingCategory>
#include <QDir>
using namespace std;

int main(int argc, char* argv[]) {
	QGuiApplication app(argc, argv);
	QQmlApplicationEngine engine;
	engine.addImportPath(app.applicationDirPath() + QDir::separator() + "qml");
	qDebug() << "Import paths:" << engine.importPathList(); // Debugging line
	engine.load("qrc:/app.qml");
	app.exec();

	return 0;
}
