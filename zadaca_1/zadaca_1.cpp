#include <iostream>
#include <cmath>
#include <fstream>
#include <random>
#include <chrono>
#include <vector>

// pokretanje: g++ zadaca_1.cpp
// ./a.out

using namespace std;

double funkcijaA(double x)
{
    double fx = 0.2 * (x - 2.0) * sin(7.0 * x - 15.0) + 1;
    if (fx >= 1.0)
    {
        fx = cos(2.0 / (pow(x - 6.0, 2.0) + 1.0)) + 0.7;
    }
    return fx;
}

int main(void)
{
    unsigned long long seed = chrono::high_resolution_clock::now().time_since_epoch().count();
    mt19937_64 rng(seed);
    double Xlb = 2.0;
    double Xub = 6.0;
    double xNB;
    double fxNB;
    unsigned swarmSize = 5;
    vector<double> xPB;
    vector<double> x;
    vector<double> v;

    long nIterations = 100;
    double w = 0.6;
    double C1 = 1.2;
    double C2 = 1.8;

    uniform_real_distribution<double> Rx(Xlb, Xub);
    uniform_real_distribution<double> r(0.0, 1.0);
    ofstream MyFile("PSO01_askarica.csv");

    x.resize(swarmSize);
    v.resize(swarmSize);
    xPB.resize(swarmSize);
    for (unsigned i = 0; i < swarmSize; i++)
    {
        x.at(i) = Rx(rng);
        v.at(i) = 0.0;
        xPB.at(i) = x.at(i);
        if (i == 0 || funkcijaA(xPB.at(i)) < fxNB)
        {
            xNB = xPB.at(i);
            fxNB = funkcijaA(xNB);
        }
    }

    MyFile << "bestX ; funkcijaA(bestX)" << endl;

    for (long iter = 0; iter < nIterations; iter++)
    {
        for (unsigned i = 0; i < swarmSize; i++)
        {
            v[i] = w * v[i] + C1 * r(rng) * (xPB[i] - x[i]) + C2 * r(rng) * (xNB - x[i]);
            x[i] = x[i] + v[i];

            if (x[i] > Xub)
            {
                x[i] = Xub;
            }
            else if (x[i] < Xlb)
            {
                x[i] = Xlb;
            }
            if (funkcijaA(x[i]) < funkcijaA(xPB[i]))
            {
                xPB[i] = x[i];
            }
            if (funkcijaA(xPB[i]) < fxNB)
            {
                xNB = xPB[i];
                fxNB = funkcijaA(xNB);
            }
        }
        MyFile << xNB << ";" << fxNB << endl;
    }
    cout << "Najbolje pronadeno rjesenje: xNB =  " << xNB << "  f(xNB) = " << fxNB << endl;

    MyFile.close();
}