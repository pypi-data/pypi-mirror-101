class Character:
    
    def __init__(self, string):
        
        """ Character class for character manipulation
        
        Attributes:
            string (string) representing a string to be manipulated
        """
        
        self.str = string
        
    def reverse_character(self):
    
        """Function to reverse a string 
        
        Args:
            none
        
        Returns:
            Reversed string
        
        """
        return self.str[::-1]
        