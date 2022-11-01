from cmath import exp
from macpep_scylladb.utils.parser import get_accessions, get_id, get_review_status, get_sequence


protein_txt = """ID   IQIP1_MOUSE             Reviewed;         559 AA.
AC   A0A088MLT8; A8IJC6; A8IJD0; A8IJD3; F6YL02; F8WI70; Q3TI53; Q52KH1; Q6P9Y8;
AC   Q9CX07; Q9JLR0;
DT   22-NOV-2017, integrated into UniProtKB/Swiss-Prot.
DT   22-NOV-2017, sequence version 2.
DT   03-AUG-2022, entry version 35.
DE   RecName: Full=IQCJ-SCHIP1 readthrough transcript protein {ECO:0000305};
GN   Name=Iqcj-Schip1 {ECO:0000250|UniProtKB:B3KU38};
GN   Synonyms=Iqschfp {ECO:0000312|MGI:MGI:5439400}, Schip1
GN   {ECO:0000312|EMBL:AIN40496.1};
OS   Mus musculus (Mouse).
OC   Eukaryota; Metazoa; Chordata; Craniata; Vertebrata; Euteleostomi; Mammalia;
OC   Eutheria; Euarchontoglires; Glires; Rodentia; Myomorpha; Muroidea; Muridae;
OC   Murinae; Mus; Mus.
OX   NCBI_TaxID=10090 {ECO:0000312|EMBL:AIN40496.1};
RN   [1]
RP   NUCLEOTIDE SEQUENCE [MRNA] (ISOFORM IQCJ-SCHIP1-1), ALTERNATIVE SPLICING,
RP   SUBCELLULAR LOCATION, INTERACTION WITH ANK3 AND CALMODULIN, MUTAGENESIS OF
RP   53-ILE-GLN-54, AND REGION.
RC   STRAIN=FVB/NJ;
RX   PubMed=18550753; DOI=10.1523/jneurosci.1044-08.2008;
RA   Martin P.M., Carnaud M., Garcia del Cano G., Irondelle M., Irinopoulou T.,
RA   Girault J.A., Dargent B., Goutebroze L.;
RT   "Schwannomin-interacting protein-1 isoform IQCJ-SCHIP-1 is a late component
RT   of nodes of Ranvier and axon initial segments.";
RL   J. Neurosci. 28:6111-6117(2008).
RN   [2]
RP   NUCLEOTIDE SEQUENCE [MRNA] (ISOFORM IQCJ-SCHIP1-2), FUNCTION, AND
RP   DISRUPTION PHENOTYPE.
RX   PubMed=25953347; DOI=10.1242/dev.119248;
RA   Klingler E., Martin P.M., Garcia M., Moreau-Fauvarque C., Falk J.,
RA   Chareyre F., Giovannini M., Chedotal A., Girault J.A., Goutebroze L.;
RT   "The cytoskeleton-associated protein SCHIP1 is involved in axon guidance,
RT   and is required for piriform cortex and anterior commissure development.";
RL   Development 142:2026-2036(2015).
RN   [3]
RP   FUNCTION.
RX   PubMed=25950943; DOI=10.1111/jnc.13158;
RA   Papandreou M.J., Vacher H., Fache M.P., Klingler E., Rueda-Boroni F.,
RA   Ferracci G., Debarnot C., Piperoglou C., Garcia Del Cano G., Goutebroze L.,
RA   Dargent B.;
RT   "CK2-regulated schwannomin-interacting protein IQCJ-SCHIP-1 association
RT   with AnkG contributes to the maintenance of the axon initial segment.";
RL   J. Neurochem. 134:527-537(2015).
RN   [4]
RP   FUNCTION, INTERACTION WITH KCNQ2; KCNQ3 AND SPTBN4, SUBUNIT, AND DISRUPTION
RP   PHENOTYPE.
RX   PubMed=27979964; DOI=10.1074/jbc.m116.758029;
RA   Martin P.M., Cifuentes-Diaz C., Devaux J., Garcia M., Bureau J.,
RA   Thomasseau S., Klingler E., Girault J.A., Goutebroze L.;
RT   "Schwannomin-interacting protein 1 isoform IQCJ-SCHIP1 is a multipartner
RT   ankyrin- and spectrin-binding protein involved in the organization of nodes
RT   of Ranvier.";
RL   J. Biol. Chem. 292:2441-2456(2017).
CC   -!- FUNCTION: May play a role in action potential conduction in myelinated
CC       cells through the organization of molecular complexes at nodes of
CC       Ranvier and axon initial segments (PubMed:25953347, PubMed:25950943,
CC       PubMed:27979964). May also play a role in axon outgrowth and guidance
CC       (PubMed:25953347). {ECO:0000269|PubMed:25950943,
CC       ECO:0000269|PubMed:25953347, ECO:0000269|PubMed:27979964}.
CC   -!- SUBUNIT: Homooligomer (via coiled coil domain) (PubMed:27979964).
CC       Interacts (via IQ domain) with calmodulin; the interaction is direct
CC       and lost in presence of calcium (PubMed:18550753). Interacts with ANK3
CC       (via ANK repeats); required for its localization at axon initial
CC       segments (AIS) and nodes of Ranvier (PubMed:18550753). Interacts with
CC       SPTBN4 (PubMed:27979964). Interacts with KCNQ2 and KCNQ3
CC       (PubMed:27979964). {ECO:0000269|PubMed:18550753,
CC       ECO:0000269|PubMed:27979964}.
CC   -!- SUBCELLULAR LOCATION: Cell projection, axon
CC       {ECO:0000269|PubMed:18550753}. Cytoplasm
CC       {ECO:0000250|UniProtKB:B3KU38}. Note=Localizes to the axon initial
CC       segments (AIS) and nodes of Ranvier of neurons and is absent from
CC       dendrites. {ECO:0000269|PubMed:18550753}.
CC   -!- ALTERNATIVE PRODUCTS:
CC       Event=Alternative splicing; Named isoforms=7;
CC       Name=Iqcj-schip1-1; Synonyms=IQCJ-SCHIP-1
CC       {ECO:0000303|PubMed:18550753};
CC         IsoId=A0A088MLT8-1; Sequence=Displayed;
CC       Name=Iqcj-schip1-2;
CC         IsoId=A0A088MLT8-2; Sequence=VSP_059226;
CC       Name=Iqcj-1;
CC         IsoId=Q8BPW0-1; Sequence=External;
CC       Name=Schip1-1; Synonyms=Schip-1a;
CC         IsoId=P0DPB4-1, Q3TI53-5; Sequence=External;
CC       Name=Schip1-2;
CC         IsoId=P0DPB4-2, Q3TI53-1; Sequence=External;
CC       Name=Schip1-3;
CC         IsoId=P0DPB4-3, Q3TI53-3; Sequence=External;
CC       Name=Schip1-4; Synonyms=Schip-1b;
CC         IsoId=P0DPB4-4, Q3TI53-6; Sequence=External;
CC   -!- DISRUPTION PHENOTYPE: Mice lacking all isoforms encoded by both Schip1
CC       and Iqcj-Schip1 are fertile and survive as long as wild-type mice.
CC       However, they exhibit mild growth delay associated with ataxia and
CC       reduced pain sensitivity. They display decreased thickness of the
CC       piriform cortex and partial agenesis of the anterior comissure which
CC       could be due to impaired axon elongation and guidance. The morphology
CC       of nodes of Ranvier is affected but nerves do not exhibit significant
CC       electrophysiological characteristic differences. A reduction in the
CC       number of axonal projections in the peripheral nerve system is also
CC       observed. {ECO:0000269|PubMed:25953347, ECO:0000269|PubMed:27979964}.
CC   -!- MISCELLANEOUS: [Isoform Iqcj-schip1-1]: Based on a naturally occurring
CC       readthrough transcript which produces an IQCJ-SCHIP1 fusion protein.
CC       {ECO:0000269|PubMed:18550753}.
CC   -!- MISCELLANEOUS: [Isoform Iqcj-schip1-2]: Based on a naturally occurring
CC       readthrough transcript which produces an IQCJ-SCHIP1 fusion protein.
CC       {ECO:0000269|PubMed:25950943}.
CC   ---------------------------------------------------------------------------
CC   Copyrighted by the UniProt Consortium, see https://www.uniprot.org/terms
CC   Distributed under the Creative Commons Attribution (CC BY 4.0) License
CC   ---------------------------------------------------------------------------
DR   EMBL; EU163409; ABW06762.1; -; mRNA.
DR   EMBL; KJ941154; AIN40496.1; -; mRNA.
DR   CCDS; CCDS79923.1; -. [A0A088MLT8-1]
DR   RefSeq; NP_001106890.1; NM_001113419.2. [A0A088MLT8-1]
DR   AlphaFoldDB; A0A088MLT8; -.
DR   SMR; A0A088MLT8; -.
DR   Ensembl; ENSMUST00000182006; ENSMUSP00000138212; ENSMUSG00000102422. [A0A088MLT8-1]
DR   GeneID; 100505386; -.
DR   KEGG; mmu:100505386; -.
DR   UCSC; uc056zsu.1; mouse. [A0A088MLT8-1]
DR   CTD; 100505386; -.
DR   MGI; MGI:5439400; Iqschfp.
DR   VEuPathDB; HostDB:ENSMUSG00000102422; -.
DR   GeneTree; ENSGT00390000011127; -.
DR   OMA; CGTCVPE; -.
DR   OrthoDB; 1290403at2759; -.
DR   ChiTaRS; Gm21949; mouse.
DR   PRO; PR:A0A088MLT8; -.
DR   Proteomes; UP000000589; Chromosome 3.
DR   RNAct; A0A088MLT8; protein.
DR   Bgee; ENSMUSG00000102422; Expressed in dentate gyrus of hippocampal formation granule cell and 22 other tissues.
DR   GO; GO:0043194; C:axon initial segment; IDA:UniProtKB.
DR   GO; GO:0030054; C:cell junction; IBA:GO_Central.
DR   GO; GO:0005737; C:cytoplasm; IEA:UniProtKB-SubCell.
DR   GO; GO:0033268; C:node of Ranvier; IDA:UniProtKB.
DR   GO; GO:0005886; C:plasma membrane; IBA:GO_Central.
DR   GO; GO:0030506; F:ankyrin binding; IDA:UniProtKB.
DR   GO; GO:0005516; F:calmodulin binding; IDA:UniProtKB.
DR   GO; GO:0044325; F:transmembrane transporter binding; IPI:UniProtKB.
DR   GO; GO:0008366; P:axon ensheathment; IMP:UniProtKB.
DR   GO; GO:0051494; P:negative regulation of cytoskeleton organization; ISS:UniProtKB.
DR   GO; GO:0035332; P:positive regulation of hippo signaling; IBA:GO_Central.
DR   InterPro; IPR029362; IQCJ-SCHIP1_N.
DR   InterPro; IPR039045; SCHIP_1.
DR   InterPro; IPR015649; SCHIP_1_C.
DR   PANTHER; PTHR13103; PTHR13103; 1.
DR   Pfam; PF15157; IQCJ-SCHIP1; 1.
DR   Pfam; PF10148; SCHIP-1; 1.
PE   1: Evidence at protein level;
KW   Alternative splicing; Cell projection; Coiled coil; Cytoplasm;
KW   Reference proteome.
FT   CHAIN           1..559
FT                   /note="IQCJ-SCHIP1 readthrough transcript protein"
FT                   /id="PRO_0000442333"
FT   DOMAIN          47..67
FT                   /note="IQ"
FT   REGION          64..141
FT                   /note="Disordered"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   REGION          161..295
FT                   /note="Disordered"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   REGION          312..332
FT                   /note="Disordered"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   REGION          380..426
FT                   /note="Disordered"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   REGION          415..559
FT                   /note="Required for interaction with ankyrins"
FT                   /evidence="ECO:0000269|PubMed:18550753"
FT   COILED          496..530
FT                   /evidence="ECO:0000255"
FT   COMPBIAS        69..97
FT                   /note="Polar residues"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   COMPBIAS        108..141
FT                   /note="Polar residues"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   COMPBIAS        169..183
FT                   /note="Acidic residues"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   COMPBIAS        201..220
FT                   /note="Polar residues"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   COMPBIAS        312..329
FT                   /note="Polar residues"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   COMPBIAS        395..411
FT                   /note="Polar residues"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   VAR_SEQ         98..325
FT                   /note="Missing (in isoform Iqcj-schip1-2)"
FT                   /id="VSP_059226"
FT   MUTAGEN         53..54
FT                   /note="IQ->AA: Loss of interaction with calmodulin."
FT                   /evidence="ECO:0000269|PubMed:18550753"
SQ   SEQUENCE   559 AA;  61917 MW;  72C5FB63AD80036D CRC64;
     MRLEELKRLQ NPLEQVDDGK YLLENHQLAM DVENNIENYP LSLQPLESKV KIIQRAWREY
     LQRQDPLEKR SPSPPSVSSD KLSSSVSMNT FSDSSTPDYR EDGMDLGSDA GSSSSSRASS
     QSNSTKVTPC SECKSSSSPG GSLDLVSALE DYEEPFPVYQ KKVIDEWAPE EDGEEEEEED
     DRGYRDDGCP AREPGDVSAR IGSSGSGSRS AATTMPSPMP NGNLHPHDPQ DLRHNGNVVV
     AGRPNASRVP RRPIQKTQPP GSRRGGRNRA SGGLCLQPPD GGTRVPEEPP APPMDWEALE
     KHLAGLQFRE QEVRNQGQAR TNSTSAQKNE RESIRQKLAL GSFFDDGPGI YTSCSKSGKP
     SLSARLQSGM NLQICFVNDS GSDKDSDADD SKTETSLDTP LSPMSKQSSS YSDRDTTEEE
     SESLDDMDFL TRQKKLQAEA KMALAMAKPM AKMQVEVEKQ NRKKSPVADL LPHMPHISEC
     LMKRSLKPTD LRDMTIGQLQ VIVNDLHSQI ESLNEELVQL LLIRDELHTE QDAMLVDIED
     LTRHAESQQK HMAEKMPAK"""

def test_get_id_should_find_id():
    # Arrange
    expected = "IQIP1_MOUSE"
    # Act / Assert
    assert get_id(protein_txt) == expected

def test_get_accessions_should_find_accessions():
    # Arrange
    expected = ["A0A088MLT8", "A8IJC6", "A8IJD0", "A8IJD3", "F6YL02", "F8WI70", "Q3TI53", "Q52KH1", "Q6P9Y8", "Q9CX07", "Q9JLR0"]
    # Act / Assert
    assert get_accessions(protein_txt) == expected

def test_get_sequence_should_find_sequence():
    # Arrange
    expected = "MRLEELKRLQNPLEQVDDGKYLLENHQLAMDVENNIENYPLSLQPLESKVKIIQRAWREYLQRQDPLEKRSPSPPSVSSDKLSSSVSMNTFSDSSTPDYREDGMDLGSDAGSSSSSRASSQSNSTKVTPCSECKSSSSPGGSLDLVSALEDYEEPFPVYQKKVIDEWAPEEDGEEEEEEDDRGYRDDGCPAREPGDVSARIGSSGSGSRSAATTMPSPMPNGNLHPHDPQDLRHNGNVVVAGRPNASRVPRRPIQKTQPPGSRRGGRNRASGGLCLQPPDGGTRVPEEPPAPPMDWEALEKHLAGLQFREQEVRNQGQARTNSTSAQKNERESIRQKLALGSFFDDGPGIYTSCSKSGKPSLSARLQSGMNLQICFVNDSGSDKDSDADDSKTETSLDTPLSPMSKQSSSYSDRDTTEEESESLDDMDFLTRQKKLQAEAKMALAMAKPMAKMQVEVEKQNRKKSPVADLLPHMPHISECLMKRSLKPTDLRDMTIGQLQVIVNDLHSQIESLNEELVQLLLIRDELHTEQDAMLVDIEDLTRHAESQQKHMAEKMPAK"
    # Act / Assert
    assert get_sequence(protein_txt) == expected

def test_get_review_status_should_be_true():
    assert get_review_status(protein_txt) == True