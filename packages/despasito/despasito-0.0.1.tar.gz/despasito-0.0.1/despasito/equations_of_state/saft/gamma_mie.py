# -- coding: utf8 --

r"""
    
    EOS object for SAFT-:math:`\gamma`-Mie
    
    Equations referenced in this code are from V. Papaioannou et al J. Chem. Phys. 140 054107 2014
    
"""

import numpy as np
import logging

from . import constants
from . import gamma_mie_funcs as funcs
# Later this line will be in an abstract class file in this directory, and all versions of SAFT will reference it
from despasito.equations_of_state.interface import EOStemplate

# ________________ Saft Family ______________
# NoteHere: Insert SAFT family abstract class in this directory to clean up


class saft_gamma_mie(EOStemplate):

    r"""
    Initialize EOS object for SAFT-:math:`\gamma`-Mie.
    
    All input and calculated parameters are defined as hidden attributes.
    
    Parameters
    ----------
    beads : list[str]
        List of unique bead names used among components
    nui : numpy.ndarray
        :math:`\\nu_{i,k}/k_B`. Array of number of components by number of bead types. Defines the number of each type of group in each component.
    beadlibrary : dict
        A dictionary where bead names are the keys to access EOS self interaction parameters:

        - epsilon: :math:`\epsilon_{k,k}/k_B`, Energy well depth scaled by Boltzmann constant
        - sigma: :math:`\sigma_{k,k}`, Size parameter [m]
        - mass: Bead mass [kg/mol]
        - l_r: :math:`\lambda^{r}_{k,k}`, Exponent of repulsive term between groups of type k
        - l_a: :math:`\lambda^{a}_{k,k}`, Exponent of attractive term between groups of type k\
        - Vks: :math:`V_{k,s}`, Number of groups, k, in component
        - Sk: Optional, :math:`S_{k}`, Shape parameter of group k
        - epsilon*: Optional, Interaction energy between each bead and association site. Asterisk represents string from sitenames.
        - K**: Optional, Bonding volume between each association site. Asterisk represents two strings from sitenames.
        - Nk*: Optional, The number of sites of from list sitenames. Asterisk represents string from sitenames.

    crosslibrary : dict, Optional, default: {}
        Optional library of bead cross interaction parameters. As many or as few of the desired parameters may be defined for whichever group combinations are desired.

        - epsilon: :math:`\epsilon_{k,l}/k_B`, Energy parameter scaled by Boltzmann Constant
        - l_r: :math:`\lambda^{r}_{k,l}`, Exponent of repulsive term between groups of type k and l
        - epsilon*: Optional, Interaction energy between each bead and association site. Asterisk represents string from sitenames.
        - K**: Optional, Bonding volume between each association site. Asterisk represents two strings from sitenames.

    sitenames : list[str], Optional, default: ["H", "e1", "e2"]
        List of unique association sites used among components
        
    Attributes
    ----------
    T : float, default: numpy.nan
        Temperature value is initially defined as NaN for a placeholder until temperature dependent attributes are initialized by using a method of this class.
    
    """

    def __init__(self, kwargs):

        #logger = logging.getLogger(__name__)

        # Self interaction parameters
        self._nui = kwargs['nui']
        self._beads = kwargs['beads']
        self._beadlibrary = kwargs['beadlibrary']

        massi = np.zeros(len(self._nui))
        for i in range(len(self._nui)):
            for k in range(np.size(self._beads)):
                massi[i] += self._nui[i, k] * self._beadlibrary[self._beads[k]]["mass"]
        self._massi = massi

        # Cross interaction parameters
        if 'crosslibrary' in list(kwargs.keys()):
            crosslibrary = kwargs['crosslibrary']
        else:
            crosslibrary = {}

        epsilonkl, sigmakl, l_akl, l_rkl, Ckl = funcs.calc_interaction_matrices(self._beads, self._beadlibrary, crosslibrary=crosslibrary)

        self._crosslibrary = crosslibrary
        self._epsilonkl = epsilonkl
        self._sigmakl = sigmakl
        self._l_akl = l_akl
        self._l_rkl = l_rkl
        self._Ckl = Ckl

        # Association sites
        if 'sitenames' in list(kwargs.keys()):
            self._sitenames = kwargs['sitenames']
        else:
            self._sitenames = ["H", "e1", "e2"]

        epsilonHB, Kklab, nk = funcs.calc_assoc_matrices(self._beads, self._beadlibrary, sitenames=self._sitenames, crosslibrary=self._crosslibrary)

        self._epsilonHB = epsilonHB
        self._Kklab = Kklab
        self._nk = nk

        # Initialize temperature attribute
        self.T = np.nan

    def _temp_dependent_variables(self, T):

        """
        Temperature dependent variables are initialized or updated.
    
        Parameters
        ----------
        T : float, default: numpy.nan
            Temperature of the system [K]
    
        Attributes
        ----------
        T : float, default: numpy.nan
            Temperature of the system
        """

        #logger = logging.getLogger(__name__)

        dkk, dkl, x0kl = funcs.calc_hard_sphere_matricies(self._beads, self._beadlibrary, self._sigmakl, T)
        self.T = T
        self._dkk = dkk
        self._dkl = dkl
        self._x0kl = x0kl

    def _xi_dependent_variables(self, xi):

        """
        Variables dependent on composition are initialized or updated.
    
        Parameters
        ----------
        xi : list[float]
            Mole fraction of component

        """

        #logger = logging.getLogger(__name__)

        Cmol2seg, xsk, xskl = funcs.calc_composition_dependent_variables(xi, self._nui, self._beads, self._beadlibrary)
        self._Cmol2seg = Cmol2seg
        self._xsk = xsk
        self._xskl = xskl

    def P(self, rho, T, xi):
        """
        Compute pressure given system information.
       
        Parameters
        ----------
        rho : numpy.ndarray
            Number density of system [mol/m^3]
        T : float
            Temperature of the system [K]
        xi : list[float]
            Mole fraction of each component
       
        Returns
        -------
        P : numpy.ndarray
            Array of pressure values [Pa] associated with each density and so equal in length
        """

        #logger = logging.getLogger(__name__)

        if len(xi) != len(self._nui):
            raise ValueError("Number of components in mole fraction list doesn't match components in nui. Check bead_config.")

        if T != self.T:
            self._temp_dependent_variables(T)

        self._xi_dependent_variables(xi)
        
        if np.isscalar(rho):
            rho = np.array([rho])
        elif type(rho) != np.ndarray:
            rho = np.array(rho)

        rho = rho*constants.Nav

        step = np.sqrt(np.finfo(float).eps) *rho * 10000.0
        # Decreasing step size by 2 orders of magnitude didn't reduce noise in P values
        nrho = np.size(rho)

        # computer rho+step and rho-step for better a bit better performance
        A = funcs.calc_A(np.append(rho + step, rho - step), xi, T, self._beads, self._beadlibrary, self._massi, self._nui, self._Cmol2seg, self._xsk, self._xskl, self._dkk, self._epsilonkl, self._sigmakl, self._dkl, self._l_akl, self._l_rkl, self._Ckl,self._x0kl, self._epsilonHB, self._Kklab, self._nk)

        P_tmp = (A[:nrho]-A[nrho:])*((constants.kb*T)/(2.0*step))*rho**2

        return P_tmp

    def fugacity_coefficient(self, P, rho, xi, T, dy=1e-4):

        """
        Compute fugacity coefficient.
      
        Parameters
        ----------
        P : float
            Pressure of the system [Pa]
        rho : float
            Molar density of system [mol/m^3]
        T : float
            Temperature of the system [K]
        xi : list[float]
            Mole fraction of each component
    
        Returns
        -------
        mui : numpy.ndarray
            Array of chemical potential values for each component
        """

        #logger = logging.getLogger(__name__)

        if len(xi) != len(self._nui):
            raise ValueError("Number of components in mole fraction list doesn't match components in nui. Check bead_config.")

        if T != self.T:
            self._temp_dependent_variables(T)

        self._xi_dependent_variables(xi)

        Z = P / (rho * T * constants.Nav * constants.kb)
        phi_tmp = np.zeros(len(xi))

#        #### Traditional Central Difference Method
#        # Set step size in finite difference method
#        exp = np.floor(np.log10(rho))-3 # Make sure step size is three orders of magnitude lower
#        drho = 10**exp
#        logger.debug("    Compute phi for density, {}, with step size {}.".format(rho,drho))
#
#        # compute phi
#        Ares = funcs.calc_Ares(rho *  constants.Nav, xi, T, self._beads, self._beadlibrary, self._massi, self._nui, self._Cmol2seg, self._xsk, self._xskl, self._dkk, self._epsilonkl, self._sigmakl, self._dkl, self._l_akl, self._l_rkl, self._Ckl,self._x0kl, self._epsilonHB, self._Kklab, self._nk)
#        rhoi = rho*np.array(xi,float)
#        for i in range(np.size(phi_tmp)):
#            dAres = np.zeros(2)
#            for j, delta in enumerate((drho, -drho)):
#                rhoi_temp = np.copy(rhoi)
#                if rhoi_temp[i] != 0.:
#                    rhoi_temp[i] += delta
#                dAres[j] = self._calc_dAres_drhoi_wrap(T, rhoi_temp)
#            phi_tmp[i] = Ares + rho*(dAres[0] - dAres[1]) / (2.0 * drho) - np.log(Z) 
#            #with open("OldPhi.csv","a") as f:
#            #    f.write("{}, {}, {}, {}, {}, {}, {}\n".format(i,xi[i],phi_tmp[i], Ares, rho, dAres, drho))

        #### Transform y=log(rhoi) Central Difference Method without worrying about negative mole fractions 
        # Set step size in finite difference method
        y = np.log(rho*np.array(xi,float))
        #dy = 0.05

        # compute phi
        Ares = funcs.calc_Ares(rho *  constants.Nav, xi, T, self._beads, self._beadlibrary, self._massi, self._nui, self._Cmol2seg, self._xsk, self._xskl, self._dkk, self._epsilonkl, self._sigmakl, self._dkl, self._l_akl, self._l_rkl, self._Ckl,self._x0kl, self._epsilonHB, self._Kklab, self._nk)
        for i in range(np.size(phi_tmp)):
            if xi[i] != 0.0:
                dAres = np.zeros(2)
                for j, delta in enumerate((dy, -dy)):
                    y_temp = np.copy(y)
                    y_temp[i] += delta
                    dAres[j] = self._calc_dAres_drhoi_wrap(T, np.exp(y_temp))
                phi_tmp[i] = Ares + rho/np.exp(y[i])*(dAres[0] - dAres[1]) / (2.0 * dy) - np.log(Z)
            else:
                phi_tmp[i] = 0.0 # This should be zero, but to prevent the thermo calculation from complaining about diving by zero we give it a value, the mole fraction is zero though, so it'll go away.
        ##########################################

        phi = np.exp(phi_tmp)

        # Reset composition dependent variables
        self._xi_dependent_variables(xi)

        return phi

    def _calc_dAres_drhoi_wrap(self, T, rhoi):
        """
        Compute derivative of Helmholtz energy wrt to density.
      
        Parameters
        ----------
        T : float
            Temperature of the system [K]
        rhoi : float
            Molar density of each component, add up to the total density [mol/m^3]
    
        Returns
        -------
        Ares : float
            Helmholtz energy give number of moles, length of array rho
        """

        #logger = logging.getLogger(__name__)

        if T != self.T:
            self._temp_dependent_variables(T)

        # Calculate new xi values
        rho = np.array([np.sum(rhoi)])
        xi = rhoi/rho

        self._xi_dependent_variables(xi)

        Cmol2seg, xsk, xskl = funcs.calc_composition_dependent_variables(xi, self._nui, self._beads, self._beadlibrary)

        Ares = funcs.calc_Ares(rho * constants.Nav, xi, T, self._beads, self._beadlibrary, self._massi, self._nui, Cmol2seg, xsk, xskl, self._dkk, self._epsilonkl, self._sigmakl, self._dkl, self._l_akl, self._l_rkl, self._Ckl, self._x0kl, self._epsilonHB, self._Kklab, self._nk)

        return Ares

    def _chemicalpotential_old(self, P, rho, xi, T):
        """
        Compute chemical potential given system information.
      
        Parameters
        ----------
        P : float
            Pressure of the system [Pa]
        rho : float
            Molar density of system [mol/m^3]
        T : float
            Temperature of the system [K]
        xi : list[float]
            Mole fraction of each component
    
        Returns
        -------
        mui : numpy.ndarray
            Array of chemical potential values for each component
        """

        logger = logging.getLogger(__name__)

        if len(xi) != len(self._nui):
            raise ValueError("Number of components in mole fraction list doesn't match components in nui. Check bead_config.")

        if T != self.T:
            self._temp_dependent_variables(T)

        self._xi_dependent_variables(xi)

        daresdxi = np.zeros_like(xi)
        mui = np.zeros_like(xi)

        # Set step size in finite difference method
        dnmol = 1.0E-4
        xi = np.array(xi,float)
        xi_tmp = xi[xi!=0.]
        if any(xi_tmp-dnmol < 0.):
            exp = np.floor(np.log10(min(xi_tmp)))-2 # Make sure step size is two orders of magnitude lower
            logger.debug("    Mole fraction, {}, is smaller than increment, {}. Use new increment, {}.".format(xi,dnmol,10**exp))
            dnmol = 10**exp

        # compute mui
        for i in range(np.size(mui)):
            dAres = np.zeros(2)
            ares = funcs.calc_Ares(rho * constants.Nav, xi, T, self._beads, self._beadlibrary, self._massi, self._nui, self._Cmol2seg, self._xsk, self._xskl,self._dkk, self._epsilonkl, self._sigmakl, self._dkl, self._l_akl, self._l_rkl, self._Ckl, self._x0kl, self._epsilonHB, self._Kklab, self._nk)
            for j, delta in enumerate((dnmol, -dnmol)):
                xi_temp = np.copy(xi)
                if xi_temp[i] != 0.:
                    xi_temp[i] += delta
                Cmol2seg_tmp, xsk_tmp, xskl_tmp = funcs.calc_composition_dependent_variables(xi_temp, self._nui, self._beads, self._beadlibrary)
                # xi_temp/=(nmol+delta)
                dAres[j] = funcs.calc_Ares(rho * constants.Nav, xi_temp, T, self._beads, self._beadlibrary, self._massi, self._nui, Cmol2seg_tmp, xsk_tmp, xskl_tmp, self._dkk, self._epsilonkl, self._sigmakl, self._dkl, self._l_akl, self._l_rkl, self._Ckl, self._x0kl, self._epsilonHB, self._Kklab, self._nk)
            daresdxi[i] = (dAres[0] - dAres[1]) / (2.0 * dnmol)

        # compute Z
        Z = P / (rho * T * constants.Nav * constants.kb)

        xjdaresdxj = np.sum(xi * daresdxi)
        for i in range(np.size(mui)):
            mui[i] = ares + Z - 1.0 + daresdxi[i] - xjdaresdxj - np.log(Z)
    
        return mui

    def density_max(self, xi, T, maxpack=0.65):

        """
        Estimate the maximum density based on the hard sphere packing fraction.
        
        Parameters
        ----------
        xi : list[float]
            Mole fraction of each component
        T : float
            Temperature of the system [K]
        maxpack : float, Optional, default: 0.65
            Maximum packing fraction
        
        Returns
        -------
        maxrho : float
            Maximum molar density [mol/m^3]
        """

        #logger = logging.getLogger(__name__)

        if T != self.T:
            self._temp_dependent_variables(T)

        self._xi_dependent_variables(xi)

        # estimate the maximum density based on the hard sphere packing fraction
        # etax, assuming a maximum packing fraction specified by maxpack
        maxrho = maxpack * 6.0 / (self._Cmol2seg * np.pi * np.sum(self._xskl * (self._dkl**3))) / constants.Nav

        return maxrho

    def param_guess(self, fit_params):
        """
        Generate initial guesses for the parameters to be fit.

        Parameters
        ----------
        fit_params : list[str]
            A list of parameters to be fit. See EOS mentation for supported parameter names. Cross interaction parameter names should be composed of parameter name and the other bead type, separated by an underscore (e.g. epsilon_CO2).

        Returns
        -------
        param_initial_guesses : numpy.ndarray, 
            An array of initial guesses for parameters, these will be optimized throughout the process.
    """

        #logger = logging.getLogger(__name__)

        l_fitparams = len(fit_params)
        if l_fitparams == 1:
            param_initial_guesses = np.array([l_fitparams])
        else:
            param_initial_guesses = np.zeros(1,l_fitparams)

        for i,param in enumerate(fit_params):
            if (param == "epsilon" or param.startswith('epsilon_')):
                param_initial_guesses[i] = 200.0
            elif param.startswith('epsilon'):
                param_initial_guesses[i] = 1000.0
            elif param.startswith('l_a'):
                param_initial_guesses[i] = 6.0
            elif param.startswith('l_r'):
                param_initial_guesses[i] = 12.0
            elif param.startswith('K'):
                param_initial_guesses[i] = 100.0e-30
            elif param.startswith('Sk'):
                param_initial_guesses[i] = 0.5
            else:
                raise ValueError("The parameter name {} does not fall under any of the catagories, epsilon, epsilon (assoc), l_a, l_r, K (assoc), or Sk".format(param)) 

        return param_initial_guesses

    def update_parameters(self, param_name, bead_names, param_value):
        r"""
        Update a single parameter value during parameter fitting process.

        To refresh those parameters that are dependent on to _beadlibrary or _crosslibrary, use method "parameter refresh".
        
        Parameters
        ----------
        param_name : str
            name of parameters being updated
        bead_names : list
            List of bead names to be changed. For a self interaction parameter, the length will be 1, for a cross interaction parameter, the length will be two.
        param_value : float
            Value of parameter
        """

        #logger = logging.getLogger(__name__)

        param_types = ["epsilon", "sigma", "l_r", "l_a", "Sk", "K"]

        if len(bead_names) > 2:
            raise ValueError("The bead names {} were given, but only a maximum of 2 are permitted.".format(", ".join(bead_names)))
        if not set(bead_names).issubset(self._beads):
            raise ValueError("The bead names {} were given, but they are not in the allowed list: {}".format(", ".join(bead_names),", ".join(self._beads)))

        # Non bonded parameters
        if (param_name in ["epsilon", "sigma", "l_r", "l_a", "Sk"]):
            # Self interaction parameter
            if len(bead_names) == 1:
                self._beadlibrary[bead_names[0]][param_name] = param_value
            # Cross interaction parameter
            elif len(bead_names) == 2:
                if bead_names[1] in list(self._crosslibrary.keys()):
                    if bead_names[0] in list(self._crosslibrary[bead_names[1]].keys()):
                        self._crosslibrary[bead_names[1]][bead_names[0]][param_name] = param_value
                    else:
                        self._crosslibrary[bead_names[1]] = {bead_names[0]:{param_name:param_value}}
                elif bead_names[0] in list(self._crosslibrary.keys()):
                    if bead_names[1] in list(self._crosslibrary[bead_names[0]].keys()): 
                        self._crosslibrary[bead_names[0]][bead_names[1]][param_name] = param_value
                    else:
                        self._crosslibrary[bead_names[0]] = {bead_names[1]:{param_name:param_value}}
                else:
                    self._crosslibrary[bead_names[0]] = {bead_names[1]:{param_name:param_value}}

        # Association Sites
        elif any([param_name.startswith('epsilon'), param_name.startswith('K')]):

            # Ensure sitenames are valid and on list
            if tmp[0] == True: tmp_name_full = param_name.replace("epsilon","")
            elif tmp[1] == True: tmp_name_full = param_name.replace("K","")
            flag = 0

            for site1 in self._sitenames:
                if tmp_name_full.startswith(site1):
                    tmp_name = tmp_name_full.replace(site1,"")
                    for site2 in self._sitenames:
                        if tmp_name == site2:
                            flag = 1
                            break
                    if flag == 1:
                        break
            if flag == 0:
                raise ValueError("site_names should be two different sites in the list: {}. You gave: {}".format(tmp_name_full,", ".join(sitenames=self._sitenames)))

            # Self interaction parameter
            if len(bead_names) == 1:
                self._beadlibrary[bead_names[0]][param_name+"".join(site_names)] = param_value
            # Cross interaction parameter
            elif len(bead_names) == 2:
                if bead_names[0] in list(self._crosslibrary[bead_names[1]].keys()):
                    self._crosslibrary[bead_names[1]][bead_names[0]][param_name+"".join(site_names)] = param_value
                else:
                    self._crosslibrary[bead_names[0]][bead_names[1]][param_name+"".join(site_names)] = param_value                        

        else:
            raise ValueError("The parameter name {} is not found in the allowed parameter types: {}".format(param_name,", ".join(param_types)))

    def parameter_refresh(self):
        r""" 
        To refresh dependent parameters
        
        Those parameters that are dependent on _beadlibrary and _crosslibrary attributes **must** be updated by running this function after all parameters from update_parameters method have been changed.
        """

        #logger = logging.getLogger(__name__)

        # Update Non bonded matrices
        self._epsilonkl, self._sigmakl, self._l_akl, self._l_rkl, self._Ckl = funcs.calc_interaction_matrices(self._beads, self._beadlibrary, crosslibrary=self._crosslibrary)

        # Update Association site matrices
        self._epsilonHB, self._Kklab, self._nk = funcs.calc_assoc_matrices(self._beads,self._beadlibrary,sitenames=self._sitenames,crosslibrary=self._crosslibrary)

        # Update temperature dependent variables
        if np.isnan(self.T) == False:
            self._temp_dependent_variables(self.T)


    def __str__(self):

        string = "Beads:" + str(self._beads) + "\n"
        string += "T:" + str(self.T) + "\n"
        return string


