#Place this python script in a folder, it will create a html gallery for it

import sys,os

root = "./"
path = os.path.join(root, "targetdirectory")

f = open("html_gallery.html", "a")
f.write("<html><head><style>body{overflow-x: scroll;width: auto;white-space: nowrap;}</style></head><body>\n")
f.write("<script>\n")
f.write("setInterval(scrollWin, 15);\n")
f.write("function scrollWin() {\n")
f.write("    window.scrollBy(2, 0);\n")

f.write("    if(document.body.scrollLeft + window.innerWidth >= document.body.scrollWidth){\n")
f.write("        window.scrollTo(0, 0);\n")
f.write("    }\n")

f.write("}\n")
f.write("document.body.onkeyup = function(e){\n")
f.write("    if(e.keyCode == 32){\n")
f.write("        window.scrollBy(1000, 0);\n")
f.write("    }\n")
f.write("}\n")
f.write("</script>\n")

for path, subdirs, files in os.walk(root):
    for name in files:
        if name.endswith(".jpg") or name.endswith(".png") or name.endswith(".webp")or name.endswith(".jpeg"):
            f.write("<img src='" + os.path.join(path, name) + "' height='900'>\n")

f.write("</body></html>")
f.close()
