/*
    Copyright or © or Copr. Project-Team S3 (Sound Signals and Systems) and
    Analysis/Synthesis team, Laboratory of Sciences and Technologies of Music and
    Sound (UMR 9912), IRCAM-CNRS-UPMC, 1 place Igor Stravinsky, F-75004 Paris
    * contributors : Antoine Falaize, Thomas Hélie,
    * corresponding contributor: antoine.falaize@ircam.fr
    * date: 2016/11/12 11:49:10

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

    Created on 2016/11/12 11:49:10

    @author: Antoine Falaize



===============================================================================

    This file was automatically generated 
    by PyPHS v0.1.9a, on 2016/11/12 11:49:10.

    It contains the code for the simulation of system 'RLC'.

===============================================================================
*/

#include "phobj.h"

// Acessors to system dimensions
const unsigned int RLC::get_nx() const { return nx; }
const unsigned int RLC::get_nxnl() const { return nxnl; }
const unsigned int RLC::get_nw() const { return nw; }
const unsigned int RLC::get_nwnl() const { return nwnl; }
const unsigned int RLC::get_ny() const { return ny; }
const unsigned int RLC::get_nsubs() const { return nsubs; }

// Acessors to system variables

vector<double> RLC::get_x() const {
    vector<double> v = vector<double>(2);
    for (int i=0; i<2; i++) {
        v[i] = x[i];
    }
    return v;
}

vector<double> RLC::get_dx() const {
    vector<double> v = vector<double>(2);
    for (int i=0; i<2; i++) {
        v[i] = dx[i];
    }
    return v;
}

vector<double> RLC::get_dxH() const {
    vector<double> v = vector<double>(2);
    for (int i=0; i<2; i++) {
        v[i] = dxH[i];
    }
    return v;
}

vector<double> RLC::get_w() const {
    vector<double> v = vector<double>(1);
    for (int i=0; i<1; i++) {
        v[i] = w[i];
    }
    return v;
}

vector<double> RLC::get_z() const {
    vector<double> v = vector<double>(1);
    for (int i=0; i<1; i++) {
        v[i] = z[i];
    }
    return v;
}

vector<double> RLC::get_y() const {
    vector<double> v = vector<double>(1);
    for (int i=0; i<1; i++) {
        v[i] = y[i];
    }
    return v;
}

// Mutators for system variables

void RLC::set_x(vector<double> & v) {
    for (int i=0; i<2; i++) {
        x[i] = v[i];
    }
}

void RLC::set_u(vector<double> & v) {
    for (int i=0; i<1; i++) {
        u[i] = v[i];
    }
}

void RLC::process(vector<double> & u_vec){

    set_u(u_vec);
    x_update();
    barNnlnl_update();
    barNnly_update();
    Nnlnl_update();
    Nnly_update();
    c_update();
    Fnl_update();
    unsigned int n = 0;
    while (n<100 & Fnl.transpose()*Fnl > 2.22044604925e-16){
        jac_fnl_update();
        jac_Fnl_update();
        vnl_update();
        fnl_update();
        Fnl_update();
        n++;
    }
    dx_update();
    dxH_update();
    w_update();
    z_update();
    y_update();
}

// Default Constructor:
RLC::RLC() : 
xnl( & x.block<2, 1>(0, 0)(0)),
dxnl( & vnl.block<2, 1>(0, 0)(0)),
wnl( & vnl.block<1, 1>(2, 0)(0)),
dxHnl( & fnl.block<2, 1>(0, 0)(0)),
znl( & fnl.block<1, 1>(2, 0)(0))
{

    for(int i=0; i<3; i++){
        vnl[i] = 0;
    }    
    
    // Matrices constants
    double barNnlnl_data[] = {0, 1.00000000000000, 1.00000000000000, -1.00000000000000, 0, 0, -1.00000000000000, 0, 0};
    double barNnly_data[] = {1.00000000000000, 0, 0};
    double jac_fnl_data[] = {0, 0, 0, 0, 0, 0, 0, 0, (*R1)};
    double Inl_data[] = {96000.0000000000, 0, 0, 0, 96000.0000000000, 0, 0, 0, 1};
    double Nynl_data[] = {-1.00000000000000, 0, 0};
    double Nyy_data[] = {0};
    
    // Matrices init
    barNnlnl = Map<Matrix<double, 3, 3>> (barNnlnl_data);
    barNnly = Map<Matrix<double, 3, 1>> (barNnly_data);
    jac_fnl = Map<Matrix<double, 3, 3>> (jac_fnl_data);
    Inl = Map<Matrix<double, 3, 3>> (Inl_data);
    Nynl = Map<Matrix<double, 1, 3>> (Nynl_data);
    Nyy = Map<Matrix<double, 1, 1>> (Nyy_data);
};

// Constructor with state initalization:
RLC::RLC(vector<double> & x0) : 
xnl( & x.block<2, 1>(0, 0)(0)),
dxnl( & vnl.block<2, 1>(0, 0)(0)),
wnl( & vnl.block<1, 1>(2, 0)(0)),
dxHnl( & fnl.block<2, 1>(0, 0)(0)),
znl( & fnl.block<1, 1>(2, 0)(0))
{

    if (x.size() == x0.size()) {
        set_x(x0);
    }
    else {
        cerr << "Size of x0 does not match size of x" << endl;
        exit(1);
    }

    for(int i=0; i<3; i++){
        vnl[i] = 0;
    }    
    
    // Matrices constants
    double barNnlnl_data[] = {0, 1.00000000000000, 1.00000000000000, -1.00000000000000, 0, 0, -1.00000000000000, 0, 0};
    double barNnly_data[] = {1.00000000000000, 0, 0};
    double jac_fnl_data[] = {0, 0, 0, 0, 0, 0, 0, 0, (*R1)};
    double Inl_data[] = {96000.0000000000, 0, 0, 0, 96000.0000000000, 0, 0, 0, 1};
    double Nynl_data[] = {-1.00000000000000, 0, 0};
    double Nyy_data[] = {0};
    
    // Matrices init
    barNnlnl = Map<Matrix<double, 3, 3>> (barNnlnl_data);
    barNnly = Map<Matrix<double, 3, 1>> (barNnly_data);
    jac_fnl = Map<Matrix<double, 3, 3>> (jac_fnl_data);
    Inl = Map<Matrix<double, 3, 3>> (Inl_data);
    Nynl = Map<Matrix<double, 1, 3>> (Nynl_data);
    Nyy = Map<Matrix<double, 1, 1>> (Nyy_data);
};

// Default Destructor:
RLC::~RLC() {};

// Concatenation updates

void RLC::dx_update(){
    dx << dxnl;
}

void RLC::w_update(){
    w << wnl;
}

void RLC::z_update(){
    z << znl;
}

void RLC::dxH_update(){
    dxH << dxHnl;
}

// Functions updates
void RLC::fnl_update(){
fnl(0, 0) = (((*dxL) < -2.22044604925031e-16) ? (
   (-0.5*pow((*xL), 2)/(*L) + 0.5*pow((*dxL) + (*xL), 2)/(*L))/(*dxL)
)
: (((*dxL) < 2.22044604925031e-16) ? (
   1.0*(*xL)/(*L)
)
: (
   (-0.5*pow((*xL), 2)/(*L) + 0.5*pow((*dxL) + (*xL), 2)/(*L))/(*dxL)
)));
fnl(1, 0) = (((*dxC) < -2.22044604925031e-16) ? (
   (-0.5*pow((*xC), 2)/(*C) + 0.5*pow((*dxC) + (*xC), 2)/(*C))/(*dxC)
)
: (((*dxC) < 2.22044604925031e-16) ? (
   1.0*(*xC)/(*C)
)
: (
   (-0.5*pow((*xC), 2)/(*C) + 0.5*pow((*dxC) + (*xC), 2)/(*C))/(*dxC)
)));
fnl(2, 0) = (*R1)*(*wR1);
};

void RLC::x_update(){
    x << x + dx;
}

void RLC::Nnlnl_update(){
    Nnlnl << barNnlnl;
}

void RLC::Nnly_update(){
    Nnly << barNnly;
}

void RLC::c_update(){
    c << Nnly*u;
}

void RLC::Fnl_update(){
    Fnl << Inl * vnl - Nnlnl*fnl - c;
}

void RLC::jac_Fnl_update(){
    jac_Fnl << Inl - Nnlnl*jac_fnl;
}

void RLC::vnl_update(){
    vnl << vnl - jac_Fnl.inverse()*Fnl;
}

void RLC::y_update(){
    y << Nynl*fnl + Nyy*u;
}

// Matrices updates
void RLC::barNnlnl_update(){
};
void RLC::barNnly_update(){
};
void RLC::jac_fnl_update(){
jac_fnl(0, 0) = (((*dxL) < -2.22044604925031e-16) ? (
   -(-0.5*pow((*xL), 2)/(*L) + 0.5*pow((*dxL) + (*xL), 2)/(*L))/pow((*dxL), 2) + 0.5*(2*(*dxL) + 2*(*xL))/((*L)*(*dxL))
)
: (((*dxL) < 2.22044604925031e-16) ? (
   0
)
: (
   -(-0.5*pow((*xL), 2)/(*L) + 0.5*pow((*dxL) + (*xL), 2)/(*L))/pow((*dxL), 2) + 0.5*(2*(*dxL) + 2*(*xL))/((*L)*(*dxL))
)));
jac_fnl(1, 1) = (((*dxC) < -2.22044604925031e-16) ? (
   -(-0.5*pow((*xC), 2)/(*C) + 0.5*pow((*dxC) + (*xC), 2)/(*C))/pow((*dxC), 2) + 0.5*(2*(*dxC) + 2*(*xC))/((*C)*(*dxC))
)
: (((*dxC) < 2.22044604925031e-16) ? (
   0
)
: (
   -(-0.5*pow((*xC), 2)/(*C) + 0.5*pow((*dxC) + (*xC), 2)/(*C))/pow((*dxC), 2) + 0.5*(2*(*dxC) + 2*(*xC))/((*C)*(*dxC))
)));
};
void RLC::Inl_update(){
};
void RLC::Nynl_update(){
};
void RLC::Nyy_update(){
};