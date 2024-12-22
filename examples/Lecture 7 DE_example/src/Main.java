import java.util.Random;

public class Main {
    public static void main(String[] args) {

        for (int i = 1; i <= 12; i++) { //12 different test functions
            for (int run = 0; run < 10; run++) { //10 runs with different random number generators (different seeds)
                DE de = new DE(40, 0.5, 0.9, i, 30, new Random(run));
                double fBest = de.solve(50000);
                System.out.println("Function " + i + " Run " + run + " fBest: " + fBest);
            }
        }

    }
}