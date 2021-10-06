import os
import json
from pathlib import Path
import shutil
import sys

from utils.tagspaces_getter import Tags
import tagdefs

class ModelDef:
	def __hash__(self):
		pass
	
	def __eq__(self):
		pass

def main():
	#namespace = input("Namespace: ")
	folder = "miniaturia"
	namespace = "miniaturia_mod"

	os.chdir(folder)

	json_files = [file for file in os.listdir("./blockstates") if file.endswith(".json")]
	fails = list()

	for filename in json_files:
		print("Process " + filename)
		try:
			states_path = Path("./blockstates/" + filename)
			states_json = json.loads(states_path.read_text())
			if "forge_marker" not in states_json:
				fails.append(filename)
				print(filename, "Not ForgeBlockState!")
				continue
			if "variants" not in states_json:
				print(filename, "No variants")
				input()
				continue
			default = None
			if "defaults" in states_json:
				default = states_json["defaults"]["model"]
			for variant in states_json["variants"].keys():
				variant = states_json["variants"][variant]
				model_def = ModelDef()
				print(variant)
				model_def.model = variant["model"]
			#print(states_json)
			
			"""
			tags = Tags(model_path)
			skip = False
			for prefix in skip_prefixes:
				if filename.startswith(prefix):
					print("Skip template model " + prefix)
					skip = True
					break
			if skip:
				tags.add(tagdefs.skip)
				continue
			
			with open(model_path) as json_file:
				json_text = json.load(json_file)
				glass = filename.startswith("window_")
				cutout = False
				solid = False
				if glass:
					cutout = True
				elif "leaves" in filename:
					cutout = True
				elif filename.startswith("neon_"):
					tags.add(tagdefs.layer.translucent)
				
				if "parent" in json_text:
					parent = json_text["parent"]
					if parent in skip_models:
						print("Skip " + json_text["parent"])
						tags.add(tagdefs.skip)
						continue
					if parent in block_models:
						solid = True
					elif parent.startswith("block/cube"):
						solid = True
					if not cutout:
						if parent in cutout_models:
							cutout = True
				elif "textures" not in json_text:
					print("Skip template model")
					tags.add(tagdefs.skip)
					continue
				if not cutout:
					for prefix in cutout_prefixes:
						if filename.startswith(prefix):
							cutout = True
							break
					
				if glass:
					tags.add(tagdefs.glass)
				if cutout:
					tags.add(tagdefs.layer.cutout)
					if solid:
						tags.add(tagdefs.shape_block)
				elif solid:
					tags.add(tagdefs.template.block)
			"""
				
		except Exception as e:
			print(e)
			raise e
			fails.append(filename)

	print("Fails:\n" + "\n".join(fails))

main()
