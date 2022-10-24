from cmath import exp
from macpep_scylladb.utils.parser import get_id


protein_txt = """ID   AUTS2_MOUSE             Reviewed;        1261 AA.
AC   A0A087WPF7; E9PWJ4; Q6ZQB3; Q8BWI6;
DT   25-OCT-2017, integrated into UniProtKB/Swiss-Prot.
DT   25-OCT-2017, sequence version 2.
DT   12-OCT-2022, entry version 48.
DE   RecName: Full=Autism susceptibility gene 2 protein homolog;
GN   Name=Auts2; Synonyms=Kiaa0442 {ECO:0000312|EMBL:BAC97954.1};
OS   Mus musculus (Mouse).
OC   Eukaryota; Metazoa; Chordata; Craniata; Vertebrata; Euteleostomi; Mammalia;
OC   Eutheria; Euarchontoglires; Glires; Rodentia; Myomorpha; Muroidea; Muridae;
OC   Murinae; Mus; Mus.
OX   NCBI_TaxID=10090 {ECO:0000312|Proteomes:UP000000589};
RN   [1]
RP   NUCLEOTIDE SEQUENCE [LARGE SCALE MRNA] (ISOFORM 2).
RX   PubMed=16141072; DOI=10.1126/science.1112014;
RA   Carninci P., Kasukawa T., Katayama S., Gough J., Frith M.C., Maeda N.,
RA   Oyama R., Ravasi T., Lenhard B., Wells C., Kodzius R., Shimokawa K.,
RA   Bajic V.B., Brenner S.E., Batalov S., Forrest A.R., Zavolan M., Davis M.J.,
RA   Wilming L.G., Aidinis V., Allen J.E., Ambesi-Impiombato A., Apweiler R.,
RA   Aturaliya R.N., Bailey T.L., Bansal M., Baxter L., Beisel K.W., Bersano T.,
RA   Bono H., Chalk A.M., Chiu K.P., Choudhary V., Christoffels A.,
RA   Clutterbuck D.R., Crowe M.L., Dalla E., Dalrymple B.P., de Bono B.,
RA   Della Gatta G., di Bernardo D., Down T., Engstrom P., Fagiolini M.,
RA   Faulkner G., Fletcher C.F., Fukushima T., Furuno M., Futaki S.,
RA   Gariboldi M., Georgii-Hemming P., Gingeras T.R., Gojobori T., Green R.E.,
RA   Gustincich S., Harbers M., Hayashi Y., Hensch T.K., Hirokawa N., Hill D.,
RA   Huminiecki L., Iacono M., Ikeo K., Iwama A., Ishikawa T., Jakt M.,
RA   Kanapin A., Katoh M., Kawasawa Y., Kelso J., Kitamura H., Kitano H.,
RA   Kollias G., Krishnan S.P., Kruger A., Kummerfeld S.K., Kurochkin I.V.,
RA   Lareau L.F., Lazarevic D., Lipovich L., Liu J., Liuni S., McWilliam S.,
RA   Madan Babu M., Madera M., Marchionni L., Matsuda H., Matsuzawa S., Miki H.,
RA   Mignone F., Miyake S., Morris K., Mottagui-Tabar S., Mulder N., Nakano N.,
RA   Nakauchi H., Ng P., Nilsson R., Nishiguchi S., Nishikawa S., Nori F.,
RA   Ohara O., Okazaki Y., Orlando V., Pang K.C., Pavan W.J., Pavesi G.,
RA   Pesole G., Petrovsky N., Piazza S., Reed J., Reid J.F., Ring B.Z.,
RA   Ringwald M., Rost B., Ruan Y., Salzberg S.L., Sandelin A., Schneider C.,
RA   Schoenbach C., Sekiguchi K., Semple C.A., Seno S., Sessa L., Sheng Y.,
RA   Shibata Y., Shimada H., Shimada K., Silva D., Sinclair B., Sperling S.,
RA   Stupka E., Sugiura K., Sultana R., Takenaka Y., Taki K., Tammoja K.,
RA   Tan S.L., Tang S., Taylor M.S., Tegner J., Teichmann S.A., Ueda H.R.,
RA   van Nimwegen E., Verardo R., Wei C.L., Yagi K., Yamanishi H.,
RA   Zabarovsky E., Zhu S., Zimmer A., Hide W., Bult C., Grimmond S.M.,
RA   Teasdale R.D., Liu E.T., Brusic V., Quackenbush J., Wahlestedt C.,
RA   Mattick J.S., Hume D.A., Kai C., Sasaki D., Tomaru Y., Fukuda S.,
RA   Kanamori-Katayama M., Suzuki M., Aoki J., Arakawa T., Iida J., Imamura K.,
RA   Itoh M., Kato T., Kawaji H., Kawagashira N., Kawashima T., Kojima M.,
RA   Kondo S., Konno H., Nakano K., Ninomiya N., Nishio T., Okada M., Plessy C.,
RA   Shibata K., Shiraki T., Suzuki S., Tagami M., Waki K., Watahiki A.,
RA   Okamura-Oho Y., Suzuki H., Kawai J., Hayashizaki Y.;
RT   "The transcriptional landscape of the mammalian genome.";
RL   Science 309:1559-1563(2005).
RN   [2]
RP   NUCLEOTIDE SEQUENCE [LARGE SCALE GENOMIC DNA].
RC   STRAIN=C57BL/6J;
RX   PubMed=19468303; DOI=10.1371/journal.pbio.1000112;
RA   Church D.M., Goodstadt L., Hillier L.W., Zody M.C., Goldstein S., She X.,
RA   Bult C.J., Agarwala R., Cherry J.L., DiCuccio M., Hlavina W., Kapustin Y.,
RA   Meric P., Maglott D., Birtle Z., Marques A.C., Graves T., Zhou S.,
RA   Teague B., Potamousis K., Churas C., Place M., Herschleb J., Runnheim R.,
RA   Forrest D., Amos-Landgraf J., Schwartz D.C., Cheng Z., Lindblad-Toh K.,
RA   Eichler E.E., Ponting C.P.;
RT   "Lineage-specific biology revealed by a finished genome assembly of the
RT   mouse.";
RL   PLoS Biol. 7:E1000112-E1000112(2009).
RN   [3]
RP   NUCLEOTIDE SEQUENCE [LARGE SCALE MRNA] (ISOFORM 2).
RX   PubMed=15489334; DOI=10.1101/gr.2596504;
RG   The MGC Project Team;
RT   "The status, quality, and expansion of the NIH full-length cDNA project:
RT   the Mammalian Gene Collection (MGC).";
RL   Genome Res. 14:2121-2127(2004).
RN   [4] {ECO:0000312|EMBL:BAC97954.1}
RP   NUCLEOTIDE SEQUENCE [LARGE SCALE MRNA] OF 848-1261.
RC   TISSUE=Embryonic tail {ECO:0000312|EMBL:BAC97954.1};
RX   PubMed=14621295; DOI=10.1093/dnares/10.4.167;
RA   Okazaki N., Kikuno R., Ohara R., Inamoto S., Koseki H., Hiraoka S.,
RA   Saga Y., Nagase T., Ohara O., Koga H.;
RT   "Prediction of the coding sequences of mouse homologues of KIAA gene: III.
RT   The complete nucleotide sequences of 500 mouse KIAA-homologous cDNAs
RT   identified by screening of terminal sequences of cDNA clones randomly
RT   sampled from size-fractionated libraries.";
RL   DNA Res. 10:167-180(2003).
RN   [5]
RP   IDENTIFICATION BY MASS SPECTROMETRY [LARGE SCALE ANALYSIS].
RC   TISSUE=Kidney;
RX   PubMed=21183079; DOI=10.1016/j.cell.2010.12.001;
RA   Huttlin E.L., Jedrychowski M.P., Elias J.E., Goswami T., Rad R.,
RA   Beausoleil S.A., Villen J., Haas W., Sowa M.E., Gygi S.P.;
RT   "A tissue-specific atlas of mouse protein phosphorylation and expression.";
RL   Cell 143:1174-1189(2010).
RN   [6]
RP   SUBCELLULAR LOCATION, DEVELOPMENTAL STAGE, AND TISSUE SPECIFICITY.
RX   PubMed=19948250; DOI=10.1016/j.gep.2009.11.005;
RA   Bedogni F., Hodge R.D., Nelson B.R., Frederick E.A., Shiba N., Daza R.A.,
RA   Hevner R.F.;
RT   "Autism susceptibility candidate 2 (Auts2) encodes a nuclear protein
RT   expressed in developing brain regions implicated in autism
RT   neuropathology.";
RL   Gene Expr. Patterns 10:9-15(2010).
RN   [7]
RP   FUNCTION, INTERACTION WITH PREX1; DOCK1 AND ELMO2, SUBCELLULAR LOCATION,
RP   DOMAIN, ALTERNATIVE SPLICING, AND TISSUE SPECIFICITY.
RX   PubMed=25533347; DOI=10.1016/j.celrep.2014.11.045;
RA   Hori K., Nagai T., Shan W., Sakamoto A., Taya S., Hashimoto R., Hayashi T.,
RA   Abe M., Yamazaki M., Nakao K., Nishioka T., Sakimura K., Yamada K.,
RA   Kaibuchi K., Hoshino M.;
RT   "Cytoskeletal regulation by AUTS2 in neuronal migration and
RT   neuritogenesis.";
RL   Cell Rep. 9:2166-2179(2014).
RN   [8]
RP   DISRUPTION PHENOTYPE, SUBCELLULAR LOCATION, IDENTIFICATION IN A COMPLEX
RP   WITH PCGF5 AND RNF2, AND TISSUE SPECIFICITY.
RX   PubMed=25519132; DOI=10.1038/nature13921;
RA   Gao Z., Lee P., Stafford J.M., von Schimmelmann M., Schaefer A.,
RA   Reinberg D.;
RT   "An AUTS2-polycomb complex activates gene expression in the CNS.";
RL   Nature 516:349-354(2014).
CC   -!- FUNCTION: Component of a Polycomb group (PcG) multiprotein PRC1-like
CC       complex, a complex class required to maintain the transcriptionally
CC       repressive state of many genes, including Hox genes, throughout
CC       development. PcG PRC1 complex acts via chromatin remodeling and
CC       modification of histones; it mediates monoubiquitination of histone H2A
CC       'Lys-119', rendering chromatin heritably changed in its expressibility.
CC       The PRC1-like complex that contains PCGF5, RNF2, CSNK2B, RYBP and AUTS2
CC       has decreased histone H2A ubiquitination activity, due to the
CC       phosphorylation of RNF2 by CSNK2B. As a consequence, the complex
CC       mediates transcriptional activation (By similarity). In the cytoplasm,
CC       plays a role in axon and dendrite elongation and in neuronal migration
CC       during embryonic brain development. Promotes reorganization of the
CC       actin cytoskeleton, lamellipodia formation and neurite elongation via
CC       its interaction with RAC guanine nucleotide exchange factors, which
CC       then leads to the activation of RAC1 (PubMed:25533347).
CC       {ECO:0000250|UniProtKB:Q8WXX7, ECO:0000269|PubMed:25533347}.
CC   -!- SUBUNIT: Component of a PRC1-like complex that contains PCGF5, RNF2,
CC       CSNK2B, RYBP and AUTS2 (PubMed:25519132). Within this complex,
CC       interacts directly with PCGF5 and CSNK2B (By similarity). Interacts
CC       with the histone acetyltransferase EP300/p300 (By similarity).
CC       Interacts (via Pro-rich region) with PREX1, DOCK1 and ELMO2
CC       (PubMed:25533347). {ECO:0000250|UniProtKB:Q8WXX7,
CC       ECO:0000269|PubMed:25533347, ECO:0000305|PubMed:25519132}.
CC   -!- INTERACTION:
CC       A0A087WPF7; Q99K48: Nono; NbExp=4; IntAct=EBI-27122375, EBI-607499;
CC   -!- SUBCELLULAR LOCATION: Nucleus {ECO:0000269|PubMed:19948250,
CC       ECO:0000269|PubMed:25519132, ECO:0000269|PubMed:25533347}. Cytoplasm,
CC       cytoskeleton {ECO:0000269|PubMed:25533347}. Cell projection, growth
CC       cone {ECO:0000269|PubMed:25533347}. Note=Detected both in cytoplasm and
CC       nucleus (PubMed:25533347). Colocalizes with RAC1 at actin-rich growth
CC       cones (PubMed:25533347). Detected on the promoter region of actively
CC       transcribed genes (PubMed:25519132). {ECO:0000269|PubMed:25519132,
CC       ECO:0000269|PubMed:25533347}.
CC   -!- ALTERNATIVE PRODUCTS:
CC       Event=Alternative splicing; Named isoforms=3;
CC       Name=1;
CC         IsoId=A0A087WPF7-1; Sequence=Displayed;
CC       Name=2;
CC         IsoId=A0A087WPF7-2; Sequence=VSP_059125, VSP_059126;
CC       Name=3;
CC         IsoId=A0A087WPF7-3; Sequence=VSP_059124, VSP_059127;
CC   -!- TISSUE SPECIFICITY: Detected in brain cortex in embryo, neonates and
CC       adults (at protein level) (PubMed:19948250, PubMed:25533347,
CC       PubMed:25519132). Detected in embryonic and adult Purkinje cells in the
CC       cerebellum (PubMed:19948250). Detected in dorsal thalamus and in
CC       dopaminergic neurons in substantia nigra (PubMed:19948250).
CC       {ECO:0000269|PubMed:19948250, ECO:0000269|PubMed:25519132,
CC       ECO:0000269|PubMed:25533347}.
CC   -!- DEVELOPMENTAL STAGE: Detected in embryonic brain cortex at 15 dpc, and
CC       at clearly lower levels in adult brain cortex, hippocampus and in
CC       cerebellum Purkinje cells (at protein level) (PubMed:25519132). Very
CC       low and barely detectable in embryonic brain at 11 dpc. Detected in the
CC       developing brain cortex, thalamus and cerebellum at 12 and 14 dpc.
CC       Uniformly expressed all along the preplate at 13 dpc. At 16 dpc, highly
CC       expressed in neurons in deep and superficial layers of the frontal
CC       cortical region of the preplate, with much lower expression in the
CC       caudal region or the preplate. Highly expressed in thalamus at 14 dpc,
CC       and at much lower levels in adults. Highly expressed in hippocampus
CC       after 13 dpc; expression levels increase subsequently and are high in
CC       dentate gyrus and the CA region of the hippocampus at 19 dpc.
CC       Expression in dentate gyrus, granule cell layer and the CA region of
CC       the hippocampus continues in neonates and into adulthood.
CC       {ECO:0000269|PubMed:19948250}.
CC   -!- DOMAIN: The Pro-rich region is important for the interaction with RAC
CC       guanine nucleotide exchange factors and the subsequent activation of
CC       RAC1, which then promotes lamellipodia formation.
CC       {ECO:0000269|PubMed:25533347}.
CC   -!- DISRUPTION PHENOTYPE: Brain-specific gene disruption gives rise to no
CC       visible phenotype at birth. Mutant mice have normal weight at birth,
CC       but then show decreased weight gain over the next few days, decreased
CC       milk uptake, impaired motor skills and impaired ultrasonic vocalization
CC       after maternal separation. {ECO:0000269|PubMed:25519132}.
CC   -!- SIMILARITY: Belongs to the AUTS2 family. {ECO:0000305}.
CC   ---------------------------------------------------------------------------
CC   Copyrighted by the UniProt Consortium, see https://www.uniprot.org/terms
CC   Distributed under the Creative Commons Attribution (CC BY 4.0) License
CC   ---------------------------------------------------------------------------
DR   EMBL; AK052418; BAC34980.1; -; mRNA.
DR   EMBL; AC102355; -; NOT_ANNOTATED_CDS; Genomic_DNA.
DR   EMBL; AC103371; -; NOT_ANNOTATED_CDS; Genomic_DNA.
DR   EMBL; AC104195; -; NOT_ANNOTATED_CDS; Genomic_DNA.
DR   EMBL; AC113203; -; NOT_ANNOTATED_CDS; Genomic_DNA.
DR   EMBL; AC113510; -; NOT_ANNOTATED_CDS; Genomic_DNA.
DR   EMBL; AC117622; -; NOT_ANNOTATED_CDS; Genomic_DNA.
DR   EMBL; AC118932; -; NOT_ANNOTATED_CDS; Genomic_DNA.
DR   EMBL; AC121298; -; NOT_ANNOTATED_CDS; Genomic_DNA.
DR   EMBL; AC121500; -; NOT_ANNOTATED_CDS; Genomic_DNA.
DR   EMBL; AC157928; -; NOT_ANNOTATED_CDS; Genomic_DNA.
DR   EMBL; AC164607; -; NOT_ANNOTATED_CDS; Genomic_DNA.
DR   EMBL; BC151031; AAI51032.1; -; mRNA.
DR   EMBL; BC151047; AAI51048.1; -; mRNA.
DR   EMBL; AK129144; BAC97954.1; -; mRNA.
DR   RefSeq; NP_796021.2; NM_177047.3.
DR   AlphaFoldDB; A0A087WPF7; -.
DR   IntAct; A0A087WPF7; 19.
DR   MINT; A0A087WPF7; -.
DR   STRING; 10090.ENSMUSP00000139759; -.
DR   iPTMnet; A0A087WPF7; -.
DR   PhosphoSitePlus; A0A087WPF7; -.
DR   jPOST; A0A087WPF7; -.
DR   PaxDb; A0A087WPF7; -.
DR   ProteomicsDB; 277230; -. [A0A087WPF7-1]
DR   ProteomicsDB; 277231; -. [A0A087WPF7-2]
DR   ProteomicsDB; 277232; -. [A0A087WPF7-3]
DR   Antibodypedia; 623; 92 antibodies from 23 providers.
DR   Ensembl; ENSMUST00000161226; ENSMUSP00000159434; ENSMUSG00000029673. [A0A087WPF7-1]
DR   Ensembl; ENSMUST00000161374; ENSMUSP00000124730; ENSMUSG00000029673. [A0A087WPF7-3]
DR   UCSC; uc008zuv.1; mouse. [A0A087WPF7-1]
DR   UCSC; uc008zuw.1; mouse.
DR   MGI; MGI:1919847; Auts2.
DR   VEuPathDB; HostDB:ENSMUSG00000029673; -.
DR   eggNOG; ENOG502QSH4; Eukaryota.
DR   GeneTree; ENSGT00940000154823; -.
DR   PhylomeDB; A0A087WPF7; -.
DR   Reactome; R-MMU-8939243; RUNX1 interacts with co-factors whose precise effect on RUNX1 targets is not known.
DR   BioGRID-ORCS; 319974; 5 hits in 20 CRISPR screens.
DR   ChiTaRS; Auts2; mouse.
DR   PRO; PR:A0A087WPF7; -.
DR   Proteomes; UP000000589; Chromosome 5.
DR   RNAct; A0A087WPF7; protein.
DR   Bgee; ENSMUSG00000029673; Expressed in floor plate of midbrain and 272 other tissues.
DR   ExpressionAtlas; A0A087WPF7; baseline and differential.
DR   GO; GO:0005737; C:cytoplasm; IEA:UniProtKB-KW.
DR   GO; GO:0005856; C:cytoskeleton; IEA:UniProtKB-SubCell.
DR   GO; GO:0030426; C:growth cone; IDA:UniProtKB.
DR   GO; GO:0005634; C:nucleus; IDA:UniProtKB.
DR   GO; GO:0003682; F:chromatin binding; ISO:MGI.
DR   GO; GO:0031532; P:actin cytoskeleton reorganization; IMP:UniProtKB.
DR   GO; GO:0048675; P:axon extension; IMP:UniProtKB.
DR   GO; GO:0097484; P:dendrite extension; IMP:UniProtKB.
DR   GO; GO:0098582; P:innate vocalization behavior; IMP:MGI.
DR   GO; GO:0001764; P:neuron migration; IMP:UniProtKB.
DR   GO; GO:0051571; P:positive regulation of histone H3-K4 methylation; ISO:MGI.
DR   GO; GO:2000620; P:positive regulation of histone H4-K16 acetylation; ISO:MGI.
DR   GO; GO:0010592; P:positive regulation of lamellipodium assembly; IMP:UniProtKB.
DR   GO; GO:0035022; P:positive regulation of Rac protein signal transduction; IMP:UniProtKB.
DR   GO; GO:0045944; P:positive regulation of transcription by RNA polymerase II; ISO:MGI.
DR   GO; GO:0060013; P:righting reflex; IMP:MGI.
DR   InterPro; IPR023246; AUTS2.
DR   PANTHER; PTHR14429; PTHR14429; 1.
DR   Pfam; PF15336; Auts2; 1.
DR   PRINTS; PR02044; FIBROSIN1LPF.
PE   1: Evidence at protein level;
KW   Alternative splicing; Cell projection; Cytoplasm; Cytoskeleton; Nucleus;
KW   Phosphoprotein; Reference proteome; Transcription;
KW   Transcription regulation.
FT   CHAIN           1..1261
FT                   /note="Autism susceptibility gene 2 protein homolog"
FT                   /id="PRO_0000441889"
FT   REGION          1..88
FT                   /note="Disordered"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   REGION          105..236
FT                   /note="Disordered"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   REGION          251..486
FT                   /note="Disordered"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   REGION          288..471
FT                   /note="Important for regulation of lamellipodia formation"
FT                   /evidence="ECO:0000269|PubMed:25533347"
FT   REGION          505..545
FT                   /note="Disordered"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   REGION          771..1023
FT                   /note="Disordered"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   REGION          1121..1148
FT                   /note="Disordered"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   REGION          1201..1261
FT                   /note="Disordered"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   COMPBIAS        45..61
FT                   /note="Polar residues"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   COMPBIAS        105..132
FT                   /note="Basic and acidic residues"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   COMPBIAS        144..162
FT                   /note="Basic and acidic residues"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   COMPBIAS        178..221
FT                   /note="Polar residues"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   COMPBIAS        275..292
FT                   /note="Basic and acidic residues"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   COMPBIAS        323..362
FT                   /note="Pro residues"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   COMPBIAS        363..416
FT                   /note="Polar residues"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   COMPBIAS        429..451
FT                   /note="Polar residues"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   COMPBIAS        460..475
FT                   /note="Pro residues"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   COMPBIAS        771..791
FT                   /note="Polar residues"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   COMPBIAS        817..851
FT                   /note="Basic and acidic residues"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   COMPBIAS        879..932
FT                   /note="Basic and acidic residues"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   COMPBIAS        959..997
FT                   /note="Basic and acidic residues"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   COMPBIAS        1003..1017
FT                   /note="Polar residues"
FT                   /evidence="ECO:0000256|SAM:MobiDB-lite"
FT   MOD_RES         1200
FT                   /note="Phosphoserine"
FT                   /evidence="ECO:0000250|UniProtKB:Q8WXX7"
FT   MOD_RES         1235
FT                   /note="Phosphoserine"
FT                   /evidence="ECO:0000250|UniProtKB:Q8WXX7"
FT   VAR_SEQ         1..457
FT                   /note="Missing (in isoform 3)"
FT                   /id="VSP_059124"
FT   VAR_SEQ         231..258
FT                   /note="ASDASSEKLFNTVLVNKDPELGVGALPE -> VRRHPLHCKHNPQGSGCTVT
FT                   CLLVPVPL (in isoform 2)"
FT                   /id="VSP_059125"
FT   VAR_SEQ         259..1261
FT                   /note="Missing (in isoform 2)"
FT                   /id="VSP_059126"
FT   VAR_SEQ         563..577
FT                   /note="Missing (in isoform 3)"
FT                   /id="VSP_059127"
SQ   SEQUENCE   1261 AA;  138920 MW;  0E5C161A1211D6FF CRC64;
     MDGPTRGHGL RKKRRSRSQR DRERRSRAGL GTGAAGGIGA GRTRAPSLAS SSGSDKEDNG
     KPPSSAPSRP RPPRRKRRES TSAEEDIIDG FAMTSFVTFE ALEKDVAVKP QERAEKRQTP
     LTKKKREALT NGLSFHSKKS RLSHSHHYSS DRENDRNLCQ HLGKRKKMPK GLRQLKPGQN
     SCRDSDSESA SGESKGFQRS SSRERLSDSS APSSLGTGYF CDSDSDQEEK ASDASSEKLF
     NTVLVNKDPE LGVGALPEHN QDAGPIVPKI SGLERSQEKS QDCCKEPVFE PVVLKDPHPQ
     LPQLPSQAQA EPQLQIPSPG PDLVPRTEAP PQFPPPSTQP AQGPPEAQLQ PAPLPQVQQR
     PPRPQSPSHL LQQTLPPVQS HPSSQSLSQP LSAYNSSSLS LNSLSSRSST PAKTQPAPPH
     ISHHPSASPF PLSLPNHSPL HSFTPTLQPP AHSHHPNMFA PPTALPPPPP LTSGSLQVPG
     HPAGSTYSEQ DILRQELNTR FLASQSADRG ASLGPPPYLR TEFHQHQHQH QHTHQHTHQH
     TFTPFPHAIP PTAIMPTPAP PMFDKYPTKV DPFYRHSLFH SYPPAVSGIP PMIPPTGPFG
     SLQGAFQPKT SNPIDVAARP GTVPHTLLQK DPRLTDPFRP MLRKPGKWCA MHVHIAWQIY
     HHQQKVKKQM QSDPHKLDFG LKPEFLSRPP GPSLFGAIHH PHDLARPSTL FSAAGAAHPT
     GTPFGPPPHH SNFLNPAAHL EPFNRPSTFT GLAAVGGNAF GGLGNPSVTP NSVFGHKDSP
     SVQNFSNPHE PWNRLHRTPP SFPTPPPWLK PGELERSASA AAHDRDRDVD KRDSSVSKDD
     KERESVEKRH PSHPSPAPPV PVSALGHNRS STDPTTRGHL NTEAREKDKP KEKERDHSGS
     RKDLTTEEHK AKESHLPERD GHSHEGRAAG EEPKQLSRVP SPYVRTPGVD STRPNSTSSR
     EAEPRKGEPA YENPKKNAEV KVKEERKEDH DLPTEAPQAH RTSEAPPPSS SASASVHPGP
     LASMPMTVGV TGIHAMNSIG SLDRTRMVTP FMGLSPIPGG ERFPYPSFHW DPMRDPLRDP
     YRDLDMHRRD PLGRDFLLRN DPLHRLSTPR LYEADRSFRD REPHDYSHHH HHHHHPLAVD
     PRREHERGGH LDERERLHVL REDYEHPRLH PVHPASLDGH LPHPSLLTPG LPSMHYPRIS
     PTAGHQNGLL NKTPPTAALS APPPLISTLG GRPGSPRRTT PLSAEIRERP PSHTLKDIEA
     R"""


def test_get_id_should_find_id():
    # Arrange
    expected = "AUTS2_MOUSE"
    # Act / Assert
    assert get_id(protein_txt) == expected
    