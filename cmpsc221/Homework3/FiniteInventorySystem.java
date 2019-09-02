import edu.psu.cmpsc221.exceptions.InventoryFullException;
import edu.psu.cmpsc221.exceptions.ItemNotInInventoryException;

public class FiniteInventorySystem extends InventorySystem {

    private int inventorySpaceLeft;

    public FiniteInventorySystem(int inventorySpaceLeft)
    {
        this.inventorySpaceLeft = inventorySpaceLeft;
    }

    @Override
    protected boolean canAddItem(Item item) {
        if(inventorySpaceLeft <= 0)
            return false;
        inventorySpaceLeft--;
        return true;
    }

    @Override
    protected String getInventoryFullMessage() {
        return "You cannot add this item to your inventory! You have no space left!";
    }

    @Override
    protected Item removeItemNamed(String item) throws ItemNotInInventoryException
    {
        inventorySpaceLeft++;
        return super.removeItemNamed(item);
    }
}
