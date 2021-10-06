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

def dumpRes(namespace, filename):
	override = Path("./override_resources/" + filename)
	if override.exists():
		if override.stat().st_size != 0:
			shutil.copyfile(override, os.path.join("./resources", filename))
	else:
		path = Path("./resources/" + filename)
		path.parent.mkdir(parents=True, exist_ok=True)
		with open(path, "w+") as f:
			resources = dict()
			if namespace == "cocricotmod":
				filename = "block/" + filename
			resources["parent"] = namespace + ":" + filename.replace("\\", "/")[:len(filename)-5]
			json.dump(resources, f, sort_keys=True, indent=2)

def main():
	#namespace = input("Namespace: ")
	folder = "cocricot"
	namespace = "cocricotmod"
	#folder = "yuushya"
	#namespace = "yuushya"

	os.chdir(folder)

	try:
		shutil.rmtree("./data")
		shutil.rmtree("./resources")
	except OSError as e:
		#print("Error: %s - %s." % (e.filename, e.strerror))
		pass
	Path("./data").mkdir(parents=True, exist_ok=True)
	Path("./resources").mkdir(parents=True, exist_ok=True)

	json_files = []
	for root, dirs, files in os.walk("./models"):
		if root.endswith(".ts"):
			continue
		root = root.replace("/models", "", 1)
		for name in files:
			if name.endswith(".json"):
				json_files.append(root + "/" + name)
	fails = list()
	tag_map = {}
	tag_map["block"] = ("template", "block")
	tag_map["directional"] = ("template", "directional")
	tag_map["horizontal"] = ("template", "horizontal")
	tag_map["pillar"] = ("template", "pillar")
	tag_map["glass"] = ("glass", True)
	tag_map["shape-block"] = ("shape", "block")
	tag_map["cutout"] = ("renderType", "cutout")
	tag_map["cutoutMipped"] = ("renderType", "cutoutMipped")
	tag_map["translucent"] = ("renderType", "translucent")

	# 6131 files
	for filename in json_files:
		filename = filename[2:]
		print("Process " + filename)
		try:
			override = Path("./override_data/" + filename)
			if override.exists():
				if override.stat().st_size != 0:
					shutil.copyfile(override, os.path.join("./data", filename))
					dumpRes(namespace, filename)
				continue

			model_path = os.path.join("./models", filename)
			tags = Tags(model_path).tags
			if "skip" in tags or "skip2" in tags:
				continue
			
			data = {}
			for tag in tags:
				if tag.startswith("g."):
					data["group"] = namespace + ":" + tag[2:]
				if tag not in tag_map:
					continue
				pair = tag_map[tag]
				data[pair[0]] = pair[1]
			
			path = Path("./data/" + filename)
			path.parent.mkdir(parents=True, exist_ok=True)
			with open(path, "w+") as f:
				json.dump(data, f, sort_keys=True, indent=2)
			dumpRes(namespace, filename)
		except Exception as e:
			print(e)
			fails.append(filename)

	print("Fails:\n" + "\n".join(fails))

main()
