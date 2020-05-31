import pdftotext
import sys, getopt

if __name__=="__main__":
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(sys.argv[1:],"hi:o:")
   except getopt.GetoptError:
      print('pdftotxt.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('pdftotxt.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt == "-i":
         inputfile = arg
      elif opt == "-o":
         outputfile = arg
   with open(inputfile, "rb") as f:
         pdf = pdftotext.PDF(f)
   with open(outputfile, 'w') as f:
         f.write("\n\n".join(pdf))