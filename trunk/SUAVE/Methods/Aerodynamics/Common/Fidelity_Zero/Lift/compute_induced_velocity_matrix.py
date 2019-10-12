## @ingroup Methods-Aerodynamics-Common-Fidelity_Zero-Lift
# compute_induced_velocity_matrix.py
# 
# Created:  May 2018, M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# package imports
import SUAVE
import numpy as np
from SUAVE.Core import Units , Data

## @ingroup Methods-Aerodynamics-Common-Fidelity_Zero-Lift
def compute_induced_velocity_matrix(data,n_sw,n_cw,theta_w,mach):

    # unpack 
    ones = np.atleast_3d(np.ones_like(theta_w))

    # Prandtl Glauret Transformation for subsonic
    inv_root_beta = np.zeros_like(mach)
    inv_root_beta[mach<1] = 1/np.sqrt(1-mach[mach<1]**2)     
    inv_root_beta[mach>1] = 1/np.sqrt(mach[mach>1]**2-1) 
    if np.any(mach==1):
        raise('Mach of 1 cannot be used in building compressibiliy corrections.')
    inv_root_beta = np.atleast_3d(inv_root_beta)

    XAH  = np.atleast_3d(data.XAH*inv_root_beta)
    YAH  = np.atleast_3d(data.YAH*ones)
    ZAH  = np.atleast_3d(data.ZAH*ones)
    XBH  = np.atleast_3d(data.XBH*inv_root_beta)
    YBH  = np.atleast_3d(data.YBH*ones)
    ZBH  = np.atleast_3d(data.ZBH*ones)

    XA1  = np.atleast_3d(data.XA1*inv_root_beta)
    YA1  = np.atleast_3d(data.YA1*ones)
    ZA1  = np.atleast_3d(data.ZA1*ones)
    XA2  = np.atleast_3d(data.XA2*inv_root_beta)
    YA2  = np.atleast_3d(data.YA2*ones)
    ZA2  = np.atleast_3d(data.ZA2*ones)

    XB1  = np.atleast_3d(data.XB1*inv_root_beta)
    YB1  = np.atleast_3d(data.YB1*ones)
    ZB1  = np.atleast_3d(data.ZB1*ones)
    XB2  = np.atleast_3d(data.XB2*inv_root_beta)
    YB2  = np.atleast_3d(data.YB2*ones)
    ZB2  = np.atleast_3d(data.ZB2*ones)

    XAC  = np.atleast_3d(data.XAC*inv_root_beta)
    YAC  = np.atleast_3d(data.YAC*ones)
    ZAC  = np.atleast_3d(data.ZAC*ones)
    XBC  = np.atleast_3d(data.XBC*inv_root_beta)
    YBC  = np.atleast_3d(data.YBC*ones)
    ZBC  = np.atleast_3d(data.ZBC*ones)
    XC   = np.atleast_3d(data.XC*inv_root_beta)
    YC   = np.atleast_3d(data.YC*ones) 
    ZC   = np.atleast_3d(data.ZC*ones)  
    n_w  = data.n_w

    theta_w = np.atleast_3d(0)     # wake model set to freestream
    n_aoa   = np.shape(theta_w)[0]

    # -------------------------------------------------------------------------------------------
    # Compute velocity induced by horseshoe vortex segments on every control point by every panel
    # ------------------------------------------------------------------------------------------- 
    n_cp     = n_w*n_cw*n_sw # total number of control points 

    # Make all the hats
    n_cw_1   = n_cw-1
    XC_hats  = np.atleast_3d(np.cos(theta_w)*XC + np.sin(theta_w)*ZC)
    YC_hats  = np.atleast_3d(YC)
    ZC_hats  = np.atleast_3d(-np.sin(theta_w)*XC + np.cos(theta_w)*ZC)

    XA2_hats = np.atleast_3d(np.cos(theta_w)*XA2[:,:,n_cw_1::n_cw]   + np.sin(theta_w)*ZA2[:,:,n_cw_1::n_cw])
    YA2_hats = np.atleast_3d(YA2[:,:,n_cw_1::n_cw])
    ZA2_hats = np.atleast_3d(-np.sin(theta_w)*XA2[:,:,n_cw_1::n_cw]  + np.cos(theta_w)*ZA2[:,:,n_cw_1::n_cw])

    XB2_hats = np.atleast_3d(np.cos(theta_w)*XB2[:,:,n_cw_1::n_cw]   + np.sin(theta_w)*ZB2[:,:,n_cw_1::n_cw])
    YB2_hats = np.atleast_3d(YB2[:,:,n_cw_1::n_cw]) 
    ZB2_hats = np.atleast_3d(-np.sin(theta_w)*XB2[:,:,n_cw_1::n_cw]  + np.cos(theta_w)*ZB2[:,:,n_cw_1::n_cw])

    # Expand out the hats to be of length n instead of n_sw
    XA2_hats = np.atleast_3d(np.repeat(XA2_hats,n_cw,axis=2))
    YA2_hats = np.atleast_3d(np.repeat(YA2_hats,n_cw,axis=2))
    ZA2_hats = np.atleast_3d(np.repeat(ZA2_hats,n_cw,axis=2))
    XB2_hats = np.atleast_3d(np.repeat(XB2_hats,n_cw,axis=2))
    YB2_hats = np.atleast_3d(np.repeat(YB2_hats,n_cw,axis=2))
    ZB2_hats = np.atleast_3d(np.repeat(ZB2_hats,n_cw,axis=2))

    # If YBH is negative, flip A and B, ie negative side of the airplane. Vortex order flips
    boolean = YBH<0.
    XA1[boolean], XB1[boolean] = XB1[boolean], XA1[boolean]
    YA1[boolean], YB1[boolean] = YB1[boolean], YA1[boolean]
    ZA1[boolean], ZB1[boolean] = ZB1[boolean], ZA1[boolean]
    XA2[boolean], XB2[boolean] = XB2[boolean], XA2[boolean]
    YA2[boolean], YB2[boolean] = YB2[boolean], YA2[boolean]
    ZA2[boolean], ZB2[boolean] = ZB2[boolean], ZA2[boolean]    
    XAH[boolean], XBH[boolean] = XBH[boolean], XAH[boolean]
    YAH[boolean], YBH[boolean] = YBH[boolean], YAH[boolean]
    ZAH[boolean], ZBH[boolean] = ZBH[boolean], ZAH[boolean]

    XA2_hats[boolean], XB2_hats[boolean] = XB2_hats[boolean], XA2_hats[boolean]
    YA2_hats[boolean], YB2_hats[boolean] = YB2_hats[boolean], YA2_hats[boolean]
    ZA2_hats[boolean], ZB2_hats[boolean] = ZB2_hats[boolean], ZA2_hats[boolean]

    # Transpose thing
    XC = np.swapaxes(XC,1,2) 
    YC = np.swapaxes(YC,1,2) 
    ZC = np.swapaxes(ZC,1,2) 

    XC_hats = np.swapaxes(XC_hats,1,2) 
    YC_hats = np.swapaxes(YC_hats,1,2) 
    ZC_hats = np.swapaxes(ZC_hats,1,2)     

    # compute influence of bound vortices 
    C_AB_bv = np.transpose(vortex(XC, YC, ZC, XAH, YAH, ZAH, XBH, YBH, ZBH),axes=[1,2,3,0])

    # compute influence of 3/4 left legs
    C_AB_34_ll = np.transpose(vortex(XC, YC, ZC, XA2, YA2, ZA2, XAH, YAH, ZAH),axes=[1,2,3,0])

    # compute influence of whole panel left legs 
    C_AB_ll   =  np.transpose(vortex(XC, YC, ZC, XA2, YA2, ZA2, XA1, YA1, ZA1),axes=[1,2,3,0])

    # compute influence of 3/4 right legs
    C_AB_34_rl = np.transpose(vortex(XC, YC, ZC, XBH, YBH, ZBH, XB2, YB2, ZB2),axes=[1,2,3,0])

    # compute influence of whole right legs 
    C_AB_rl = np.transpose(vortex(XC, YC, ZC, XB1, YB1, ZB1, XB2, YB2, ZB2),axes=[1,2,3,0])

    # velocity induced by left leg of vortex (A to inf)
    C_Ainf  = np.transpose(vortex_to_inf_l(XC_hats, YC_hats, ZC_hats, XA2_hats, YA2_hats, ZA2_hats,theta_w),axes=[1,2,3,0])

    # velocity induced by right leg of vortex (B to inf)
    C_Binf  = np.transpose(vortex_to_inf_r(XC_hats, YC_hats, ZC_hats, XB2_hats, YB2_hats, ZB2_hats,theta_w),axes=[1,2,3,0])

    # compute Mach Cone Matrix
    MCM = np.ones_like(C_AB_bv)
    MCM = compute_mach_cone_matrix(XC,YC,ZC,MCM,mach)
    data.MCM = MCM 

    # multiply by mach cone 
    C_AB_bv     = C_AB_bv    * MCM
    C_AB_34_ll  = C_AB_34_ll * MCM
    C_AB_ll     = C_AB_ll    * MCM
    C_AB_34_rl  = C_AB_34_rl * MCM
    C_AB_rl     = C_AB_rl    * MCM
    C_Ainf      = C_Ainf     * MCM
    C_Binf      = C_Binf     * MCM  

    # Add the right and left influences seperately
    C_AB_llrl_roll = C_AB_ll+C_AB_rl

    # Prime the arrays
    mask      = np.ones((n_aoa,n_cp,n_cp,3))
    C_AB_llrl = np.zeros((n_aoa,n_cp,n_cp,3))

    for idx in range(n_cw-1):    

        # Make a mask
        mask[:,n_cw-idx-1::n_cw,:]= np.zeros_like(mask[:,n_cw-idx-1::n_cw,:])  

        # Roll it over to the next component
        C_AB_llrl_roll = np.roll(C_AB_llrl_roll,-1,axis=1)   

        # Add in the components that we need
        C_AB_llrl = C_AB_llrl+ C_AB_llrl_roll*mask

    # Add all the influences together
    C_mn = C_AB_34_ll + C_AB_bv + C_AB_34_rl + C_Ainf + C_Binf + C_AB_llrl

    DW_mn = C_AB_34_ll + C_AB_bv  + C_AB_34_rl + C_Ainf + C_Binf + C_AB_llrl

    return C_mn, DW_mn

# -------------------------------------------------------------------------------
# vortex strength computation
# -------------------------------------------------------------------------------
def vortex(X,Y,Z,X1,Y1,Z1,X2,Y2,Z2):

    # Take all the differences
    X_X1  = X-X1
    X_X2  = X-X2
    X2_X1 = X2-X1

    Y_Y1  = Y-Y1
    Y_Y2  = Y-Y2
    Y2_Y1 = Y2-Y1

    Z_Z1  = Z-Z1
    Z_Z2  = Z-Z2 
    Z2_Z1 = Z2-Z1 

    R1R2X  =   Y_Y1*Z_Z2 - Z_Z1*Y_Y2 
    R1R2Y  = -(X_X1*Z_Z2 - Z_Z1*X_X2)
    R1R2Z  =   X_X1*Y_Y2 - Y_Y1*X_X2
    SQUARE = R1R2X*R1R2X + R1R2Y*R1R2Y + R1R2Z*R1R2Z
    SQUARE[SQUARE==0] = 1e-32
    R1     = np.sqrt(X_X1*X_X1 + Y_Y1*Y_Y1 + Z_Z1*Z_Z1) 
    R2     = np.sqrt(X_X2*X_X2 + Y_Y2*Y_Y2 + Z_Z2*Z_Z2) 
    R0R1   = X2_X1*X_X1 + Y2_Y1*Y_Y1 + Z2_Z1*Z_Z1
    R0R2   = X2_X1*X_X2 + Y2_Y1*Y_Y2 + Z2_Z1*Z_Z2
    RVEC   = np.array([R1R2X,R1R2Y,R1R2Z])
    COEF   = (1/(4*np.pi))*(RVEC/SQUARE) * (R0R1/R1 - R0R2/R2)

    if np.isnan(COEF).any():
        print('NaN!')       

    return COEF

def vortex_to_inf_l(X,Y,Z,X1,Y1,Z1,tw): 

    # Take all the differences
    X_X1  = X-X1    
    Y_Y1  = Y-Y1
    Y1_Y  = Y1-Y
    Z_Z1  = Z-Z1

    DENUM =  Z_Z1*Z_Z1 + Y1_Y*Y1_Y    
    DENUM[DENUM==0] = 1e-32
    XVEC  = -Y1_Y*np.sin(tw)/DENUM
    YVEC  =  (Z_Z1)/DENUM
    ZVEC  =  Y1_Y*np.cos(tw)/DENUM
    BRAC  =  1 + (X_X1 / (np.sqrt(X_X1*X_X1 + Y_Y1*Y_Y1 + Z_Z1*Z_Z1)))
    RVEC   = np.array([XVEC, YVEC, ZVEC])
    COEF  = (1/(4*np.pi))*RVEC*BRAC  

    if np.isnan(COEF).any():
        print('NaN!')   

    return COEF

def vortex_to_inf_r(X,Y,Z,X1,Y1,Z1,tw):

    # Take all the differences
    X_X1  = X-X1    
    Y_Y1  = Y-Y1
    Y1_Y  = Y1-Y
    Z_Z1  = Z-Z1    

    DENUM =  Z_Z1*Z_Z1 + Y1_Y*Y1_Y
    DENUM[DENUM==0] = 1e-32
    XVEC  = Y1_Y*np.sin(tw)/DENUM
    YVEC  = -Z_Z1/DENUM
    ZVEC  = -Y1_Y*np.cos(tw)/DENUM
    BRAC  =  1 + (X_X1 / (np.sqrt(X_X1*X_X1+ Y_Y1*Y_Y1+ Z_Z1*Z_Z1)))
    RVEC   = np.array([XVEC, YVEC, ZVEC])
    COEF  = (1/(4*np.pi))*RVEC*BRAC      

    if np.isnan(COEF).any():
        print('NaN!')   

    return COEF


def compute_mach_cone_matrix(XC,YC,ZC,MCM,mach):
    for m_idx in range(len(mach)):
        c = np.arcsin(1/mach[m_idx])
        for cp_idx in range(len(XC[m_idx,:])):
            del_x = XC[m_idx,:] - XC[m_idx,cp_idx] 
            del_y = YC[m_idx,:] - YC[m_idx,cp_idx] 
            del_z = ZC[m_idx,:] - ZC[m_idx,cp_idx] 
            flag  = -c*del_x**2 + del_y**2 + del_z**2
            idxs  = np.where(flag > 0.0)[0]
            MCM[m_idx,cp_idx,idxs]  = [0.0, 0.0, 0.0]     
    return MCM