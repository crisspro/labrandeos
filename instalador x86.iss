#define MyAppName "Labrandeos"
#define MyAppVersion "2.0"
#define MyAppPublisher "Crisspro"
#define MyAppURL "https://github.com/crisspro/labrandeos"
#define MyAppExeName "Labrandeos.exe"
#define MyAppAssocName MyAppName + " File"
#define MyAppAssocExt ".lap"
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt

[Setup]
MinVersion=10.0
AppId={{0ADF5CAD-AACB-4B5C-9F22-2BA42A27B55C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
ChangesAssociations=yes
DisableProgramGroupPage=yes
LicenseFile=C:\Users\criss\Desktop\proyectos python\Labrandeos\LICENSE.txt
OutputDir=C:\Users\criss\Desktop
OutputBaseFilename=Labrandeos v{#MyAppVersion} x86 installer
Compression=lzma
SolidCompression=yes
WizardStyle=modern
CloseApplications=yes
CloseApplicationsFilter=*.exe
VersionInfoVersion={#MyAppVersion}
VersionInfoDescription={#MyAppName} Installer
VersionInfoCompany={#MyAppPublisher}
VersionInfoCopyright=© 2025 {#MyAppPublisher}
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\criss\Desktop\proyectos python\Labrandeos\build\exe.win32-3.12\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion sign
Source: "C:\Users\criss\Desktop\proyectos python\Labrandeos\build\exe.win32-3.12\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\criss\Desktop\proyectos python\Labrandeos\LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion

[Registry]
Root: HKCR; Subkey: ".lap"; ValueType: string; ValueName: ""; ValueData: "Labrandeos"; Flags: uninsdeletevalue
Root: HKCR; Subkey: "Labrandeos"; ValueType: string; ValueName: ""; ValueData: "Archivo de Labrandeos"; Flags: uninsdeletekey
Root: HKCR; Subkey: "Labrandeos\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"
Root: HKCR; Subkey: "Labrandeos\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""
Root: HKCR; Subkey: "Labrandeos\SupportedTypes"; ValueType: string; ValueName: ".lap"; ValueData: ""

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[UninstallDelete]
Type: filesandordirs; Name: "{localappdata}\Labrandeos"
Type: dirifempty; Name: "{app}"

[Messages]
CloseApplicationsFilter=Labrandeos debe cerrarse antes de continuar.

[Code]
function InitializeSetup(): Boolean;
var
  UninstallString: String;
  ResultCode: Integer;
  UninstallMsg, CannotContinueMsg, ErrorMsg: String;
begin
  Result := True;

  // Definir mensajes según el idioma seleccionado
  if ActiveLanguage = 'english' then
  begin
    UninstallMsg := 'A previous version of Labrandeos was detected. It needs to be uninstalled before continuing.' + #13#10 + #13#10 +
      'Do you want to uninstall the previous version now?';
    CannotContinueMsg := 'Setup cannot continue without uninstalling the previous version.';
    ErrorMsg := 'Error uninstalling previous version. Code: ';
  end
  else
  begin
    UninstallMsg := 'Se detectó una versión anterior de Labrandeos. Es necesario desinstalarla antes de continuar.' + #13#10 + #13#10 +
      '¿Desea desinstalar la versión anterior ahora?';
    CannotContinueMsg := 'La instalación no puede continuar sin desinstalar la versión anterior.';
    ErrorMsg := 'Error al desinstalar la versión anterior. Código: ';
  end;

  if RegQueryStringValue(HKLM,
    'Software\Microsoft\Windows\CurrentVersion\Uninstall\{0ADF5CAD-AACB-4B5C-9F22-2BA42A27B55C}_is1',
    'UninstallString', UninstallString) then
  begin
    if MsgBox(UninstallMsg, mbInformation, MB_YESNO) = IDYES then
    begin
      UninstallString := RemoveQuotes(UninstallString);
      if not Exec(UninstallString, '/SILENT', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
      begin
        MsgBox(ErrorMsg + IntToStr(ResultCode), mbError, MB_OK);
        Result := False;
      end;
    end
    else begin
      MsgBox(CannotContinueMsg, mbInformation, MB_OK);
      Result := False;
    end;
  end;
end;