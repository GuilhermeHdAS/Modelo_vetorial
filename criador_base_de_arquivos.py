arquivobase = open("base.txt","w")
base = arquivobase.write("a.toy\nb.toy\nc.toy\nd.toy")
arquivobase.close()

arquivoconsulta = open("consulta.txt","w")
consulta = arquivoconsulta.write("W & Y")
arquivoconsulta.close()

arquivo1 = open("a.toy","w")
arq1 = arquivo1.write("W W W X")
arquivo1.close()

arquivo2 = open("b.toy","w")
arq2 = arquivo2.write("W W Y")
arquivo2.close()

arquivo3 = open("c.toy","w")
arq3 = arquivo3.write("W W")
arquivo3.close()

arquivo4 = open("d.toy","w")
arq4 = arquivo4.write("X X")
arquivo4.close()