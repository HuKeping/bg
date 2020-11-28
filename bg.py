#!/usr/bin/env python3

import os
import subprocess
import yaml

def main():
	
	with open("backup_list.yaml", "r") as stream:
		try:
			data = yaml.safe_load(stream)
		except:
			print(yaml.YAMLError)

	for i in data:
		# cleanup
		os.system("rm -rf %s " % i)

		# step1: git clone --no-checkout https://github.com/openssl/openssl.git openssl
		os.system("git clone -q --no-checkout %s %s" % (data[i]["origin"], i))

		# step2: git -C openssl remote add backup https://github.com/HuKeping/openssl.git
		os.system("git -C %s remote add backup %s " % (i, data[i]["backup"]))
		
		for j in data[i]["branch"] or []:
			# step3-1: git -C openssl push backup refs/remotes/origin/OpenSSL_1_1_1-stable:refs/heads/OpenSSL_1_1_1-stable_force -f
			if os.system("git -C %s push -q backup refs/remotes/origin/%s:refs/heads/%s_force -f " % (i, j, j)) == 0:
				print("-- Sync %s:%s_force OK" % (i, j))
			else:
				print("-- Sync %s:%s_force Fail" % (i, j))

			# step3-2: git -C openssl push backup refs/remotes/origin/OpenSSL_1_1_1-stable:refs/heads/OpenSSL_1_1_1-stable
			if os.system("git -C %s push -q backup refs/remotes/origin/%s:refs/heads/%s " % (i, j, j)) == 0:
				print("-- Sync %s:%s OK" % (i, j))
			else:
				print("-- Sync %s:%s Fail" % (i, j))

		for j in data[i]["tag"] or []:
			# step4-1: git -C openssl push backup refs/tags/OpenSSL_1_1_1g:refs/tags/OpenSSL_1_1_1g_force -f
			if os.system("git -C %s push -q backup refs/tags/%s:refs/tags/%s_force -f " % (i, j, j)) == 0:
				print("-- Sync %s:%s_force OK" % (i, j))
			else:
				print("-- Sync %s:%s_force Fail" % (i, j))

			# step4-2: git -C openssl push backup refs/tags/OpenSSL_1_1_1g:refs/tags/OpenSSL_1_1_1g
			if os.system("git -C %s push -q backup refs/tags/%s:refs/tags/%s " % (i, j, j)) == 0:
				print("-- Sync %s:%s OK" % (i, j))
			else:
				print("-- Sync %s:%s Fail" % (i, j))

if __name__ == "__main__":
	main()
