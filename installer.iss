[Setup]
AppName=My AI Human
AppVersion=1.0
DefaultDirName={pf}\MyAIHuman
DefaultGroupName=MyAIHuman
OutputDir=installer
OutputBaseFilename=MyAIHumanSetup

[Files]
Source: "dist\app.exe"; DestDir: "{app}"
Source: "dist\service.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\My AI Human"; Filename: "{app}\app.exe"

[Run]
Filename: "{app}\service.exe"; Description: "Start AI Service"; Flags: nowait postinstall
