# PDF 转换成 图片
# Poppler是用于呈现可移植文档格式(PDF)文档的免费软件实用程序库。
# 用了subprocess.Popen来运行pdftoppm
# Windows版的pdftoppm.exe可以在这下载：http://blog.alivate.com.au/poppler-windows/
#
'''
Usage: pdftoppm [options] [PDF-file [PPM-file-prefix]]
  -f <int>                 : first page to print
  -l <int>                 : last page to print
  -o                       : print only odd pages
  -e                       : print only even pages
  -singlefile              : write only the first page and do not add digits
  -r <fp>                  : resolution, in DPI (default is 150)
  -rx <fp>                 : X resolution, in DPI (default is 150)
  -ry <fp>                 : Y resolution, in DPI (default is 150)
  -scale-to <int>          : scales each page to fit within scale-to*scale-to pixel box
  -scale-to-x <int>        : scales each page horizontally to fit in scale-to-x pixels
  -scale-to-y <int>        : scales each page vertically to fit in scale-to-y pixels
  -x <int>                 : x-coordinate of the crop area top left corner
  -y <int>                 : y-coordinate of the crop area top left corner
  -W <int>                 : width of crop area in pixels (default is 0)
  -H <int>                 : height of crop area in pixels (default is 0)
  -sz <int>                : size of crop square in pixels (sets W and H)
  -cropbox                 : use the crop box rather than media box
  -mono                    : generate a monochrome PBM file
  -gray                    : generate a grayscale PGM file
  -png                     : generate a PNG file
  -jpeg                    : generate a JPEG file
  -jpegopt <string>        : jpeg options, with format <opt1>=<val1>[,<optN>=<valN>]*
  -tiff                    : generate a TIFF file
  -tiffcompression <string>: set TIFF compression: none, packbits, jpeg, lzw, deflate
  -freetype <string>       : enable FreeType font rasterizer: yes, no
  -thinlinemode <string>   : set thin line mode: none, solid, shape. Default: none
  -aa <string>             : enable font anti-aliasing: yes, no
  -aaVector <string>       : enable vector anti-aliasing: yes, no
  -opw <string>            : owner password (for encrypted files)
  -upw <string>            : user password (for encrypted files)
  -q                       : don't print any messages or errors
  -v                       : print copyright and version info
  -h                       : print usage information
  -help                    : print usage information
  --help                   : print usage information
  -?                       : print usage information
'''
import subprocess

pathPdftoppm = r'.\poppler-0.68.0\bin\pdftoppm.exe' #Windows版的pdftoppm.exe路径
pathPdf = r't.pdf' #PDF 文件路径
strCmd = "{} -jpeg {} out".format(pathPdftoppm, pathPdf)
subprocess.Popen(strCmd)

print("转换完成")
