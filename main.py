class MemorySlot:
    #This parameterized constroctor use to update the new proses details
    def __init__(self, process_id, size):
        #ProcessId
        self.process_id = process_id
        #ProcessSize
        self.size = size
        #Boolean value for check the alocation true false
        self.is_allocated = False
        #mark next node as none
        self.next = None

class SlotManager:

    # This parameterized constructor use to update OS and main memory details
    def __init__(self, memory_size, os_size):
        self.memory_size = memory_size
        self.os_size = os_size
        self.free_memory = memory_size - os_size
        self.head = MemorySlot(None, self.free_memory)

#this function is used to alocate the new process to the main memory
    def allocate(self, process_id, size):
        current = self.head
#use wile loop for the content select
        while current:
            # this logic is check the size of process and the allocation Status
            if not current.is_allocated and current.size >= size:
                #logic when size is equal
                if current.size == size:
                    current.process_id = process_id
                    current.is_allocated = True
                else:
                    #logic when size is smale than free space
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

    # this function is used to release the memory status
    def release_memory(self, process_id2):
        current = self.head
       # print(current.process_id)
       #print(process_id2)
       # print(current.is_allocated)
        while current:
            if current.process_id == process_id2 and current.is_allocated:
                #remove process id
                current.process_id = None
                #set boolien value as false
                current.is_allocated = False
                #call to calculate free block
                self.merge_free_blocks()
                print(current.size)
                #total free size
                self.free_memory += current.size
                print(f"Memory released for Process {process_id2}.")
                return
            current = current.next
        print(f"Error: Process {process_id2} not found or not allocated")

    # this function is used to calculate the free blocks of  the status r
    def merge_free_blocks(self):
        current = self.head
        while current and current.next:
            if not current.is_allocated and not current.next.is_allocated:
                current.size += current.next.size
                current.next = current.next.next
            else:
                current = current.next
#this function is used to print the status relatd to the 3rd switch fun call
    def print_status(self):
        current = self.head
        print("Memory Usage:")
        while current:
            status = "Allocated" if current.is_allocated else "Free"
            print(f"Process ID: {current.process_id}, Size: {current.size}KB, Status: {status}")
            current = current.next
        print()

#main memory size definition and os Size definition
print("\n/////////////////////////////////////////////////////////////////////////////////////////////////////////")
Mainmemory_size = int(input("Enter the total memory size in KB: "))
OS_size = int(input("Enter the size of the operating system in KB: "))
print("\n/////////////////////////////////////////////////////////////////////////////////////////////////////////")
slot = SlotManager(Mainmemory_size, OS_size)

while True:
    #Menu for the user console interfce
    print("\n1. Allocate process")
    print("2. Release process")
    print("3. Print memory status")
    print("4. Exit")
    choice = int(input("Enter your choice: "))
#Switch case combination to call the correct funtion behaviours
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