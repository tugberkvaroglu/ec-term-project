
import java.util.Random;

/**
 * Imp. of Differential Evolution Algorithm at
 * https://en.wikipedia.org/wiki/Differential_evolution
 *
 * @author user
 */
public class DE {

    //DE parameters
    private double F, CR; //F: differential weight, CR: crossover probability
    private int NP; //population size

    private double[][] solutions;
    private double[] fValues;
    private int funcNo, dimension;
    private double lowerBound, upperBound;

    private double[] best;
    private double fBest;

    private Random rng;

    StandardTestFunctions objFunc;

    public DE(int NP, double F, double CR, int funcNo, int dim, Random rng) {
        this.NP = NP;
        this.F = F;
        this.CR = CR;
        this.funcNo = funcNo;
        this.rng = rng;

        dimension = dim;
        objFunc = new StandardTestFunctions(rng);

        lowerBound = objFunc.getLowerBound(funcNo);
        upperBound = objFunc.getUpperBound(funcNo);
    }

    public double solve( int maxFEs) {
        int FEs = 0;

        //init solutions
        solutions = new double[NP][dimension];

        //init solutions with random values
        for (int i = 0; i < NP; i++) {
            for (int j = 0; j < dimension; j++) {
                solutions[i][j] = lowerBound + rng.nextDouble() * (upperBound - lowerBound);
            }
        }

        fValues = new double[NP];
        best = new double[dimension];
        fBest = Double.MAX_VALUE;

        //fill fValues for initial solutions
        for (int i = 0; i < NP; i++) {
            fValues[i] = objFunc.test_func(solutions[i], funcNo);
            FEs ++;
        }

        while (FEs < maxFEs) {
            for (int i = 0; i < NP; i++) { //For each agent X_i in the population
                double[] X_i = solutions[i];
                double fX_i = fValues[i];

                //Pick three agents from the population at random, they must be distinct from each other as well as from agent
                int r1, r2, r3;

                do {
                    r1 = rng.nextInt(NP);
                } while (r1 == i);

                double[] X_r1 = solutions[r1];

                do {
                    r2 = rng.nextInt(NP);
                } while (r2 == i || r2 == r1);

                double[] X_r2 = solutions[r2];

                do {
                    r3 = rng.nextInt(NP);
                } while (r3 == i || r3 == r1 || r3 == r2);

                double[] X_r3 = solutions[r3];

                int J = rng.nextInt(dimension); //Pick a random dimension index J

                double rand;
                double[] U_i = new double[dimension]; //the agent's potentially new position

                // combination of mutation and crossover
                for (int k = 0; k < dimension; k++) {
                    rand = rng.nextDouble();
                    if (rand < CR || k == J) {
                        U_i[k] = X_r1[k] + F * (X_r2[k] - X_r3[k]); //DE-rand-1 mutation strategy
                    } else {
                        U_i[k] = X_i[k];
                    }
                }

                //Ensure that the candidate solution is within the search space
                for (int j1 = 0; j1 < dimension; j1++) {
                    if (U_i[j1] < lowerBound) {
                        U_i[j1] = lowerBound;
                    } else if (U_i[j1] > upperBound) {
                        U_i[j1] = upperBound;
                    }
                }

                double fU_i = objFunc.test_func(U_i, funcNo); //Evaluate the candidate solution y
                FEs++;

                if (fU_i < fX_i) {
                    //replace the agent in the population with the improved candidate solution, that is, replace X_i with y in the population
                    solutions[i] = U_i;
                    fValues[i] = fU_i;

                    if (fU_i < fBest) {
                        //replace the global best
                        System.arraycopy(U_i, 0, best, 0, dimension);
                        fBest = fU_i;

                        //System.out.println("FEs: " + FEs + " Best: " + fBest);
                    }
                }

                if (FEs >= maxFEs) { //if maximum FEs budget is reached then exit loop
                    break;
                }
            }

        }
        return fBest; //return the best solution found
    }

}