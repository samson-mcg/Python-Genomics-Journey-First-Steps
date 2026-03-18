
import random

codon_to_aa = {
    "UUU": "Phenylalanine", "UUC": "Phenylalanine", "UCU": "Serine", 
    "UCC": "Serine", "UCA": "Serine", "UCG": "Serine", "AGU": "Serine", 
    "AGC": "Serine", "UAU": "Tyrosine", "UAC": "Tyrosine", "UGU": "Cysteine", 
    "UGC": "Cysteine", "UGG": "Tryptophan", "UUA": "Leucine", "UUG": "Leucine", 
    "CUU": "Leucine", "CUC": "Leucine", "CUA": "Leucine", "CUG": "Leucine",
    "CCU": "Proline", "CCC": "Proline", "CCA": "Proline", "CCG": "Proline",
    "CAU": "Histidine", "CAC": "Histidine", "CAA": "Glutamine", "CAG": "Glutamine",
    "CGU": "Arginine", "CGC": "Arginine", "CGA": "Arginine", "CGG": "Arginine",
    "AGA": "Arginine", "AGG": "Arginine", "AUU": "Isoleucine", "AUC": "Isoleucine", 
    "AUA": "Isoleucine", "ACU": "Threonine", "ACC": "Threonine", "ACA": "Threonine", 
    "ACG": "Threonine", "AAU": "Asparagine", "AAC": "Asparagine", "AAA": "Lysine", 
    "AAG": "Lysine", "GUU": "Valine", "GUC": "Valine", "GUA": "Valine", 
    "GUG": "Valine", "GCU": "Alanine", "GCC": "Alanine", "GCA": "Alanine", 
    "GCG": "Alanine", "GAU": "Aspartic acid", "GAC": "Aspartic acid",
    "GAA": "Glutamic acid", "GAG": "Glutamic acid", "GGU": "Glycine", 
    "GGC": "Glycine", "GGA": "Glycine", "GGG": "Glycine", "AUG": "Methionine"
}   

stop_codons = ["UAA", "UAG", "UGA"]

aa_to_symbol = {
    "Phenylalanine": "F","Serine": "S", "Tyrosine": "Y", "Cysteine": "C", "Tryptophan": "W",
    "Leucine": "L", "Proline": "P", "Histidine": "H", "Glutamine": "Q", "Arginine": "R",
    "Isoleucine": "I", "Threonine": "T", "Asparagine": "N", "Lysine": "K", "Valine": "V",
    "Alanine": "A", "Aspartic acid": "D", "Glutamic acid" : "E", "Glycine" : "G","Methionine" : "M", 
}   

def random_rna_seq(length):
    """Generates a random RNA sequence of given length."""
    return ''.join(random.choice(['A', 'U', 'C', 'G']) for _ in range(length))

def rna_to_proteins(RNA): 
    """Translates RNA into protein sequences using the first reading frame"""
    protein_sequences = []      
    current_sequence = []
    is_translating = False      

    for i in range(0, len(RNA) -2, 3):
        codon = RNA[i:i+3]
        
        if codon == "AUG" and not is_translating:
            is_translating = True                    
            current_sequence = ["Methionine"]
        elif codon in stop_codons and is_translating:  
            current_sequence.append("Stop")
            protein_sequences.append(current_sequence)
            current_sequence = []
            is_translating = False            
        elif is_translating:
            amino_acid = codon_to_aa.get(codon)
            if amino_acid:
                current_sequence.append(amino_acid)
    
    # Output formatting
    for idx, seq in enumerate(protein_sequences, start=1):
        print(f"Seq{idx}: {seq}") # Full amino acid names
        letters = ''.join([aa_to_symbol[aa] for aa in seq if aa != 'Stop'])
        print(f"Seq{idx} (single-letter code) : {letters}\n")

def rna_search(RNA):
    """searches an rna sequence for the positions of codons that code for an amino acid """
    while True:
        query = input("\nEnter a Codon (AUG), AA Name (Methionine), or Symbol (M) to search for its positions, or write 'exit' to quit: ").strip()
        if query.lower() == 'exit':
             break
        
        target_codons = []
        if len(query) == 1:
            symbol = query.upper()
            full_name = next((name for name, s in aa_to_symbol.items() if s == symbol), None)
            if full_name:
                    target_codons = [c for c, name in codon_to_aa.items() if name == full_name]
        elif query.capitalize() in aa_to_symbol:
                full_name = query.capitalize()
                target_codons = [c for c, name in codon_to_aa.items() if name == full_name]
        elif len(query) == 3:
            target_codons = [query.upper()]
        if not target_codons:
            print(f"Could not identify '{query}'. Check your spelling! ")
            continue
            
        all_matches = []
        for i in range(len(RNA)-2):
            if RNA[i:i+3] in target_codons:
                all_matches.append(i)
        if all_matches:
            print(f"\n--- Results for {query} (Targeting: {', '.join(target_codons)}) ---")
            in_frame = [m for m in all_matches if m % 3 == 0]
            out_frame = [m for m in all_matches if m % 3 != 0]
            print(f"Total occurences: {len(all_matches)}")
            print(f"In-Frame (Frame 0): {in_frame if in_frame else 'None'}")
            print(f"Out-of-Frame: {out_frame if out_frame else 'None'}")
        else:
            print(f"No occurences of '{query}' found in the RNA sequence. Please try again.")

if __name__ == "__main__":
    print("=== RNA Sequence Analysis Tools ===")
    try:
        user_input = input("Enter the length of the random RNA sequence to generate: ")
        length = int(user_input)
        RNA = random_rna_seq(length)
        print(f"\nGenerated RNA: {RNA}\n")

        print("TRANSLATION RESULTS:")
        rna_to_proteins(RNA)
        print("\nSEARCH UTILITY:")
        rna_search(RNA)
    except ValueError:
        print("Invalid input! Please enter a whole number for the sequence length.")
  
