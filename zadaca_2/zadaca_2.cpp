#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <random>
#include <cmath>
#include <chrono>
#include <algorithm> 

// pokretanje: g++ zadaca_2.cpp
// ./a.out

#define POPULACIJA_N 5
#define KOMPONENTE_N 4
#define MAX_GEN 2000

struct tocka
{
    double x;
    double y;
};

using namespace std;

vector<tocka> tocke = 
{
    {.x=2,.y=3.4},
    {.x=0.2,.y=0.6},
    {.x=8,.y=17},
    {.x=-3,.y=-0.5},
    {.x=12,.y=25}
};

double odstupanje(vector<double> const& v);
void ispisVektora(vector<double> const& v, double fit);
void ispisU_CSV(ofstream& MyFile, vector<double> const& v, double fit);

void init(mt19937& generator, vector< vector<double> >& populacija, double& beta, double& pr)
{
    time_t time = chrono::system_clock::to_time_t(chrono::system_clock::now());
    mt19937::result_type seed = static_cast<mt19937::result_type>(time);
    generator = mt19937(seed);
    uniform_real_distribution<double> distribucija(-5.0,5.0);

    // rand
    beta = 1.0;
    pr = 0.5;

    for(uint16_t j = 0; j < POPULACIJA_N; j++)
    {
        vector<double> v;
        for(uint8_t i=0; i<KOMPONENTE_N; i++)
            v.push_back(distribucija(generator));
        populacija.push_back(v);
    }
}

void izbor(mt19937& generator, vector<uint16_t>& izbornik, uint16_t& i1, uint16_t& i2, uint16_t& i3)
{
    uniform_int_distribution<uint16_t> distribucija(0,izbornik.size()-1); //za izbor vektora
    i1 = distribucija(generator);
    i2 = distribucija(generator);
    while (i2 == i1) {
        i2 = distribucija(generator);
    }
    i3 = distribucija(generator);
    while (i3 == i1 || i3 == i2) {
        i3 = distribucija(generator);
    }
}

void mutacija(vector< vector<double> > const& populacija, double beta, uint16_t i1, uint16_t i2, uint16_t i3, vector<double>& rezultat)
{
    for(uint8_t i=0; i<KOMPONENTE_N; i++)
        rezultat[i] = populacija[i1][i] + beta * (populacija[i2][i] - populacija[i3][i]);
}

void krizanje(mt19937& generator, uniform_int_distribution<uint8_t>& distribucija1, 
    uniform_real_distribution<double> distribucija2, vector<uint8_t>& izbornik, 
    vector<double> const& x, vector<double> const& u, double pr, vector<double>& J)
{
    for(auto it=izbornik.begin(); it!=izbornik.end(); ++it)
        *it = 1;
    uint8_t k = distribucija1(generator); //bira se neka komponenta
    izbornik[k] = 0;
    J[k] = u[k]; //bar jedna komponenta iz probnog vektora
    for(uint8_t i=0; i<KOMPONENTE_N-1; i++)
    {
        double p = distribucija2(generator); //vrijednost između 0 i 1
        k = distribucija1(generator); //bira se komponenta
        while(izbornik[k]==0)
            k=(k+1)%izbornik.size();
        izbornik[k] = 0;
        if(p<pr)
            J[k] = u[k]; //uzima se komponenta iz probnog vektora
        else
            J[k] = x[k]; //uzima se komponenta iz roditeljskog vektora
    }
}

void solver(mt19937& generator, string csvfilename, vector< vector<double> >& populacija, double beta, double pr)
{
    bool printToCSV = false;
    vector<uint16_t> izbornik; //za biranje indeksa vektora iz populacije
    izbornik.reserve(POPULACIJA_N);
    vector<uint8_t> izbornik1(KOMPONENTE_N); //za biranje komponenti
    uniform_int_distribution<uint8_t> distribucija1(0,KOMPONENTE_N-1); //za izbor komponenti
    uniform_real_distribution<double> distribucija2(0.0,1.0); //za vjerojatnosti
    vector<double> u(KOMPONENTE_N); //probni vektor
    vector<double> J(KOMPONENTE_N); //potomak
    vector<double> fits(populacija.size());
    for(uint16_t i=0; i<populacija.size(); i++) //unaprijed se racunaju fits
        fits[i] = odstupanje(populacija[i]);
    uint generacija = 1;

    ofstream MyFile;
    if (csvfilename != "")
	{
		MyFile = ofstream(csvfilename);
		printToCSV = true;
        MyFile << "a;b;c;d;fit" << endl;
	}

    while(1)
    {
        for(uint16_t i=0; i<populacija.size(); i++)
        {
            double fit;
            uint16_t i1, i2, i3;
            izbornik.clear();
            for(uint16_t j=0; j<POPULACIJA_N; j++)
            {
                if(i!=j)
                {
                    izbornik.push_back(j);
                }
            }
            izbor(generator, izbornik, i1, i2, i3); // biraju se sva tri
            mutacija(populacija, beta, i1, i2, i3, u);
            krizanje(generator, distribucija1, distribucija2, izbornik1, populacija[i], u, pr, J);
            fit = odstupanje(J);
            if(fit < fits[i])
            {
                populacija[i] = J;
                fits[i] = fit;
            }
        }
        double d = odstupanje(populacija[0]);
        cout << "Gen " << generacija << endl << "\t";
        ispisVektora(populacija[0], d);

        if (printToCSV)
            ispisU_CSV(MyFile,populacija[0],d);

        generacija++;
        if(d < 0.01 || generacija > MAX_GEN) //uvjet zaustavljanja
            break;
    }; 
    if (printToCSV) MyFile.close();
}

int main()
{
    mt19937 generator;
    vector< vector<double> > populacija;
    double pr;
    double beta;

    init(generator, populacija, beta, pr);
    solver(generator, "DE_data.csv", populacija, beta, pr);

    return 0;
}

double odstupanje(vector<double> const& v) // formula za lineariziranje funkcije oblika (ax + b) / (cx + d)
{
    if(v.size() != 4) // Treba imati 4 parametra a, b, c, d
        return numeric_limits<double>::max();

    double error = 0.0;
    for(auto& point : tocke)
    {
        double f_x = (v[0] * point.x + v[1]) / (v[2] * point.x + v[3]); // Računanje f(x)
        double residual = f_x - point.y; // Računanje reziduala
        error += residual * residual; // Dodavanje kvadrata reziduala
    }
    return sqrt(error); // Vraćanje kvadratnog korijena od sume kvadrata reziduala
}


void ispisVektora(vector<double> const& v, double fit)
{
    vector<double>::const_iterator it;
    cout << "(";
    for(it=v.begin(); it!=v.end()-1; ++it)
        cout << (double)(*it) << ";";
    cout << (double)(*it) << "), fit: " << fit << endl;
}

void ispisU_CSV(ofstream& MyFile, vector<double> const& v, double fit)
{
    vector<double>::const_iterator it;
    for(it=v.begin(); it!=v.end()-1; ++it)
        MyFile << (double)(*it) << ";";
    MyFile << (double)(*it) << ";" << fit << endl;
}
