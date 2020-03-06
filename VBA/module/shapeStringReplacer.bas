' HowToUse
' 1.Create Module in VBA
' 2.Paste this module
' 3.Write "RepText(A,B)"

Option Explicit

Public Function RepText(ByRef findStr As String, ByRef repStr As String)

    Dim sh As Shape

    For Each sh In ActiveSheet.Shapes
        If sh.TextFrame2.HasText = msoTrue Then
            sh.TextFrame2.TextRange.Text = Replace(sh.TextFrame2.TextRange.Text, findStr, repStr)
        End If
    Next

End Function