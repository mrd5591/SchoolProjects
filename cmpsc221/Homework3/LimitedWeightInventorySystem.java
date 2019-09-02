import edu.psu.cmpsc221.exceptions.ItemNotInInventoryException;

public class LimitedWeightInventorySystem extends InventorySystem
{
    private int maxWeight;
    private int currentTotalWeight;

    public LimitedWeightInventorySystem(int maxWeight)
    {
        this.maxWeight = maxWeight;
        this.currentTotalWeight = 0;
    }

    @Override
    protected boolean canAddItem(Item item) {
        if(item.getWeight() + currentTotalWeight > maxWeight)
            return false;
        currentTotalWeight += item.getWeight();
        return true;
    }

    @Override
    protected String getInventoryFullMessage() {
        return "You cannot add this item to your inventory! It is too heavy!";
    }

    @Override
    protected Item removeItemNamed(String item) throws ItemNotInInventoryException
    {
        Item rmItem = super.removeItemNamed(item);
        currentTotalWeight -= rmItem.getWeight();
        return rmItem;
    }
}
