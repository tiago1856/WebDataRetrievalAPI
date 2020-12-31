
import WebDataRetrieval as dr

try:
	s = dr.WebDataRetrieval()	
	print (s.getData("racius", "HEMOVIDA Lda"))
	print (s.getData("codigopostal.ciberforma", "HEMOVIDA Lda", nif=506036944))
	print (s.getData("portugalio", "HEMOVIDA Lda"))
	print (s.getData("einforma", "HEMOVIDA Lda", nif=506036944))
	print (s.getData("nif", "HEMOVIDA Lda", nif=506036944))
	print (s.getAll(name="HEMOVIDA Lda", nif=506036944, key_google=YOUR_KEY))
	print (s.getServices())
	print (s.getBaseUrls())	
	print (s.getData("google", name="HEMOVIDA Lda", country="portugal", key_google=YOUR_KEY))
	print (s.getData("nif", name="HEMOVIDA Lda", nif=506036944, key_nif=YOUR_KEY))
except Exception as e:
	print (e)

