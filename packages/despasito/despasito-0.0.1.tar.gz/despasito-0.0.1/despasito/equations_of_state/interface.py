"""
    Interface needed to create further equation of state (EOS) objects. 

    All folders in this directory refer back to this interface. Using this template all future EOS will be easily exchanged.
    
"""

# All folders in this directory refer back to this interface

from abc import ABC, abstractmethod


# __________________ EOS Interface _________________
class EOStemplate(ABC):

    """
    Interface used in all EOS object options.

    By using this template, all EOS objects are then easily exchanged.
    """

    @abstractmethod
    def P(self, rho, T, xi):
        """
        Output pressure value predicted by EOS.
        """
        pass

    @abstractmethod
    def fugacity_coefficient(self, P, rho, xi, T):
        """
        Output chemical potential predicted by EOS.
        """
        pass

    @abstractmethod
    def density_max(self, xi, T):
        """
        Output maximum packing density predicted by EOS.
        """
        pass

    @abstractmethod
    def param_guess(self, fit_params):
        """
        Output a guess for the given parameter type.
        """
        pass

    @abstractmethod
    def update_parameters(self, param_name, bead_names, param_value):
        """
        Update a given parameter in EOS.
        """
        pass

