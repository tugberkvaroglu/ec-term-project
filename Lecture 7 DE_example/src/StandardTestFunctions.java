import java.util.Random;

public class StandardTestFunctions {
    private Random rng;

    public StandardTestFunctions(Random rng) {
        this.rng = rng;
    }

    public double getUpperBound(int funcNum) {
        switch (funcNum) {
            case 1:
                return 100;
            case 2:
                return 10;
            case 3:
                return 100;
            case 4:
                return 100;
            case 5:
                return 30;
            case 6:
                return 100;
            case 7:
                return 1.28;
            case 8:
                return 500;
            case 9:
                return 5.12;
            case 10:
                return 32;
            case 11:
                return 600;
            case 12:
                return 50;

        }
        return Double.NaN;
    }

    public double getLowerBound(int funcNum) {
        return -getUpperBound(funcNum);
    }

    public double getOptimum(int funcNum, int dimension) {
        if (funcNum == 8) {
            return ((double)dimension) * -418.982887272433799807913601398;
        } else {
            return 0;
        }
    }

    public double test_func(double[] x, int func_num) {
        switch (func_num) {
            case 1:
                return f1(x);
            case 2:
                return f2(x);
            case 3:
                return f3(x);
            case 4:
                return f4(x);
            case 5:
                return f5(x);
            case 6:
                return f6(x);
            case 7:
                return f7(x);
            case 8:
                return f8(x);
            case 9:
                return f9(x);
            case 10:
                return f10(x);
            case 11:
                return f11(x);
            case 12:
                return f12(x);
        }
        return Double.NaN;
    }

    //sphere
    private double f1(double[] x) {
        double total = 0.0;

        for (int i = 0; i < x.length; i++) {
            total += Math.pow(x[i], 2);
        }

        return total;
    }

    //schwefel2_22
    private double f2(double[] x) {
        double total1 = 0.0, total2 = 1.0;

        for (int i = 0; i < x.length; i++) {
            total1 += Math.abs(x[i]);
            total2 *= Math.abs(x[i]);
        }

        return total1 + total2;
    }

    //schwefel1_2
    private double f3(double[] x) {
        double total = 0.0;

        for (int i = 0; i < x.length; i++) {
            double total2 = 0.0;
            for (int j = 0; j < i; j++) {
                total2 += x[j];
            }
            total += Math.pow(total2, 2);
        }

        return total;
    }

    //schwefel2_21
    private double f4(double[] x) {
        double max = 0.0;

        for (int i = 0; i < x.length; i++) {
            if (x[i] > max) {
                max = x[i];
            }
        }

        return max;
    }

    //generalizedRosenbrock
    private double f5(double[] x) {
        double total = 0.0;

        for (int i = 0; i < x.length - 1; i++) {
            total += 100.0 * Math.pow(x[i + 1] - Math.pow(x[i], 2), 2) + Math.pow(x[i] - 1, 2);
        }

        return total;
    }

    //step
    private double f6(double[] x) {
        double total = 0.0;

        for (int i = 0; i < x.length; i++) {
            total += Math.pow(Math.floor(x[i] + 0.5), 2);
        }

        return total;
    }

    //quartic with noise
    private double f7(double[] x) {
        double total = 0.0;

        for (int i = 0; i < x.length; i++) {
            total += (((double) (i + 1)) * Math.pow(x[i], 4));
        }

        total += rng.nextDouble(); //add noise
        return total;
    }

    //Generalized Schwefel’s Problem 2.26
    private double f8(double[] x) {
        double total = 0.0;

        for (int i = 0; i < x.length; i++) {
            total += (x[i] * Math.sin(Math.sqrt(Math.abs(x[i]))));
        }

        return -total;
    }

    //Generalized Rastrigin’s Function
    private double f9(double[] x) {
        double total = 0.0;

        for (int i = 0; i < x.length; i++) {
            total += (Math.pow(x[i], 2) - (10.0 * Math.cos(2.0 * Math.PI * x[i])) + 10.0);
        }

        return total;
    }

    //Ackley’s Function
    private double f10(double[] x) {
        double total1 = 0.0;
        double total2 = 0.0;

        for (int i = 0; i < x.length; i++) {
            total1 += Math.pow(x[i], 2);
            total2 += (Math.cos(2.0 * Math.PI * x[i]));
        }

        return (-20.0 * Math.exp(-0.2 * Math.sqrt(total1 / ((double) x.length)))
                - Math.exp(total2 / ((double) x.length)) + 20.0 + Math.E);
    }

    //Generalized Griewank Function
    private double f11(double[] x) {
        double total1 = 0.0;
        double total2 = 1.0;

        for (int i = 0; i < x.length; i++) {
            total1 += Math.pow(x[i], 2);
            total2 *= Math.cos(x[i] / Math.sqrt(i + 1));
        }

        return (1.0 / 4000.0) * total1 - total2 + 1;
    }

    //Generalized Penalized Function 1
    private double f12(double[] x) {
        double total1 = 0.0;
        double total2 = 0.0;
        double y1 = 1.0 + (x[0] + 1.0) / 4.0;
        double yn = 1.0 + (x[x.length - 1] + 1.0) / 4.0;
        for (int i = 0; i < x.length - 1; i++) {
            double yi = 1.0 + (x[i] + 1.0) / 4.0;
            double yi1 = 1.0 + (x[i + 1] + 1.0) / 4.0;
            total1 += Math.pow(yi - 1, 2) * (1.0 + 10.0 * Math.pow(Math.sin(Math.PI * yi1), 2));
            total2 += u(x[i], 10, 100, 4);
        }

        total2 += u(x[x.length - 1], 10, 100, 4); //for the last i

        return (Math.PI / 30.0) * (10 * Math.pow(Math.sin(Math.PI * y1), 2) + total1 + Math.pow(yn - 1, 2)) + total2;
    }

    private double u(double xi, double a, double k, double m) {
        if (xi > a) {
            return k * Math.pow(xi - a, m);
        }

        if (xi >= -a && xi <= a) {
            return 0;
        }

        if (xi < -a) {
            return k * Math.pow(-xi - a, m);
        }

        return Double.NaN;
    }
}
