# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 02:09:01 2016

@author: Falaize
"""

def main_presolve(phs):
    str_main = """
//
//  main.cpp
//  phs
//
//  Created by Antoine Falaize on 21/09/2015.
//  Copyright (c) 2015 Antoine Falaize. All rights reserved.
//

#include <iostream>
"""+ '#include "'+phs.paths['cpp']+"/" + ("phobj").upper() + '.h"\n\n'+\
"""
#include "vector"

#include <fstream>
#include <string>

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

    ifstream x0File;
    x0File.open("""+ '"'+phs.paths['data']+"/"+ """x0.txt");

    if (x0File.fail()) {
        cerr << "Failed opening x0 file" << endl;
        exit(1);
    }

    ifstream uFile;
    uFile.open("""+ '"'+phs.paths['data']+"/"+ """u.txt");

    if (uFile.fail()) {
        cerr << "Failed opening input file" << endl;
        exit(1);
    }

    ifstream pFile;
    pFile.open("""+'"'+ phs.paths['data']+"/"+ """p.txt");

    if (pFile.fail()) {
        cerr << "Failed opening parameters file" << endl;
        exit(1);
    }

    unsigned int nt = 0;

    vector<double> xVector("""+ str(phs.dims.x()) +""");
    vector<double> x0Vector("""+ str(phs.dims.x()) +""");
    vector<double> dxHVector("""+ str(phs.dims.x()) +""");
    vector<double> dxVector("""+ str(phs.dims.x()) +""");
    vector<double> wVector("""+ str(phs.dims.w()) +""");
    vector<double> zVector("""+ str(phs.dims.w()) +""");
    vector<double> uVector("""+ str(phs.dims.y()) +""");
    vector<double> yVector("""+ str(phs.dims.y()) +""");
    vector<double> pVector("""+ str(phs.dims.p()) +""");

    typedef std::vector< std::vector<double> > matrix;

    matrix matU(0, vector<double>("""+ str(phs.dims.y()) +"""));
    matrix matP(0, vector<double>("""+ str(phs.dims.p()) +"""));

    for (unsigned int i=0; i<"""+ str(+phs.dims.x()) +"""; i++) {
        x0File >> x0Vector[i];
    }

"""+ '    ' + phs.label.upper() +' sys(x0Vector);'+\
"""
    
    
    // Get input data
    cout <<"Reading input..." << endl;
    while (!uFile.eof()) {
    
        for (unsigned int i=0; i<sys.get_ny(); i++) {
            uFile >> uVector[i];
        }

        // Get parameters data
        for (unsigned int i=0; i<sys.get_np(); i++) {
            pFile >> pVector[i];
        }
        matU.push_back(uVector);
        matP.push_back(pVector);

        nt = unsigned(int(matU.size()));
    }

    uFile.close();
    pFile.close();

    nt -= 1;
    
    matrix matX(nt, vector<double>("""+ str(phs.dims.x()) +"""));
    matrix matdX(nt, vector<double>("""+ str(phs.dims.x()) +"""));
    matrix matdxH(nt, vector<double>("""+ str(phs.dims.x()) +"""));
    matrix matW(nt, vector<double>("""+ str(phs.dims.w()) +"""));
    matrix matZ(nt, vector<double>("""+ str(phs.dims.w()) +"""));
    matrix matY(nt, vector<double>("""+ str(phs.dims.y()) +"""));

    // Compute
    cout <<"Process simulation..." << endl;
    int ETA, ETAm, ETAs;
    float progress = 0.0;
    timer t;	
    t.start();        
    for (unsigned int n=0; n<nt; n++) {
        
        int barWidth = 20;
        std::cout << "[";
        int pos = barWidth * progress;
        for (int i = 0; i < barWidth; ++i) {
            if (i < pos) std::cout << "=";
            else if (i == pos) std::cout << ">";
            else std::cout << " ";
        }
        progress = float(n)/float(nt); 
        if(1){
            ETA = int((nt-(n+1.))*(t.elapsedTime()/(n+1.)));
            ETAm = ETA/60;            
            ETAs = ETA%60;
            std::cout << "] " << int(progress * 100.0) << " % simulation, ETA: " << ETAm << "m" << ETAs << "s\\r" << endl ;
            std::cout.flush();
        }
        
        uVector = matU[n];
        pVector = matP[n];

        // Get x before process update
        xVector = sys.get_x();

        // Process update
        sys.process(uVector, pVector);

        // Get quantities
        dxVector = sys.get_dx();
        dxHVector = sys.get_dxH();
        wVector = sys.get_w();
        zVector = sys.get_z();
        yVector = sys.get_y();

        matX[n] = xVector;
        matdX[n] = dxVector;
        matdxH[n] = dxHVector;
        matW[n] = wVector;
        matZ[n] = zVector;
        matY[n] = yVector;
    }

    ofstream xFile;
    xFile.open("""+'"'+ phs.paths['data']+"/"+ """x.txt");
    ofstream dxHFile;
    dxHFile.open("""+'"'+ phs.paths['data']+"/"+ """dxH.txt");
    ofstream dxFile;
    dxFile.open("""+'"'+ phs.paths['data']+"/"+ """dx.txt");

    ofstream wFile;
    wFile.open("""+'"'+ phs.paths['data']+"/"+ """w.txt");
    ofstream zFile;
    zFile.open("""+'"'+ phs.paths['data']+"/"+ """z.txt");

    ofstream yFile;
    yFile.open("""+'"'+ phs.paths['data']+"/"+ """y.txt");

    // Save
    cout << "Write output..."<< endl;
    for (unsigned int n=0; n<nt; n++) {

        int barWidth = 20;
        std::cout << "[";
        int pos = barWidth * progress;
        for (int i = 0; i < barWidth; ++i) {
            if (i < pos) std::cout << "=";
            else if (i == pos) std::cout << ">";
            else std::cout << " ";
        }
        progress = float(n)/float(nt); 
        if(1){
            ETA = int((nt-(n+1.))*(t.elapsedTime()/(n+1.)));
            ETAm = ETA/60;            
            ETAs = ETA%60;
            std::cout << "] " << int(progress * 100.0) << " % export, ETA: " << ETAm << "m" << ETAs << "s\\r" << endl ;
            std::cout.flush();
        }

        // cout << "Writing Data " << int(100.0*float(n)/nt) << endl;
        xVector = matX[n];
        dxVector = matdX[n];
        dxHVector = matdxH[n];

        wVector = matW[n];
        zVector = matZ[n];

        yVector = matY[n];
        
        // Save quantities
        for (unsigned int i=0; i<sys.get_nx(); i++) {
            xFile << xVector[i] << " ";
            dxFile << dxVector[i] << " ";
            dxHFile << dxHVector[i] << " ";
        }

        for (unsigned int i=0; i<sys.get_nw(); i++) {
            wFile << wVector[i] << " ";
            zFile << zVector[i] << " ";
        }

        for (unsigned int i=0; i<sys.get_ny(); i++) {
            yFile << yVector[i] << " ";
        }

        xFile << endl;
        dxFile << endl;
        dxHFile << endl;

        wFile << endl;
        zFile << endl;    

        yFile << endl;
        
    }

    xFile.close();
    dxFile.close();
    dxHFile.close();
    wFile.close();
    zFile.close();
    yFile.close();

    cout << endl;
    cout << "Data written at" << endl;
    cout << endl;
    cout << """+'"'+ phs.paths['data']+"/"+'"' +"""<< endl;
    cout << endl;
    
    return 0;
}
"""
    main_file = open(phs.paths['cpp']+"/main.cpp", 'w')
    main_file.write(str_main)
    main_file.close()
    return str_main
    




def main_full(phs):
    str_main = """
//
//  main.cpp
//  phs
//
//  Created by Antoine Falaize on 21/09/2015.
//  Copyright (c) 2015 Antoine Falaize. All rights reserved.
//

#include <iostream>
"""+ '#include "'+phs.paths['cpp']+"/" + ('phobj').upper() + '.h"\n\n'+\
"""
#include "vector"

#include <fstream>
#include <string>
#include <cstdio>
#include <time.h>
#include <math.h>

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

    ifstream x0File;
    x0File.open("""+ '"'+phs.paths['data']+"/"+ """x0.txt");

    if (x0File.fail()) {
        cerr << "Failed opening x0 file" << endl;
        exit(1);
    }

    ifstream uFile;
    uFile.open("""+ '"'+phs.paths['data']+"/"+ """u.txt");

    if (uFile.fail()) {
        cerr << "Failed opening input file" << endl;
        exit(1);
    }

    ifstream pFile;
    pFile.open("""+'"'+ phs.paths['data']+"/"+ """p.txt");

    if (pFile.fail()) {
        cerr << "Failed opening parameters file" << endl;
        exit(1);
    }

    unsigned int nt = 0;

    vector<double> xVector("""+ str(phs.dims.x()) +""");
    vector<double> x0Vector("""+ str(phs.dims.x()) +""");
    vector<double> dxHVector("""+ str(phs.dims.x()) +""");
    vector<double> dxVector("""+ str(phs.dims.x()) +""");
    vector<double> wVector("""+ str(phs.dims.w()) +""");
    vector<double> zVector("""+ str(phs.dims.w()) +""");
    vector<double> uVector("""+ str(phs.dims.y()) +""");
    vector<double> yVector("""+ str(phs.dims.y()) +""");
    vector<double> pVector("""+ str(phs.dims.p()) +""");

    typedef std::vector< std::vector<double> > matrix;

    matrix matU(0, vector<double>("""+ str(phs.dims.y()) +"""));
    matrix matP(0, vector<double>("""+ str(phs.dims.p()) +"""));

    for (unsigned int i=0; i<"""+ str(+phs.dims.x()) +"""; i++) {
        x0File >> x0Vector[i];
    }

"""+ '    ' + phs.label.upper() +' sys(x0Vector);'+\
"""
    
    
    // Get input data
    cout <<"Reading input..." << endl;
    while (!uFile.eof()) {
    
        for (unsigned int i=0; i<sys.get_ny(); i++) {
            uFile >> uVector[i];
        }

        // Get parameters data
        for (unsigned int i=0; i<sys.get_np(); i++) {
            pFile >> pVector[i];
        }
        matU.push_back(uVector);
        matP.push_back(pVector);

        nt = unsigned(int(matU.size()));
    }

    uFile.close();
    pFile.close();

    nt -= 1;
    
    // Compute
    cout <<"Process simulation..." << endl;
    int ETA, ETAm, ETAs;
    float progress = 0.0;
    timer t;	
    t.start();

    ofstream xFile;
    xFile.open("""+'"'+ phs.paths['data']+"/"+ """x.txt");
    ofstream dxHFile;
    dxHFile.open("""+'"'+ phs.paths['data']+"/"+ """dxH.txt");
    ofstream dxFile;
    dxFile.open("""+'"'+ phs.paths['data']+"/"+ """dx.txt");

    ofstream wFile;
    wFile.open("""+'"'+ phs.paths['data']+"/"+ """w.txt");
    ofstream zFile;
    zFile.open("""+'"'+ phs.paths['data']+"/"+ """z.txt");

    ofstream yFile;
    yFile.open("""+'"'+ phs.paths['data']+"/"+ """y.txt");
    
    for (unsigned int n=0; n<nt; n++) {
        
        int barWidth = 20;
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
            std::cout << "] " << int(progress * 100.0) << " % done, ETA: " << ETAm << "m" << ETAs << "s\\r" << endl ;
            std::cout.flush();
        }
        
        uVector = matU[n];
        pVector = matP[n];

        // Get x before process update
        xVector = sys.get_x();

        // Process update
        sys.process(uVector, pVector);

        // Get quantities
        dxVector = sys.get_dx();
        dxHVector = sys.get_dxH();
        wVector = sys.get_w();
        zVector = sys.get_z();
        yVector = sys.get_y();

//            matX[n] = xVector;
//            matdX[n] = dxVector;
//            matdxH[n] = dxHVector;
//            matW[n] = wVector;
//            matZ[n] = zVector;
//            matY[n] = yVector;
 
        for (unsigned int i=0; i<sys.get_nx(); i++) {
            xFile << xVector[i] << " ";
            dxFile << dxVector[i] << " ";
            dxHFile << dxHVector[i] << " ";
        }

        for (unsigned int i=0; i<sys.get_nw(); i++) {
            wFile << wVector[i] << " ";
            zFile << zVector[i] << " ";
        }

        for (unsigned int i=0; i<sys.get_ny(); i++) {
            yFile << yVector[i] << " ";
        }

        xFile << endl;
        dxFile << endl;
        dxHFile << endl;

        wFile << endl;
        zFile << endl;    

        yFile << endl;
        
    }

    xFile.close();
    dxFile.close();
    dxHFile.close();
    wFile.close();
    zFile.close();
    yFile.close();

    cout << endl;
    cout << "Data written at" << endl;
    cout << endl;
    cout << """+'"'+ phs.paths['data']+"/"+'"' +"""<< endl;
    cout << endl;
    
    return 0;
}
"""
    main_file = open(phs.paths['cpp']+"/main.cpp", 'w')
    main_file.write(str_main)
    main_file.close()
    return str_main
