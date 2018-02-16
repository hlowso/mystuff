import mystuff.mytheory.hard_coded
import mystuff.mytheory.general
import mystuff.mytheory.jazz 
import mystuff.mytheory.bass.walk 

class Bassist(mystuff.mytheory.jazz.Comper):
	def __init__(self, bass):
		mystuff.mytheory.jazz.Comper.__init__(self, bass)
		self.comp_styles['swung'] = mystuff.mytheory.bass.walk.walk
