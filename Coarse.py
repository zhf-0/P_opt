import pyamg
import numpy as np

def Coarsening(A):
    '''
    Input: matrix A in csr format 
    Output: the index of all coarse points 
    '''
    
    # There are many C/F splitting methods including RS, PMIS, PMISc, CLJP, CLJPc, and CR
    # The default splitting method is RS
    # Ref url: https://pyamg.readthedocs.io/en/latest/generated/pyamg.classical.html#pyamg.classical.ruge_stuben_solver
    ml = pyamg.ruge_stuben_solver(A, max_levels=2, max_coarse=1, CF='RS',keep=True)
    print(ml)

    # The CF splitting, 1 == C-node and 0 == F-node
    splitting = ml.levels[0].splitting
    C_nodes = splitting == 1
    F_nodes = splitting == 0

    node_idx = np.arange(A.shape[0])
    coarse_idx = node_idx[C_nodes]

    # you can also check the P matrix
    p = ml.levels[0].P
    print('P matrix')
    print(p)
    
    return coarse_idx

if __name__ == '__main__':
    A = pyamg.gallery.poisson((10,10), format='csr')  # 2D Poisson problem on 10x10 grid
    coarse_idx = Coarsening(A)
    print('coarse index =',coarse_idx)


