import classes


def read_header(file, gif):
    gif.version = file.read(6)


def read_LSD(file, gif):
    block = file.read(7)
    LSD = {}
    packed = {}
    gif.width = block[0:1]
    gif.height = block[2:3]
    packedBytes = block[4]
    gif.GCT
    packed['GCTFlag'] = get_bits(packedBytes, 0)
    packed['colorResolution'] = get_bits(packedBytes, 1, 3)
    packed['sortFlag'] = get_bits(packedBytes, 4)
    packed['sizeOfGCT'] = get_bits(packedBytes, 5, 7)
    LSD['packed'] = packed
    LSD['backgroundColor'] = block[5]
    LSD['pixelAspectRatio'] = block[6]
    gif["LSD"] = LSD


def read_GCT(file):
    GCT_size = 2 ** (int(gif.get('LSD').get('packed').get('sizeOfGCT'), 2) + 1)
    gif['GCT'] = file.read(3 * GCT_size)


def read_Application_Extension(file):
    application = {}
    application['sizeApplicationBlock'] = file.read(1)
    application['applicationIdentifier'] = file.read(8)
    application['applicationAuthenticationCode'] = file.read(3)
    data = b""
    while byte := file.read(1) != b'\x00':
        data += byte
    application['data'] = data
    gif['applicationExtension'] = application


def read_Graphic_Control_Extension(file):
    graphicControl = {}
    packed = {}
    graphicControl['sizeGraphicControlBlock'] = file.read(1)
    packedBlock = file.read(1)
    packed['reserved'] = get_bits(packedBlock[0], 0, 2)
    packed['disposalMethod'] = get_bits(packedBlock[0], 3, 5)
    packed['userInputFlag'] = get_bits(packedBlock[0], 6)
    packed['transparentColorFlag'] = get_bits(packedBlock[0], 7)
    graphicControl['packed'] = packed
    gif['graphicControlExtension'] = graphicControl


def image_descriptor(file):
    imageDescriptor = {}
    packed = {}
    imageDescriptor['imageLeft'] = file.read(2)
    imageDescriptor['imageTop'] = file.read(2)
    imageDescriptor['imageWidth'] = file.read(2)
    imageDescriptor['imageHeight'] = file.read(2)
    packedBlock = file.read(1)
    packed['localColorTableFlag'] = get_bits(packedBlock, 0)
    packed['interlaceFlag'] = get_bits(packedBlock, 1)
    packed['sortFlag'] = get_bits(packedBlock, 2)
    packed['reserved'] = get_bits(packedBlock, 3, 4)
    packed['sizeLocalColorTableFlag'] = get_bits(packedBlock, 5, 7)
    imageDescriptor['packed'] = packed
    gif['imageDescriptor'] = imageDescriptor


def read_local_color_table(file):
    LCT_size = 2 ** (gif.get('imageDescriptor').get('packed').get('sizeOfGCT') + 1)
    gif['LCT'] = file.read(LCT_size)


def read_image_data(file):
    imageData = {}
    imageData['LZWCodeSize'] = file.read(1)
    data = b""
    while byte := file.read(1) != b'\x00':
        data += byte
    imageData['data'] = data
    gif['imageData'] = imageData


def read_comment_extension(file):
    commentExtension = {}
    data = b""
    while byte := file.read(1) != b'\x00':
        data += byte
    commentExtension['data'] = data
    gif['commentExtension'] = commentExtension


def read_plain_text(file):
    plainText = {}
    plainText['blockSize'] = file.read(1)
    plainText['gridLeftPosition'] = file.read(2)
    plainText['gridTopPosition'] = file.read(2)
    plainText['gridWidth'] = file.read(2)
    plainText['gridHeight'] = file.read(2)
    plainText['charCellWidth'] = file.read(1)
    plainText['charCellHeight'] = file.read(1)
    plainText['TextColor'] = file.read(1)
    plainText['TextBackground'] = file.read(1)

    data = b""
    while byte := file.read(1) != b'\x00':
        data += byte
    plainText['data'] = data
    gif['plainTextExtension'] = plainText


def main():
    gif = classes.Gif()
    with open("try.gif", "rb") as file:
        read_header(file)
        read_LSD(file)
        if gif.get('LSD').get('packed').get('GCTFlag') == '1':
            read_GCT(file)

        while True:

            extensionIntroducer = file.read(1)

            if extensionIntroducer == b'\x21':
                extensionLabel = file.read(1)

                if extensionLabel == b'\xFF':
                    read_Application_Extension(file)

                elif extensionLabel == b'\xF9':
                    read_Graphic_Control_Extension(file)

                elif extensionLabel == b'\xFE':
                    read_comment_extension(file)

                elif extensionLabel == b'\x01':
                    read_plain_text(file)

            elif extensionIntroducer == b'\x2C':
                image_descriptor(file)

                if gif.get('imageDescriptor').get('packed').get('localColorTableFlag') == 1:
                    read_local_color_table(file)

                read_image_data(file)
            else:
                break
    print(gif)

