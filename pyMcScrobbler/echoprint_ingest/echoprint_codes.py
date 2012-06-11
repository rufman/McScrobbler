import os, json, sys
import subprocess

def main(echoprint_loc, root_dir):
	ingest_file = open('music_to_ingest.json', 'wr+')
	args = ['%s/echoprint-codegen' % (echoprint_loc)];
	ingest_file.write("[")
	
	for root, dirs, files in os.walk(root_dir):
		for f in files:
			args.append(os.path.join(root, f));
			p = subprocess.Popen(args, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			output, errors = p.communicate()
			output = eval(output)
			try:
				code = output[0]['code']
				for item in ingest_file.readlines():
					item = eval(item)
					if item[0]['code'] == code:
						print "already fingerprinted song %s by %s" % (output[0]['metadata']['title'], output[0]['metadata']['artist'])
				else:
					ingest_file.write(str(output[0])+',')

			except KeyError:
				pass
			args.pop()
	
	ingest_file.write("]")
	
if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2])
