import java.util.ArrayList;
import java.util.List;

public class Homework2
{
    public static void main(String[] args) {
        // Example 1
        Function<Integer, Integer> function = new CalculateSuccessor();
        Integer[] integerArray = {1, 3, 4, 2, 5};
        PrintArray(map(function, integerArray)); // map returns {2, 4, 5, 3, 6}
        // Example 2
        Function<Integer, String> anotherFunction = new CalculateLength();
        String[] stringArray = { "Java", "C++", "Smalltalk" };
        PrintArray(map(anotherFunction, stringArray)); // map returns {4, 3, 9}
        // Example 3
        Function<Double, Double> tripleFunction = new CalculateTriple();
        Double[] doubleArray = { 2.0, 4.0, 5.0, 1.0 };
        PrintArray(map(tripleFunction, doubleArray)); // map returns {6.0, 12.0, 15.0, 3.0}
    }

    private static class CalculateSuccessor implements Function<Integer, Integer>
    {
        @Override
        public Integer apply(Integer parameter)
        {
            return parameter + 1;
        }
    }

    private static class CalculateLength implements Function<Integer, String>
    {
        @Override
        public Integer apply(String parameter)
        {
            return parameter.length();
        }
    }

    private static class CalculateTriple implements Function<Double, Double>
    {
        @Override
        public Double apply(Double parameter)
        {
            return parameter * 3;
        }
    }

    public static <R, D> R[] map(Function<R, D> function, D[] array)
    {
        List<R> values = new ArrayList<>();
        for(D d : array)
            values.add(function.apply(d));
        return (R[])values.toArray();
    }

    public static <T> void PrintArray(T[] array)
    {
        System.out.print("{");
        for(int i = 0; i<array.length; i++)
        {
            if(i == array.length-1)
                System.out.print(array[i]);
            else
                System.out.print(array[i]+", ");
        }
        System.out.println("}");
    }
}
