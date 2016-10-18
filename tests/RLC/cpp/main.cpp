/*
    Copyright or © or Copr. Project-Team S3 (Sound Signals and Systems) and
    Analysis/Synthesis team, Laboratory of Sciences and Technologies of Music and
    Sound (UMR 9912), IRCAM-CNRS-UPMC, 1 place Igor Stravinsky, F-75004 Paris
    * contributors : Antoine Falaize, Thomas Hélie,
    * corresponding contributor: antoine.falaize@ircam.fr
    * date: 2016/10/04 19:05:37

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

    Created on 2016/10/04 19:05:37

    @author: Antoine Falaize



===============================================================================

    This file was automatically generated 
    by PyPHS v0.1.5, on 2016/10/04 19:05:37.

    It contains the code for the simulation of system 'RLC'.

===============================================================================
*/


#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <cstdio>
#include <time.h>
#include <math.h>

#include "phobj.h"

using namespace std;

class timer {
private:
    unsigned long begTime;
public:
    void start() {
        begTime = clock();
    }
    unsigned long elapsedTime() {
        return ((unsigned long) clock() - begTime) / CLOCKS_PER_SEC;
    }
    bool isTimeout(unsigned long seconds) {
        return seconds >= elapsedTime();
    }
};


int main() {    
    
    // System dimensions
    const unsigned int nx = 2;
    const unsigned int nxnl = 2;
    const unsigned int nw = 1;
    const unsigned int nwnl = 1;
    const unsigned int ny = 1;
    const unsigned int nsubs = 3;
    
    const unsigned int nt = 1920;

    vector<double> x0Vector(nx);
    vector<double> uVector(ny);
    vector<double> xVector(nx);
    vector<double> dxVector(nx);
    vector<double> dxHVector(nx);
    vector<double> wVector(nw);
    vector<double> zVector(nw);
    vector<double> yVector(ny);

    ifstream x0File;
    x0File.open("/Users/Falaize/Documents/DEV/python/pypHs/tests/RLC/data/x0.txt");

    if (x0File.fail()) {
        cerr << "Failed opening x0 file" << endl;
        exit(1);
    }

    ifstream uFile;
    uFile.open("/Users/Falaize/Documents/DEV/python/pypHs/tests/RLC/data/u.txt");

    if (uFile.fail()) {
        cerr << "Failed opening u file" << endl;
        exit(1);
    }


    // Instance of port-Hamiltonian system
    RLC PHS(x0Vector);

    int barWidth = 20;
    int ETA, ETAm, ETAs;
    float progress = 0.0;
    timer t;

    // Process
    t.start();

    ofstream xFile;
    xFile.open("/Users/Falaize/Documents/DEV/python/pypHs/tests/RLC/data/x.txt");
    ofstream dxFile;
    dxFile.open("/Users/Falaize/Documents/DEV/python/pypHs/tests/RLC/data/dx.txt");
    ofstream dxHFile;
    dxHFile.open("/Users/Falaize/Documents/DEV/python/pypHs/tests/RLC/data/dxH.txt");
    ofstream wFile;
    wFile.open("/Users/Falaize/Documents/DEV/python/pypHs/tests/RLC/data/w.txt");
    ofstream zFile;
    zFile.open("/Users/Falaize/Documents/DEV/python/pypHs/tests/RLC/data/z.txt");
    ofstream yFile;
    yFile.open("/Users/Falaize/Documents/DEV/python/pypHs/tests/RLC/data/y.txt");


    for (unsigned int n = 0; n < nt; n++) {


        // Get input data
        for (unsigned int i=0; i<ny; i++) {
            uFile >> uVector[i];
        }
        std::cout << "[";
        int pos = barWidth * progress;
        for (int i = 0; i < barWidth; ++i) {
            if (i < pos) std::cout << "=";
            else if (i == pos) std::cout << ">";
            else std::cout << " ";
        }
        progress = float(n)/float(nt);
        if(1){
            ETA = (float(nt)/float(n+1)-1.)*(t.elapsedTime());
            ETAm = int(floor(ETA))/60;
            ETAs = floor(ETA%60);
            std::cout << "] " << int(progress * 100.0) << " % done, ETA: " << ETAm << "m" << ETAs << "s\r" << endl ;
            std::cout.flush();
        }
        // Process update
        PHS.process(uVector);
        // Get quantities
xVector = PHS.get_x();
dxVector = PHS.get_dx();
dxHVector = PHS.get_dxH();
        for (unsigned int i = 0; i < nx; i++) {
            xFile << xVector[i] << " ";
            dxFile << dxVector[i] << " ";
            dxHFile << dxHVector[i] << " ";
        }
        xFile << endl;
        dxFile << endl;
        dxHFile << endl;

wVector = PHS.get_w();
zVector = PHS.get_z();
        for (unsigned int i = 0; i < nw; i++) {
            wFile << wVector[i] << " ";
            zFile << zVector[i] << " ";
        }
        wFile << endl;
        zFile << endl;

yVector = PHS.get_y();
        for (unsigned int i = 0; i < ny; i++) {
            yFile << yVector[i] << " ";
        }
        yFile << endl;
    }
    uFile.close();
    yFile.close();
    xFile.close();
    dxFile.close();
    dxHFile.close();
    wFile.close();
    zFile.close();
    cout << endl;
    cout << "Data written at" << endl;
    cout << endl;
    cout << "/Users/Falaize/Documents/DEV/python/pypHs/tests/RLC/data/"<< endl;
    cout << endl;

    return 0;
}
