set s = CreateObject("SAPI.SpVoice")
s.Speak Wscript.Arguments(0), 3
s.WaitUntilDone(30000)