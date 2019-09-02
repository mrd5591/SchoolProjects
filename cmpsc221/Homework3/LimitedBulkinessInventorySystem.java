import edu.psu.cmpsc221.exceptions.ItemNotInInventoryException;

public class LimitedBulkinessInventorySystem extends InventorySystem
{
    private int maxBulk;
    private int currentTotalBulk;

    public LimitedBulkinessInventorySystem(int maxBulk)
    {
        this.maxBulk = maxBulk;
        this.currentTotalBulk = 0;
    }

    @Override
    protected boolean canAddItem(Item item) {
        if(item.getBulk() + currentTotalBulk > maxBulk)
            return false;
        currentTotalBulk += item.getBulk();
        return true;
    }

    @Override
    protected String getInventoryFullMessage() {
        return "You cannot add this item to your inventory! It is too bulky!";
    }

    @Override
    protected Item removeItemNamed(String item) throws ItemNotInInventoryException
    {
        Item rmItem = super.removeItemNamed(item);
        currentTotalBulk -= rmItem.getBulk();
        return rmItem;
    }
}
