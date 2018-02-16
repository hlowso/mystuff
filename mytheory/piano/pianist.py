import mystuff.mytheory.hard_coded
import mystuff.mytheory.general
import mystuff.mytheory.jazz 
import mystuff.mytheory.piano.swung_comp

class Pianist(mystuff.mytheory.jazz.Comper):
	def __init__(self, piano):
		mystuff.mytheory.jazz.Comper.__init__(self, piano)
		self.comp_styles['swung'] = mystuff.mytheory.piano.swung_comp.outline