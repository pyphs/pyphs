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

#include "phobj.h"

// Acessors to system dimensions
const unsigned int THIELESMALL::get_nx() const { return nx; }
const unsigned int THIELESMALL::get_nxl() const { return nxl; }
const unsigned int THIELESMALL::get_nxnl() const { return nxnl; }
const unsigned int THIELESMALL::get_nw() const { return nw; }
const unsigned int THIELESMALL::get_nwl() const { return nwl; }
const unsigned int THIELESMALL::get_ny() const { return ny; }
const unsigned int THIELESMALL::get_nsubs() const { return nsubs; }

// Acessors to system variables

vector<double> THIELESMALL::get_x() const {
    vector<double> v = vector<double>(3);
    for (int i=0; i<3; i++) {
        v[i] = x[i];
    }
    return v;
}

vector<double> THIELESMALL::get_dx() const {
    vector<double> v = vector<double>(3);
    for (int i=0; i<3; i++) {
        v[i] = dx[i];
    }
    return v;
}

vector<double> THIELESMALL::get_dxH() const {
    vector<double> v = vector<double>(3);
    for (int i=0; i<3; i++) {
        v[i] = dxH[i];
    }
    return v;
}

vector<double> THIELESMALL::get_w() const {
    vector<double> v = vector<double>(2);
    for (int i=0; i<2; i++) {
        v[i] = w[i];
    }
    return v;
}

vector<double> THIELESMALL::get_z() const {
    vector<double> v = vector<double>(2);
    for (int i=0; i<2; i++) {
        v[i] = z[i];
    }
    return v;
}

vector<double> THIELESMALL::get_y() const {
    vector<double> v = vector<double>(1);
    for (int i=0; i<1; i++) {
        v[i] = y[i];
    }
    return v;
}

// Mutators for system variables

void THIELESMALL::set_x(vector<double> & v) {
    for (int i=0; i<3; i++) {
        x[i] = v[i];
    }
}

void THIELESMALL::set_u(vector<double> & v) {
    for (int i=0; i<1; i++) {
        u[i] = v[i];
    }
}

void THIELESMALL::process(vector<double> & u_vec){

    set_u(u_vec);
    x_update();
    iDl_update();
    barNlxl_update();
    barNlnl_update();
    barNly_update();
    barNnlxl_update();
    barNnlnl_update();
    barNnly_update();
    Dl_update();
    Nlxl_update();
    Nlnl_update();
    Nly_update();
    Nnlxl_update();
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
    vl_update();
    fl_update();
    dx_update();
    dxH_update();
    w_update();
    z_update();
    y_update();
}

// Default Constructor:
THIELESMALL::THIELESMALL() : 
xl( & x.block<2, 1>(0, 0)(0)),
xnl( & x.block<1, 1>(2, 0)(0)),
dxl( & vl.block<2, 1>(0, 0)(0)),
dxnl( & vnl.block<1, 1>(0, 0)(0)),
wl( & vl.block<2, 1>(2, 0)(0)),
dxHl( & fl.block<2, 1>(0, 0)(0)),
dxHnl( & fnl.block<1, 1>(0, 0)(0)),
zl( & fl.block<2, 1>(2, 0)(0))
{

    for(int i=0; i<1; i++){
        vnl[i] = 0;
    }    
    
    // Matrices constants
    double iDl_data[] = {96000.0000000000, 0.5*(*Bl)/(*M), 0, -0.5/(*M), -0.5*(*Bl)/(*L), 96000.0000000000, -0.5/(*L), 0, 0, 1.0*(*R), 1, 0, 1.0*(*A), 0, 0, 1};
    double barNlxl_data[] = {0, -1.0*(*Bl)/(*M), 0, 1.0/(*M), 1.0*(*Bl)/(*L), 0, 1.0/(*L), 0};
    double barNlnl_data[] = {-1.00000000000000, 0, 0, 0};
    double barNly_data[] = {0, 1.00000000000000, 0, 0};
    double barNnlnl_data[] = {0};
    double barNnll_data[] = {0.5/(*M), 0, 0, 0};
    double barNnlxl_data[] = {1.0/(*M), 0};
    double barNnly_data[] = {0};
    double jac_fnl_data[] = {0};
    double Inl_data[] = {96000.0000000000};
    double Nyl_data[] = {0, -1.00000000000000, 0, 0};
    double Nynl_data[] = {0};
    double Nyy_data[] = {0};
    
    // Matrices init
    iDl = Map<Matrix<double, 4, 4>> (iDl_data);
    barNlxl = Map<Matrix<double, 4, 2>> (barNlxl_data);
    barNlnl = Map<Matrix<double, 4, 1>> (barNlnl_data);
    barNly = Map<Matrix<double, 4, 1>> (barNly_data);
    barNnlnl = Map<Matrix<double, 1, 1>> (barNnlnl_data);
    barNnll = Map<Matrix<double, 1, 4>> (barNnll_data);
    barNnlxl = Map<Matrix<double, 1, 2>> (barNnlxl_data);
    barNnly = Map<Matrix<double, 1, 1>> (barNnly_data);
    jac_fnl = Map<Matrix<double, 1, 1>> (jac_fnl_data);
    Inl = Map<Matrix<double, 1, 1>> (Inl_data);
    Nyl = Map<Matrix<double, 1, 4>> (Nyl_data);
    Nynl = Map<Matrix<double, 1, 1>> (Nynl_data);
    Nyy = Map<Matrix<double, 1, 1>> (Nyy_data);
};

// Constructor with state initalization:
THIELESMALL::THIELESMALL(vector<double> & x0) : 
xl( & x.block<2, 1>(0, 0)(0)),
xnl( & x.block<1, 1>(2, 0)(0)),
dxl( & vl.block<2, 1>(0, 0)(0)),
dxnl( & vnl.block<1, 1>(0, 0)(0)),
wl( & vl.block<2, 1>(2, 0)(0)),
dxHl( & fl.block<2, 1>(0, 0)(0)),
dxHnl( & fnl.block<1, 1>(0, 0)(0)),
zl( & fl.block<2, 1>(2, 0)(0))
{

    if (x.size() == x0.size()) {
        set_x(x0);
    }
    else {
        cerr << "Size of x0 does not match size of x" << endl;
        exit(1);
    }

    for(int i=0; i<1; i++){
        vnl[i] = 0;
    }    
    
    // Matrices constants
    double iDl_data[] = {96000.0000000000, 0.5*(*Bl)/(*M), 0, -0.5/(*M), -0.5*(*Bl)/(*L), 96000.0000000000, -0.5/(*L), 0, 0, 1.0*(*R), 1, 0, 1.0*(*A), 0, 0, 1};
    double barNlxl_data[] = {0, -1.0*(*Bl)/(*M), 0, 1.0/(*M), 1.0*(*Bl)/(*L), 0, 1.0/(*L), 0};
    double barNlnl_data[] = {-1.00000000000000, 0, 0, 0};
    double barNly_data[] = {0, 1.00000000000000, 0, 0};
    double barNnlnl_data[] = {0};
    double barNnll_data[] = {0.5/(*M), 0, 0, 0};
    double barNnlxl_data[] = {1.0/(*M), 0};
    double barNnly_data[] = {0};
    double jac_fnl_data[] = {0};
    double Inl_data[] = {96000.0000000000};
    double Nyl_data[] = {0, -1.00000000000000, 0, 0};
    double Nynl_data[] = {0};
    double Nyy_data[] = {0};
    
    // Matrices init
    iDl = Map<Matrix<double, 4, 4>> (iDl_data);
    barNlxl = Map<Matrix<double, 4, 2>> (barNlxl_data);
    barNlnl = Map<Matrix<double, 4, 1>> (barNlnl_data);
    barNly = Map<Matrix<double, 4, 1>> (barNly_data);
    barNnlnl = Map<Matrix<double, 1, 1>> (barNnlnl_data);
    barNnll = Map<Matrix<double, 1, 4>> (barNnll_data);
    barNnlxl = Map<Matrix<double, 1, 2>> (barNnlxl_data);
    barNnly = Map<Matrix<double, 1, 1>> (barNnly_data);
    jac_fnl = Map<Matrix<double, 1, 1>> (jac_fnl_data);
    Inl = Map<Matrix<double, 1, 1>> (Inl_data);
    Nyl = Map<Matrix<double, 1, 4>> (Nyl_data);
    Nynl = Map<Matrix<double, 1, 1>> (Nynl_data);
    Nyy = Map<Matrix<double, 1, 1>> (Nyy_data);
};

// Default Destructor:
THIELESMALL::~THIELESMALL() {};

// Concatenation updates

void THIELESMALL::dx_update(){
    dx << dxl,dxnl;
}

void THIELESMALL::w_update(){
    w << wl;
}

void THIELESMALL::z_update(){
    z << zl;
}

void THIELESMALL::dxH_update(){
    dxH << dxHl,dxHnl;
}

// Functions updates
void THIELESMALL::fl_update(){
fl(0, 0) = (((*dxM) < -2.22044604925031e-16) ? (
   (-0.5*pow((*xM), 2)/(*M) + 0.5*pow((*dxM) + (*xM), 2)/(*M))/(*dxM)
)
: (((*dxM) < 2.22044604925031e-16) ? (
   1.0*(*xM)/(*M)
)
: (
   (-0.5*pow((*xM), 2)/(*M) + 0.5*pow((*dxM) + (*xM), 2)/(*M))/(*dxM)
)));
fl(1, 0) = (((*dxL) < -2.22044604925031e-16) ? (
   (-0.5*pow((*xL), 2)/(*L) + 0.5*pow((*dxL) + (*xL), 2)/(*L))/(*dxL)
)
: (((*dxL) < 2.22044604925031e-16) ? (
   1.0*(*xL)/(*L)
)
: (
   (-0.5*pow((*xL), 2)/(*L) + 0.5*pow((*dxL) + (*xL), 2)/(*L))/(*dxL)
)));
fl(2, 0) = (*R)*(*wR);
fl(3, 0) = (*A)*(*wA);
};
void THIELESMALL::fnl_update(){
fnl(0, 0) = (((*dxK) < -2.22044604925031e-16) ? (
   (-1.0L/2.0L*(*K0)*(*xK)*((1.0L/2.0L)*pow((*xK), 3) + (*xK)) + (1.0L/2.0L)*(*K0)*((*dxK) + (*xK))*((*dxK) + (*xK) + (1.0L/2.0L)*pow((*dxK) + (*xK), 3)))/(*dxK)
)
: (((*dxK) < 2.22044604925031e-16) ? (
   (1.0L/2.0L)*(*K0)*(*xK)*((3.0L/2.0L)*pow((*xK), 2) + 1) + (1.0L/2.0L)*(*K0)*((1.0L/2.0L)*pow((*xK), 3) + (*xK))
)
: (
   (-1.0L/2.0L*(*K0)*(*xK)*((1.0L/2.0L)*pow((*xK), 3) + (*xK)) + (1.0L/2.0L)*(*K0)*((*dxK) + (*xK))*((*dxK) + (*xK) + (1.0L/2.0L)*pow((*dxK) + (*xK), 3)))/(*dxK)
)));
};

void THIELESMALL::x_update(){
    x << x + dx;
}

void THIELESMALL::Dl_update(){
    Dl << iDl.inverse();
}

void THIELESMALL::Nlxl_update(){
    Nlxl << Dl*barNlxl;
}

void THIELESMALL::Nlnl_update(){
    Nlnl << Dl*barNlnl;
}

void THIELESMALL::Nly_update(){
    Nly << Dl*barNly;
}

void THIELESMALL::Nnlxl_update(){
    Nnlxl << barNnlxl + barNnll*Nlxl;
}

void THIELESMALL::Nnlnl_update(){
    Nnlnl << barNnlnl + barNnll*Nlnl;
}

void THIELESMALL::Nnly_update(){
    Nnly << barNnly + barNnll*Nly;
}

void THIELESMALL::c_update(){
    c << Nnlxl*x + Nnly*u;
}

void THIELESMALL::Fnl_update(){
    Fnl << Inl * vnl - Nnlnl*fnl - c;
}

void THIELESMALL::jac_Fnl_update(){
    jac_Fnl << Inl - Nnlnl*jac_fnl;
}

void THIELESMALL::vnl_update(){
    vnl << vnl - jac_Fnl.inverse()*Fnl;
}

void THIELESMALL::vl_update(){
    vl << Nlxl*xl + Nlnl*fnl + Nly*u;
}

void THIELESMALL::y_update(){
    y << Nyl*fl + Nynl*fnl + Nyy*u;
}

// Matrices updates
void THIELESMALL::iDl_update(){
};
void THIELESMALL::barNlxl_update(){
};
void THIELESMALL::barNlnl_update(){
};
void THIELESMALL::barNly_update(){
};
void THIELESMALL::barNnlnl_update(){
};
void THIELESMALL::barNnll_update(){
};
void THIELESMALL::barNnlxl_update(){
};
void THIELESMALL::barNnly_update(){
};
void THIELESMALL::jac_fnl_update(){
jac_fnl(0, 0) = (((*dxK) < -2.22044604925031e-16) ? (
   ((1.0L/2.0L)*(*K0)*((*dxK) + (*xK))*((3.0L/2.0L)*pow((*dxK) + (*xK), 2) + 1) + (1.0L/2.0L)*(*K0)*((*dxK) + (*xK) + (1.0L/2.0L)*pow((*dxK) + (*xK), 3)))/(*dxK) - (-1.0L/2.0L*(*K0)*(*xK)*((1.0L/2.0L)*pow((*xK), 3) + (*xK)) + (1.0L/2.0L)*(*K0)*((*dxK) + (*xK))*((*dxK) + (*xK) + (1.0L/2.0L)*pow((*dxK) + (*xK), 3)))/pow((*dxK), 2)
)
: (((*dxK) < 2.22044604925031e-16) ? (
   0
)
: (
   ((1.0L/2.0L)*(*K0)*((*dxK) + (*xK))*((3.0L/2.0L)*pow((*dxK) + (*xK), 2) + 1) + (1.0L/2.0L)*(*K0)*((*dxK) + (*xK) + (1.0L/2.0L)*pow((*dxK) + (*xK), 3)))/(*dxK) - (-1.0L/2.0L*(*K0)*(*xK)*((1.0L/2.0L)*pow((*xK), 3) + (*xK)) + (1.0L/2.0L)*(*K0)*((*dxK) + (*xK))*((*dxK) + (*xK) + (1.0L/2.0L)*pow((*dxK) + (*xK), 3)))/pow((*dxK), 2)
)));
};
void THIELESMALL::Inl_update(){
};
void THIELESMALL::Nyl_update(){
};
void THIELESMALL::Nynl_update(){
};
void THIELESMALL::Nyy_update(){
};