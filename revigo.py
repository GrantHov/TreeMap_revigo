"""
This script automatically retrieves the REVIGO R script and generates the TreeMap plot.

The input file is a list of GO enrichment analysis files.

For example, the "list_of_files.txt" should look like:
homeologs_30C_12C_SC_Component_Down.txt
homeologs_30C_12C_SC_Component_UP.txt
homeologs_30C_12C_SC_Function_Down.txt
homeologs_30C_12C_SC_Function_UP.txt

Each of GO enrichment files should be formatted as (standard SGD GO enrichment file):

GOID	TERM	CORRECTED_PVALUE	UNCORRECTED_PVALUE	NUM_LIST_ANNOTATIONS	LIST_SIZE	TOTAL_NUM_ANNOTATIONS	POPULATION_SIZE	FDR_RATE	EXPECTED_FALSE_POSITIVES	ANNOTATED_GENES
GO:0034470	ncRNA processing	7.90E-09	9.20E-12	48	252	471	7166	0.00%	0	YHR196W, YOL077C, YDR021W, YLR222C, YOR274W, YNL207W, YGR145W, YLR197W, YPL081W, YDR045C, YDR165W, YNL182C, YHR088W, YJL098W, YLR063W, YGR081C, YPL146C, YBR142W, YKL021C, YGR128C, YNL147W, YHR197W, YJR041C, YNL110C, YOL144W, YKR060W, YNL002C, YPR144C, YHR065C, YLR002C, YMR259C, YBL071W-A, YJL010C, YDR083W, YKL014C, YKR081C, YJL109C, YNL119W, YOR310C, YNR038W, YKL078W, YMR093W, YOR287C, YOR004W, YGL171W, YNL062C, YDR449C, YHR052W
GO:0006364	rRNA processing	2.13E-08	2.48E-11	40	252	353	7166	0.00%	0	YNL147W, YGR128C, YHR197W, YBR142W, YKL021C, YNL110C, YJR041C, YLR063W, YGR081C, YPL146C, YPL081W, YNL182C, YHR088W, YOL077C, YHR196W, YDR021W, YGR145W, YNL207W, YLR197W, YLR222C, YGL171W, YOR004W, YOR287C, YHR052W, YDR449C, YOR310C, YMR093W, YNR038W, YKL078W, YJL010C, YKL014C, YDR083W, YKR081C, YJL109C, YNL002C, YKR060W, YOL144W, YPR144C, YLR002C, YHR065C
GO:0042254	ribosome biogenesis	3.85E-08	4.49E-11	47	252	475	7166	0.00%	0	YGR145W, YOL127W, YNL207W, YLR197W, YLR222C, YOL077C, YHR196W, YDR021W, YNL182C, YHR088W, YGL099W, YPL081W, YIL052C, YPL146C, YGR081C, YLR063W, YNL110C, YJR041C, YHR197W, YGR128C, YNL147W, YKL021C, YBR142W, YLR002C, YHR065C, YOL144W, YKR060W, YNL002C, YPR144C, YDL063C, YKR081C, YJL109C, YJL010C, YOR340C, YKL014C, YDR083W, YNR053C, YMR093W, YKL078W, YNR038W, YOR310C, YHR052W, YDR449C, YDR101C, YGL171W, YOR004W, YOR287C

"""


from robobrowser import RoboBrowser
import subprocess
import re


with open("list_of_files.txt","r+") as filenames:
	for filename in filenames.readlines():
		print filename
		filename=filename.rstrip()
		goterms_file=open(filename,"r+")
		goterms=""
		for line in goterms_file.readlines():
			if line.startswith("GOID"):
				continue
			elif line.startswith("GO:"):
				
				line=line.rstrip().split("\t")
				line=line[0]+" "+line[2] 
				goterms=goterms + "\n" + line.rstrip()
			else:
				print line
				break
	
		if len(goterms)>0:
			#~ #print goterms
			name_for_r=filename.split(".")[0] + ".R"
			rscript=open(name_for_r,"w")

			br = RoboBrowser(parser="lxml")
			br.open("http://revigo.irb.hr/")

			form = br.get_form()
			form["goList"].value = goterms
	
			br.submit_form(form)
	
			download_rsc_link = br.find("a", href=re.compile("toR_treemap.jsp"))
			br.follow_link(download_rsc_link)
			r_code = br.response.content.decode("utf-8")
			r_code = r_code.replace("lot more","\npng('./%s.png', units='in', width=10, heigh=7, res=400)"%(filename.split(".")[0])).replace("pdf(","#pdf(").replace("REVIGO Gene Ontology treemap",filename.split(".")[0])
			#print r_code
			rscript.write(r_code)
	
			goterms_file.close()
			rscript.close()
			subprocess.call("Rscript "+name_for_r,shell=True)
	

#~ download_csv_link = br.find("a", href=re.compile("export.jsp"))
#~ br.follow_link(download_csv_link)
#~ csv_content = br.response.content.decode("utf-8")
#~ print(csv_content)
