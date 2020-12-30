
import WebDataRetrieval as dr

try:
	s = dr.WebDataRetrieval()	
	#print (s.getData("racius", "HEMOVIDA Lda"))
	#print (s.getData("codigopostal.ciberforma", "HEMOVIDA Lda", 506036944))
	#print (s.getData("portugalio", "HEMOVIDA Lda"))
	#print (s.getData("einforma", "HEMOVIDA Lda", 506036944))
	#pprint (s.getData("nif", "HEMOVIDA Lda", 506036944))
	#print (s.getAll(name="HEMOVIDA Lda", nif=506036944))

	#print (s.getServices())
	#print (s.getBaseUrls())	
except Exception as e:
	print (e)
