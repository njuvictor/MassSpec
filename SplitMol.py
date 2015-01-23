'''
    Split molecules into pieces
'''

from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Descriptors import MolWt

def BreakBond():
    pass

def ReturnTwoMol(mol):
    Draw.MolToFile(mol, "tmp.png")
    for bond in mol.GetBonds():
        emol = Chem.EditableMol(mol)
        #print bond.GetBondType()
        #print bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()
        emol.RemoveBond(bond.GetBeginAtomIdx(), bond.GetEndAtomIdx())
        m2 = emol.GetMol()
        Draw.MolToFile(m2, "tmp.png")
        smile = Chem.MolToSmiles(m2)
        if "." in smile:
            smiles = smile.split(".")
            yield Chem.MolFromSmiles(smiles[0]), Chem.MolFromSmiles(smiles[1])

def BreakForOneSMILE(smile):
    mol = Chem.MolFromSmiles(smile)
    for mol1, mol2 in ReturnTwoMol(mol):
        print MolWt(mol1), MolWt(mol2)


if __name__ == "__main__":
    smile = "C(CCC(=O)O)CCN"
    BreakForOneSMILE(smile)
