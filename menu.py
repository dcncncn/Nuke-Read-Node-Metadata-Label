
import nuke


def _read_metadata(node, key):
    try:
        value = node.metadata(key)
        return value if value is not None else None
    except Exception:
        return None


def update_read_label(node=None):
    if node is None:
        nodes = nuke.selectedNodes('Read')
    else:
        nodes = [node]

    for read in nodes:
        try:
            first = int(read['origfirst'].value())
            last = int(read['origlast'].value())
            count = last - first + 1

            colorspace = read['colorspace'].value()

            # Resolution
            width = _read_metadata(read, 'input/width')
            height = _read_metadata(read, 'input/height')

            if not width or not height:
                fmt = read.format()
                width = fmt.width()
                height = fmt.height()

            # FPS
            fps = _read_metadata(read, 'input/frame_rate')

            if fps is None:
                fps = nuke.root()['fps'].value()

            # Codec
            codec = _read_metadata(read, 'quicktime/codec_name')

            if not codec:
                codec = 'N/A'

            # Colored Read Label
            label = (
                '<font color="#005BFF"><b>Frame:</b> {} - {}</font>\n'
                '<font color="#FFF28A"><b>Count:</b> ({})</font>\n'
                '<font color="#7FFF00"><b>Colorspace:</b> {}</font>\n'
                '<font color="#35D8FF"><b>Format:</b> {}x{}</font>\n'
                '<font color="#B000FF"><b>Fps:</b> {:.3f}</font>\n'
                '<font color="#FF40C8"><b>Code:</b> {}</font>'
            ).format(
                first,
                last,
                count,
                colorspace,
                int(width),
                int(height),
                float(fps),
                codec
            )

            read['label'].setValue(label)

        except Exception as exc:
            nuke.tprint(
                'Read label update failed: {} ({})'.format(
                    read.name(), exc
                )
            )


# Automatically update new Read nodes
def auto_update_read_label():
    read = nuke.thisNode()

    try:
        from PySide6.QtCore import QTimer
    except ImportError:
        try:
            from PySide2.QtCore import QTimer
        except ImportError:
            update_read_label(read)
            return

    QTimer.singleShot(
        0,
        lambda node=read: update_read_label(node)
    )


# Menu and shortcut
nuke.menu('Nuke').addCommand(
    'Custom/Update Read Label',
    update_read_label,
    'Ctrl+Alt+R'
)


# Auto-update when creating Read nodes
nuke.addOnUserCreate(
    auto_update_read_label,
    nodeClass='Read'
)
