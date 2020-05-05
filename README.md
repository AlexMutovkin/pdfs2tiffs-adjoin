# pdfs2tiffs-adjoin

Script for Ligron company.

Goal:

conversion and join of the PDF files in the TIFF

Details:

converting PDFs in the working path to TIFFs and collecting them
in the multipage TIFFs, sorted by 8-digit order number taken from 
a PDF's file name.

Example:

№ 72011159

c:\temp\555\72011159_jjjl.pdf -> c:\temp\555\72011159_jjjl.tif

№ 72011159

...no need to join files

№ 72011352

c:\temp\555\72011352.pdf -> c:\temp\555\72011352.tif

c:\temp\555\72011352 plan.pdf -> c:\temp\555\72011352 plan.tif

c:\temp\555\72011352 sheet2.pdf -> c:\temp\555\72011352 sheet2.tif

c:\temp\555\72011352.tif >> c:\temp\555\72011352_ALL_IN_ONE.tif

c:\temp\555\72011352 plan.tif +> c:\temp\555\72011352_ALL_IN_ONE.tif

c:\temp\555\72011352 sheet2.tif +> c:\temp\555\72011352_ALL_IN_ONE.tif

