import initialize_blocks
def blocks_occupied():
    """
    makes list of where all blocks are
    """
    territory_lst = list()
    for i in range(25):
        territory_lst.append(list())
        
      
    return territory_lst
def make_occupied():
    """
    initialize where all blocks are
    """
    nobles, other_blocks = initialize_blocks.initialize_blocks()
    territory_lst = blocks_occupied()
    for block in nobles:
        territory_lst[block.location].append(block)
    for block in other_blocks:
        territory_lst[block.location].append(block)
    print(territory_lst)
    return territory_lst
make_occupied()
    
