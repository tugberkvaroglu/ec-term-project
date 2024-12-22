import java.util.Random;

public class Main {
    public static void main(String[] args) {

        // Run DE algorithm for 12 functions, 10 runs each
        /*for (int i = 1; i <= 12; i++) {
            for (int run = 0; run < 10; run++) {
                DE de = new DE(40, 0.5, 0.9, i, 30, new Random(run));
                double fBest = de.solve(50000);
                System.out.println("Function " + i + " Run " + run + " fBest: " + fBest);
            }
        }*/

        // Run PSO algorithm for 12 functions, 10 runs each
        for (int i = 1; i <= 12; i++) {
            for (int run = 0; run < 10; run++) {
                PSO pso = new PSO(40, 0.5, 1.5, 1.5, i, 30, new Random(run));
                double fBest = pso.solve(50000);
                System.out.println("Function " + i + " Run " + run + " fBest: " + fBest);
            }
        }
    }
}