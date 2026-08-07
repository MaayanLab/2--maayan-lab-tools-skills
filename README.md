# Ma'ayan Lab Bioinformatics Tools: Agent Skills

A collection Ma'ayan Lab's bioinformatics tools as skills for any AI agent that supports Agent Skills. These skills utilize several gene set libraries, databases, search engines, and have abilities across various analysis and mapping functions.

[AI agent skills](https://agentskills.io/home) are a format that provides AI agents with specialized capabilities and knowledge. By integrating bioinformatics tools as skills, you can simply submit queries and the AI agent will run relevant and specific analyses and searches, allowing for a smoother workflow that integrates multiple tools into one place. These skills are compatible with any AI agent that supports the open Agent Skills standard, including Claude Code, Codex, and more.

## Included Tools

As of now, this working list contains 14 skills, each one including:
- Documentation (``SKILL.md``)
- Example code and results
- Usage guides and descriptions

Tools are covered in the following categories:

### Enrichment Analysis

Ma'ayan Lab's enrichment analysis tools identify statistically significant overlaps between experimentally-generated gene sets and curated gene sets of anotations including pathways, ontologies, transcription factors, diseases, phenotypes, cells and tissues, and others. Interpreting various omics datasets, the below enrichment analysis tools assist researchers in forming hypotheses on the molecular mechanisms behind changes to key biological and pathophysiological processes. 

- **Enrichr:** Gene-list enrichment analysis tool that includes 225 gene-set libraies and an alternative approach to rank enriched terms. 
    - [Website](https://maayanlab.cloud/Enrichr/) and [publication](https://pubmed.ncbi.nlm.nih.gov/23586463/).
- **ChEA3:** ChIP-X Enrichment Analysis Version 3 (ChEA3) is a transcription factor (TF) enrichment analysis tool with a background database containing a collection of gene set libraries generated from multiple sources including TF-gene co-expression from RNA-seq studies, TF-target associations from ChIP-seq experiments, and TF-gene co-occurence computed from crowd-submitted gene lists. ChEA3 retrieves a ranked list of TFs associated with the gene sets you provide.
    - [Website](https://maayanlab.cloud/chea3/) and [publication](https://pmc.ncbi.nlm.nih.gov/articles/PMC6602523/).
- **KEA3:** Using a list of genes or differentially phosphorylated proteins, KEA3 will infer and retrieve upstream kinases whose putative substrates are overrepresented. Its database contains putative kinase-substrate interactions collected from publicly available datasets.
    - [Website](https://maayanlab.cloud/kea3/) and [publication](https://academic.oup.com/nar/article/49/W1/W304/6279841).
- **Rummagene:** Rummagene provides access to human and mouse gene sets extracted from (as of now) 6,327,912 PubMed Central articles, finding 147,611 articles that contain 793,703 gene sets. Rummagene uses these gene sets for enrichment analysis, free text and table title search and will find matching gene sets ranked by their overlap with your input gene set. This tool can also be used for transcription factor and kinase enrichment analyses, for universal predictions of cell types for single cell RNA-seq data, and for gene function predictions. Combining gene set similarity with abstract similarity, Rummagene can discover surprising relationships between biological processes, concepts, and named entities.
    - [Website](https://rummagene.com/) and [publication](https://www.nature.com/articles/s42003-024-06177-7).


### Drug and Target Discovery

Drug and target discovery tools rank drugs and targets by using published Connectivity Mapping resources of transcriptomics and proteomics of chemical and genetic perturbations and then following up with expression. These tools are designed to produce hypotheses for experimental validation and can assist you in identifying MoAs for new drugs, suggesting targets for cell removal by antibody-drug conjugates, and uncovering relationships between drugs, targets, and diseases. You can submit single genes, gene sets, and expression signatures to receive ranked lists of drugs and targets.

- **SigCom-LINCS:** SigCom LINCS serves over a million gene expression signatures processed, analyzed, and visualized from LINCS, GTEx, and GEO. Using a single gene, a gene set, sets of up and down genes, or any search term, SigCom LINCS can provide rapid signature similarity searches for mimickers and reversers, along with offering a metadata search function that finds and analyzes subsets of signatures and information about genes and drugs. SigCom LINCS is findable, accessible, interoperable, and reusable (FAIR) with metadata linked to standard ontologies and vocabularies.
    - [Website](https://maayanlab.cloud/sigcom-lincs/#/SignatureSearch/UpDown) and [publication](https://academic.oup.com/nar/article/50/W1/W697/6582159?login=true).


### Gene and Drug Pages

These tools serve as centralized spaces for detailed information on genes, proteins, drugs, and their functions and interactions, and also utilize ML/AI to provide predictions for human genes functions, as well as targets and side effects for preclinical compounds.

- **GeneRanger:** GeneRanger provides access to processed data about the expression of human genes and proteins across human cell types, tissues, and cell lines from several atlases.
    - [Website](https://generanger.maayanlab.cloud/en/gene/A1CF?database=ARCHS4) and [publication](https://academic.oup.com/nar/article/51/W1/W213/7160193).
- **PrismEXP:** PrismEXP predicts a variety of gene annotations including pathway membership, Gene Ontology terms, and human and mouse phenotypes using uniformly aligned data from ARCHS4. Predictions from PrismEXP outperform predictions made with the global cross-tissue co-expression correlation matrix approach on all tested domains, and training using one annotation domain can be used to predict annotations in other domains.
    - [Website](https://maayanlab.cloud/prismexp) and [publication](https://peerj.com/articles/14927/).
- **ARCHS4:** All RNA-seq and ChIP-seq Signature Search Space (ARCHS4) provides access to gene counts from HiSeq 2000 and HiSeq 2500 platforms for human and mouse experiments from GEO and SRA. Search features allow browsing of the data by metadata annotation, ability to submit your own up and down gene sets, and explore matching samples enriched for annotated gene sets. Human samples are aligned against the GRCh38 human reference genome, and mouse samples against the GRCm38 mouse reference genome.
    - [Website](https://archs4.org/) and [publication](https://www.nature.com/articles/s41467-018-03751-6).
- **Geneshot:** Geneshot allows you to enter arbitrary search terms to receive ranked list of relevant genes containing genes previously published in association with the search term, as well as genes predicted to be associated with the search term based on data integration from multiple sources.
    - [Website](https://maayanlab.cloud/geneshot/) and [publication](https://academic.oup.com/nar/article/47/W1/W571/5494749?login=true).


### Data Portals

Ma'ayan Lab's NIH-funded data and information portals integrate, standardize, and share diverse biomedical datasets, lowering the barrier to data access and promote collaborations across the scientific community.

- **Harmonizome:** Harmonizome is a biological knowledge engine built on top of information about genes and proteins from 114 datasets and contains attribute tables on genes, proteins, cell lines, tissues, experimental perturbations, diseases, phenotypes, or drugs, depending on the dataset. Gene-gene and attribute-attribute similarity networks are computed from attribute tables and can be integrated to perform various computational analyses for knowledge discovery and hypothesis generation.
    - [Website](https://maayanlab.cloud/Harmonizome/) and [publication](https://academic.oup.com/database/article/doi/10.1093/database/baw100/2630482)


### Miscellaneous

Collection of useful bioinformatics tools with features including assembling and augmenting gene sets, comprehensive Connectivity Mapping searching, and more.

- **GeneSetCart:** GeneSetCart allows you to fetch gene sets from various Common Fund programs data sources, augment the sets with gene-gene co-expression correlations or protein-protein interactions, perform set operations such as union, consensus, and intersection on multiple sets, visualize and analyze the gene sets in a single sesion.
    - [Website](https://genesetcart.cfde.cloud/) and [publication](https://pubmed.ncbi.nlm.nih.gov/40208796/)
- **Perturb-Seqr:** Using up and down gene sets, Perturb-Seqr can identify small molecules and gene perturbations that produce the most similar or opposite effect on gene expression. Perturb-Seqr contains over 425,000 sets of up- and down-regulated genes measuring the effects of over 8,500 unique drugs, and over 12,000 unique gene perturbations, targeting approximately 1,000 unique cell lines, and various cell types and tissues, all gathered from processed data from Bridge2AI CM4AI (Perturb-seq), LINCS (L1000), Tahoe-100M, NIBR (DRUG-seq), the original CMap (cDNA microarrays), Ginkgo Bioworks (DRUG-seq), SciPlex, DeepCover MoA (Proteomics), Perturb Atlas (Perturb-seq), Replogle et al. (Perturb-seq), CREEDS (cDNA microarrays), and RummaGEO (RNA-seq). The 12 Connectivity Mapping resources are organized into 16 gene set libraries, 9 drug perturbation and 7 gene perturbation followed by expression.
    - [Website](https://perturbseqr.maayanlab.cloud/)


## Example Use Cases

Example use cases can be found in ``test_case_examples``. Files are split between Appyters and notebooks. Some files may be found in both if an Appyters and notebooks version exists.