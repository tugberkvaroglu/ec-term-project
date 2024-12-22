
import java.util.Random;

public class PSO {

    //PSO parameters
    private double w, c1, c2; //w: inertia weight, c1: cognitive weight, c2: social weight
    private int NP; //population size

    private double[][] X, V, P;
    private double[] fX, fP;

    private int funcNo, dimension;
    private double lowerBound, upperBound;

    private double[] G;
    private double fG;

    private Random rng;

    StandardTestFunctions objFunc;

    public PSO(int NP, double w, double c1, double c2, int funcNo, int dim, Random rng) {
        this.NP = NP;
        this.w = w;
        this.c1 = c1;
        this.c2 = c2;
        this.funcNo = funcNo;
        this.rng = rng;

        dimension = dim;
        objFunc = new StandardTestFunctions(rng);

        lowerBound = objFunc.getLowerBound(funcNo);
        upperBound = objFunc.getUpperBound(funcNo);
    }

    public double solve(int maxFEs) {
        int FEs = 0;

        //init solutions
        X = new double[NP][dimension];
        V = new double[NP][dimension];
        P = new double[NP][dimension];

        //init f values
        fX = new double[NP];
        fP = new double[NP];

        //init global best
        G = new double[dimension];
        fG = Double.POSITIVE_INFINITY;

        //init X with random values, fill P with X, and evaluate fX, fP, fG
        for (int i = 0; i < NP; i++) {
            for (int j = 0; j < dimension; j++) {
                X[i][j] = lowerBound + rng.nextDouble() * (upperBound - lowerBound);
            }
            System.arraycopy(X[i], 0, P[i], 0, dimension);
            fX[i] = objFunc.test_func(X[i], funcNo);
            fP[i] = fX[i];

            if (fX[i] < fG) {
                System.arraycopy(X[i], 0, G, 0, dimension);
                fG = fX[i];
            }

            FEs++;
        }

        // init V with random values
        double diff = Math.abs(upperBound - lowerBound);
        for (int i = 0; i < NP; i++) {
            for (int j = 0; j < dimension; j++) {
                V[i][j] = -diff + rng.nextDouble() * 2 * diff;
            }
        }

        while (FEs < maxFEs) {
            for (int i = 0; i < NP; i++) { //For each agent X_i in the population
                for (int j = 0; j < dimension; j++) {
                    double r1 = rng.nextDouble();
                    double r2 = rng.nextDouble();

                    V[i][j] = w * V[i][j]
                            + c1 * r1 * (P[i][j] - X[i][j])
                            + c2 * r2 * (G[j] - X[i][j]);
                    X[i][j] = X[i][j] + V[i][j];
                }

                //Ensure that the candidate solution is within the search space
                for (int j = 0; j < dimension; j++) {
                    if (X[i][j] < lowerBound) {
                        X[i][j] = lowerBound;
                    } else if (X[i][j] > upperBound) {
                        X[i][j] = upperBound;
                    }
                }

                fX[i] = objFunc.test_func(X[i], funcNo);
                FEs++;

                if (fX[i] < fP[i]) {
                    System.arraycopy(X[i], 0, P[i], 0, dimension);
                    fP[i] = fX[i];

                    if (fX[i] < fG) {
                        System.arraycopy(X[i], 0, G, 0, dimension);
                        fG = fX[i];
                    }
                }

                if (FEs >= maxFEs) { //if maximum FEs budget is reached then exit loop
                    break;
                }
            }

        }
        return fG; //return the best solution found
    }

}