class Drummer(mystuff.mytheory.jazz.Comper):
	def __init__(self, kit):
		mystuff.mytheory.jazz.Comper.__init__(self, kit)
		self.comp_styles['swung'] = mystuff.mytheory.kit.swung_groove.groove()