from macpep_scylladb.proteomics.AminoAcid import REPLACEABLE_AMBIGIOUS_AMINO_ACID_LOOKUP


def is_sequence_containing_replaceable_ambigous_amino_acids(sequence: str) -> bool:
    """
    Determines if a sequence contains ambigous amino acids.

    Parameters
    ----------
    sequence : str
        Amino acid sequence.

    Returns

    -------
    True if the sequence contains ambigous amino acids, otherwise False
    """
    for one_letter_code in REPLACEABLE_AMBIGIOUS_AMINO_ACID_LOOKUP.keys():
        if one_letter_code in sequence:
            return True
    return False


def differentiate_ambigous_sequences(
    ambigous_sequence: str,
) -> set:
    """
    Calculates all possible combinations of an ambigous sequence.

    Parameters
    ----------
    ambigous_sequence : str
        Amino acid sequence with ambigous amino acids.

    Returns
    Set of sequences
    """
    differentiated_sequences: set = set()
    __differentiate_ambigous_sequences(ambigous_sequence, differentiated_sequences)
    return differentiated_sequences


def __differentiate_ambigous_sequences(
    sequence: str, differentiated_sequences: set, position: int = 0
):
    """
    Recursivly calculates all possible differentiate combinations of ambigous sequence.

    Parameters
    ----------
    sequence : str
        Current sequence
    differentiated_sequences : Set[str]
        A set() where the differentiated sequences where stored.
    position : int
        current position in the sequence
    """
    if position == len(sequence):
        differentiated_sequences.add(sequence)
        return
    if not sequence[position] in REPLACEABLE_AMBIGIOUS_AMINO_ACID_LOOKUP:
        __differentiate_ambigous_sequences(
            sequence, differentiated_sequences, position + 1
        )
    else:
        for replacement_amino_acid in REPLACEABLE_AMBIGIOUS_AMINO_ACID_LOOKUP[
            sequence[position]
        ]:
            new_sequence = (
                sequence[:position]
                + replacement_amino_acid.one_letter_code
                + sequence[position + 1 :]
            )
            __differentiate_ambigous_sequences(
                new_sequence, differentiated_sequences, position + 1
            )
