import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import sys
sys.path.append("C:\Program Files (x86)\Deltares\Probabilistic toolkit\Python")
import toolkit
import os

def LimitStateFunction(p, mR, R, aQ, mQ, Q, G):
    Z = p * mR * R - aQ *  mQ *Q - (1-aQ) * G
    return Z

def UnityCheck(p, V_R, gamma_R, V_Q, gamma_Q):
    R_kar = 1 - 1.645 * V_R
    Q_kar = norm.ppf(0.98, loc = 1, scale = V_Q)
    G_kar = 1
    UC = p * R_kar / gamma_R - aQ * Q_kar * gamma_Q - (1-aQ) * G_kar
    return UC

if __name__ == "__main__":
   
    # loop = 0
    gamma_R = 1.1
    gamma_Q = 1.05
    p = 2.9
    V_mR = 0.15
    V_R = 0.15
    aQ = 0.1
    V_mQ = 0.1
    V_Q = 0.15
    V_G = 0.05
    
    UC = UnityCheck(p, V_R, gamma_R, V_Q, gamma_Q)
    print('UC = ', UC)
    
    PTKfile = 'Portfolio_v1'

    toolkit.Initialize()
    toolkit.Load(os.path.abspath(f"{PTKfile}.tkx"))
    # toolkit.SetVariableValue(variables_tochange[0], "Mean", [p][loop])
    toolkit.SetVariableValue('aQ', "Mean", aQ)
    toolkit.Run()
    
    # retrieve results
    vars = toolkit.GetVariables()

    beta = toolkit.GetReliabilityIndex()
    Pf = toolkit.GetProbabilityFailure()
    alphas=[]
    DPvalues=[]
    for var in vars[:-1]:
        alphas.append(toolkit.GetAlpha(var))
        DPvalues.append(toolkit.GetAlphaPhysical(var))
    
    results = {"p": [],
               "aQ": [],
               "UC": [],
               "Beta": [],
               "Pf": [],
               "alphas": [],
               "DPvalues": [],
               "VarNames": []}
    
    results["p"].append(p)
    results["aQ"].append(aQ)
    results["UC"].append(float(UC))
    results["Beta"].append(float(beta))
    results["Pf"].append(float(Pf))
    results["alphas"].append(list(map(float, alphas)))
    results["DPvalues"].append(list(map(float, DPvalues)))
    results["VarNames"].append(vars)

    toolkit.Exit()

    
    
    
    
    