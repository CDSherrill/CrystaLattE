#!/usr/bin/env python

#
# @BEGIN LICENSE
#
# CrystaLattE: The tool for the automated calculation of crystal lattice
# energies.
#
# Copyright (c) 2017-2018
# Carlos H. Borca
# C. David Sherrill
#
# The copyrights for code used from other parties are included in
# the corresponding files.
#
# This file is part of CrystaLattE.
#
# CrystaLattE is free software; you can redistribute it and/or modify
# it under the tesms of the GNU Lesser General Public License as
# published by the Free Software Foundation, version 3.
#
# CrystaLattE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with CrystaLattE; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA.
#
# @END LICENSE
#

# Import standard Python modules.
import os


# ======================================================================
def success_check(fname, verbose=0):
    """Takes a Psi4 output file and checks if it contains the string
    'coffee' to decide if the calculation was successful or not.

    Arguments:
    <str> fname
        Name of the Psi4 output file to check.
    <int> verbose
        Adjusts the level of detail of the printouts.
    
    Returns:
    <bool> beer
        True if the calculation was successful, false otherwise.
    """

    beer = False
    with open(fname, 'r') as outf:
        for line in outf:
            if "Psi4 exiting successfully. Buy a developer a beer!" in line:
                beer = True
                break
            
            else:
                continue
    return beer
# ======================================================================


# ======================================================================
def get_nmer_key(fname, verbose=0):
    """Takes a Psi4 output file and find the N-mer name to produce a 
    dictionary key.
    
    Arguments:
    <str> fname
        Name of the Psi4 output file to check.
    <int> verbose
        Adjusts the level of detail of the printouts.
    
    Returns:
    <str> key
        The key to create a new N-mer dictionary in the dictionary
        containing all N-mers.
    """
    
    with open(fname, 'r') as outf:
        for line in outf:
            # Find the name of the N-mer, and use it to create
            # the key for its entry in the nmers dictionary.
            if "Psithon input for N-mer:" in line:
                splt = line[:-1].split(":")
                key = splt[-1].strip()
    
    return key
# ======================================================================


# ======================================================================
def get_nmer_data(fname, verbose=0):
    """.
    
    Arguments:
    <str> fname
        Name of the Psi4 output file to check.
    <int> verbose
        Adjusts the level of detail of the printouts.
    
    Returns:
    """

    with open(fname, 'r') as outf:
        for line in outf:
            
            # Find the number of replicas of the N-mer.
            if "Number of replicas:" in line:
                splt = line[:-1].split(":")
                replicas = int(splt[-1].strip())

            # Find the number of replicas of the N-mer.
            if "Priority index for input:" in line:
                splt = line[:-1].split(":")
                priority_min = float(splt[-1].strip())

            # Find the list of minimum monomer separations of the N-mer.
            if "Minimum monomer separations:" in line:
                splt = line[:-1].split(":")
                msps = splt[-1].strip()
                min_monomer_separations = msps.split()

            # Find the list of minimum monomer separations of the N-mer.
            if "Minimum COM separations:" in line:
                splt = line[:-1].split(":")
                csps = splt[-1].strip()
                com_monomer_separations = csps.split()

    return replicas, priority_min, min_monomer_separations, com_monomer_separations
    
# ======================================================================


if __name__ == "__main__":

    # A dictionary for storing N-mers will be created.
    nmers = {}
    
    d = os.getcwd()
    
    for f in os.listdir(d):
    
        # Find output files using the default extension.
        #NOTE: This is prone to error if the extension was changed.
        if f.endswith(".out"):
            
            print(os.path.join(d, f)) #debug

            # Check if Psi4 exited successfully.
            # Why bothering analyzing a file otherwise?
            success = success_check(f)
            print(success) #debug
    
            if success:
                # If the output was ran successufully, get the N-mer name
                # to create a key for its soon-to-be created dictionary.
                keynmer = get_nmer_key(f)
                print(keynmer) #debug

                # Create a new dictionary for the current N-mer.
                nmers[keynmer]= {}
                print(nmers) #debug

                # Populate the current N-mer dictionary with the data
                # from the Psi4 output file.
                replicas, priority_min, min_monomer_separations, com_monomer_separations = get_nmer_data(f)
                print(replicas) #debug
                print(priority_min) #debug
                print(min_monomer_separations) #debug
                print(com_monomer_separations) #debug

        else:
            continue
