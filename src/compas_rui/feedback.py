import rhinoscriptsyntax as rs  # type: ignore


def confirm(message):
    result = rs.MessageBox(message, buttons=4 | 32 | 256 | 0, title="Confirmation")
    return result == 6


def warn(message):
    return rs.MessageBox(message, title="Warning")
