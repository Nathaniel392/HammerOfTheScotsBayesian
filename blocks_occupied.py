import initialize_blocks

def blocks_occupied():
    """
    Returns a list of 24 lists
    """
    territory_lst = list()
    for i in range(25):
        territory_lst.append(list())
        
      
    return territory_lst

def make_occupied(scenario, block_list):
    """
    Initialize the locations of blocks
    scenario:  1=Braveheart, 2=Bruce
    block_list:  list of all block objects, no alliegance assigned
    """

    #Loop through the blocks and assign alliegance according to the init list

    #Pick the scenario based on input
    if scenario == 1:   #Braveheart
        file = 'braveheart_init.txt'
    elif scenario == 2: #Bruce
        file = 'bruce_init.txt'
    #Take init information from file into a 2d list, same method as initialize_blocks()
    block_init_info = initialize_blocks.read_file(file)

    #Convert number data into int objects
    for row, line in enumerate(block_init_info):
        for col, data in enumerate(line):
            if data.isdigit():
                block_init_info[row][col] = int(data)

    #print(block_init_info)

    for blockID, line in enumerate(block_init_info):
        print(line)

        block_list[blockID] = 1  #Alliegance: SCOTLAND or ENGLAND
    print(block_init_info)

    territory_lst = blocks_occupied()
    for block in nobles:
        territory_lst[block.location].append(block)
    for block in other_blocks:
        territory_lst[block.location].append(block)

    return territory_lst

def main():
    make_occupied(1, [])

#x = initialize_blocks.read_file('braveheart_init.txt')
#print(x)

if __name__ == '__main__':
    main()
