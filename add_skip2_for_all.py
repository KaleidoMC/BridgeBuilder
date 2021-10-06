from utils.tagspaces_getter import Tags
from pathlib import Path
import tagdefs

import os
import json
from pathlib import Path
import shutil
import sys

from utils.tagspaces_getter import Tags
import tagdefs

def main():
	#namespace = input("Namespace: ")
	#folder = "cocricot"
	#namespace = "cocricotmod"
	folder = "yuushya"
	namespace = "yuushya"

	os.chdir(folder)

	json_files = []
	for root, dirs, files in os.walk("./models"):
		if root.endswith(".ts"):
			continue
		root = root.replace("/models", "", 1)
		for name in files:
			if name.endswith(".json"):
				json_files.append(root + "/" + name)

	for filename in json_files:
		print("Process " + filename)

		model_path = os.path.join("./models", filename)
		tags = Tags(model_path)
		tags.remove("skip")
		tags.add(tagdefs.skip2)

main()
