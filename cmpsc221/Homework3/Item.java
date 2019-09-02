public class Item {
    public Item(String name, String lookDescription, int weight, int bulk) {
        this.lookDescription = lookDescription;
        this.name = name;
        this.weight = weight;
        this.bulk = bulk;
    } /* end Item */

    public String getLookDescription() {
        return lookDescription;
    } /* end getLookDescription */

    public String getName() {
        return name;
    } /* end getName */

    public int getWeight()
    {
        return weight;
    } /* end getWeight */

    public int getBulk()
    {
        return bulk;
    } /* end getBulk */

    private String lookDescription;
    private String name;
    private int weight;
    private int bulk;
} /* end Item */
