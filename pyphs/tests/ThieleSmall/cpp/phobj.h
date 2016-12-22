/*
    Copyright or © or Copr. Project-Team S3 (Sound Signals and Systems) and
    Analysis/Synthesis team, Laboratory of Sciences and Technologies of Music and
    Sound (UMR 9912), IRCAM-CNRS-UPMC, 1 place Igor Stravinsky, F-75004 Paris
    * contributors : Antoine Falaize, Thomas Hélie,
    * corresponding contributor: antoine.falaize@ircam.fr
    * date: 2016/11/26 23:33:31

    This software (pypHs) is a computer program whose purpose is to generate C++
    code for the simulation of multiphysics system described by graph structures.
    It is composed of a library (pypHs.py) and a dictionnary (Dictionnary.py)

    This software is governed by the CeCILL-B license under French law and
    abiding by the rules of distribution of free software.  You can  use,
    modify and/ or redistribute the software under the terms of the CeCILL-B
    license as circulated by CEA, CNRS and INRIA at the following URL
    "http://www.cecill.info".

    As a counterpart to the access to the source code and  rights to copy,
    modify and redistribute granted by the license, users are provided only
    with a limited warranty  and the software's author,  the holder of the
    economic rights, and the successive licensors  have only  limited liability.

    In this respect, the user's attention is drawn to the risks associated
    with loading,  using,  modifying and/or developing or reproducing the
    software by the user in light of its specific status of free software,
    that may mean  that it is complicated to manipulate,  and  that  also
    therefore means  that it is reserved for developers  and  experienced
    professionals having in-depth computer knowledge. Users are therefore
    encouraged to load and test the software's suitability as regards their
    requirements in conditions enabling the security of their systems and/or
    data to be ensured and,  more generally, to use and operate it in the
    same conditions as regards security.

    The fact that you are presently reading this means that you have had
    knowledge of the CeCILL-B license and that you accept its terms.

    Created on 2016/11/26 23:33:31

    @author: Antoine Falaize



===============================================================================

    This file was automatically generated 
    by PyPHS v0.1.9c4_DEV, on 2016/11/26 23:33:31.

    It contains the code for the simulation of system 'THIELESMALL'.

===============================================================================
*/

#ifndef THIELESMALL_H
#define THIELESMALL_H

#include "iostream"
#include "vector"
#include "math.h"

# include "data.h"

#include </Users/.../eigen/Eigen/Dense>

using namespace std;
using namespace Eigen;

class THIELESMALL {

public:    
    
    // Acessors to system dimensions    
    const unsigned int get_nx() const;    
    const unsigned int get_nxl() const;    
    const unsigned int get_nxnl() const;    
    const unsigned int get_nw() const;    
    const unsigned int get_nwl() const;    
    const unsigned int get_ny() const;    
    const unsigned int get_nsubs() const;    
    
    // Acessors to system variables    
    vector<double> get_x() const;    
    vector<double> get_dx() const;    
    vector<double> get_dxH() const;    
    vector<double> get_w() const;    
    vector<double> get_z() const;    
    vector<double> get_y() const;    
    
    // Mutators for system variables    
    void set_x(vector<double> &);    
    void set_u(vector<double> &);
    void process(vector<double> &);    
    
    // Default Constructor:
    THIELESMALL();    
    
    // Constructor with state initalization:
    THIELESMALL(vector<double> &);    
    
    // Default Destructor:
    ~THIELESMALL();

private:    
    
    // System dimensions
    const unsigned int nx = 3;
    const unsigned int nxl = 2;
    const unsigned int nxnl = 1;
    const unsigned int nw = 2;
    const unsigned int nwl = 2;
    const unsigned int ny = 1;
    const unsigned int nsubs = 7;    
    
    // Runtime vectors    
    Matrix<double, 3, 1> x;    
    Matrix<double, 3, 1> dx;    
    Matrix<double, 3, 1> dxH;    
    Matrix<double, 2, 1> w;    
    Matrix<double, 2, 1> z;    
    Matrix<double, 1, 1> u;    
    Matrix<double, 1, 1> y;    
    Matrix<double, 4, 1> vl;    
    Matrix<double, 1, 1> vnl;    
    Matrix<double, 4, 1> fl;    
    Matrix<double, 1, 1> fnl;    
    
    // Arguments blocks    
    Map<Matrix<double, 2, 1>> xl;
    Map<Matrix<double, 1, 1>> xnl;
    Map<Matrix<double, 2, 1>> dxl;
    Map<Matrix<double, 1, 1>> dxnl;
    Map<Matrix<double, 2, 1>> wl;
    Map<Matrix<double, 2, 1>> dxHl;
    Map<Matrix<double, 1, 1>> dxHnl;
    Map<Matrix<double, 2, 1>> zl;    
    
    // Concatenation updates
    void dx_update();
    void w_update();
    void z_update();
    void dxH_update();    
    
    // Functions updates
    void fl_update();
    void fnl_update();
    void x_update();
    void Dl_update();
    void Nlxl_update();
    void Nlnl_update();
    void Nly_update();
    void Nnlxl_update();
    void Nnlnl_update();
    void Nnly_update();
    void c_update();
    void Fnl_update();
    void jac_Fnl_update();
    void vnl_update();
    void vl_update();
    void y_update();    
    
    // Functions arguments    
    double * xM = & x(0, 0);    
    double * xL = & x(1, 0);    
    double * xK = & x(2, 0);    
    double * dxM = & vl(0, 0);    
    double * dxL = & vl(1, 0);    
    double * wR = & vl(2, 0);    
    double * wA = & vl(3, 0);    
    double * dxK = & vnl(0, 0);    
    double * uIN = & u(0, 0);    
    
    // Functions parameters
    const unsigned int subs_ref = 0;
    
    const double * Bl = & subs[subs_ref][0];    
    const double * K2 = & subs[subs_ref][1];    
    const double * R = & subs[subs_ref][2];    
    const double * K0 = & subs[subs_ref][3];    
    const double * L = & subs[subs_ref][4];    
    const double * A = & subs[subs_ref][5];    
    const double * M = & subs[subs_ref][6];    
    
    // Matrices definitions    
    Matrix<double, 4, 4> iDl;
    Matrix<double, 4, 2> barNlxl;
    Matrix<double, 4, 1> barNlnl;
    Matrix<double, 4, 1> barNly;
    Matrix<double, 1, 1> barNnlnl;
    Matrix<double, 1, 4> barNnll;
    Matrix<double, 1, 2> barNnlxl;
    Matrix<double, 1, 1> barNnly;
    Matrix<double, 1, 1> jac_fnl;
    Matrix<double, 1, 1> Inl;
    Matrix<double, 1, 4> Nyl;
    Matrix<double, 1, 1> Nynl;
    Matrix<double, 1, 1> Nyy;
    Matrix<double, 4, 4> Dl;
    Matrix<double, 4, 2> Nlxl;
    Matrix<double, 4, 1> Nlnl;
    Matrix<double, 4, 1> Nly;
    Matrix<double, 1, 2> Nnlxl;
    Matrix<double, 1, 1> Nnlnl;
    Matrix<double, 1, 1> Nnly;
    Matrix<double, 1, 1> c;
    Matrix<double, 1, 1> Fnl;
    Matrix<double, 1, 1> jac_Fnl;    
    
    // Matrices updates    
    void iDl_update();
    void barNlxl_update();
    void barNlnl_update();
    void barNly_update();
    void barNnlnl_update();
    void barNnll_update();
    void barNnlxl_update();
    void barNnly_update();
    void jac_fnl_update();
    void Inl_update();
    void Nyl_update();
    void Nynl_update();
    void Nyy_update();
};

#endif /* THIELESMALL_H */
