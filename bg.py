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
		# avoid "/openssl", "/etc/openssl" error
		repo_name = i.replace('/', '_')

		# cleanup
		os.system("rm -rf %s " % repo_name)

		# step1: git clone --no-checkout https://github.com/openssl/openssl.git openssl
		os.system("git clone -q --no-checkout %s %s" % (data[i]["origin"], repo_name))

		# step2: git -C openssl remote add backup https://github.com/HuKeping/openssl.git
		os.system("git -C %s remote add backup %s " % (repo_name, data[i]["backup"]))

		for j in data[i]["branch"] or []:
			# step3-1: git -C openssl push backup refs/remotes/origin/OpenSSL_1_1_1-stable:refs/heads/OpenSSL_1_1_1-stable_force -f
			if os.system("git -C %s push -q backup refs/remotes/origin/%s:refs/heads/%s_force -f " % (repo_name, j, j)) == 0:
				print("-- Sync %s:%s_force OK" % (repo_name, j))
			else:
				print("-- Sync %s:%s_force Fail" % (repo_name, j))

			# step3-2: git -C openssl push backup refs/remotes/origin/OpenSSL_1_1_1-stable:refs/heads/OpenSSL_1_1_1-stable
			if os.system("git -C %s push -q backup refs/remotes/origin/%s:refs/heads/%s " % (repo_name, j, j)) == 0:
				print("-- Sync %s:%s OK" % (repo_name, j))
			else:
				print("-- Sync %s:%s Fail" % (repo_name, j))

		for j in data[i]["tag"] or []:
			# step4-1: git -C openssl push backup refs/tags/OpenSSL_1_1_1g:refs/tags/OpenSSL_1_1_1g_force -f
			if os.system("git -C %s push -q backup refs/tags/%s:refs/tags/%s_force -f " % (repo_name, j, j)) == 0:
				print("-- Sync %s:%s_force OK" % (repo_name, j))
			else:
				print("-- Sync %s:%s_force Fail" % (repo_name, j))

			# step4-2: git -C openssl push backup refs/tags/OpenSSL_1_1_1g:refs/tags/OpenSSL_1_1_1g
			if os.system("git -C %s push -q backup refs/tags/%s:refs/tags/%s " % (repo_name, j, j)) == 0:
				print("-- Sync %s:%s OK" % (repo_name, j))
			else:
				print("-- Sync %s:%s Fail" % (repo_name, j))

if __name__ == "__main__":
	main()
