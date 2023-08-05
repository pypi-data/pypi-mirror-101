r"""
Objects for storing and producing objective values for comparing experimental data to EOS predictions.    
"""

import numpy as np
import logging

from despasito.thermodynamics import thermo
from despasito.fit_parameters import fit_funcs as ff
from despasito.fit_parameters.interface import ExpDataTemplate

##################################################################
#                                                                #
#                       Liquid Density                           #
#                                                                #
##################################################################
class Data(ExpDataTemplate):

    r"""
    Object for liquid density data. This data is evaluated with "liquid_properties". 

    Parameters
    ----------
    data_dict : dict
        Dictionary of exp data of type rhol.

        * name : str, data type, in this case RhoL
        * calctype : str, Optional, default: 'liquid_properties'
        * T : list, List of temperature values for calculation
        * xi : list, List of liquid mole fractions used in liquid_properties calculations
        * weights : list/float, Either a list as long as the number of data points to multiply by the objective value associated with each point, or a float to multiply the objective value of this data set.
        * rhodict : dict, Optional, default: {"minrhofrac":(1.0 / 60000.0), "rhoinc":10.0, "vspacemax":1.0E-4}, Dictionary of options used in calculating pressure vs. mole fraction curves.

    Attributes
    ----------
    name : str
        Data type, in this case rhol
    calctype : str, Optional, default: 'liquid_properties'
        Thermodynamic calculation type
    T : list
        List of temperature values for calculation
    xi : list
        List of liquid mole fractions, sum(xi) should equal 1
    """

    def __init__(self, data_dict):

        logger = logging.getLogger(__name__)

        # Self interaction parameters
        self.name = data_dict["name"]
        try:
            self.calctype = data_dict["calctype"]
        except:
            self.calctype = "liquid_properties"

        data_type = []
        data_type_name = []
        if "xi" in data_dict:
            self.xi = data_dict["xi"]
            data_type.append(self.xi)
            data_type_name.append("xi")
        if "T" in data_dict:
            self.T = data_dict["T"]
            data_type.append(self.T)
            data_type_name.append("T")
        if "rhol" in data_dict:
            self.rhol = data_dict["rhol"]
            data_type.append(self.rhol)
            data_type_name.append("rhol")
        if "P" in data_dict:
            if (type(P) == float or len(P)==1):
                self.P = np.ones(self.T)*P
            else:
                self.P = P
        else:
            self.P = np.ones(self.T)*101325.0
            logger.info("Assume atmospheric pressure")
        data_type.append(self.P)
        data_type_name.append("P")

        tmp = ["xi","T","rhol"]
        if not all([hasattr(self,x) for x in tmp]):
            raise ImportError("Given liquid property data, values for T, xi, and rhol should have been provided.")

        try:
            self.weights = data_dict["weights"]
        except:
            self.weights = 1.0

        try:
            self._rhodict = data_dict["rhodict"]
        except:
            self._rhodict = {"minrhofrac":(1.0 / 300000.0), "rhoinc":10.0, "vspacemax":1.0E-4}

        logger.info("Data type 'liquid_properties' initiated with calctype, {}, and data types: {}".format(self.calctype,", ".join(data_type_name)))

    def _thermo_wrapper(self, eos):

        """
        Generate thermodynamic predictions from eos object

        Parameters
        ----------
        eos : obj
            EOS object with updated parameters

        Returns
        -------
        phase_list : float
            A list of the predicted thermodynamic values estimated from thermo calculation. This list can be composed of lists or floats
        """

        try:
            output_dict = thermo(eos,{"calculation_type":self.calctype,"Tlist":self.T,"xilist":self.xi,"Plist":self.P,"rhodict":self._rhodict})
            output = output_dict["rhol"]
        except:
            raise ValueError("Calculation of calc_rhol failed")
        return output


    def objective(self, eos):

        """
        Generate objective function value from this dataset

        Parameters
        ----------
        eos : obj
            EOS object with updated parameters

        Returns
        -------
        obj_val : float
            A value for the objective function
        """

        phase_list = self._thermo_wrapper(eos)

        # Reformat array of results
        phase_list, len_list = ff.reformat_ouput(phase_list) 
        phase_list = np.transpose(np.array(phase_list))

        # objective function
        obj_value = np.sum((((phase_list[0] - self.rhol) / self.rhol)**2)*self.weights)

        return obj_value

    def __str__(self):

        string = "Data Set Object\nname: %s\ncalctype:%s\nNdatapts:%g" % {self.name, self.calctype, len(self.T)}
        return string
