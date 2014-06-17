# -*- mode: python -*-
backend_mod_names = ('file', 'Gnome', 'Google', 'keyczar', 'kwallet', 'multi','OS_X', 'pyfs', 'SecretService', 'Windows')
a = Analysis(['main.py'],
             pathex=['/media/roger/Storage/aiudirog/GoogleVoiceLinuxClient'],
             hiddenimports = ['keyring.backends.file',
                 'keyring.backends.Gnome',
                 'keyring.backends.Google',
                 'keyring.backends.keyczar',
                 'keyring.backends.kwallet',
                 'keyring.backends.multi',
                 'keyring.backends.OS_X',
                 'keyring.backends.pyfs',
                 'keyring.backends.SecretService',
                 'keyring.backends.Windows',
                 'keyring.util'],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Google Voice Linux Client',
          icon="/media/roger/Storage/aiudirog/GoogleVoiceLinuxClient/resources/google-voice-icon.png",
          debug=False,
          strip=None,
          upx=True,
          console=False )
