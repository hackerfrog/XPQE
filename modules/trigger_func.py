from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QTextCursor

from logger import log

from PyQt5.QtWidgets import QFileDialog, QMessageBox

from gui.ProfileManager import ProfileManager


def open_profile_manager(profiler):
    """
    Open Profile Manager dialog
    :param profiler: object of Profiler class
    :return: None
    """
    profile_manger = ProfileManager(profiler)


def toggle_check(element, state):
    """
    Toggle function to Show/Hide given PyQt element
    :param element: PyQt element object
    :param state: current state of element
    :return: None
    """
    if state:
        element.show()
    else:
        element.hide()


def copy_cell():
    """
    Manual Copy function when Copy Menu Item is click
    :return: None
    """
    # TODO: Create manual copy feature
    log.info('Copy Cell')


def save_file(editor, file_manager):
    """
    Save file when Save Menu Item or Shortcut is triggered
    :param editor: PyQt editor element
    :param file_manager: object of FileManger class
    :return: None
    """
    editor_text = editor.toPlainText()

    if file_manager.location:
        # if location exisit in file manger then just overwrite file without opening save dialog
        log.debug('Had file location : {}, Overwriting on same path'.format(file_manager.location))
        with open(file_manager.location, 'w') as file:
            file.write(editor_text)
        log.info('File Saved @ {}'.format(file_manager.location))

        log.debug('Updating file context details')
        file_manager.set_hash(editor_text)
    else:
        # if location is None then it's a new file
        save_file_dialog = QFileDialog.getSaveFileName(None, 'Save', '/', 'Cross SQL Files (*.xsql)')

        if save_file_dialog[0]:
            with open(save_file_dialog[0], 'w') as file:
                file.write(editor_text)
            log.info('File Saved @ {}'.format(save_file_dialog[0]))

            log.debug('Updating file context details')
            file_manager.set_hash(editor_text)
            file_manager.set_location(save_file_dialog[0])


def new_file(editor, file_manager):
    """
    Open new empty file on editor when New Menu Item or Shortcut is triggered
    :param editor: object of editor
    :param file_manager: object of FileManger class
    :return: None
    """
    editor_text = editor.toPlainText()
    # check change in content of editor before opening new empty file
    if file_manager.compare_hash(editor_text):
        # Hash matched means no changes, directly open new empty file
        log.debug('Clearing editor')
        editor.setPlainText('')
        log.debug('Resetting file context details')
        file_manager.reset()
    else:
        # Changes found open confirmation dialog
        alert_message = QMessageBox()
        alert_message.setIcon(QMessageBox.Warning)
        alert_message.setText('You are having unsaved changes...')
        alert_message.setWindowTitle('Unsaved Changes Alter!')
        alert_message.setStandardButtons(QMessageBox.Save | QMessageBox.Ignore | QMessageBox.Cancel)

        alert_action = alert_message.exec()
        if alert_action == QMessageBox.Save:
            save_file(editor, file_manager)
            new_file(editor, file_manager)
        elif alert_action == QMessageBox.Ignore:
            file_manager.reset(string=editor_text)
            new_file(editor, file_manager)
        elif alert_message == QMessageBox.Cancel:
            pass


def open_file(editor, file_manager):
    """
    Open file from user disk
    :param editor: object of editor
    :param file_manager: object of FileManger class
    :return: None
    """
    open_file_dialog = QFileDialog.getOpenFileName(None, 'Open', '/')

    if open_file_dialog[0]:
        log.info('Opening File @ {}'.format(open_file_dialog[0]))
        with open(open_file_dialog[0], 'r') as file:
            file_text = file.read()

        editor.setPlainText(file_text)

        log.debug('Updating file context details')
        file_manager.set_hash(file_text)
        file_manager.set_location(open_file_dialog[0])
        log.debug('Complete File Openning @ {}'.format(open_file_dialog[0]))


def save_as_file(editor, file_manager):
    """
    Save file without checking any constrains
    :param editor: object of editor
    :param file_manager: object of FileManager class
    :return: None
    """
    save_as_file_dialog = QFileDialog.getSaveFileName(None, 'Save As', '/', 'Cross SQL Files (*.xsql)')

    if save_as_file_dialog[0]:
        editor_text = editor.toPlainText()
        with open(save_as_file_dialog[0], 'w') as file:
            file.write(editor_text)
        log.info('File Saved @ {}'.format(save_as_file_dialog[0]))

        log.debug('Updating file context details')
        file_manager.set_hash(editor_text)
        file_manager.set_location(save_as_file_dialog[0])


def undo_text(editor):
    """
    Undo feature of editor
    :param editor: object to editor
    :return: None
    """
    editor.undo()


def redo_text(editor):
    """
    Redo feature of editor
    :param editor: object to editor
    :return: None
    """
    editor.redo()


def cut_text(editor):
    """
    Cut selected text from an editor
    :param editor: object to editor
    :return: None
    """
    editor.cut()


def copy_text(editor):
    """
    Copy selected text from an editor
    :param editor: object to editor
    :return: None
    """
    editor.copy()


def paste_text(editor):
    """
    Paste text from clipboard to editor
    :param editor: object to editor
    :return: None
    """
    editor.paste()


def toggle_line_comment(editor):
    """
    Toggle comment on line with current location of editor cursor
    :param editor: object of editor
    :return:None
    """
    COMMENT_CHARS = '-- '

    cursor = editor.textCursor()
    # get start and end position of selected text
    selection_start = cursor.selectionStart()
    selection_end = cursor.selectionEnd()

    # get block numbers of start and positions
    cursor.setPosition(selection_start)
    start_block = cursor.blockNumber()
    cursor.setPosition(selection_end)
    end_block = cursor.blockNumber()

    # move cursor to starting of first line
    cursor.movePosition(QTextCursor.Start)
    cursor.movePosition(QTextCursor.NextBlock, n=start_block)

    # comment/uncomment each selected line
    for _ in range(0, end_block - start_block + 1):
        cursor.movePosition(QTextCursor.StartOfLine)
        pos1 = cursor.position()
        cursor.movePosition(QTextCursor.EndOfLine)
        pos2 = cursor.position()

        # check if current line is empty, then just add comment
        if pos1 == pos2:
            cursor.movePosition(QTextCursor.StartOfLine)
            cursor.insertText(COMMENT_CHARS)
            cursor.movePosition(QTextCursor.NextBlock)
            continue

        # select first 3 chars of line
        cursor.movePosition(QTextCursor.StartOfLine)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
        text = cursor.selectedText()
        print(text)

        # line is already commented or not
        if text == COMMENT_CHARS:
            cursor.removeSelectedText()
        else:
            cursor.movePosition(QTextCursor.StartOfLine)
            cursor.insertText(COMMENT_CHARS)
        # move to next line block
        cursor.movePosition(QTextCursor.NextBlock)


def toggle_auto_commit(context, state):
    context['server.autocommit'] = state


def run_xsql(editor, engine_manager):
    """
    Run XSQL query
    :param editor: object of editor
    :param engine_manager: object of EngineManager class
    :return: None
    """
    cursor = editor.textCursor()
    xsql = cursor.selectedText()
    if len(xsql) == 0:
        xsql = editor.toPlainText()
    log.info(xsql)

    engine_manager.parse(xsql)


def fmt(color, style=''):
    """
    Creates format for syntax highlighter
    :param color: color name or hex code of color
    :param style: text weight style
    :return: object of QTextCharFormat class
    """
    _color = QColor()
    _color.setNamedColor(color)

    _fmt = QTextCharFormat()
    _fmt.setForeground(_color)
    if 'bold' in style:
        _fmt.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _fmt.setFontItalic(True)

    return _fmt
