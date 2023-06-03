class MemorySlot:
    def __init__(self, process_id, size):
        self.process_id = process_id
        self.size = size
        self.is_allocated = False
        self.next = None

class SlotManager:
    def __init__(self, memory_size, os_size):
        self.memory_size = memory_size
        self.os_size = os_size
        self.free_memory = memory_size - os_size
        self.head = MemorySlot(None, self.free_memory)

    def allocate(self, process_id, size):
        current = self.head

        while current:
            if not current.is_allocated and current.size >= size:
                if current.size == size:
                    current.process_id = process_id
                    current.is_allocated = True
                else:
                    new_slot = MemorySlot(process_id, size)
                    new_slot.next = current.next
                    current.next = new_slot
                    current.size -= size
                    current.process_id = current.next.process_id
                    current.is_allocated = True
                   # print(current.next.process_id)
                print(f"Process {process_id} allocated {size}KB of memory.")
                return
            current = current.next
        print(f"Error: Not enough memory Process {process_id}")

    def release_memory(self, process_id2):
        current = self.head
       # print(current.process_id)
       #print(process_id2)
       # print(current.is_allocated)
        while current:
            if current.process_id == process_id2 and current.is_allocated:
                current.process_id = None
                current.is_allocated = False
                self.merge_free_blocks()
                print(current.size)
                self.free_memory += current.size
                print(f"Memory released for Process {process_id2}.")
                return
            current = current.next
        print(f"Error: Process {process_id2} not found or not allocated")

    def merge_free_blocks(self):
        current = self.head
        while current and current.next:
            if not current.is_allocated and not current.next.is_allocated:
                current.size += current.next.size
                current.next = current.next.next
            else:
                current = current.next

    def print_status(self):
        current = self.head
        print("Memory Usage:")
        while current:
            status = "Allocated" if current.is_allocated else "Free"
            print(f"Process ID: {current.process_id}, Size: {current.size}KB, Status: {status}")
            current = current.next
        print()


print("\n/////////////////////////////////////////////////////////////////////////////////////////////////////////")
Mainmemory_size = int(input("Enter the total memory size in KB: "))
OS_size = int(input("Enter the size of the operating system in KB: "))
print("\n/////////////////////////////////////////////////////////////////////////////////////////////////////////")
slot = SlotManager(Mainmemory_size, OS_size)

while True:
    print("\n1. Allocate process")
    print("2. Release process")
    print("3. Print memory status")
    print("4. Exit")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        process_id = input("Enter the process Name/ID: ")
        size = int(input("Enter the memory size needed in KB: "))
        slot.allocate(process_id, size)
    elif choice == 2:
        process_id = input("Enter the process ID to release memory: ")
        slot.release_memory(process_id)
    elif choice == 3:
        slot.print_status()
    elif choice == 4:
        break
    else:
        print("Invalid.......Please try again.")