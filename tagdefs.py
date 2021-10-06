from utils.tagspaces_getter import TagDef

class layer:
	def __init__(self):
		self.cutout = TagDef("cutout", "#cd74e6ff", "white")
		self.cutoutMipped = TagDef("cutoutMipped", "#cd74e6ff", "white")
		self.translucent = TagDef("translucent", "#cd74e6ff", "white")

class template:
	def __init__(self):
		self.block = TagDef("block", "#008000ff", "white")
		self.horizontal = TagDef("horizontal", "#008000ff", "white")
		self.directional = TagDef("directional", "#008000ff", "white")
		self.pillar = TagDef("pillar", "#008000ff", "white")
		self.item = TagDef("item", "#008000ff", "white")

skip = TagDef("skip", "#fa573cff", "white")
skip2 = TagDef("skip2", "#fa573cff", "white")
glass = TagDef("glass", "#fa573cff", "white")
shape_block = TagDef("shape-block", "#fa573cff", "white")
template = template()
layer = layer()
