; ============================================================
; BXZ-lang Installer
; Version: v1.2.2.1
; Developer: BXZ Language Team
; Company: BoxZero, Inc.
; ============================================================

#define MyAppName "BXZ-lang"
#define MyAppVersion "1.2.2.1"
#define MyAppPublisher "BoxZero, Inc."
#define MyAppURL "https://www.boxzero.ir/"
#define MyAppExeName "bxz.exe"

; ============================================================
; BXZ FILE ASSOCIATION
; ============================================================

#define MyAppAssocName "BXZ Source File"
#define MyAppAssocExt ".bxz"
#define MyAppAssocKey "BXZFile"

#define DoubleAmp(Value) StringChange(Value, "&", "&&")


; ============================================================
; SETUP
; ============================================================

[Setup]

AppId={{DDC4FBE4-AD6D-40C0-862B-C6F68D4C4B74}

AppName={#MyAppName}
AppVersion={#MyAppVersion}

AppPublisher={#MyAppPublisher}

AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; ------------------------------------------------------------
; Installation directory
; ------------------------------------------------------------

DefaultDirName=C:\BXZ

DefaultGroupName=BXZ-Lang

DisableProgramGroupPage=yes
AllowNoIcons=yes

; ------------------------------------------------------------
; Architecture
; ------------------------------------------------------------

ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; ------------------------------------------------------------
; File associations
; ------------------------------------------------------------

ChangesAssociations=yes

; ------------------------------------------------------------
; Administrator privileges
; Required for system PATH
; ------------------------------------------------------------

PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=commandline

; ------------------------------------------------------------
; Icons
; ------------------------------------------------------------

SetupIconFile=C:\Users\samya\Desktop\bxz-lang\bxz-install.ico

UninstallDisplayIcon={app}\bxz.exe

; ------------------------------------------------------------
; Installer output
; ------------------------------------------------------------

OutputBaseFilename=BXZ-Setup

Compression=lzma
SolidCompression=yes

WizardStyle=modern dark

; ------------------------------------------------------------
; License
; ------------------------------------------------------------

LicenseFile=C:\Users\samya\Documents\licanse\License.txt


; ============================================================
; TASKS
; ============================================================

[Tasks]

Name: "desktopicon"; \
    Description: "{cm:CreateDesktopIcon}"; \
    GroupDescription: "{cm:AdditionalIcons}"; \
    Flags: unchecked


; ============================================================
; FILES
; ============================================================

[Files]

; ------------------------------------------------------------
; BXZ compiler
; ------------------------------------------------------------

Source: "C:\Users\samya\Desktop\bxz-lang\target\debug\bxz.exe"; \
    DestDir: "{app}"; \
    Flags: ignoreversion

; ------------------------------------------------------------
; BXZ file icon
; ------------------------------------------------------------

Source: "C:\Users\samya\Desktop\bxz-lang\assets\bxz-file.ico"; \
    DestDir: "{app}\assets"; \
    Flags: ignoreversion

; ------------------------------------------------------------
; Application icon
; ------------------------------------------------------------

Source: "C:\Users\samya\Desktop\bxz-lang\assets\bxz.ico"; \
    DestDir: "{app}\assets"; \
    Flags: ignoreversion skipifsourcedoesntexist

; ------------------------------------------------------------
; PNG assets
; ------------------------------------------------------------

Source: "C:\Users\samya\Desktop\bxz-lang\assets\bxz.png"; \
    DestDir: "{app}\assets"; \
    Flags: ignoreversion skipifsourcedoesntexist

Source: "C:\Users\samya\Desktop\bxz-lang\assets\bxz-file.png"; \
    DestDir: "{app}\assets"; \
    Flags: ignoreversion skipifsourcedoesntexist


; ============================================================
; REGISTRY
; ============================================================

[Registry]

; ------------------------------------------------------------
; .bxz extension
; ------------------------------------------------------------

Root: HKCR; \
    Subkey: "{#MyAppAssocExt}"; \
    ValueType: string; \
    ValueName: ""; \
    ValueData: "{#MyAppAssocKey}"; \
    Flags: uninsdeletevalue

; ------------------------------------------------------------
; BXZFile ProgID
; ------------------------------------------------------------

Root: HKCR; \
    Subkey: "{#MyAppAssocKey}"; \
    ValueType: string; \
    ValueName: ""; \
    ValueData: "{#MyAppAssocName}"; \
    Flags: uninsdeletekey

; ------------------------------------------------------------
; BXZ file icon
; ------------------------------------------------------------

Root: HKCR; \
    Subkey: "{#MyAppAssocKey}\DefaultIcon"; \
    ValueType: string; \
    ValueName: ""; \
    ValueData: "{app}\assets\bxz-file.ico,0"

; ------------------------------------------------------------
; Open .bxz with BXZ
; ------------------------------------------------------------

Root: HKCR; \
    Subkey: "{#MyAppAssocKey}\shell\open\command"; \
    ValueType: string; \
    ValueName: ""; \
    ValueData: """{app}\{#MyAppExeName}"" ""%1"""


; ============================================================
; START MENU / DESKTOP
; ============================================================

[Icons]

Name: "{group}\{#MyAppName}"; \
    Filename: "{app}\{#MyAppExeName}"

Name: "{group}\{cm:ProgramOnTheWeb,{#MyAppName}}"; \
    Filename: "{#MyAppURL}"

Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; \
    Filename: "{uninstallexe}"

Name: "{autodesktop}\{#MyAppName}"; \
    Filename: "{app}\{#MyAppExeName}"; \
    Tasks: desktopicon


; ============================================================
; RUN AFTER INSTALL
; ============================================================

[Run]

Filename: "{app}\{#MyAppExeName}"; \
    Description: "{cm:LaunchProgram,{#DoubleAmp(MyAppName)}}"; \
    Flags: nowait postinstall skipifsilent


; ============================================================
; CODE
; ============================================================

[Code]

const
  EnvironmentKey =
    'SYSTEM\CurrentControlSet\Control\Session Manager\Environment';
    

function NormalizePathEntry(S: String): String;
begin
  S := Trim(S);

  while (Length(S) > 0) and
        ((S[Length(S)] = '\') or
         (S[Length(S)] = '/')) do
  begin
    Delete(S, Length(S), 1);
  end;

  Result := Uppercase(S);
end;


function PathContainsBXZ(PathValue: String): Boolean;
var
  Entry: String;
  P: Integer;
  BXZPath: String;
begin
  Result := False;

  BXZPath := ExpandConstant('{app}');

  while Length(PathValue) > 0 do
  begin
    P := Pos(';', PathValue);

    if P > 0 then
    begin
      Entry := Copy(PathValue, 1, P - 1);
      Delete(PathValue, 1, P);
    end
    else
    begin
      Entry := PathValue;
      PathValue := '';
    end;

    if NormalizePathEntry(Entry) =
       NormalizePathEntry(BXZPath) then
    begin
      Result := True;
      Exit;
    end;
  end;
end;

function AddBXZToPath(): Boolean;
var
  CurrentPath: String;
  BXZPath: String;
begin
  Result := False;

  BXZPath := ExpandConstant('{app}');

  if not RegQueryStringValue(
    HKEY_LOCAL_MACHINE,
    EnvironmentKey,
    'Path',
    CurrentPath
  ) then
  begin
    CurrentPath := '';
  end;
  
  if PathContainsBXZ(CurrentPath) then
  begin
    Result := True;
    Exit;
  end;

  if CurrentPath = '' then
  begin
    CurrentPath := BXZPath;
  end
  else
  begin
    CurrentPath := CurrentPath + ';' + BXZPath;
  end;

  Result :=
    RegWriteExpandStringValue(
      HKEY_LOCAL_MACHINE,
      EnvironmentKey,
      'Path',
      CurrentPath
    );
end;

function RemoveBXZFromPath(): Boolean;
var
  CurrentPath: String;
  NewPath: String;
  Entry: String;
  BXZPath: String;
  P: Integer;
  FirstEntry: Boolean;
begin
  Result := False;

  BXZPath := ExpandConstant('{app}');

  if not RegQueryStringValue(
    HKEY_LOCAL_MACHINE,
    EnvironmentKey,
    'Path',
    CurrentPath
  ) then
  begin
    Result := True;
    Exit;
  end;

  NewPath := '';
  FirstEntry := True;

  while Length(CurrentPath) > 0 do
  begin
    P := Pos(';', CurrentPath);

    if P > 0 then
    begin
      Entry := Copy(CurrentPath, 1, P - 1);
      Delete(CurrentPath, 1, P);
    end
    else
    begin
      Entry := CurrentPath;
      CurrentPath := '';
    end;

    if NormalizePathEntry(Entry) <>
       NormalizePathEntry(BXZPath) then
    begin
      if not FirstEntry then
      begin
        NewPath := NewPath + ';';
      end;

      NewPath := NewPath + Entry;
      FirstEntry := False;
    end;
  end;

  Result :=
    RegWriteExpandStringValue(
      HKEY_LOCAL_MACHINE,
      EnvironmentKey,
      'Path',
      NewPath
    );
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    AddBXZToPath();
  end;
end;

procedure CurUninstallStepChanged(
  CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    RemoveBXZFromPath();
  end;
end;